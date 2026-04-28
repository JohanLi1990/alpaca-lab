from __future__ import annotations

import logging
import math
from datetime import datetime, timedelta, timezone

import pandas as pd

from alpaca.trading.enums import OrderSide

from core.backtest_base import AlpacaBacktestBase
from core.live_trader_base import AlpacaLiveTraderBase
from data.alpaca_data import fetch_bars
import risk.metrics as risk

log = logging.getLogger(__name__)


class CrossSectionalMomentum(AlpacaBacktestBase):
    """Cross-sectional momentum strategy on a symbol universe.

    Ranks symbols by N-day simple price return each Friday, goes long
    the top ``top_n`` equal-weight, and rebalances weekly.

    Parameters
    ----------
    data : dict[str, pd.DataFrame]
        Output of ``data.alpaca_data.fetch_bars`` — symbol → OHLCV+return DataFrame.
    lookback : int
        Number of trading days for momentum return calculation.
    top_n : int
        Number of symbols to hold long.
    initial_amount : float
        Starting capital in USD.
    ftc : float
        Fixed transaction cost per trade.
    ptc : float
        Proportional transaction cost per trade.
    verbose : bool
        If True, print each order.
    """

    def __init__(
        self,
        data: dict[str, pd.DataFrame],
        lookback: int = 60,
        top_n: int = 3,
        initial_amount: float = 10_000.0,
        ftc: float = 0.0,
        ptc: float = 0.0,
        verbose: bool = True,
    ) -> None:
        super().__init__(data, initial_amount, ftc, ptc, verbose)
        self.lookback = lookback
        self.top_n = top_n
        self._holdings: set[str] = set()   # currently held symbols

    # ------------------------------------------------------------------
    # Signal
    # ------------------------------------------------------------------

    def compute_scores(self, bar: int) -> pd.Series:
        """Compute N-day simple price return for each symbol at bar.

        Returns
        -------
        pd.Series
            Symbols ranked descending by return score.
        """
        if bar < self.lookback:
            return pd.Series(dtype=float)

        scores: dict[str, float] = {}
        date_now = self.dates[bar]
        date_prev = self.dates[bar - self.lookback]

        for symbol, df in self.data.items():
            try:
                price_now = float(df.loc[date_now, "close"])
                price_prev = float(df.loc[date_prev, "close"])
                scores[symbol] = (price_now - price_prev) / price_prev
            except KeyError:
                scores[symbol] = float("-inf")

        return pd.Series(scores).sort_values(ascending=False)

    # ------------------------------------------------------------------
    # Event handler
    # ------------------------------------------------------------------

    def on_bar(self, bar: int) -> None:
        """Rebalance portfolio on Fridays based on momentum signal."""
        scores = self.compute_scores(bar)
        if scores.empty:
            return

        # Cash-out rule: only consider symbols with positive momentum
        positive = scores[scores > 0]
        target = set(positive.head(self.top_n).index)

        # 1. Sell symbols no longer in target (dropped or all momentum negative)
        for symbol in list(self._holdings):
            if symbol not in target:
                units = self.units_held.get(symbol, 0.0)
                if units > 0:
                    self.place_sell_order(symbol, bar, units)
                self._holdings.discard(symbol)

        # 2. Buy new entries equal-weight (skip if no positive-momentum symbols)
        new_entries = target - self._holdings
        if new_entries:
            allocation = self.cash / len(new_entries)
            for symbol in new_entries:
                self.place_buy_order(symbol, bar, allocation)
                self._holdings.add(symbol)

    # ------------------------------------------------------------------
    # Run override (adds risk summary + plot)
    # ------------------------------------------------------------------

    def run_backtest(self, save_path: str | None = None) -> pd.Series:
        """Run the full event-driven backtest and print risk summary.

        Parameters
        ----------
        save_path : str, optional
            If provided, save the equity curve plot to this file path.

        Returns
        -------
        pd.Series
            Equity curve indexed by date.
        """
        super().run_backtest()

        equity = pd.Series(
            [v for _, v in self.equity_curve],
            index=pd.to_datetime([d for d, _ in self.equity_curve]),
        )
        risk.print_summary(equity)
        risk.plot_equity_curve(equity, title="M7 Cross-Sectional Momentum — Equity Curve", save_path=save_path)
        return equity


# ---------------------------------------------------------------------------
# Live paper trader
# ---------------------------------------------------------------------------

