"""Pre-earnings feature engineering for PEAD training and live inference.

Computes features from daily OHLCV bars using only information available by the
decision date. Training mode also derives the target label from T-1 close to
earnings-day open.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
from scipy import stats

log = logging.getLogger(__name__)


def build_features(
    events_df: pd.DataFrame,
    bars_dict: dict[str, pd.DataFrame],
    symbol: str = "GOOGL",
    qqq_symbol: str = "QQQ",
    include_labels: bool = True,
    entry_offset_days: int = 3,
) -> pd.DataFrame:
    """Build feature vectors from pre-earnings daily bars.

    Parameters
    ----------
    events_df : pd.DataFrame
        Events DataFrame with columns: earnings_date, symbol, and either
        t_minus_1 (training) or t_minus_3 (inference).
    bars_dict : dict[str, pd.DataFrame]
        Dict mapping symbol → OHLCV DataFrame indexed by date with columns:
        open, high, low, close, volume.
    symbol : str
        The symbol to analyze (e.g., "GOOGL").
    qqq_symbol : str
        The benchmark symbol for relative features (default "QQQ").
    include_labels : bool
        If True, require T-1 and earnings-day bars and compute y/gap_return.
        If False, build inference features using only bars available by T-3.
    entry_offset_days : int
        Entry day offset E where entry occurs on T-E and the feature window ends
        at T-(E+1).

    Returns
    -------
    pd.DataFrame
        Feature DataFrame indexed by earnings_date with columns:
        - drift_7d: 7-day cumulative return
        - drift_slope: OLS slope of closes normalized by mean close
        - up_day_count: number of up days in window
        - down_day_count: number of down days in window
        - rel_volume_mean: mean daily volume / 20-day baseline
        - down_volume_ratio: volume on down days / total volume
        - atr_ratio: mean range / 20-day baseline range
        - gap_count: number of intraday gaps > 0.5%
        - rel_drift_vs_qqq: stock return - QQQ return
        - y: binary label (1 if T open > T-1 close, else 0), training only
        - gap_return: continuous gap return, training only

    Raises
    ------
    ValueError
        If insufficient data or look-ahead bias detected.
    """
    if symbol not in bars_dict:
        raise ValueError(f"Symbol {symbol} not in bars_dict")
    if qqq_symbol not in bars_dict:
        raise ValueError(f"QQQ symbol {qqq_symbol} not in bars_dict")
    if entry_offset_days < 1:
        raise ValueError(f"entry_offset_days must be >= 1, got {entry_offset_days}")

    bars = bars_dict[symbol].copy()
    bars_qqq = bars_dict[qqq_symbol].copy()

    # Ensure index is datetime; normalize to date-only for consistent slicing
    bars.index = pd.to_datetime(bars.index).date
    bars_qqq.index = pd.to_datetime(bars_qqq.index).date
    bars.index = pd.DatetimeIndex(bars.index)
    bars_qqq.index = pd.DatetimeIndex(bars_qqq.index)
    trading_dates = pd.DatetimeIndex(sorted(bars.index.unique()))
    
    events_df = events_df.copy()
    events_df["earnings_date"] = pd.to_datetime(events_df["earnings_date"])
    if include_labels:
        if "t_minus_1" not in events_df.columns:
            raise ValueError("events_df must include t_minus_1 when include_labels=True")
        events_df["t_minus_1"] = pd.to_datetime(events_df["t_minus_1"])
    elif "t_feature_anchor" in events_df.columns:
        events_df["t_feature_anchor"] = pd.to_datetime(events_df["t_feature_anchor"])

    rows = []

    for _, event in events_df.iterrows():
        earnings_date = event["earnings_date"].date()

        if include_labels:
            t_minus_1_date = event["t_minus_1"].date()
            t_minus_1_ts = pd.Timestamp(t_minus_1_date)
            if t_minus_1_ts not in trading_dates:
                log.warning(
                    "Event on %s: missing T-1 bar for %s; dropping",
                    earnings_date,
                    symbol,
                )
                continue

            t_minus_1_idx = int(trading_dates.get_loc(t_minus_1_ts))  # type: ignore[arg-type]
            if t_minus_1_idx < entry_offset_days:
                log.warning(
                    "Event on %s: fewer than %d bars between T-%d anchor and T-1 for %s; dropping",
                    earnings_date,
                    entry_offset_days,
                    entry_offset_days,
                    symbol,
                )
                continue

            t_feature_anchor_ts = trading_dates[t_minus_1_idx - entry_offset_days]
        else:
            if "t_feature_anchor" in event and pd.notna(event["t_feature_anchor"]):
                t_feature_anchor_ts = pd.Timestamp(event["t_feature_anchor"].date())
            else:
                eligible_dates = trading_dates[trading_dates < pd.Timestamp(earnings_date)]
                if len(eligible_dates) < entry_offset_days:
                    log.warning(
                        "Event on %s: fewer than %d pre-earnings trading bars for %s; dropping",
                        earnings_date,
                        entry_offset_days,
                        symbol,
                    )
                    continue
                t_feature_anchor_ts = eligible_dates[-entry_offset_days]

            if t_feature_anchor_ts not in trading_dates:
                log.warning(
                    "Event on %s: missing feature-anchor T-%d bar for %s; dropping",
                    earnings_date,
                    entry_offset_days + 1,
                    symbol,
                )
                continue

        all_bars_before_anchor = bars[bars.index <= t_feature_anchor_ts].copy()
        
        if len(all_bars_before_anchor) < 7:
            log.warning(
                "Event on %s: fewer than 7 bars before feature anchor T-%d; dropping",
                earnings_date,
                entry_offset_days + 1,
            )
            continue
        
        feature_window = all_bars_before_anchor.iloc[-7:].copy()

        # Verify no look-ahead relative to the offset-derived entry decision.
        if feature_window.index.max() > t_feature_anchor_ts:
            raise ValueError(
                f"Look-ahead detected for {symbol} earnings on {earnings_date}: "
                f"feature window extends past T-{entry_offset_days + 1}"
            )

        t_open_date = pd.Timestamp(earnings_date)

        # Feature 1: Price drift
        close_t7 = float(feature_window["close"].iloc[0])
        close_t1 = float(feature_window["close"].iloc[-1])
        drift_7d = (close_t1 - close_t7) / close_t7 if close_t7 > 0 else 0.0

        # Feature 2: Drift slope (OLS on closes)
        closes = feature_window["close"].values
        x = np.arange(len(closes))
        if len(closes) > 1:
            slope, _, _, _, _ = stats.linregress(x, closes)
            mean_close = np.mean(closes)
            drift_slope = slope / mean_close if mean_close > 0 else 0.0
        else:
            drift_slope = 0.0

        # Feature 3: Up/Down day counts
        daily_ret = feature_window["close"].pct_change().dropna()
        up_day_count = (daily_ret > 0).sum()
        down_day_count = (daily_ret < 0).sum()

        # Feature 4: Relative volume
        # Baseline: 20 trading days immediately prior to the 7-day feature window.
        # feature_window is the last 7 rows of all_bars_before_t1, so baseline
        # ends at the row immediately before that trailing window.
        baseline_end_idx = len(all_bars_before_anchor) - 8
        if baseline_end_idx >= 19:
            baseline_window = all_bars_before_anchor.iloc[baseline_end_idx - 19:baseline_end_idx + 1].copy()
        else:
            baseline_window = all_bars_before_anchor.iloc[:baseline_end_idx + 1].copy()
        
        if len(baseline_window) > 0:
            baseline_vol = baseline_window["volume"].mean()
        else:
            baseline_vol = 1.0
        window_vol = feature_window["volume"].mean()
        rel_volume_mean = window_vol / baseline_vol if baseline_vol > 0 else 1.0

        # Feature 5: Down volume ratio
        down_days = feature_window[feature_window["close"].diff() < 0]
        down_vol_total = down_days["volume"].sum() if len(down_days) > 0 else 0.0
        total_vol = feature_window["volume"].sum()
        down_volume_ratio = down_vol_total / total_vol if total_vol > 0 else 0.0

        # Feature 6: ATR ratio (intraday range)
        feature_ranges = (feature_window["high"] - feature_window["low"]).mean()
        if len(baseline_window) > 0:
            baseline_ranges = (baseline_window["high"] - baseline_window["low"]).mean()
        else:
            baseline_ranges = 1.0
        atr_ratio = feature_ranges / baseline_ranges if baseline_ranges > 0 else 1.0

        # Feature 7: Gap count (overnight gaps > 0.5%)
        gaps = abs(feature_window["open"].values[1:] - feature_window["close"].values[:-1]) / (
            feature_window["close"].values[:-1] + 1e-8
        )
        gap_count = (gaps > 0.005).sum()

        # Feature 8: Relative to QQQ
        # Extract QQQ bars for the same window
        all_qqq_before_anchor = bars_qqq[bars_qqq.index <= t_feature_anchor_ts].copy()
        if len(all_qqq_before_anchor) >= 7:
            qqq_window = all_qqq_before_anchor.iloc[-7:].copy()
            qqq_close_t7 = float(qqq_window["close"].iloc[0])
            qqq_close_t1 = float(qqq_window["close"].iloc[-1])
            qqq_drift = (qqq_close_t1 - qqq_close_t7) / qqq_close_t7 if qqq_close_t7 > 0 else 0.0
            rel_drift_vs_qqq = drift_7d - qqq_drift
        else:
            log.warning(f"Event on {earnings_date}: insufficient QQQ bars; using drift only")
            rel_drift_vs_qqq = drift_7d

        row = {
            "earnings_date": event["earnings_date"],
            "drift_7d": drift_7d,
            "drift_slope": drift_slope,
            "up_day_count": up_day_count,
            "down_day_count": down_day_count,
            "rel_volume_mean": rel_volume_mean,
            "down_volume_ratio": down_volume_ratio,
            "atr_ratio": atr_ratio,
            "gap_count": gap_count,
            "rel_drift_vs_qqq": rel_drift_vs_qqq,
        }

        if include_labels:
            # Target label remains the original PEAD gap objective: T-1 close to T open.
            if t_open_date not in bars.index:
                log.warning("Event on %s: missing T-open bar for %s; dropping", earnings_date, symbol)
                continue

            close_t1_value = bars.loc[t_minus_1_ts, "close"]
            if isinstance(close_t1_value, pd.Series):
                close_t1_value = close_t1_value.iloc[0]
            close_t1_float = np.asarray(close_t1_value, dtype=np.float64).item()
            open_t_value = bars.loc[t_open_date, "open"]
            if isinstance(open_t_value, pd.Series):
                open_t_value = open_t_value.iloc[0]
            open_t_float = np.asarray(open_t_value, dtype=np.float64).item()
            gap_return = (open_t_float / close_t1_float - 1.0) if close_t1_float > 0 else 0.0
            row["y"] = 1 if gap_return > 0.0 else 0
            row["gap_return"] = gap_return

        rows.append(row)

    if not rows:
        raise ValueError(
            f"No valid events for feature engineering (check data range and bar availability)"
        )

    result = pd.DataFrame(rows)
    result.set_index("earnings_date", inplace=True)
    result.index = pd.to_datetime(result.index)
    result.sort_index(inplace=True)

    log.info("Built features for %d events", len(result))
    if include_labels and "y" in result.columns:
        log.info("Baseline positive gap rate: %.2f%%", result["y"].mean() * 100)

    return result
