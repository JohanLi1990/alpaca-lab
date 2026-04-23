"""Earnings event calendar fetcher and classifier.

Provides functions to fetch earnings dates from yfinance, classify them by timing
(AMC/BMO), compute T-1 trading dates, and filter by confidence.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf
from pandas.tseries.holiday import USFederalHolidayCalendar

log = logging.getLogger(__name__)


def _get_nyse_trading_dates(start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
    """Return all NYSE trading dates between start and end (inclusive)."""
    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start=start, end=end)
    date_range = pd.bdate_range(start=start, end=end, freq='B')
    # Remove holidays and weekends
    trading_dates = date_range[~date_range.isin(holidays)]
    return trading_dates


def _prior_trading_day(earnings_date: pd.Timestamp, trading_dates: pd.DatetimeIndex) -> pd.Timestamp | None:
    """Return the prior trading day before earnings_date, or None if none exists."""
    # Normalize earnings_date to tz-naive date for comparison
    if hasattr(earnings_date, 'date'):
        earnings_date_normalized = pd.Timestamp(earnings_date.date())
    else:
        earnings_date_normalized = earnings_date
    before = trading_dates[trading_dates < earnings_date_normalized]
    if len(before) == 0:
        return None
    return before[-1]


def fetch_earnings_events(
    symbol: str,
    start: str = "2016-01-01",
    end: str = "2025-12-31",
    timing: str | None = None,
    limit: int = 100,
) -> pd.DataFrame:
    """Fetch and classify earnings events for a symbol.

    Parameters
    ----------
    symbol : str
        Ticker symbol (e.g., "GOOGL").
    start : str
        Start date as YYYY-MM-DD.
    end : str
        End date as YYYY-MM-DD.
    timing : str or None
        Filter by timing: "AMC" (after close), "BMO" (before open), or None (all).
    limit : int
        Maximum number of events to fetch from yfinance (max 100).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - earnings_date: pandas Timestamp of the event date
        - release_time: "AMC", "BMO", or "UNKNOWN"
        - t_minus_1: prior trading day (entry date)
        - symbol: ticker symbol

    Raises
    ------
    ValueError
        If no events are returned after filtering.
    """
    if limit > 100:
        limit = 100

    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)

    # Fetch raw earnings dates from yfinance
    try:
        ticker = yf.Ticker(symbol)
        raw_events = ticker.get_earnings_dates(limit=limit)
    except Exception as e:
        raise ValueError(f"Failed to fetch earnings dates for {symbol}: {e}") from e

    if raw_events is None or raw_events.empty:
        raise ValueError(f"No earnings dates returned for {symbol}")

    # Reset index so earnings date is a column (yfinance returns it as index)
    work = raw_events.reset_index()
    if "Earnings Date" not in work.columns:
        raise ValueError(f"No 'Earnings Date' column in yfinance response for {symbol}")

    # Normalize index to datetime
    work["event_dt"] = pd.to_datetime(work["Earnings Date"], errors="coerce")
    work = work.dropna(subset=["event_dt"]).copy()

    # Filter to requested date range
    work = work[
        (work["event_dt"].dt.date >= start_ts.date()) &
        (work["event_dt"].dt.date <= end_ts.date())
    ].copy()

    if work.empty:
        raise ValueError(
            f"No earnings events found for {symbol} between {start} and {end}"
        )

    # Classify by timing
    classified_rows = []
    excluded_count = 0

    # Build trading calendar for T-1 computation
    trading_dates = _get_nyse_trading_dates(start_ts, end_ts)

    for _, row in work.iterrows():
        ts = row["event_dt"]
        rel_time = "UNKNOWN"

        if ts.tzinfo is not None:
            # Convert to America/New_York
            ny_ts = ts.tz_convert("America/New_York")
            hour = ny_ts.hour
            minute = ny_ts.minute
            hm = hour * 60 + minute

            # 16:00 ET = 960 minutes, 09:30 ET = 570 minutes
            if hm >= 960:
                rel_time = "AMC"
            elif hm < 570:
                rel_time = "BMO"
            else:
                rel_time = "MIDDAY"
                excluded_count += 1
                continue
        else:
            excluded_count += 1
            continue

        # Compute T-1
        t_minus_1 = _prior_trading_day(ts, trading_dates)
        if t_minus_1 is None:
            log.warning(f"No prior trading day found for {symbol} earnings on {ts.date()}")
            excluded_count += 1
            continue

        classified_rows.append({
            "earnings_date": ts,
            "release_time": rel_time,
            "t_minus_1": t_minus_1,
            "symbol": symbol,
        })

    if excluded_count > 0:
        log.warning(f"Excluded {excluded_count} events with ambiguous or missing timing for {symbol}")

    if not classified_rows:
        raise ValueError(
            f"No valid events with timing classification for {symbol} between {start} and {end}"
        )

    df = pd.DataFrame(classified_rows)

    # Apply timing filter if requested
    if timing is not None:
        if timing not in ("AMC", "BMO"):
            raise ValueError(f"timing must be 'AMC', 'BMO', or None; got {timing}")
        df = df[df["release_time"] == timing].copy()

        if df.empty:
            raise ValueError(
                f"No {timing} events found for {symbol} between {start} and {end}"
            )

        log.info(f"Filtered to {len(df)} {timing} events for {symbol}")

    log.info(f"Fetched {len(df)} earnings events for {symbol}")
    return df