class LiveMomentumTrader(AlpacaLiveTraderBase):
    """Cross-sectional momentum live paper trader.

    Uses the same signal as ``CrossSectionalMomentum`` but submits real orders
    to the Alpaca paper trading account.

    Parameters
    ----------
    symbols : list[str]
        Universe of symbols to rank.
    lookback : int
        N-day return lookback window.
    top_n : int
        Number of symbols to hold.
    initial_amount : float
        Approximate portfolio size used for equal-weight allocation.
    """

    def __init__(
        self,
        symbols: list[str],
        lookback: int = 60,
        top_n: int = 3,
        initial_amount: float = 10_000.0,
        max_capital: float | None = None,
    ) -> None:
        super().__init__(paper=True)
        self.symbols = symbols
        self.lookback = lookback
        self.top_n = top_n
        self.initial_amount = initial_amount
        self.max_capital = max_capital

    # ------------------------------------------------------------------
    # Signal
    # ------------------------------------------------------------------

    def _last_completed_utc_day(self) -> datetime:
        """Return the latest fully completed UTC calendar day for daily bars."""
        return datetime.now(timezone.utc) - timedelta(days=1)

    def compute_signal(self) -> list[str]:
        """Fetch latest data and return top-N positive-momentum symbols.

        Returns
        -------
        list[str]
            Top-N symbols ranked by N-day return, best first.
            If all scores are non-positive, returns an empty list (stay in cash).
        """
        last_complete_day_utc = self._last_completed_utc_day()
        end = last_complete_day_utc.strftime("%Y-%m-%d")
        # Fetch extra days to ensure we have enough trading days.
        start = (last_complete_day_utc - timedelta(days=self.lookback * 2)).strftime("%Y-%m-%d")

        data = fetch_bars(self.symbols, start, end)

        scores: dict[str, float] = {}
        for symbol, df in data.items():
            if len(df) < self.lookback + 1:
                scores[symbol] = float("-inf")
                continue
            price_now = float(df["close"].iloc[-1])
            price_prev = float(df["close"].iloc[-(self.lookback + 1)])
            scores[symbol] = (price_now - price_prev) / price_prev

        ranked = sorted(scores, key=lambda s: scores[s], reverse=True)
        positive_ranked = [symbol for symbol in ranked if scores[symbol] > 0]
        return positive_ranked[: self.top_n]

    # ------------------------------------------------------------------
    # Rebalance
    # ------------------------------------------------------------------

    def rebalance(self) -> None:
        """Execute a full signal → order cycle.

        Computes the momentum signal, diffs against current positions,
        and submits market orders for changes.
        """
        self._warn_if_outside_hours()

        log.info("--- LiveMomentumTrader: rebalancing ---")
        target = set(self.compute_signal())
        if not target:
            log.warning("No symbols with positive momentum. Target is 100%% cash.")
        log.info("Target holdings: %s", sorted(target))

        current = self.get_current_positions()
        log.info("Current positions: %s", current)

        # Sell dropped holdings
        for symbol, qty in current.items():
            if symbol in self.symbols and symbol not in target:
                self.submit_order(symbol, OrderSide.SELL, math.floor(qty))

        # Fetch recent prices for target and currently held universe symbols.
        # Used for share sizing and optional capital-cap accounting.
        strategy_held = {symbol for symbol in current if symbol in self.symbols}
        symbols_for_prices = sorted(target | strategy_held)
        last_complete_day_utc = self._last_completed_utc_day()
        end = last_complete_day_utc.strftime("%Y-%m-%d")
        start = (last_complete_day_utc - timedelta(days=5)).strftime("%Y-%m-%d")
        price_data = fetch_bars(symbols_for_prices, start, end) if symbols_for_prices else {}

        # Estimate available capital
        account = self.client.get_account()
        available_cash = float(getattr(account, "cash", 0.0) or 0.0)

        deployable_cash = available_cash
        if self.max_capital is not None:
            current_value = 0.0
            for symbol in strategy_held:
                if symbol in price_data and not price_data[symbol].empty:
                    px = float(price_data[symbol]["close"].iloc[-1])
                    current_value += float(current[symbol]) * px
            remaining_budget = max(self.max_capital - current_value, 0.0)
            deployable_cash = min(available_cash, remaining_budget)
            log.info(
                "Capital cap=$%,.2f | current strategy value=$%,.2f | deployable cash=$%,.2f",
                self.max_capital, current_value, deployable_cash,
            )

        allocation = deployable_cash / len(target) if target else 0.0

        # Buy new entries
        for symbol in target:
            if symbol not in current or current[symbol] == 0:
                price = float(price_data[symbol]["close"].iloc[-1])
                qty = math.floor(allocation / price)
                if qty > 0:
                    self.submit_order(symbol, OrderSide.BUY, qty)

        log.info("--- rebalance complete ---")

