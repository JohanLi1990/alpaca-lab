"""PEAD live trading calendar utilities.

Handles earnings date fetching, NYSE trading calendar operations,
and T-N offset calculations.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pandas as pd
from pandas.tseries.holiday import GoodFriday, USFederalHolidayCalendar

from data.earnings_calendar import fetch_earnings_events

log = logging.getLogger(__name__)

_MARKET_TZ = ZoneInfo("America/New_York")


_NYSE_HOLIDAYS = pd.DatetimeIndex([])


def get_current_market_datetime(now: datetime | None = None) -> datetime:
    """Return the current timestamp in US/Eastern market time.

    If ``now`` is provided as a naive datetime, treat it as UTC for deterministic
    tests and cron environments.
    """
    if now is None:
        return datetime.now(_MARKET_TZ)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return now.astimezone(_MARKET_TZ)


def get_current_market_date(now: datetime | None = None) -> datetime.date:
    """Return today's date in US/Eastern market time."""
    return get_current_market_datetime(now).date()


def _get_nyse_holidays(start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
    federal_holidays = USFederalHolidayCalendar().holidays(start=start, end=end)
    good_fridays = GoodFriday.dates(start, end)
    holidays = federal_holidays.union(good_fridays)
    return pd.DatetimeIndex(sorted(holidays.unique()))


def get_trading_dates(start: str | datetime, end: str | datetime) -> pd.DatetimeIndex:
    """Return all NYSE trading dates in range (exclude weekends, US holidays).
    
    Parameters
    ----------
    start : str or datetime
        Start date (YYYY-MM-DD or datetime)
    end : str or datetime
        End date (YYYY-MM-DD or datetime)
        
    Returns
    -------
    pd.DatetimeIndex
        All trading dates between start and end (inclusive)
    """
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    
    holidays = _get_nyse_holidays(start_ts, end_ts)
    
    # Business day range (Mon-Fri)
    date_range = pd.bdate_range(start=start_ts, end=end_ts, freq='B')
    
    # Remove holidays
    trading_dates = date_range[~date_range.isin(holidays)]
    return trading_dates


def calculate_offset_trading_date(
    anchor_date: str | datetime,
    offset: int,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
) -> datetime | None:
    """Compute a trading date at offset from anchor (accounting for weekends/holidays).
    
    Parameters
    ----------
    anchor_date : str or datetime
        Reference date (YYYY-MM-DD or datetime)
    offset : int
        Trading day offset (-3 for T-3, +1 for T+1, etc.)
    start : str or datetime, optional
        Start of trading calendar range (default: 2 years before anchor)
    end : str or datetime, optional
        End of trading calendar range (default: 2 years after anchor)
        
    Returns
    -------
    datetime or None
        Trading date at offset, or None if unavailable
    """
    anchor_ts = pd.Timestamp(anchor_date)
    
    # Default calendar range if not provided
    if start is None:
        start = anchor_ts - timedelta(days=730)
    if end is None:
        end = anchor_ts + timedelta(days=730)
    
    trading_dates = get_trading_dates(start, end)
    
    # Normalize anchor to date-only for comparison
    anchor_normalized = pd.Timestamp(anchor_ts.date())
    
    if anchor_normalized not in trading_dates:
        log.warning("Anchor date %s is not a trading date", anchor_normalized)
        return None
    
    anchor_idx = trading_dates.get_loc(anchor_normalized)
    shifted_idx = anchor_idx + offset
    
    if shifted_idx < 0 or shifted_idx >= len(trading_dates):
        log.warning(
            "Cannot compute T%+d for %s: index %d out of range [0, %d)",
            offset, anchor_normalized, shifted_idx, len(trading_dates),
        )
        return None
    
    return trading_dates[shifted_idx]


def get_entry_trading_date(
    earnings_date: str | datetime,
    entry_offset_days: int,
) -> datetime | None:
    """Return the trading date for entry day T-E."""
    return calculate_offset_trading_date(earnings_date, -entry_offset_days)


def get_feature_anchor_trading_date(
    earnings_date: str | datetime,
    entry_offset_days: int,
) -> datetime | None:
    """Return the last fully known trading date before entry (T-(E+1))."""
    return calculate_offset_trading_date(earnings_date, -(entry_offset_days + 1))


def get_pead_timing_dates(
    earnings_date: str | datetime,
    entry_offset_days: int,
) -> dict[str, datetime | None]:
    """Return derived PEAD timing dates for a configured entry offset."""
    return {
        "entry_date": get_entry_trading_date(earnings_date, entry_offset_days),
        "feature_anchor_date": get_feature_anchor_trading_date(earnings_date, entry_offset_days),
        "exit_date": calculate_offset_trading_date(earnings_date, 1),
    }


def is_today_entry_date(
    symbol: str,
    earnings_dates_dict: dict[str, str],
    entry_offset_days: int = 3,
) -> bool:
    """Check if today is T-3 for a symbol (entry trigger).
    
    Parameters
    ----------
    symbol : str
        Stock symbol
    earnings_dates_dict : dict[str, str]
        Mapping of symbol → earnings_date (YYYY-MM-DD)
        
    Returns
    -------
    bool
        True if today is exactly T-3 for this symbol's nearest earnings
    """
    if symbol not in earnings_dates_dict:
        return False
    
    earnings_date = earnings_dates_dict[symbol]
    entry_date = get_entry_trading_date(earnings_date, entry_offset_days)
    
    if entry_date is None:
        return False
    
    today = pd.Timestamp(get_current_market_date())
    return today == pd.Timestamp(entry_date.date())


def is_today_exit_date(
    symbol: str,
    earnings_dates_dict: dict[str, str],
) -> bool:
    """Check if today is T+1 or later for a symbol (exit trigger).
    
    Parameters
    ----------
    symbol : str
        Stock symbol
    earnings_dates_dict : dict[str, str]
        Mapping of symbol → earnings_date (YYYY-MM-DD)
        
    Returns
    -------
    bool
        True if today is T+1 or later for this symbol's earnings
    """
    if symbol not in earnings_dates_dict:
        return False
    
    earnings_date = earnings_dates_dict[symbol]
    t_plus_1 = calculate_offset_trading_date(earnings_date, 1)
    
    if t_plus_1 is None:
        return False
    
    today = pd.Timestamp(get_current_market_date())
    return today >= pd.Timestamp(t_plus_1.date())


def fetch_nearest_earnings(symbol: str, limit: int = 5) -> str | None:
    """Fetch nearest upcoming earnings date for a symbol.
    
    Parameters
    ----------
    symbol : str
        Stock symbol
    limit : int
        Number of recent earnings to fetch from yfinance
        
    Returns
    -------
    str or None
        Nearest future earnings date (YYYY-MM-DD), or None if not found
    """
    try:
        today = get_current_market_date()
        tomorrow = today + timedelta(days=1)
        end_date = today + timedelta(days=365)
        
        events_df = fetch_earnings_events(
            symbol=symbol,
            start=str(tomorrow),
            end=str(end_date),
            limit=limit,
        )
        
        if events_df.empty:
            log.warning("No upcoming earnings found for %s", symbol)
            return None
        
        nearest_earnings = events_df.iloc[0]["earnings_date"]
        return str(pd.Timestamp(nearest_earnings).date())
    except Exception as e:
        log.error("Failed to fetch earnings for %s: %s", symbol, e)
        return None


# Simple cache to avoid repeated yfinance calls within same cronjob execution
_earnings_cache: dict[str, str] = {}


def get_cached_earnings(symbol: str, use_cache: bool = True) -> str | None:
    """Get earnings date for symbol with optional caching.
    
    Parameters
    ----------
    symbol : str
        Stock symbol
    use_cache : bool
        Whether to use cache (default: True)
        
    Returns
    -------
    str or None
        Earnings date (YYYY-MM-DD)
    """
    if use_cache and symbol in _earnings_cache:
        return _earnings_cache[symbol]
    
    earnings_date = fetch_nearest_earnings(symbol)
    if earnings_date and use_cache:
        _earnings_cache[symbol] = earnings_date
    
    return earnings_date


def clear_earnings_cache() -> None:
    """Clear earnings date cache (useful for testing)."""
    global _earnings_cache
    _earnings_cache.clear()
