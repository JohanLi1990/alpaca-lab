"""Event-driven backtest for PEAD strategy.

Simulates entry at open(T-E) and exit at the configured T+1 horizon based on
classifier predictions, with transaction cost modeling.
"""

from __future__ import annotations

import logging

import pandas as pd

from data.pead_calendar import calculate_offset_trading_date, get_entry_trading_date, get_feature_anchor_trading_date
from risk.metrics import print_summary, sharpe_ratio_from_returns

log = logging.getLogger(__name__)


def _to_naive_midnight(series_or_index: pd.Series | pd.Index) -> pd.Series | pd.DatetimeIndex:
    """Normalize datetime values to tz-naive midnight for key-safe joins."""
    values = pd.to_datetime(series_or_index)
    if isinstance(values, pd.Series):
        if getattr(values.dt, "tz", None) is not None:
            values = values.dt.tz_localize(None)
        return values.dt.normalize()
    idx = pd.DatetimeIndex(values)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    return idx.normalize()


def _shift_trading_day(
    trading_dates: pd.DatetimeIndex,
    anchor: pd.Timestamp,
    offset: int,
) -> pd.Timestamp | None:
    """Return the trading day at a relative offset from anchor, or None if unavailable."""
    if anchor not in trading_dates:
        return None
    anchor_idx = trading_dates.get_loc(anchor)
    shifted_idx = anchor_idx + offset
    if shifted_idx < 0 or shifted_idx >= len(trading_dates):
        return None
    return trading_dates[shifted_idx]


class PEADBacktest:
    """Event-driven backtest for Post-Earnings Announcements Drift strategy.

    Simulates offset-driven positions: buy at open(T-E), sell at T+1 open/close.
    """

    def __init__(
        self,
        predictions_df: pd.DataFrame,
        bars_dict: dict[str, pd.DataFrame],
        events_df: pd.DataFrame,
        symbol: str = "GOOGL",
        position_size: float = 0.05,
        ptc: float = 0.001,
        initial_amount: float = 10000.0,
        entry_offset_days: int = 3,
        exit_mode: str = "t_plus_1_open",
    ):
        """Initialize PEAD backtest.

        Parameters
        ----------
        predictions_df : pd.DataFrame
            Walk-forward predictions with columns: pred_label, prob_positive, y, gap_return.
        bars_dict : dict[str, pd.DataFrame]
            Dict mapping symbol → OHLCV DataFrame indexed by date.
        events_df : pd.DataFrame
            Events DataFrame with columns: earnings_date, t_minus_1.
        symbol : str
            The symbol being traded (default "GOOGL").
        position_size : float
            Position size as fraction of capital per trade (default 0.05 = 5%).
        ptc : float
            Proportional transaction cost per leg (default 0.001 = 0.1%).
        initial_amount : float
            Starting capital (default 10000).
        """
        self.predictions_df = predictions_df.copy()
        self.bars_dict = bars_dict
        self.events_df = events_df.copy()
        self.symbol = symbol
        self.position_size = position_size
        self.ptc = ptc
        self.initial_amount = initial_amount
        self.entry_offset_days = entry_offset_days
        self.exit_mode = exit_mode
        if self.entry_offset_days < 1:
            raise ValueError(f"entry_offset_days must be >= 1; got {self.entry_offset_days}")
        if self.exit_mode not in {"t_plus_1_open", "t_plus_1_close"}:
            raise ValueError(
                "exit_mode must be 't_plus_1_open' or 't_plus_1_close'; "
                f"got {self.exit_mode}"
            )

        # Ensure datetime indices
        # Normalize to date-only so timestamps from different sources (e.g. 16:00
        # earnings events vs 00:00 bars) align on calendar day keys.
        self.predictions_df.index = _to_naive_midnight(self.predictions_df.index)
        self.events_df["earnings_date"] = _to_naive_midnight(self.events_df["earnings_date"])
        self.events_df["t_minus_1"] = _to_naive_midnight(self.events_df["t_minus_1"])
        self.predictions_df.sort_index(inplace=True)
        self.events_df.sort_values("earnings_date", inplace=True)
        self.events_df.reset_index(drop=True, inplace=True)

        self.equity_curve = None
        self.trades_df = None
        self.benchmark_report = None

    def run(self) -> tuple[pd.Series, pd.DataFrame]:
        """Run backtest and return equity curve and trades.

        Returns
        -------
        tuple[pd.Series, pd.DataFrame]
            - equity_curve: Series indexed by earnings_date with account value
            - trades_df: DataFrame with per-trade records
        """
        bars = self.bars_dict[self.symbol].copy()
        bars.index = _to_naive_midnight(bars.index)
        equity = self.initial_amount
        equity_curve_values = [equity]
        equity_curve_dates = [pd.Timestamp(self.events_df.iloc[0]["earnings_date"]) - pd.Timedelta(days=1)]
        trades = []
        evaluated_events = []

        for _, event in self.events_df.iterrows():
            event_ts = pd.Timestamp(event["earnings_date"])
            t_minus_1_ts = pd.Timestamp(event["t_minus_1"])
            earnings_date = event_ts.date()

            # Check if we have a prediction for this event
            if event_ts not in self.predictions_df.index:
                continue

            pred = self.predictions_df.loc[event_ts]

            # Derive entry and feature-anchor dates from the trading calendar, not from
            # available bar rows, so missing bars are detected as missing data rather than
            # silently changing the intended offsets.
            entry_ts = get_entry_trading_date(event_ts, self.entry_offset_days)
            if entry_ts is None:
                log.warning(
                    f"No bar at T-{self.entry_offset_days} for {self.symbol} earnings on {earnings_date}"
                )
                continue

            feature_anchor_ts = get_feature_anchor_trading_date(event_ts, self.entry_offset_days)
            if feature_anchor_ts is None:
                log.warning(
                    "No feature-anchor bar at T-%d for %s earnings on %s",
                    self.entry_offset_days + 1,
                    self.symbol,
                    earnings_date,
                )
                continue

            exit_ts = calculate_offset_trading_date(event_ts, 1)
            if exit_ts is None:
                log.warning(f"No T+1 bar for {self.symbol} earnings on {earnings_date}")
                continue

            if entry_ts not in bars.index:
                log.warning(f"Missing entry bar at {entry_ts.date()} for {self.symbol}")
                continue
            if feature_anchor_ts not in bars.index:
                log.warning(
                    "Missing feature-anchor bar at %s for %s",
                    feature_anchor_ts.date(),
                    self.symbol,
                )
                continue
            if exit_ts not in bars.index:
                log.warning(f"Missing exit bar at {exit_ts.date()} for {self.symbol}")
                continue

            entry_price = float(bars.loc[entry_ts, "open"])

            exit_field = "open" if self.exit_mode == "t_plus_1_open" else "close"
            exit_price = float(bars.loc[exit_ts, exit_field])

            gross_return = (exit_price - entry_price) / entry_price if entry_price > 0 else 0.0
            net_return = gross_return - 2 * self.ptc
            evaluated_events.append({
                "earnings_date": event_ts,
                "entry_date": entry_ts,
                "exit_date": exit_ts,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "gross_return": gross_return,
                "net_return": net_return,
                "pred_label": int(pred["pred_label"]),
                "pred_prob": pred["prob_positive"],
                "y": pred["y"],
            })

            # No model-gated trade for predicted-negative events.
            if pred["pred_label"] != 1:
                equity_curve_values.append(equity)
                equity_curve_dates.append(event_ts)
                continue

            # Calculate position
            position_value = equity * self.position_size

            # PnL
            pnl = position_value * net_return

            # Update equity
            equity += pnl

            # Record trade
            trades.append({
                "earnings_date": event_ts,
                "entry_date": entry_ts,
                "exit_date": exit_ts,
                "entry_price": entry_price,
                "exit_price": exit_price,
                "gross_return": gross_return,
                "net_return": net_return,
                "pnl": pnl,
                "equity_after": equity,
                "pred_prob": pred["prob_positive"],
                "y": pred["y"],
            })

            # Add to equity curve
            equity_curve_values.append(equity)
            equity_curve_dates.append(event_ts)

            log.debug(
                f"Trade on {earnings_date}: entry={entry_price:.2f}, exit={exit_price:.2f}, "
                f"return={net_return:.2%}, equity={equity:.2f}"
            )

        # Build equity curve
        self.equity_curve = pd.Series(
            equity_curve_values,
            index=equity_curve_dates,
        )

        # Build trades DataFrame
        if trades:
            self.trades_df = pd.DataFrame(trades)
            self.trades_df.set_index("earnings_date", inplace=True)
        else:
            self.trades_df = pd.DataFrame()

        benchmark_df = pd.DataFrame(evaluated_events)
        if not benchmark_df.empty:
            model_df = benchmark_df[benchmark_df["pred_label"] == 1].copy()
            model_avg_gross = model_df["gross_return"].mean() if not model_df.empty else 0.0
            model_avg_net = model_df["net_return"].mean() if not model_df.empty else 0.0
            model_hit_rate = (model_df["gross_return"] > 0).mean() if not model_df.empty else 0.0
            always_buy_avg_gross = benchmark_df["gross_return"].mean()
            always_buy_avg_net = benchmark_df["net_return"].mean()
            always_buy_hit_rate = (benchmark_df["gross_return"] > 0).mean()
            self.benchmark_report = {
                "evaluated_events": len(benchmark_df),
                "model_trades": len(model_df),
                "model_hit_rate": model_hit_rate,
                "model_avg_gross_return": model_avg_gross,
                "model_avg_net_return": model_avg_net,
                "always_buy_hit_rate": always_buy_hit_rate,
                "always_buy_avg_gross_return": always_buy_avg_gross,
                "always_buy_avg_net_return": always_buy_avg_net,
                "uplift_vs_always_buy": model_avg_net - always_buy_avg_net,
            }
            log.info(
                "PEAD timing-variant benchmark (entry=T-%d open, feature-anchor=T-%d close, exit=%s):",
                self.entry_offset_days,
                self.entry_offset_days + 1,
                self.exit_mode,
            )
            log.info("  Evaluated events:               %d", self.benchmark_report["evaluated_events"])
            log.info("  Model trades:                   %d", self.benchmark_report["model_trades"])
            log.info("  Model hit rate:                 %.2f%%", self.benchmark_report["model_hit_rate"] * 100)
            log.info("  Model avg gross return:         %.2f%%", self.benchmark_report["model_avg_gross_return"] * 100)
            log.info("  Model avg net return:           %.2f%%", self.benchmark_report["model_avg_net_return"] * 100)
            log.info("  Always-buy hit rate:            %.2f%%", self.benchmark_report["always_buy_hit_rate"] * 100)
            log.info("  Always-buy avg gross return:    %.2f%%", self.benchmark_report["always_buy_avg_gross_return"] * 100)
            log.info("  Always-buy avg net return:      %.2f%%", self.benchmark_report["always_buy_avg_net_return"] * 100)
            log.info("  Model uplift vs always-buy:     %.2f%%", self.benchmark_report["uplift_vs_always_buy"] * 100)
        else:
            self.benchmark_report = {
                "evaluated_events": 0,
                "model_trades": 0,
                "model_hit_rate": 0.0,
                "model_avg_gross_return": 0.0,
                "model_avg_net_return": 0.0,
                "always_buy_hit_rate": 0.0,
                "always_buy_avg_gross_return": 0.0,
                "always_buy_avg_net_return": 0.0,
                "uplift_vs_always_buy": 0.0,
            }

        log.info(
            "Backtest complete: %d trades, final equity=%.2f | entry=T-%d open | feature-anchor=T-%d close | exit=%s",
            len(trades),
            equity,
            self.entry_offset_days,
            self.entry_offset_days + 1,
            self.exit_mode,
        )
        log.info(f"Total return: {(equity - self.initial_amount) / self.initial_amount:.2%}")

        # Compute risk metrics
        # For event-driven PEAD trades, compute Sharpe from actual trade returns only
        # (not the equity curve with flats), without annualization.
        if trades:
            trade_returns = self.trades_df["net_return"].values
            sharpe = sharpe_ratio_from_returns(trade_returns, periods_per_year=None)
        else:
            sharpe = 0.0

        log.info("=" * 45)
        log.info("  Risk Summary (Trade-Based)")
        log.info("=" * 45)
        log.info("  Trades               : %d", len(trades))
        log.info("  Total Return    [%%]  : %10.2f", (equity - self.initial_amount) / self.initial_amount * 100)
        log.info("  Sharpe Ratio         : %10.2f", sharpe)
        log.info("=" * 45)

        return self.equity_curve, self.trades_df
