This file is a merged representation of the entire codebase, combined into a single document by Repomix.
The content has been processed where content has been compressed (code blocks are separated by ⋮---- delimiter).

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
core/
  __init__.py
  alpaca_credentials.py
  backtest_base.py
  live_trader_base.py
  pead_state_manager.py
  pead_trade_logger.py
data/
  __init__.py
  alpaca_data.py
  earnings_calendar.py
  pead_calendar.py
  pre_earnings_features.py
openspec/
  changes/
    archive/
      2026-04-19-momentum-m7-strategy/
        specs/
          backtest-engine/
            spec.md
          data-layer/
            spec.md
          live-trader/
            spec.md
          momentum-strategy/
            spec.md
          risk-analytics/
            spec.md
        .openspec.yaml
        design.md
        proposal.md
        tasks.md
      2026-04-21-moc-execution/
        specs/
          live-trader/
            spec.md
        .openspec.yaml
        design.md
        proposal.md
        tasks.md
      2026-04-22-ml-pre-earnings-price-prediction/
        specs/
          data-layer/
            spec.md
          earnings-calendar/
            spec.md
          ml-classifier/
            spec.md
          pead-backtest/
            spec.md
          pre-earnings-features/
            spec.md
        .openspec.yaml
        design.md
        proposal.md
        tasks.md
      2026-04-22-pead-t3-entry-tp1-exits/
        specs/
          pead-backtest/
            spec.md
          pre-earnings-features/
            spec.md
        .openspec.yaml
        design.md
        proposal.md
        tasks.md
      2026-04-23-pead-live-multi-symbol/
        specs/
          pead-live-trader/
            spec.md
          pead-state-manager/
            spec.md
          pead-trade-logger/
            spec.md
        .openspec.yaml
        design.md
        proposal.md
        tasks.md
      2026-04-24-pead-configurable-entry-offset/
        specs/
          data-layer/
            spec.md
          live-trader/
            spec.md
          pead-backtest/
            spec.md
          pead-entry-timing-config/
            spec.md
          pre-earnings-features/
            spec.md
        .openspec.yaml
        design.md
        proposal.md
        tasks.md
      2026-04-30-fix-momentum-live-cash-constrained-moc-rebalance/
        specs/
          live-trader/
            spec.md
          momentum-strategy/
            spec.md
        .openspec.yaml
        design.md
        proposal.md
        tasks.md
      2026-05-05-account-separation-v1-v2/
        specs/
          data-layer/
            spec.md
          live-trader/
            spec.md
          pead-live-trader/
            spec.md
        .openspec.yaml
        design.md
        proposal.md
        tasks.md
    expand-pead-portfolio-to-10/
      .openspec.yaml
  specs/
    backtest-engine/
      spec.md
    data-layer/
      spec.md
    earnings-calendar/
      spec.md
    live-trader/
      spec.md
    ml-classifier/
      spec.md
    momentum-strategy/
      spec.md
    pead-backtest/
      spec.md
    pead-entry-timing-config/
      spec.md
    pead-live-trader/
      spec.md
    pead-state-manager/
      spec.md
    pead-trade-logger/
      spec.md
    pre-earnings-features/
      spec.md
    risk-analytics/
      spec.md
  config.yaml
risk/
  __init__.py
  metrics.py
scripts/
  pead_live_cronjob.py
  weekly_live_rebalance.py
strategies/
  __init__.py
  momentum.py
  pead_backtest.py
  pead_classifier_live.py
  pead_classifier.py
  pead_live_trader.py
tests/
  test_alpaca_credentials.py
  test_alpaca_data.py
  test_live_trader_profiles.py
  test_momentum_live_rebalance.py
  test_pead_backtest.py
  test_pead_calendar.py
  test_pead_live_cronjob.py
  test_pre_earnings_features.py
.gitignore
.repomixignore
config.py
environment.yml
README.md
run.py
```

# Files

## File: openspec/changes/expand-pead-portfolio-to-10/.openspec.yaml
````yaml
schema: spec-driven
created: 2026-05-06
````

## File: core/__init__.py
````python

````

## File: core/alpaca_credentials.py
````python
_PROFILE_TO_ENV = {
⋮----
def resolve_alpaca_credentials(profile: str) -> tuple[str, str]
⋮----
"""Resolve Alpaca API credentials for a named profile.

    Supported profiles are:
    - v1 -> V1_APCA_API_KEY_ID / V1_APCA_API_SECRET_KEY
    - v2 -> V2_APCA_API_KEY_ID / V2_APCA_API_SECRET_KEY
    """
normalized_profile = profile.strip().lower()
⋮----
supported = ", ".join(sorted(_PROFILE_TO_ENV))
⋮----
api_key = os.environ.get(api_key_var)
secret_key = os.environ.get(secret_key_var)
missing = [name for name, value in ((api_key_var, api_key), (secret_key_var, secret_key)) if not value]
⋮----
return api_key, secret_key  # type: ignore[return-value]  # guarded by missing-vars check above
````

## File: core/pead_state_manager.py
````python
"""PEAD live trading state manager.

Manages JSON-based state file tracking current open positions per symbol.
Handles idempotency, atomic writes, and automatic cleanup of stale entries.
"""
⋮----
log = logging.getLogger(__name__)
⋮----
class PEADStateManager
⋮----
"""Manages persistent state for live PEAD trading positions.
    
    State file structure:
    {
      "NXPI": {
        "earnings_date": "2026-04-30",
        "entry_date": "2026-04-27",
        "entry_price": 125.50,
        "entry_qty": 80,
        "created_at": "2026-04-27T16:00:00Z"
      }
    }
    """
⋮----
def __init__(self, state_file: str = "output/pead_live_state.json")
⋮----
"""Initialize state manager.
        
        Parameters
        ----------
        state_file : str
            Path to JSON state file (default: output/pead_live_state.json)
        """
⋮----
def load_state(self) -> None
⋮----
"""Load state from JSON file, creating empty state if file doesn't exist."""
⋮----
def save_state(self) -> None
⋮----
"""Save state to JSON file with atomic write (pretty-printed)."""
⋮----
# Write to temporary file first, then atomically rename
temp_file = self.state_file.with_suffix('.tmp')
⋮----
"""Record a new open position (entry executed).
        
        Parameters
        ----------
        symbol : str
            Stock symbol (e.g., "NXPI")
        earnings_date : str
            Earnings date in YYYY-MM-DD format
        entry_date : str
            Entry date in YYYY-MM-DD format
        entry_price : float
            Entry fill price
        entry_qty : int
            Entry fill quantity
        """
⋮----
def remove_position(self, symbol: str) -> None
⋮----
"""Delete position after exit (clean slate for next earnings event).
        
        Parameters
        ----------
        symbol : str
            Stock symbol (e.g., "NXPI")
        """
⋮----
def get_position(self, symbol: str) -> dict[str, Any] | None
⋮----
"""Check if symbol has an open position and return details.
        
        Parameters
        ----------
        symbol : str
            Stock symbol (e.g., "NXPI")
            
        Returns
        -------
        dict or None
            Position details if open, else None
        """
⋮----
def already_traded(self, symbol: str, earnings_date: str) -> bool
⋮----
"""Check if we already traded this symbol for this earnings event (idempotency).
        
        Parameters
        ----------
        symbol : str
            Stock symbol (e.g., "NXPI")
        earnings_date : str
            Earnings date in YYYY-MM-DD format
            
        Returns
        -------
        bool
            True if position exists for this symbol and same earnings_date
        """
⋮----
def cleanup_stale_entries(self, days: int = 30) -> None
⋮----
"""Remove entries older than specified days (handles missed exits).
        
        Parameters
        ----------
        days : int
            Entries older than this many days are removed (default: 30)
        """
cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)
stale_symbols = []
⋮----
created_at_str = position.get("created_at")
⋮----
created_at = datetime.fromisoformat(created_at_str)
# Ensure timezone-aware comparison
⋮----
created_at = created_at.replace(tzinfo=timezone.utc)
````

## File: core/pead_trade_logger.py
````python
"""PEAD live trading trade logger.

Maintains append-only CSV log of all entry/exit trades for audit trail
and performance analysis.
"""
⋮----
log = logging.getLogger(__name__)
⋮----
class PEADTradeLogger
⋮----
"""Logs all PEAD live trades to append-only CSV file.
    
    CSV columns:
    symbol, earnings_date, entry_date, exit_date, entry_price, exit_price,
    qty, pnl, pnl_pct, timestamp
    """
⋮----
CSV_HEADER = [
⋮----
def __init__(self, log_file: str = "output/pead_live_trades.csv")
⋮----
"""Initialize trade logger.
        
        Parameters
        ----------
        log_file : str
            Path to CSV trade log file (default: output/pead_live_trades.csv)
        """
⋮----
def initialize_log(self) -> None
⋮----
"""Create CSV header if file doesn't exist."""
⋮----
writer = csv.DictWriter(f, fieldnames=self.CSV_HEADER)
⋮----
"""Log a completed trade (entry + exit).
        
        Parameters
        ----------
        symbol : str
            Stock symbol
        earnings_date : str
            Earnings date (YYYY-MM-DD)
        entry_date : str
            Entry date (YYYY-MM-DD)
        exit_date : str
            Exit date (YYYY-MM-DD)
        entry_price : float
            Entry fill price
        exit_price : float
            Exit fill price
        qty : int
            Shares traded
        pnl : float
            Profit/loss in dollars
        pnl_pct : float
            Profit/loss as percentage (0.05 = 5%)
        """
⋮----
timestamp = datetime.now(timezone.utc).isoformat()
row = {
⋮----
"""Optionally log a skipped entry for analysis (pred_label=0 case).
        
        Parameters
        ----------
        symbol : str
            Stock symbol
        earnings_date : str
            Earnings date (YYYY-MM-DD)
        entry_date : str
            Entry date (YYYY-MM-DD)
        reason : str
            Reason for skip (default: "pred_label=0")
        """
````

## File: data/__init__.py
````python

````

## File: data/earnings_calendar.py
````python
"""Earnings event calendar fetcher and classifier.

Provides functions to fetch earnings dates from yfinance, classify them by timing
(AMC/BMO), compute T-1 trading dates, and filter by confidence.
"""
⋮----
log = logging.getLogger(__name__)
⋮----
def _get_nyse_trading_dates(start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex
⋮----
"""Return all NYSE trading dates between start and end (inclusive)."""
cal = USFederalHolidayCalendar()
holidays = cal.holidays(start=start, end=end)
date_range = pd.bdate_range(start=start, end=end, freq='B')
# Remove holidays and weekends
trading_dates = date_range[~date_range.isin(holidays)]
⋮----
def _prior_trading_day(earnings_date: pd.Timestamp, trading_dates: pd.DatetimeIndex) -> pd.Timestamp | None
⋮----
"""Return the prior trading day before earnings_date, or None if none exists."""
# Normalize earnings_date to tz-naive date for comparison
⋮----
earnings_date_normalized = pd.Timestamp(earnings_date.date())
⋮----
earnings_date_normalized = earnings_date
before = trading_dates[trading_dates < earnings_date_normalized]
⋮----
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
⋮----
limit = 100
⋮----
start_ts = pd.Timestamp(start)
end_ts = pd.Timestamp(end)
⋮----
# Fetch raw earnings dates from yfinance
⋮----
ticker = yf.Ticker(symbol)
raw_events = ticker.get_earnings_dates(limit=limit)
⋮----
# Reset index so earnings date is a column (yfinance returns it as index)
work = raw_events.reset_index()
⋮----
# Normalize index to datetime
⋮----
work = work.dropna(subset=["event_dt"]).copy()
⋮----
# Filter to requested date range
work = work[
⋮----
# Classify by timing
classified_rows = []
excluded_count = 0
⋮----
# Build trading calendar for T-1 computation
trading_dates = _get_nyse_trading_dates(start_ts, end_ts)
⋮----
ts = row["event_dt"]
rel_time = "UNKNOWN"
⋮----
# Convert to America/New_York
ny_ts = ts.tz_convert("America/New_York")
hour = ny_ts.hour
minute = ny_ts.minute
hm = hour * 60 + minute
⋮----
# 16:00 ET = 960 minutes, 09:30 ET = 570 minutes
⋮----
rel_time = "AMC"
⋮----
rel_time = "BMO"
⋮----
rel_time = "MIDDAY"
⋮----
# Compute T-1
t_minus_1 = _prior_trading_day(ts, trading_dates)
⋮----
df = pd.DataFrame(classified_rows)
⋮----
# Apply timing filter if requested
⋮----
df = df[df["release_time"] == timing].copy()
````

## File: data/pead_calendar.py
````python
"""PEAD live trading calendar utilities.

Handles earnings date fetching, NYSE trading calendar operations,
and T-N offset calculations.
"""
⋮----
log = logging.getLogger(__name__)
⋮----
_MARKET_TZ = ZoneInfo("America/New_York")
⋮----
_NYSE_HOLIDAYS = pd.DatetimeIndex([])
⋮----
def get_current_market_datetime(now: datetime | None = None) -> datetime
⋮----
"""Return the current timestamp in US/Eastern market time.

    If ``now`` is provided as a naive datetime, treat it as UTC for deterministic
    tests and cron environments.
    """
⋮----
now = now.replace(tzinfo=timezone.utc)
⋮----
def get_current_market_date(now: datetime | None = None) -> datetime.date
⋮----
"""Return today's date in US/Eastern market time."""
⋮----
def _get_nyse_holidays(start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex
⋮----
federal_holidays = USFederalHolidayCalendar().holidays(start=start, end=end)
good_fridays = GoodFriday.dates(start, end)
holidays = federal_holidays.union(good_fridays)
⋮----
def get_trading_dates(start: str | datetime, end: str | datetime) -> pd.DatetimeIndex
⋮----
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
⋮----
holidays = _get_nyse_holidays(start_ts, end_ts)
⋮----
# Business day range (Mon-Fri)
date_range = pd.bdate_range(start=start_ts, end=end_ts, freq='B')
⋮----
# Remove holidays
trading_dates = date_range[~date_range.isin(holidays)]
⋮----
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
⋮----
# Default calendar range if not provided
⋮----
start = anchor_ts - timedelta(days=730)
⋮----
end = anchor_ts + timedelta(days=730)
⋮----
trading_dates = get_trading_dates(start, end)
⋮----
# Normalize anchor to date-only for comparison
anchor_normalized = pd.Timestamp(anchor_ts.date())
⋮----
anchor_idx = trading_dates.get_loc(anchor_normalized)
shifted_idx = anchor_idx + offset
⋮----
"""Return the trading date for entry day T-E."""
⋮----
"""Return the last fully known trading date before entry (T-(E+1))."""
⋮----
"""Return derived PEAD timing dates for a configured entry offset."""
⋮----
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
⋮----
earnings_date = earnings_dates_dict[symbol]
entry_date = get_entry_trading_date(earnings_date, entry_offset_days)
⋮----
today = pd.Timestamp(get_current_market_date())
⋮----
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
⋮----
t_plus_1 = calculate_offset_trading_date(earnings_date, 1)
⋮----
def fetch_nearest_earnings(symbol: str, limit: int = 5) -> str | None
⋮----
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
⋮----
today = get_current_market_date()
tomorrow = today + timedelta(days=1)
end_date = today + timedelta(days=365)
⋮----
events_df = fetch_earnings_events(
⋮----
nearest_earnings = events_df.iloc[0]["earnings_date"]
⋮----
# Simple cache to avoid repeated yfinance calls within same cronjob execution
_earnings_cache: dict[str, str] = {}
⋮----
def get_cached_earnings(symbol: str, use_cache: bool = True) -> str | None
⋮----
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
⋮----
earnings_date = fetch_nearest_earnings(symbol)
⋮----
def clear_earnings_cache() -> None
⋮----
"""Clear earnings date cache (useful for testing)."""
````

## File: data/pre_earnings_features.py
````python
"""Pre-earnings feature engineering for PEAD training and live inference.

Computes features from daily OHLCV bars using only information available by the
decision date. Training mode also derives the target label from T-1 close to
earnings-day open.
"""
⋮----
log = logging.getLogger(__name__)
⋮----
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
⋮----
bars = bars_dict[symbol].copy()
bars_qqq = bars_dict[qqq_symbol].copy()
⋮----
# Ensure index is datetime; normalize to date-only for consistent slicing
⋮----
trading_dates = pd.DatetimeIndex(sorted(bars.index.unique()))
⋮----
events_df = events_df.copy()
⋮----
rows = []
⋮----
earnings_date = event["earnings_date"].date()
⋮----
t_minus_1_date = event["t_minus_1"].date()
t_minus_1_ts = pd.Timestamp(t_minus_1_date)
⋮----
t_minus_1_idx = int(trading_dates.get_loc(t_minus_1_ts))  # type: ignore[arg-type]
⋮----
t_feature_anchor_ts = trading_dates[t_minus_1_idx - entry_offset_days]
⋮----
t_feature_anchor_ts = pd.Timestamp(event["t_feature_anchor"].date())
⋮----
eligible_dates = trading_dates[trading_dates < pd.Timestamp(earnings_date)]
⋮----
t_feature_anchor_ts = eligible_dates[-entry_offset_days]
⋮----
all_bars_before_anchor = bars[bars.index <= t_feature_anchor_ts].copy()
⋮----
feature_window = all_bars_before_anchor.iloc[-7:].copy()
⋮----
# Verify no look-ahead relative to the offset-derived entry decision.
⋮----
t_open_date = pd.Timestamp(earnings_date)
⋮----
# Feature 1: Price drift
close_t7 = float(feature_window["close"].iloc[0])
close_t1 = float(feature_window["close"].iloc[-1])
drift_7d = (close_t1 - close_t7) / close_t7 if close_t7 > 0 else 0.0
⋮----
# Feature 2: Drift slope (OLS on closes)
closes = feature_window["close"].values
x = np.arange(len(closes))
⋮----
mean_close = np.mean(closes)
drift_slope = slope / mean_close if mean_close > 0 else 0.0
⋮----
drift_slope = 0.0
⋮----
# Feature 3: Up/Down day counts
daily_ret = feature_window["close"].pct_change().dropna()
up_day_count = (daily_ret > 0).sum()
down_day_count = (daily_ret < 0).sum()
⋮----
# Feature 4: Relative volume
# Baseline: 20 trading days immediately prior to the 7-day feature window.
# feature_window is the last 7 rows of all_bars_before_t1, so baseline
# ends at the row immediately before that trailing window.
baseline_end_idx = len(all_bars_before_anchor) - 8
⋮----
baseline_window = all_bars_before_anchor.iloc[baseline_end_idx - 19:baseline_end_idx + 1].copy()
⋮----
baseline_window = all_bars_before_anchor.iloc[:baseline_end_idx + 1].copy()
⋮----
baseline_vol = baseline_window["volume"].mean()
⋮----
baseline_vol = 1.0
window_vol = feature_window["volume"].mean()
rel_volume_mean = window_vol / baseline_vol if baseline_vol > 0 else 1.0
⋮----
# Feature 5: Down volume ratio
down_days = feature_window[feature_window["close"].diff() < 0]
down_vol_total = down_days["volume"].sum() if len(down_days) > 0 else 0.0
total_vol = feature_window["volume"].sum()
down_volume_ratio = down_vol_total / total_vol if total_vol > 0 else 0.0
⋮----
# Feature 6: ATR ratio (intraday range)
feature_ranges = (feature_window["high"] - feature_window["low"]).mean()
⋮----
baseline_ranges = (baseline_window["high"] - baseline_window["low"]).mean()
⋮----
baseline_ranges = 1.0
atr_ratio = feature_ranges / baseline_ranges if baseline_ranges > 0 else 1.0
⋮----
# Feature 7: Gap count (overnight gaps > 0.5%)
gaps = abs(feature_window["open"].values[1:] - feature_window["close"].values[:-1]) / (
gap_count = (gaps > 0.005).sum()
⋮----
# Feature 8: Relative to QQQ
# Extract QQQ bars for the same window
all_qqq_before_anchor = bars_qqq[bars_qqq.index <= t_feature_anchor_ts].copy()
⋮----
qqq_window = all_qqq_before_anchor.iloc[-7:].copy()
qqq_close_t7 = float(qqq_window["close"].iloc[0])
qqq_close_t1 = float(qqq_window["close"].iloc[-1])
qqq_drift = (qqq_close_t1 - qqq_close_t7) / qqq_close_t7 if qqq_close_t7 > 0 else 0.0
rel_drift_vs_qqq = drift_7d - qqq_drift
⋮----
rel_drift_vs_qqq = drift_7d
⋮----
row = {
⋮----
# Target label remains the original PEAD gap objective: T-1 close to T open.
⋮----
close_t1_value = bars.loc[t_minus_1_ts, "close"]
⋮----
close_t1_value = close_t1_value.iloc[0]
close_t1_float = np.asarray(close_t1_value, dtype=np.float64).item()
open_t_value = bars.loc[t_open_date, "open"]
⋮----
open_t_value = open_t_value.iloc[0]
open_t_float = np.asarray(open_t_value, dtype=np.float64).item()
gap_return = (open_t_float / close_t1_float - 1.0) if close_t1_float > 0 else 0.0
⋮----
result = pd.DataFrame(rows)
````

## File: openspec/changes/archive/2026-04-19-momentum-m7-strategy/specs/backtest-engine/spec.md
````markdown
## ADDED Requirements

### Requirement: Event-driven iteration over time bars
The backtest engine SHALL iterate over each time bar in chronological order, evaluating strategy signals and simulating order execution at each bar.

#### Scenario: Bar-by-bar event loop
- **WHEN** `run_backtest()` is called
- **THEN** the engine processes each bar from index `lookback` to `len(data)-1` in order, calling `on_bar(bar)` exactly once per bar

### Requirement: Simulated order execution with transaction costs
The engine SHALL simulate buy and sell orders using the closing price at the signal bar, applying configurable fixed transaction cost (`ftc`) and proportional transaction cost (`ptc`).

#### Scenario: Buy order reduces cash balance
- **WHEN** a buy order is placed for N units at price P with ptc=0.001 and ftc=0
- **THEN** cash decreases by `N * P * (1 + ptc) + ftc`

#### Scenario: Sell order increases cash balance
- **WHEN** a sell order is placed for N units at price P with ptc=0.001 and ftc=0
- **THEN** cash increases by `N * P * (1 - ptc) - ftc`

### Requirement: Multi-symbol portfolio state tracking
The engine SHALL maintain portfolio state across multiple symbols: cash balance, units held per symbol, and current position per symbol.

#### Scenario: Portfolio state initialized correctly
- **WHEN** a backtest is instantiated with `initial_amount=10000`
- **THEN** cash equals 10000, units_held is an empty dict, and all positions are neutral (0)

#### Scenario: Portfolio state updated after trade
- **WHEN** a buy order is executed for symbol S
- **THEN** `units_held[S]` reflects the purchased units and cash reflects the deducted amount

### Requirement: Equity curve recorded at each rebalance
The engine SHALL record total portfolio value (cash + mark-to-market holdings) at each rebalance event, producing an equity curve as a pandas Series indexed by date.

#### Scenario: Equity curve length matches rebalance count
- **WHEN** backtest runs over a period with W weekly rebalances
- **THEN** the equity curve has exactly W+1 entries (including initial value)

### Requirement: Final close-out and summary
The engine SHALL close all open positions at the last bar and print a summary: final balance, net performance (%), number of trades, and call `calculate_risk_metrics()`.

#### Scenario: Close-out at end of backtest
- **WHEN** the event loop reaches the final bar
- **THEN** all positions are liquidated at the last closing price and the final cash balance reflects all proceeds
````

## File: openspec/changes/archive/2026-04-19-momentum-m7-strategy/specs/data-layer/spec.md
````markdown
## ADDED Requirements

### Requirement: Fetch daily OHLCV bars for a symbol universe
The system SHALL fetch historical daily bar data for a list of symbols using alpaca-py `StockHistoricalDataClient`, returning a dict mapping each symbol to a pandas DataFrame with columns: `open`, `high`, `low`, `close`, `volume` indexed by date.

#### Scenario: Successful multi-symbol fetch
- **WHEN** `fetch_bars(symbols, start, end, timeframe)` is called with a list of valid symbols and a date range
- **THEN** the function returns a dict where each key is a symbol string and each value is a DataFrame with OHLCV columns indexed by UTC date

#### Scenario: Symbol with no data in range
- **WHEN** a symbol is requested but has no data in the given date range
- **THEN** the function raises a descriptive `ValueError` identifying the missing symbol

### Requirement: Load API credentials from environment
The data layer SHALL load `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` from environment variables (via `.env` file) and MUST NOT accept credentials as hardcoded arguments.

#### Scenario: Credentials loaded from .env
- **WHEN** `fetch_bars()` is called and a `.env` file with valid credentials exists
- **THEN** the `StockHistoricalDataClient` authenticates successfully and returns data

#### Scenario: Missing credentials
- **WHEN** `APCA_API_KEY_ID` or `APCA_API_SECRET_KEY` is not set in the environment
- **THEN** the function raises a `EnvironmentError` before making any API calls

### Requirement: Compute log returns after fetch
The data layer SHALL add a `return` column to each symbol's DataFrame, computed as `log(close / close.shift(1))`, and drop rows with NaN values.

#### Scenario: Returns column present after fetch
- **WHEN** `fetch_bars()` returns successfully
- **THEN** each symbol DataFrame contains a `return` column with no NaN values
````

## File: openspec/changes/archive/2026-04-19-momentum-m7-strategy/specs/live-trader/spec.md
````markdown
## ADDED Requirements

### Requirement: Connect to Alpaca paper trading account
The live trader SHALL connect to Alpaca's paper trading endpoint using `TradingClient(api_key, secret_key, paper=True)` and MUST NOT connect to the live trading endpoint.

#### Scenario: Paper trading connection established
- **WHEN** `LiveTrader` is instantiated
- **THEN** it creates a `TradingClient` with `paper=True` and verifies the account is accessible

#### Scenario: Live endpoint connection refused
- **WHEN** `paper=False` is passed to `TradingClient`
- **THEN** the `LiveTrader` constructor raises a `ValueError` refusing to proceed

### Requirement: Compute momentum signal using latest market data
The live trader SHALL fetch the most recent N+1 daily bars for all M7 symbols using `StockHistoricalDataClient`, compute N-day returns, and rank symbols — identical logic to the backtest signal.

#### Scenario: Signal computed from latest data
- **WHEN** `compute_signal()` is called
- **THEN** it returns a ranked list of symbols using the same lookback window as the configured backtest

### Requirement: Submit market orders for target portfolio
The live trader SHALL submit `MarketOrderRequest` buy orders for new holdings and sell orders for dropped holdings at market price.

#### Scenario: Buy order submitted for new holding
- **WHEN** symbol S enters the top-N but is not currently held
- **THEN** a market buy order for `floor(allocation / current_price)` shares of S is submitted

#### Scenario: Sell order submitted for dropped holding
- **WHEN** symbol S was held but no longer in top-N
- **THEN** a market sell order for all held shares of S is submitted

#### Scenario: No order for unchanged holdings
- **WHEN** symbol S is in top-N and already held with approximately correct weight
- **THEN** no order is submitted for S

### Requirement: Weekly rebalance trigger
The live trader SHALL expose a `rebalance()` method that executes the full signal → order cycle. It is the caller's responsibility to invoke this weekly (via cron, scheduler, or manual execution).

#### Scenario: Rebalance completes without error
- **WHEN** `rebalance()` is called on a Friday during market hours or pre-market
- **THEN** all necessary orders are submitted and a summary is printed to stdout

#### Scenario: Market closed handling
- **WHEN** `rebalance()` is called outside market hours
- **THEN** orders are submitted as market orders and will fill at next open; a warning is logged

### Requirement: Log all order submissions
The live trader SHALL log each order submission (symbol, side, quantity, order ID) to stdout.

#### Scenario: Order logged on submission
- **WHEN** any order is submitted
- **THEN** a line is printed: `[YYYY-MM-DD HH:MM] BUY/SELL <qty> <symbol> → order_id=<id>`
````

## File: openspec/changes/archive/2026-04-19-momentum-m7-strategy/specs/momentum-strategy/spec.md
````markdown
## ADDED Requirements

### Requirement: Rank symbols by N-day simple return
The strategy SHALL compute the N-day simple price return for each symbol at each rebalance bar and rank symbols from highest to lowest return.

#### Scenario: Returns computed at each rebalance
- **WHEN** the rebalance event fires at bar T
- **THEN** each symbol's score is `(close[T] - close[T-N]) / close[T-N]` where N is the configured lookback window

#### Scenario: Symbols ranked correctly
- **WHEN** NVDA has return=0.42, META=0.28, AAPL=0.05, others negative
- **THEN** ranking is NVDA(1), META(2), AAPL(3), ... in descending order

### Requirement: Go long top-N symbols equal-weight
The strategy SHALL enter long positions in the top `top_n` ranked symbols, allocating equal weight (1/top_n of available capital) to each. Symbols outside the top-N SHALL be sold if currently held.

#### Scenario: Equal-weight allocation
- **WHEN** top_n=3 and available capital is $9000
- **THEN** each of the 3 selected symbols receives $3000 of capital

#### Scenario: Dropped symbol is sold
- **WHEN** symbol S was in the top-N at the previous rebalance but is no longer in the top-N at the current rebalance
- **THEN** all units of S are sold at the current closing price

#### Scenario: New symbol enters top-N
- **WHEN** symbol S enters the top-N at the current rebalance and is not currently held
- **THEN** a buy order is placed for S using its equal-weight capital allocation

### Requirement: Rebalance only on weekly frequency
The strategy SHALL only execute rebalance logic on the last trading day of each calendar week (Friday, or Thursday if Friday is a holiday).

#### Scenario: Rebalance fires on Friday
- **WHEN** the current bar's date is a Friday
- **THEN** the full ranking and rebalance logic executes

#### Scenario: No trades on non-rebalance days
- **WHEN** the current bar's date is Monday through Thursday
- **THEN** no orders are placed and portfolio state is unchanged

### Requirement: Configurable parameters
The strategy SHALL accept `lookback` (int, days), `top_n` (int), `symbols` (list of str), `start` (str date), `end` (str date), `initial_amount` (float), `ftc` (float), and `ptc` (float) as constructor parameters.

#### Scenario: Default parameters produce valid backtest
- **WHEN** strategy is instantiated with symbols=M7, lookback=60, top_n=3, initial_amount=10000
- **THEN** backtest runs without error over the configured date range
````

## File: openspec/changes/archive/2026-04-19-momentum-m7-strategy/specs/risk-analytics/spec.md
````markdown
## ADDED Requirements

### Requirement: Compute annualized Sharpe ratio from equity curve
The risk module SHALL compute the annualized Sharpe ratio from a weekly equity curve using the formula: `mean(weekly_returns) / std(weekly_returns) * sqrt(52)`, assuming risk-free rate of 0.

#### Scenario: Sharpe ratio computed correctly
- **WHEN** `sharpe_ratio(equity_curve, periods_per_year=52)` is called with a pandas Series of weekly portfolio values
- **THEN** it returns a float representing the annualized Sharpe ratio

#### Scenario: Flat equity curve returns zero Sharpe
- **WHEN** all equity values are equal (zero volatility)
- **THEN** the function returns 0.0 (not NaN or error)

### Requirement: Compute maximum drawdown
The risk module SHALL compute maximum drawdown as the largest peak-to-trough decline in the equity curve, expressed as a percentage: `(trough - peak) / peak * 100`.

#### Scenario: Maximum drawdown computed
- **WHEN** `max_drawdown(equity_curve)` is called
- **THEN** it returns a negative float representing the worst percentage decline from any peak

#### Scenario: Always-rising equity has zero drawdown
- **WHEN** the equity curve is monotonically increasing
- **THEN** `max_drawdown` returns 0.0

### Requirement: Compute Calmar ratio
The risk module SHALL compute the Calmar ratio as `annualized_return / abs(max_drawdown)`, where annualized return is `(final_value / initial_value) ^ (periods_per_year / n_periods) - 1`.

#### Scenario: Calmar ratio computed
- **WHEN** `calmar_ratio(equity_curve, periods_per_year=52)` is called
- **THEN** it returns a positive float when the strategy is profitable

### Requirement: Print risk summary
The risk module SHALL provide a `print_summary(equity_curve)` function that prints Sharpe ratio, maximum drawdown, Calmar ratio, total return (%), and number of periods to stdout.

#### Scenario: Summary printed after backtest
- **WHEN** `print_summary(equity_curve)` is called
- **THEN** all four metrics are printed with labels and rounded to 2 decimal places

### Requirement: Plot equity curve
The risk module SHALL provide a `plot_equity_curve(equity_curve, title)` function that renders a matplotlib line chart of portfolio value over time.

#### Scenario: Plot generated without error
- **WHEN** `plot_equity_curve(equity_curve, title="M7 Momentum")` is called
- **THEN** a matplotlib figure is created and displayed (or saved if a path is provided)
````

## File: openspec/changes/archive/2026-04-19-momentum-m7-strategy/.openspec.yaml
````yaml
schema: spec-driven
created: 2026-04-19
````

## File: openspec/changes/archive/2026-04-19-momentum-m7-strategy/design.md
````markdown
## Context

This is a greenfield algorithmic trading project building on the event-driven backtest pattern from Hilpisch's *Python for Algorithmic Trading* (Chapter 6). The existing `BacktestBase` / `BacktestLongOnly` classes in `strategy-lab` provide proven mechanics (event loop, order simulation, P&L tracking) but are tightly coupled to a single symbol and a remote CSV data source. This project adapts that pattern for Alpaca's API, extends it to multi-symbol portfolios, and adds a live paper trading path.

The `strategy-lab` conda environment provides all required dependencies: `alpaca-py`, `pandas`, `numpy`, `python-dotenv`.

## Goals / Non-Goals

**Goals:**
- Layered architecture (`core/`, `data/`, `strategies/`) so future strategies share infrastructure without duplication
- Event-driven backtest with full portfolio simulation: multi-symbol, weekly rebalance, transaction cost simulation
- Risk analytics: annualized Sharpe ratio (√52), max drawdown, Calmar ratio, equity curve
- Paper trading live execution via `alpaca-py` using the same signal as the backtest
- Reproducible results with configurable parameters (lookback window, top-N holdings, backtest period)

**Non-Goals:**
- Intraday (sub-daily) bars — daily bars only for this change
- Long-short — long-only
- Live trading with real money — paper account only
- Optimization / parameter sweep — single parameter set, no grid search
- Portfolio margin / leverage calculations
- Notifications or alerting

## Decisions

### D1: Layered architecture over strategy-per-folder

**Decision**: Shared `core/`, `data/`, `risk/` modules; strategy implementations under `strategies/`.

**Rationale**: A folder-per-strategy pattern duplicates data fetching, order simulation, and risk calculation across every strategy. The layered approach mirrors standard OOP design — abstract base classes in `core/`, concrete implementations in `strategies/`. When `mean_reversion` is added later, it subclasses `BacktestBase` and reuses `data/` and `risk/` unchanged.

**Alternative considered**: Copy-paste from `strategy-lab` per strategy. Rejected — creates maintenance burden and diverging logic.

```
alpaca-lab/
├── core/
│   ├── backtest_base.py       ← AlpacaBacktestBase (abstract)
│   └── live_trader_base.py    ← AlpacaLiveTraderBase (abstract)
├── data/
│   └── alpaca_data.py         ← fetch_bars() via alpaca-py
├── risk/
│   └── metrics.py             ← Sharpe, drawdown, Calmar, plot
├── strategies/
│   └── momentum.py            ← CrossSectionalMomentum(BacktestBase)
├── config.py                  ← .env loading, M7 symbols, params
└── run.py                     ← CLI entry point
```

### D2: Weekly rebalance frequency

**Decision**: Rebalance every Friday (or last trading day of the week).

**Rationale**: Cross-sectional momentum signal has low turnover on daily bars — rankings rarely change day-to-day among M7. Weekly rebalancing reduces transaction costs while capturing meaningful rank shifts. Monthly is too slow for a 7-stock universe where one breakout (e.g., NVDA) can dominate. Daily introduces noise.

**Alternative considered**: Monthly. Rejected — with only 7 symbols, monthly is too coarse; a single outlier holds for too long.

### D3: Momentum signal = N-day simple return, no skip window

**Decision**: Signal = `(price[t] - price[t-N]) / price[t-N]`, no 1-month skip.

**Rationale**: The classic "12-1" skip window (skip most recent month to avoid reversal) is designed for large cross-sectional universes. With only 7 highly-correlated mega-caps, the reversal effect is less pronounced and the skip window reduces the already-small information set. Start without skip; revisit if backtest shows reversal drag.

**Alternative considered**: Log return rolling mean (Hilpisch style). Rejected in favor of simple price return — more interpretable and standard in momentum literature.

### D4: Data fetching via alpaca-py `StockHistoricalDataClient`

**Decision**: Fetch all M7 symbols in a single batched request, cache as a dict of DataFrames keyed by symbol.

**Rationale**: Alpaca's API supports multi-symbol requests natively. Fetching once at backtest start and caching avoids repeated API calls during the event loop. The backtest iterates over time index using `.iloc[bar]` slices per the Hilpisch pattern.

**Alternative considered**: Download to CSV and read locally. Acceptable for production but adds a data management step; fetch-and-cache is simpler for the first iteration.

### D5: Risk metrics in standalone `risk/metrics.py`

**Decision**: Risk calculations are pure functions operating on an equity curve (pandas Series), not methods on the backtest class.

**Rationale**: Pure functions are easier to test, reuse across strategies, and compose. The backtest `close_out()` produces the equity curve; `risk/metrics.py` consumes it. This decouples strategy logic from analytics.

### D6: Live trader uses polling loop, not WebSocket stream

**Decision**: Live paper trader runs as a scheduled weekly job — compute signal at market open Friday, submit orders, exit.

**Rationale**: Interday momentum does not require tick-level data. A simple script that runs once per week (cron or manual trigger) is far simpler than a persistent WebSocket connection. WebSocket is appropriate for intraday strategies (future work).

**Alternative considered**: `StockDataStream` WebSocket. Rejected for this change — adds complexity without benefit for weekly frequency.

## Risks / Trade-offs

- **[Lookahead bias]** → Ensure rebalance signal uses close price of day T, execute at open of day T+1 (next Friday open). The backtest must simulate this correctly.
- **[Survivorship bias]** → M7 is a backward-looking selection; all seven have survived and thrived. Backtest results will be optimistic vs. a live forward universe. Acknowledged limitation, acceptable for this learning project.
- **[Alpaca API rate limits]** → Fetching 6 years of daily bars for 7 symbols is well within free tier limits. Low risk.
- **[Paper trading order fills]** → Alpaca paper trading uses simulated fills at last trade price. May not perfectly reflect real slippage. Acceptable for paper.
- **[M7 composition drift]** → The "M7" label is recent; historical data for these tickers exists back to 2019 but their collective identity as a group did not. Backtest treats them as a static universe throughout — this is a known approximation.

## Open Questions

- **Lookback window default**: Start with 60 days (3 months)? Easy to make configurable.
- **Transaction cost simulation**: Use Alpaca's commission-free model (ptc=0, ftc=0) for paper, or simulate realistic costs (e.g., 0.1% ptc)?
- **Benchmark**: Compare equity curve against SPY buy-and-hold? Would strengthen the backtest analysis.
````

## File: openspec/changes/archive/2026-04-19-momentum-m7-strategy/proposal.md
````markdown
## Why

This project needs a repeatable, well-tested algorithmic trading strategy that can be backtested rigorously and deployed to paper trading. Cross-sectional momentum on the Magnificent 7 (M7) provides a focused, high-signal universe to validate the full pipeline — from data ingestion through live execution — before expanding to broader universes or additional strategies.

## What Changes

- Introduce a layered project structure with shared `core/`, `data/`, and `strategies/` packages to support multiple strategies without code duplication
- Implement a cross-sectional momentum strategy targeting the M7 stocks (AAPL, MSFT, AMZN, NVDA, GOOGL, META, TSLA)
- Build an event-driven backtester modeled after the Hilpisch pattern, adapted to fetch data from Alpaca's historical bars API
- Add a risk analytics module computing Sharpe ratio, maximum drawdown, and Calmar ratio
- Implement a paper trading live trader using `alpaca-py` TradingClient with weekly rebalancing

## Capabilities

### New Capabilities

- `data-layer`: Fetch and cache daily OHLCV bars for a symbol universe via alpaca-py `StockHistoricalDataClient`
- `backtest-engine`: Event-driven backtesting base class supporting multi-symbol portfolios with transaction cost simulation
- `momentum-strategy`: Cross-sectional momentum signal: rank M7 by N-day return, go long top 3 equal-weight, rebalance weekly
- `risk-analytics`: Compute annualized Sharpe ratio (√52 for weekly), maximum drawdown (peak-to-trough), and Calmar ratio from an equity curve
- `live-trader`: Paper trading execution using `alpaca-py` TradingClient — weekly rebalance, same signal as backtest

### Modified Capabilities

## Impact

- **New packages**: `core/`, `data/`, `strategies/` under `alpaca-lab/`
- **Dependencies**: `alpaca-py`, `pandas`, `numpy`, `python-dotenv` (all present in `strategy-lab` conda env)
- **Config**: `.env` file with `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` (paper trading keys)
- **No existing code modified** — greenfield implementation
````

## File: openspec/changes/archive/2026-04-19-momentum-m7-strategy/tasks.md
````markdown
## 1. Project Structure & Config

- [x] 1.1 Create directory layout: `core/`, `data/`, `risk/`, `strategies/` with `__init__.py` files
- [x] 1.2 Create `config.py` with M7 symbol list, default parameters (lookback=60, top_n=3, start/end dates), and `.env` loading via `python-dotenv`

## 2. Data Layer (`data/alpaca_data.py`)

- [x] 2.1 Implement `fetch_bars(symbols, start, end, timeframe=TimeFrame.Day)` using `StockHistoricalDataClient`
- [x] 2.2 Add credential loading from environment variables; raise `EnvironmentError` if missing
- [x] 2.3 Add log return column (`return = log(close / close.shift(1))`) and drop NaN rows for each symbol
- [x] 2.4 Raise `ValueError` with descriptive message if any requested symbol returns empty data

## 3. Backtest Engine (`core/backtest_base.py`)

- [x] 3.1 Implement `AlpacaBacktestBase.__init__` with portfolio state: `cash`, `units_held` (dict), `trades`, `equity_curve` (list)
- [x] 3.2 Implement `place_buy_order(symbol, bar, amount)` with `ftc`/`ptc` cost simulation
- [x] 3.3 Implement `place_sell_order(symbol, bar, units)` with `ftc`/`ptc` cost simulation
- [x] 3.4 Implement `get_portfolio_value(bar)` summing cash + mark-to-market value of all holdings
- [x] 3.5 Implement `close_out(bar)` to liquidate all positions and append final equity curve entry
- [x] 3.6 Implement `run_backtest()` event loop: iterate bars, detect Friday rebalance, call `on_bar(bar)`, record equity

## 4. Risk Analytics (`risk/metrics.py`)

- [x] 4.1 Implement `sharpe_ratio(equity_curve, periods_per_year=52)` — handle zero-volatility edge case
- [x] 4.2 Implement `max_drawdown(equity_curve)` — peak-to-trough percentage
- [x] 4.3 Implement `calmar_ratio(equity_curve, periods_per_year=52)`
- [x] 4.4 Implement `print_summary(equity_curve)` printing all metrics rounded to 2 decimal places
- [x] 4.5 Implement `plot_equity_curve(equity_curve, title, save_path=None)` using matplotlib

## 5. Momentum Strategy (`strategies/momentum.py`)

- [x] 5.1 Implement `CrossSectionalMomentum(AlpacaBacktestBase).__init__` accepting all configurable parameters
- [x] 5.2 Implement `compute_scores(bar)` — N-day simple return for each symbol, return ranked Series
- [x] 5.3 Implement `on_bar(bar)` — if Friday: call `compute_scores`, select top_n, sell dropped symbols, buy new symbols equal-weight
- [x] 5.4 Implement `run_backtest()` override calling parent event loop, then `risk.print_summary(self.equity_curve)` and `risk.plot_equity_curve()`
- [x] 5.5 Verify rebalance-only-on-Friday logic: non-Friday bars must produce no orders

## 6. Entry Point (`run.py`)

- [x] 6.1 Create `run.py` CLI that instantiates `CrossSectionalMomentum` with params from `config.py` and calls `run_backtest()`
- [x] 6.2 Print backtest configuration summary (symbols, lookback, top_n, date range, initial capital) before running

## 7. Live Trader (`core/live_trader_base.py` + `strategies/momentum.py`)

- [x] 7.1 Implement `AlpacaLiveTraderBase.__init__` with `TradingClient(paper=True)`; raise `ValueError` if `paper=False`
- [x] 7.2 Implement `get_current_positions()` using `TradingClient.get_all_positions()`
- [x] 7.3 Implement `submit_order(symbol, side, qty)` using `MarketOrderRequest`; log each submission
- [x] 7.4 Add `LiveMomentumTrader(AlpacaLiveTraderBase)` with `compute_signal()` using `StockHistoricalDataClient`
- [x] 7.5 Implement `rebalance()`: fetch latest data → compute signal → diff vs current positions → submit buy/sell orders
- [x] 7.6 Add market-hours warning when `rebalance()` is called outside NYSE hours

## 8. Validation

- [ ] 8.1 Run backtest over 2019-01-01 to 2024-12-31; confirm equity curve is generated and risk metrics print without error
- [ ] 8.2 Visually inspect equity curve plot for sanity (no flat lines, no NaN gaps)
- [ ] 8.3 Run `python run.py` and confirm output includes Sharpe ratio, max drawdown, Calmar ratio
- [ ] 8.4 Run `LiveMomentumTrader.rebalance()` once against paper account; confirm orders appear in Alpaca paper dashboard
````

## File: openspec/changes/archive/2026-04-21-moc-execution/specs/live-trader/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Submit market orders for target portfolio
The live trader SHALL submit `MarketOrderRequest` buy and sell orders using `TimeInForce.CLS` (Market-on-Close) so that live execution price matches the closing price assumed by the backtest engine. Orders MUST be submitted while the market is open and before the exchange MOC cutoff (3:50 PM ET / 19:50 UTC).

#### Scenario: Buy order submitted as MOC for new holding
- **WHEN** symbol S enters the top-N but is not currently held
- **THEN** a MOC buy order (`time_in_force=TimeInForce.CLS`) for `floor(allocation / current_price)` shares of S is submitted

#### Scenario: Sell order submitted as MOC for dropped holding
- **WHEN** symbol S was held but no longer in top-N
- **THEN** a MOC sell order (`time_in_force=TimeInForce.CLS`) for all held shares of S is submitted

#### Scenario: No order for unchanged holdings
- **WHEN** symbol S is in top-N and already held with approximately correct weight
- **THEN** no order is submitted for S

### Requirement: Weekly rebalance trigger
The live trader SHALL expose a `rebalance()` method that executes the full signal → order cycle. The caller SHALL invoke this weekly via cron at `45 19 * * 1` (19:45 UTC, 2:45 PM ET) to ensure MOC orders are submitted before the 19:50 UTC exchange cutoff.

#### Scenario: Rebalance completes with MOC orders
- **WHEN** `rebalance()` is called on a Monday between market open and 19:50 UTC
- **THEN** all necessary MOC orders are submitted and confirmed via log output

#### Scenario: Market closed handling
- **WHEN** `rebalance()` is called outside market hours
- **THEN** a `RuntimeError` is raised and no orders are submitted
````

## File: openspec/changes/archive/2026-04-21-moc-execution/.openspec.yaml
````yaml
schema: spec-driven
created: 2026-04-20
````

## File: openspec/changes/archive/2026-04-21-moc-execution/design.md
````markdown
## Context

The live trader currently submits intraday market orders (`TimeInForce.DAY`) at ~10:35 AM ET every Monday. The backtest engine simulates execution at Monday's closing price. This gap means live returns will differ from backtested results even with the same signal.

Additionally, the cron is set to `35 14 * * 1` (14:35 UTC), which is only 5 minutes after open during winter (EST, UTC-5), placing execution in the noisiest window of the trading day.

## Goals / Non-Goals

**Goals:**
- Align live execution price with the backtest's close-price assumption
- Eliminate DST sensitivity in the cron timing by switching to a fixed UTC pre-close window
- Ensure `_warn_if_outside_hours` remains a useful guard under the new timing model

**Non-Goals:**
- Changing the signal computation (still based on prior close prices)
- Supporting fractional shares or notional orders
- Modifying the backtest engine (already correct)

## Decisions

### Decision: Use `TimeInForce.CLS` (MOC orders)

**Chosen**: Change `submit_order` to use `TimeInForce.CLS` in `MarketOrderRequest`.

**Alternatives considered:**
- `TimeInForce.DAY` at a later time (e.g., 15:30 UTC) — still intraday, still diverges from backtest close price
- Limit orders at last close price — complicates order management, risk of non-fill

**Rationale**: MOC is the simplest change that closes the backtest/live gap. The execution price *is* the close price, exactly what the backtest models. Alpaca paper trading supports MOC.

### Decision: Cron timing → 19:45 UTC Monday

**Chosen**: `45 19 * * 1` — 2:45 PM ET year-round (19:50 UTC is Alpaca's MOC cutoff; 5-min buffer).

**Rationale**: NYSE MOC cutoff is 3:50 PM ET = 19:50 UTC fixed (no DST shift since NYSE close is always 21:00 UTC). 19:45 UTC gives a 5-minute submission buffer while ensuring the script runs well within the window.

### Decision: Relax `_warn_if_outside_hours` to check only market-open, not time-of-day

**Chosen**: Keep the existing `is_open` check. MOC orders must be submitted while the market is open (after 9:30 AM, before 3:50 PM ET). Alpaca's clock `is_open` flag covers this window naturally — no additional time-of-day logic needed.

**Rationale**: Adding a hardcoded 19:50 UTC ceiling creates a new DST-like fragility. Alpaca's clock is the authoritative source.

## Risks / Trade-offs

- **MOC not accepted on halted stocks** → Alpaca will reject the order; the existing error logging in `submit_order` will capture this. No special handling needed for paper trading.
- **Script fires after 19:50 UTC** (e.g., cron delay, server lag) → MOC deadline missed, order rejected. Mitigation: 5-minute buffer in cron timing; operator should monitor `output/live_rebalance.log`.
- **Price slippage at close auction** → MOC fills at the official closing price; any large imbalance in the closing auction could affect fill. Negligible at these quantities vs. M7 daily volume.

## Migration Plan

1. Update `TimeInForce.DAY` → `TimeInForce.CLS` in `live_trader_base.py`
2. Update crontab on the DigitalOcean droplet: `35 14 * * 1` → `45 19 * * 1`
3. Update the crontab comment in `weekly_live_rebalance.py` and example in `README.md`
4. Next Monday: verify orders appear in Alpaca UI as MOC type, confirm fill at closing price

**Rollback**: Revert `TimeInForce.CLS` to `TimeInForce.DAY` and restore crontab. No data migration required.

## Open Questions

None — all decisions resolved in the explore session.
````

## File: openspec/changes/archive/2026-04-21-moc-execution/proposal.md
````markdown
## Why

Live orders execute mid-morning (~10:35 AM ET) using `TimeInForce.DAY`, while the backtest simulates execution at Monday's close price. This backtest/live misalignment means live results will diverge from backtested expectations. Switching to Market-on-Close (MOC) orders aligns live execution with the close price the backtest already assumes, eliminates DST sensitivity in the cron schedule, and reduces intraday slippage noise.

## What Changes

- `core/live_trader_base.py`: Change `TimeInForce.DAY` → `TimeInForce.CLS` in `submit_order`
- `core/live_trader_base.py`: Update `_warn_if_outside_hours` to also enforce a pre-close submission cutoff (must submit before 3:50 PM ET)
- `scripts/weekly_live_rebalance.py`: Update crontab comment to reflect new timing
- `README.md`: Update crontab example from `35 14 * * 1` (14:35 UTC) to `45 19 * * 1` (19:45 UTC, DST-safe)

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `live-trader`: Order submission now uses MOC (`TimeInForce.CLS`) instead of intraday market orders; `_warn_if_outside_hours` enforces a pre-close cutoff in addition to market-open check.

## Impact

- **`core/live_trader_base.py`**: `submit_order` and `_warn_if_outside_hours` change
- **`scripts/weekly_live_rebalance.py`**: Comment update only
- **`README.md`**: Crontab example update
- **`core/backtest_base.py`**: No changes required — already executes at close
- **`strategies/momentum.py`**: No changes required
- **Dependencies**: `alpaca-py` already exposes `TimeInForce.CLS`; no new packages needed
````

## File: openspec/changes/archive/2026-04-21-moc-execution/tasks.md
````markdown
## 1. Live Trader — MOC Order Execution

- [x] 1.1 In `core/live_trader_base.py`, change `time_in_force=TimeInForce.DAY` to `time_in_force=TimeInForce.CLS` in `submit_order`

## 2. Documentation — Crontab Timing

- [x] 2.1 In `scripts/weekly_live_rebalance.py`, update the crontab comment from `35 14 * * 1` (14:35 UTC) to `45 19 * * 1` (19:45 UTC) and update the timing rationale comment
- [x] 2.2 In `README.md`, update the crontab example from `35 14 * * 1` to `45 19 * * 1` and update the timing explanation

## 3. Verification

- [ ] 3.1 Update the crontab on the DigitalOcean droplet to `45 19 * * 1`
- [ ] 3.2 On next Monday, verify orders appear in Alpaca UI as MOC type and fill at the official closing price
````

## File: openspec/changes/archive/2026-04-22-ml-pre-earnings-price-prediction/specs/data-layer/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Fetch daily OHLCV bars for a symbol universe
The system SHALL fetch historical daily bar data for a list of symbols using alpaca-py `StockHistoricalDataClient`, returning a dict mapping each symbol to a pandas DataFrame with columns: `open`, `high`, `low`, `close`, `volume` indexed by date. The function SHALL accept an optional `symbols` parameter allowing single-symbol fetches (e.g., `["QQQ"]`) in addition to the existing multi-symbol use case. All other behavior is unchanged.

#### Scenario: Successful multi-symbol fetch
- **WHEN** `fetch_bars(symbols, start, end, timeframe)` is called with a list of valid symbols and a date range
- **THEN** the function returns a dict where each key is a symbol string and each value is a DataFrame with OHLCV columns indexed by UTC date

#### Scenario: Single-symbol fetch for benchmark
- **WHEN** `fetch_bars(["QQQ"], start, end)` is called
- **THEN** the function returns a dict with a single key `"QQQ"` and a valid OHLCV DataFrame

#### Scenario: Symbol with no data in range
- **WHEN** a symbol is requested but has no data in the given date range
- **THEN** the function raises a descriptive `ValueError` identifying the missing symbol

#### Scenario: Credentials loaded from .env
- **WHEN** `fetch_bars()` is called and a `.env` file with valid credentials exists
- **THEN** the `StockHistoricalDataClient` authenticates successfully and returns data

#### Scenario: Missing credentials
- **WHEN** `APCA_API_KEY_ID` or `APCA_API_SECRET_KEY` is not set in the environment
- **THEN** the function raises a `EnvironmentError` before making any API calls

#### Scenario: Returns column present after fetch
- **WHEN** `fetch_bars()` returns successfully
- **THEN** each symbol DataFrame contains a `return` column with no NaN values
````

## File: openspec/changes/archive/2026-04-22-ml-pre-earnings-price-prediction/specs/earnings-calendar/spec.md
````markdown
## ADDED Requirements

### Requirement: Fetch earnings event dates for a symbol via yfinance
The earnings calendar module SHALL fetch historical earnings dates for a given symbol using `yfinance.Ticker(symbol).get_earnings_dates(limit)`, returning a structured DataFrame with columns: `earnings_date` (date), `release_time` (`AMC` or `BMO`), and `symbol`.

#### Scenario: Successful fetch for GOOGL
- **WHEN** `fetch_earnings_events("GOOGL", start="2018-01-01")` is called
- **THEN** the function returns a DataFrame with at least one row per quarterly earnings event since 2018, each with a non-null `earnings_date` and `release_time` value

#### Scenario: Events before start date are excluded
- **WHEN** `fetch_earnings_events("GOOGL", start="2022-01-01")` is called
- **THEN** no events with `earnings_date` before 2022-01-01 appear in the result

### Requirement: Classify each event as AMC or BMO
The module SHALL classify each earnings event as `AMC` (after market close, release time after 16:00 ET) or `BMO` (before market open, release time before 09:30 ET) based on the yfinance timestamp field. Events with ambiguous or null timestamps SHALL be excluded and logged.

#### Scenario: After-close event classified as AMC
- **WHEN** yfinance reports a release time of 17:00 ET for an earnings event
- **THEN** the event is tagged `release_time = "AMC"`

#### Scenario: Pre-open event classified as BMO
- **WHEN** yfinance reports a release time of 07:00 ET for an earnings event
- **THEN** the event is tagged `release_time = "BMO"`

#### Scenario: Ambiguous timestamp excluded
- **WHEN** yfinance returns a null or mid-day timestamp for an event
- **THEN** the event is excluded from the result and a warning is logged identifying the event date and symbol

### Requirement: Filter to AMC events only for Phase 1
The module SHALL support a `timing` parameter that, when set to `"AMC"`, returns only after-close events. This is the required filter for Phase 1 of the strategy.

#### Scenario: AMC filter applied
- **WHEN** `fetch_earnings_events("GOOGL", timing="AMC")` is called
- **THEN** the returned DataFrame contains only rows where `release_time == "AMC"`

#### Scenario: No filter returns all classified events
- **WHEN** `fetch_earnings_events("GOOGL", timing=None)` is called
- **THEN** the returned DataFrame contains both AMC and BMO events (ambiguous excluded)

### Requirement: Return T-1 trading date for each event
The module SHALL compute and include a `t_minus_1` column representing the last trading day before `earnings_date`, using the NYSE calendar. This is the entry date for the strategy.

#### Scenario: T-1 is the trading day before earnings
- **WHEN** earnings date is a Wednesday
- **THEN** `t_minus_1` is the prior Tuesday (assuming no holiday)

#### Scenario: T-1 skips non-trading days
- **WHEN** earnings date is a Monday
- **THEN** `t_minus_1` is the prior Friday

### Requirement: Raise on empty result set
The module SHALL raise a descriptive `ValueError` if the fetched and filtered event set is empty after all exclusions.

#### Scenario: Empty result after filtering raises error
- **WHEN** `fetch_earnings_events("GOOGL", start="2030-01-01")` is called and no future events exist
- **THEN** a `ValueError` is raised with a message identifying the symbol and filter parameters
````

## File: openspec/changes/archive/2026-04-22-ml-pre-earnings-price-prediction/specs/ml-classifier/spec.md
````markdown
## ADDED Requirements

### Requirement: Walk-forward event-level cross-validation
The ML classifier module SHALL train and evaluate using a strictly chronological, expanding-window walk-forward protocol. Events MUST be sorted by `earnings_date` before splitting. Random shuffling is prohibited.

#### Scenario: Walk-forward produces one prediction per test event
- **WHEN** `walk_forward_predict(features_df, min_train=20)` is called
- **THEN** the function returns a Series of predicted probabilities indexed by `earnings_date`, with one prediction per event from position `min_train` onward

#### Scenario: No future data leaks into training
- **WHEN** predicting the probability for event at index N
- **THEN** only events at indices 0 through N-1 are used for training

#### Scenario: Insufficient training data skips prediction
- **WHEN** fewer than `min_train` events precede the current event
- **THEN** no prediction is made for that event and it is excluded from evaluation

### Requirement: Logistic regression as Phase 1 baseline model
The module SHALL use `sklearn.linear_model.LogisticRegression` with standardized features (`sklearn.preprocessing.StandardScaler` fit on training fold only) as the primary classifier. Scaler MUST be fit exclusively on training data and applied to test data without re-fitting.

#### Scenario: Scaler fit on training fold only
- **WHEN** walk-forward prediction is run for fold N
- **THEN** the StandardScaler is fit on events 0..N-1 and applied (not re-fit) to event N

#### Scenario: Model coefficients logged per fold
- **WHEN** verbose mode is enabled
- **THEN** feature names and their logistic regression coefficients are logged after each fold fit

### Requirement: Prediction output includes probability and binary label
The module SHALL return both predicted probability (`prob_positive`) and thresholded binary label (`pred_label`) for each test event. Default threshold is 0.5; configurable via parameter.

#### Scenario: Probability output is in [0, 1]
- **WHEN** `walk_forward_predict` returns predictions
- **THEN** all `prob_positive` values are between 0.0 and 1.0 inclusive

#### Scenario: Custom threshold applied
- **WHEN** `threshold=0.60` is passed
- **THEN** `pred_label = 1` only for events where `prob_positive >= 0.60`

### Requirement: Evaluation report with hit rate, expectancy, and calibration
The module SHALL compute and return an evaluation report covering:

- `hit_rate`: Fraction of predicted positive events where `y == 1`.
- `baseline_rate`: Unconditional fraction of positive-gap events in the full sample.
- `avg_gap_return`: Mean `gap_return` across all predicted-positive events.
- `avg_gap_return_negative`: Mean `gap_return` across predicted-negative events (for comparison).
- `n_trades`: Count of events where `pred_label == 1`.
- `n_total`: Total events evaluated.

#### Scenario: Hit rate exceeds baseline rate to indicate edge
- **WHEN** the classifier has predictive power
- **THEN** `hit_rate > baseline_rate`

#### Scenario: Evaluation report prints to log
- **WHEN** `print_eval_report(report)` is called
- **THEN** all metrics are printed with labels to stdout

### Requirement: Feature importance logging for logistic regression
The module SHALL log sorted feature coefficients (by absolute magnitude) after fitting on the full training set, to validate whether the pre-earnings flow hypothesis is reflected in the model weights.

#### Scenario: Top features logged
- **WHEN** the final fold is fit
- **THEN** feature names ranked by absolute coefficient magnitude are logged in descending order
````

## File: openspec/changes/archive/2026-04-22-ml-pre-earnings-price-prediction/specs/pead-backtest/spec.md
````markdown
## ADDED Requirements

### Requirement: Event-driven backtest simulating overnight entry at T-1 close
The PEAD backtest SHALL simulate entering a long position at T-1 close and exiting at T open for each event where `pred_label == 1`. Each trade is independent; no portfolio is held between events.

#### Scenario: Trade entered at T-1 close
- **WHEN** `pred_label == 1` for an event
- **THEN** a long entry is recorded at `close(T-1)` with configured position size as a fraction of capital

#### Scenario: Trade exited at T open
- **WHEN** a trade is open and T open bar is available
- **THEN** the position is closed at `open(T)` and PnL is recorded as `(open(T) / close(T-1) - 1) * position_value`

#### Scenario: No trade on predicted-negative event
- **WHEN** `pred_label == 0` for an event
- **THEN** no entry or exit is simulated and capital is unchanged

### Requirement: Configurable position sizing as fixed fraction of capital
The backtest SHALL support a `position_size` parameter (float, fraction of current capital, e.g. 0.05 for 5%) applied to each trade independently. Capital starts at `initial_amount`.

#### Scenario: Position size applied to current capital
- **WHEN** capital is $10,000 and `position_size=0.05`
- **THEN** each trade risks $500 of capital

### Requirement: Transaction cost applied to each leg
The backtest SHALL apply a configurable proportional transaction cost (`ptc`) to both the entry and exit leg of each trade.

#### Scenario: Transaction costs reduce PnL
- **WHEN** `ptc=0.001` (0.1%)
- **THEN** net trade return equals `(open(T) / close(T-1) - 1) - 2 * ptc`

### Requirement: Equity curve and per-trade record
The backtest SHALL produce:
- An equity curve: capital value after each event (trade or no trade), indexed by `earnings_date`.
- A per-trade record DataFrame with columns: `earnings_date`, `entry_price`, `exit_price`, `gross_return`, `net_return`, `pred_prob`, `y`.

#### Scenario: Equity curve length equals number of evaluated events
- **WHEN** backtest runs over N events
- **THEN** the equity curve has exactly N+1 entries (initial value plus one per event)

#### Scenario: Per-trade record only contains traded events
- **WHEN** backtest completes
- **THEN** the per-trade DataFrame contains only rows where `pred_label == 1`

### Requirement: Risk summary consistent with existing risk.metrics module
The backtest SHALL call `risk.print_summary(equity_curve)` after completion to produce Sharpe ratio, max drawdown, Calmar ratio, and total return using the existing module.

#### Scenario: Risk summary printed after backtest
- **WHEN** `PEADBacktest.run()` completes
- **THEN** `risk.print_summary` is called with the equity curve and prints all metrics

### Requirement: Invocable via `python run.py --mode pead-backtest`
The main entry point SHALL support `--mode pead-backtest` as a new run mode that executes the full pipeline: fetch earnings events → fetch bars → build features → walk-forward predict → backtest → print summary.

#### Scenario: pead-backtest mode runs end to end
- **WHEN** `python run.py --mode pead-backtest` is invoked
- **THEN** the full pipeline completes without error and prints a risk summary

#### Scenario: Existing modes unaffected
- **WHEN** `python run.py --mode backtest` or `--mode live` is invoked
- **THEN** behavior is identical to before this change
````

## File: openspec/changes/archive/2026-04-22-ml-pre-earnings-price-prediction/specs/pre-earnings-features/spec.md
````markdown
## ADDED Requirements

### Requirement: Build a feature vector per earnings event from T-7 to T-1 daily bars
The feature module SHALL produce a single feature vector per earnings event by computing summary statistics over the 7 trading days ending at T-1 close (inclusive). All features MUST use only data available at T-1 close with no forward-looking fields.

#### Scenario: Feature vector produced for each event
- **WHEN** `build_features(events_df, bars_dict)` is called with a valid events DataFrame and OHLCV bar data
- **THEN** the function returns a DataFrame with one row per event and one column per feature, indexed by `earnings_date`

#### Scenario: No forward-looking data used
- **WHEN** features are computed for an event with earnings date T
- **THEN** no bar at or after date T appears in the feature computation window

### Requirement: Price drift features (T-7 to T-1)
The module SHALL compute the following price drift features over the 7-day pre-earnings window:

- `drift_7d`: Cumulative simple return from close(T-7) to close(T-1).
- `drift_slope`: Ordinary-least-squares slope of daily closes over the window, normalized by the mean close.
- `up_day_count`: Number of days where `close > close.shift(1)` in the window.
- `down_day_count`: Number of days where `close < close.shift(1)` in the window.

#### Scenario: Drift computed correctly
- **WHEN** close prices over T-7 to T-1 increase monotonically
- **THEN** `drift_7d` is positive, `up_day_count` equals 6, and `down_day_count` equals 0

#### Scenario: Slope captures convexity
- **WHEN** closes accelerate upward over the window
- **THEN** `drift_slope` is positive and larger than for a linear price path with the same total drift

### Requirement: Volume pressure features (T-7 to T-1)
The module SHALL compute:

- `rel_volume_mean`: Mean daily volume over the window divided by the symbol's 20-day baseline volume computed from the 20 trading days ending at T-8 (no overlap with feature window).
- `down_volume_ratio`: Sum of volume on down days divided by total window volume.

#### Scenario: Volume baseline uses non-overlapping window
- **WHEN** baseline volume is computed for an event
- **THEN** no bar from T-7 to T-1 is included in the 20-day baseline

#### Scenario: Down-volume ratio reflects selling pressure
- **WHEN** all volume in the window occurs on down days
- **THEN** `down_volume_ratio` equals 1.0

### Requirement: Volatility regime features (T-7 to T-1)
The module SHALL compute:

- `atr_ratio`: Mean of `(high - low)` over the window divided by the mean of `(high - low)` for the 20-day baseline period ending at T-8.
- `gap_count`: Number of overnight gaps (`abs(open - prev_close) / prev_close > 0.005`) within the window.

#### Scenario: ATR expansion detected
- **WHEN** intraday ranges expand significantly in the 7-day window relative to the prior 20-day baseline
- **THEN** `atr_ratio` is greater than 1.0

### Requirement: Relative-to-market features (T-7 to T-1)
The module SHALL compute:

- `rel_drift_vs_qqq`: `drift_7d` (symbol) minus the QQQ cumulative return over the same window, using QQQ bars passed in `bars_dict`.

#### Scenario: Outperformance detected
- **WHEN** GOOGL rises 5% and QQQ rises 2% over the same window
- **THEN** `rel_drift_vs_qqq` equals approximately 0.03

### Requirement: Target label computation
The module SHALL compute the binary target label alongside features:

- `y`: 1 if `open(T) / close(T-1) - 1 > 0.0`, else 0.
- `gap_return`: Continuous gap return `open(T) / close(T-1) - 1` (stored for evaluation, not used as training label).

#### Scenario: Positive gap labeled correctly
- **WHEN** T open is higher than T-1 close
- **THEN** `y = 1` and `gap_return > 0`

#### Scenario: No-gap or negative gap labeled correctly
- **WHEN** T open equals or is below T-1 close
- **THEN** `y = 0` and `gap_return <= 0`

### Requirement: Drop events with insufficient bar history
The module SHALL exclude any event where fewer than 7 valid bars exist in the T-7 to T-1 window or where the T open bar is unavailable, and log a warning per dropped event.

#### Scenario: Event dropped on insufficient history
- **WHEN** only 4 bars are available in the feature window for an event
- **THEN** that event is excluded from the output and a warning is logged
````

## File: openspec/changes/archive/2026-04-22-ml-pre-earnings-price-prediction/.openspec.yaml
````yaml
schema: spec-driven
created: 2026-04-21
````

## File: openspec/changes/archive/2026-04-22-ml-pre-earnings-price-prediction/design.md
````markdown
## Context

The repo currently implements a weekly cross-sectional momentum strategy backed by a generic event-driven backtest engine (`core/backtest_base.py`) and an Alpaca daily-bar data layer (`data/alpaca_data.py`). Both are rule-based and calendar-driven (Monday/Friday rebalances). There is no event-conditioned or ML-driven logic anywhere.

This change introduces a new, orthogonal strategy family: a binary classifier trained on pre-earnings features (T-7 to T-1 daily bars) to predict whether the earnings reaction gap from T-1 close to T open will be positive. The initial scope is GOOGL, after-market-close events only, every-event evaluation first, with a confidence-threshold filter introduced in a second phase.

## Goals / Non-Goals

**Goals:**
- Build a reproducible, leak-proof ML pipeline: event table → features → walk-forward classifier → event-level backtest → risk summary.
- Keep the existing momentum strategy, backtest engine, and live trader completely untouched.
- Establish a science-grade evaluation protocol (walk-forward by event time, not random split) so results can be trusted for further iteration.
- Produce a `pead-backtest` run mode that can be invoked alongside existing modes without conflict.

**Non-Goals:**
- Live or paper trading of the PEAD signal (Phase 1 is research-only).
- Expanding beyond GOOGL or beyond after-close events in this change.
- Deep learning or LLM-based models.
- Intraday (minute-bar) feature engineering.
- Surprise factor or analyst estimate data.

## Decisions

### Decision: yfinance as earnings calendar source
**Choice**: Use `yfinance.Ticker("GOOGL").get_earnings_dates()` as the primary event calendar.

**Alternatives considered**:
- Alpaca's own calendar API — does not surface earnings timestamps.
- Google Investor Relations scraping — accurate but fragile, requires Selenium/BeautifulSoup; suitable only as a spot-check verification layer.
- Paid data vendors (e.g. Refinitiv, Bloomberg) — out of scope for this repo.

**Rationale**: `yfinance` is already in `environment.yml`, returns structured dates back several years, and is sufficient for a single-ticker research prototype. AMC/BMO classification is derived from the release time field. Events with ambiguous timestamps are excluded.

### Decision: Feature window is T-7 to T-1 daily bars only
**Choice**: Engineer all features exclusively from the 7 trading days preceding each earnings date using daily OHLCV bars fetched via the existing `fetch_bars` function.

**Alternatives considered**:
- Minute bars for intraday open/close pressure — materially more complex, adds latency on data fetch, not needed for phase 1 hypothesis test.
- Longer lookback (T-20, T-60) — adds context but also noise from non-earnings macro moves.

**Rationale**: The core hypothesis is specifically about pre-earnings informed flow, so the 7-day window is both theoretically motivated and small enough to avoid confounding with broader macro drift. Features include: cumulative return, daily return slope, downside-day concentration, relative volume vs 20-day baseline, ATR expansion, and stock-minus-QQQ relative return. All features are computed from information available at T-1 close with no forward-looking fields.

### Decision: Walk-forward event-level split — no random shuffle
**Choice**: Order all events chronologically. Train on events [0..N], test on event [N+1]. Expand window forward (expanding window walk-forward). Minimum training window: 20 events.

**Alternatives considered**:
- Random train/test split — standard for i.i.d. data but introduces look-ahead bias for financial time series.
- K-fold cross-validation — same bias problem plus events are not i.i.d.
- Fixed rolling window (train on last 20, test on next 1) — avoids stale data but reduces effective training size early on.

**Rationale**: Event-level walk-forward is the only protocol that matches production behavior (you never know future events when trading). Expanding window is preferred over rolling for this sample size (~40–60 GOOGL events since 2018) because rolling window training sets would be too small at the start.

### Decision: Logistic regression as Phase 1 baseline, XGBoost as Phase 2
**Choice**: Phase 1 uses `sklearn.linear_model.LogisticRegression` with standardized features. Phase 2 adds `xgboost.XGBClassifier` for non-linear interactions.

**Alternatives considered**:
- Random forest — good but less interpretable; reserve for Phase 2.
- Neural nets — no theoretical advantage over GBTs with this sample size (~40–60 rows).

**Rationale**: Logistic regression coefficients directly validate whether the feature story (downward pressure → positive gap, stretched run-up → negative gap) is reflected in the weights. If LR already has edge, that is a strong signal. XGBoost is added in Phase 2 to capture non-linear interactions (e.g. high drift AND high volume AND compressed price).

### Decision: Target label is binary sign of T-1 close to T open gap
**Choice**: `y = 1` if `open(T) / close(T-1) - 1 > 0.0`, else `y = 0`. Also compute continuous gap return for EV analysis.

**Alternatives considered**:
- Regression target (predict gap magnitude) — harder to calibrate for a threshold decision; binary classification better matches the go/no-go trading decision.
- Three-class (positive/flat/negative) — flat zone is ambiguous; start binary and extend if needed.

**Rationale**: The trading decision is binary: enter at T-1 close or not. The continuous gap return is computed alongside but only used for economic evaluation (average return per trade, not as training label).

### Decision: Entry at T-1 close, exit at T open
**Choice**: Simulate overnight position: buy at T-1 close, sell at T open. Transaction costs applied at both legs.

**Rationale**: This captures exactly the overnight gap the model predicts. T-close exit (hold through T trading session) is reserved for Phase 2 when continuation signal has been separately validated.

## Risks / Trade-offs

- **Small sample size (~40 GOOGL events from 2016–2025)** → Starting from 2016 gives approximately 40 events (10 years × 4 per year). With a 20-event minimum training window, ~20 events are available out-of-sample — roughly double what a 2018 start would yield (~12). Early walk-forward folds still have limited training points. Mitigate by reporting confidence intervals around hit rate. Accept that strong conclusions require a larger symbol universe (Phase 3).

- **yfinance AMC/BMO timestamps may be imprecise or missing** → Mitigate by excluding events with null or ambiguous time fields and spot-checking against GOOGL investor relations page. Log excluded event count.

- **Look-ahead bias in feature computation** → Mitigate by asserting that every feature references only `df.loc[:earnings_date - 1_trading_day]` slices. Add unit test that verifies feature vector date range does not touch or exceed T.

- **Overfitting to GOOGL-specific behaviour** → By design for Phase 1. Mitigation is not to scale up to production until out-of-sample walk-forward results are stable.

- **Gap-based exit ignores post-open continuation or reversal** → Phase 1 intentionally ignores intraday behaviour. If gap capture is positive, Phase 2 can test holding through T close.

## Open Questions

- What is the precise cutoff for classifying an event as AMC vs BMO? (e.g., release time after 16:00 ET = AMC). Needs to be codified in `earnings_calendar.py`.
- Should the T-open exit use the official Alpaca opening price or a 5-minute VWAP to reduce microstructure noise? Decision deferred to implementation.
- Is the 20-event minimum training window sufficient, or should it be pushed to 25? With ~40 events from 2016–2025, a 20-event seed leaves ~20 out-of-sample; pushing to 25 would reduce that to ~15. Revisit after confirming exact event count from yfinance.
````

## File: openspec/changes/archive/2026-04-22-ml-pre-earnings-price-prediction/proposal.md
````markdown
## Why

Informed order-flow in the 7 trading days before an earnings announcement leaves measurable footprints in price and volume behaviour. By training a machine learning classifier on those pre-event features we can predict whether the gap between T-1 close and T open will be positive, allowing a low-frequency, overnight entry at T-1 close that captures the earnings reaction before it fully prices in. The current repo contains only rule-based weekly momentum; this change adds the first ML-driven, event-conditioned strategy.

## What Changes

- New data module to fetch GOOGL earnings event dates and AMC/BMO timing via `yfinance`.
- New feature-engineering pipeline that constructs T-7 to T-1 pre-earnings features (price drift, volume behaviour, volatility regime, relative-to-index metrics) from Alpaca daily bars.
- New ML training and evaluation pipeline: walk-forward, event-level cross-validation using scikit-learn or XGBoost-family classifiers.
- New event-driven backtest that enters at T-1 close and exits at T open (Phase 1) or T close (Phase 2) based on classifier signal.
- New run mode `python run.py --mode pead-backtest` to execute the full pipeline end-to-end.
- New confidence-threshold filter applied on top of the base classifier to improve per-trade expectancy (Phase 2).

## Capabilities

### New Capabilities

- `earnings-calendar`: Fetch, validate, and cache earnings event dates with AMC/BMO timing for a given symbol using `yfinance`. Produces a structured event table as the source of truth for all downstream pipeline stages.
- `pre-earnings-features`: Engineer pre-event feature vectors from T-7 to T-1 daily OHLCV bars per earnings event. Features cover price drift shape, volume pressure, volatility regime, and relative-to-benchmark behaviour.
- `ml-classifier`: Train and evaluate a binary classifier (positive gap vs non-positive gap) using walk-forward, event-level splits. Supports baseline logistic regression and gradient-boosted tree models. Reports hit rate, expectancy, and calibration diagnostics.
- `pead-backtest`: Event-driven backtest that uses the classifier signal (and optional confidence threshold) to simulate overnight entries at T-1 close and exits at T open or T close. Produces an equity curve and risk summary consistent with existing `risk.metrics` standards.

### Modified Capabilities

- `data-layer`: Add support for fetching daily bars keyed by event date windows (T-N to T-1 slices) to serve the feature-engineering pipeline. No breaking changes to existing `fetch_bars` signature.

## Impact

- New dependencies already present in `environment.yml`: `yfinance`, `scikit-learn`-compatible libs, `xgboost` or similar (via existing pip installs).
- New files: `data/earnings_calendar.py`, `data/pre_earnings_features.py`, `strategies/pead_classifier.py`, `strategies/pead_backtest.py`.
- `run.py` gains a new `--mode pead-backtest` branch; existing `backtest` and `live` modes are unchanged.
- No changes to `core/backtest_base.py` or `core/live_trader_base.py` public interfaces.
- No changes to existing momentum strategy or its specs.
````

## File: openspec/changes/archive/2026-04-22-ml-pre-earnings-price-prediction/tasks.md
````markdown
## 1. Earnings Calendar

- [x] 1.1 Create `data/earnings_calendar.py` with `fetch_earnings_events(symbol, start, timing)` using `yfinance`
- [x] 1.2 Implement AMC/BMO classification: release time after 16:00 ET → AMC, before 09:30 ET → BMO, otherwise exclude and warn
- [x] 1.3 Compute `t_minus_1` column using NYSE trading calendar (pandas_market_calendars or exchange_calendars)
- [x] 1.4 Implement `timing` filter parameter to return AMC-only, BMO-only, or all classified events
- [x] 1.5 Raise `ValueError` on empty result after filtering; log count of excluded events

## 2. Pre-Earnings Feature Engineering

- [x] 2.1 Create `data/pre_earnings_features.py` with `build_features(events_df, bars_dict)` function
- [x] 2.2 Implement price drift features: `drift_7d`, `drift_slope` (OLS), `up_day_count`, `down_day_count`
- [x] 2.3 Implement volume pressure features: `rel_volume_mean` (vs T-8 to T-28 baseline), `down_volume_ratio`
- [x] 2.4 Implement volatility regime features: `atr_ratio` (window vs baseline), `gap_count`
- [x] 2.5 Implement relative-to-market feature: `rel_drift_vs_qqq` using QQQ bars from `bars_dict`
- [x] 2.6 Compute target label `y` (binary) and `gap_return` (continuous) from T open vs T-1 close
- [x] 2.7 Drop and log events with fewer than 7 valid bars in feature window or missing T open bar
- [x] 2.8 Add assertion that no feature computation window references any bar at or after earnings date T

## 3. ML Classifier

- [x] 3.1 Create `strategies/pead_classifier.py` with `walk_forward_predict(features_df, min_train, threshold)` function
- [x] 3.2 Implement expanding-window walk-forward loop: train on events 0..N-1, predict event N
- [x] 3.3 Fit `StandardScaler` on training fold only; apply (not re-fit) to test fold
- [x] 3.4 Use `LogisticRegression` as Phase 1 model; expose `model_cls` parameter for Phase 2 swap-in
- [x] 3.5 Return `prob_positive` and `pred_label` (thresholded at configurable `threshold`, default 0.5)
- [x] 3.6 Implement `evaluate(predictions_df)` that computes and returns `hit_rate`, `baseline_rate`, `avg_gap_return`, `avg_gap_return_negative`, `n_trades`, `n_total`
- [x] 3.7 Implement `print_eval_report(report)` that logs all evaluation metrics to stdout
- [x] 3.8 Log sorted feature coefficients by absolute magnitude after each fold fit when `verbose=True`

## 4. PEAD Backtest

- [x] 4.1 Create `strategies/pead_backtest.py` with `PEADBacktest` class accepting predictions, bars, `position_size`, `ptc`, `initial_amount`
- [x] 4.2 Implement `run()` method: iterate events in chronological order, simulate overnight entry at T-1 close and exit at T open for `pred_label == 1` events
- [x] 4.3 Apply `ptc` to both entry and exit legs
- [x] 4.4 Build equity curve Series indexed by `earnings_date` (N+1 entries including initial value)
- [x] 4.5 Build per-trade record DataFrame with columns: `earnings_date`, `entry_price`, `exit_price`, `gross_return`, `net_return`, `pred_prob`, `y`
- [x] 4.6 Call `risk.print_summary(equity_curve)` at end of `run()`

## 5. Data Layer Extension

- [x] 5.1 Verify `fetch_bars(["QQQ"], start, end)` works as a single-symbol call (no code change expected; add integration test or manual verification note)
- [x] 5.2 Update docstring to reflect single-symbol use case is supported

## 6. Run Mode Integration

- [x] 6.1 Add PEAD config constants to `config.py`: `PEAD_SYMBOL` ("GOOGL"), `PEAD_START_DATE` ("2016-01-01"), `PEAD_END_DATE` ("2025-12-31"), `PEAD_POSITION_SIZE`, `PEAD_PTC`, `PEAD_MIN_TRAIN` (20)
- [x] 6.2 Add `run_pead_backtest()` function in `run.py` that wires the full pipeline: earnings calendar → bars fetch → feature build → walk-forward predict → backtest → summary
- [x] 6.3 Add `--mode pead-backtest` to the argparse block in `run.py`; verify existing `backtest` and `live` modes are unaffected

## 7. Validation

- [x] 7.1 Manual smoke test: run `python run.py --mode pead-backtest` and confirm it produces evaluation report and equity curve without error
- [x] 7.2 Verify walk-forward produces predictions only from position `min_train` onward with no earlier events
- [x] 7.3 Spot-check 2–3 GOOGL earnings events against investor relations page to confirm AMC classification and T-1 date are correct
- [x] 7.4 Verify equity curve and per-trade records agree on PnL arithmetic for at least 2 events
````

## File: openspec/changes/archive/2026-04-22-pead-t3-entry-tp1-exits/specs/pead-backtest/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Event-driven backtest simulating overnight entry at T-1 close
The PEAD backtest SHALL support a configurable timing variant that enters a long position at T-3 close and exits at either T+1 open or T+1 close for each event where `pred_label == 1`. Each trade is independent; no portfolio is held between events.

#### Scenario: Trade entered at T-3 close
- **WHEN** `pred_label == 1` for an event and the configured entry timing is T-3 close
- **THEN** a long entry is recorded at `close(T-3)` with configured position size as a fraction of capital

#### Scenario: Trade exited at T+1 open
- **WHEN** a trade is open and the configured exit mode is `t_plus_1_open`
- **THEN** the position is closed at `open(T+1)` and PnL is recorded from `close(T-3)` to `open(T+1)`

#### Scenario: Trade exited at T+1 close
- **WHEN** a trade is open and the configured exit mode is `t_plus_1_close`
- **THEN** the position is closed at `close(T+1)` and PnL is recorded from `close(T-3)` to `close(T+1)`

#### Scenario: No trade on predicted-negative event
- **WHEN** `pred_label == 0` for an event
- **THEN** no entry or exit is simulated and capital is unchanged

### Requirement: Transaction cost applied to each leg
The backtest SHALL apply a configurable proportional transaction cost (`ptc`) to both the entry and exit leg of each trade.

#### Scenario: Transaction costs reduce PnL
- **WHEN** `ptc=0.001` (0.1%)
- **THEN** net trade return equals `(exit_price / entry_price - 1) - 2 * ptc`

### Requirement: Invocable via `python run.py --mode pead-backtest`
The main entry point SHALL support `--mode pead-backtest` as the PEAD timing-variant runner that executes the full pipeline: fetch earnings events → fetch bars → build features using data available by T-3 → walk-forward predict → backtest the configured entry/exit horizon → print summary.

#### Scenario: pead-backtest mode runs end to end
- **WHEN** `python run.py --mode pead-backtest` is invoked
- **THEN** the full configured timing-variant pipeline completes without error and prints a PEAD risk summary

#### Scenario: Existing non-PEAD modes unaffected
- **WHEN** `python run.py --mode backtest` or `--mode live` is invoked
- **THEN** behavior is identical to before this change

## ADDED Requirements

### Requirement: Always-buy benchmark metrics for the configured PEAD horizon
The PEAD backtest flow SHALL compute and report benchmark metrics for an always-buy strategy that trades every evaluated PEAD event using the same entry date, exit date, and transaction cost assumptions as the model-gated strategy.

#### Scenario: Benchmark uses same evaluated events
- **WHEN** benchmark metrics are computed
- **THEN** the always-buy baseline uses the same evaluated event subset as the model-gated PEAD backtest

#### Scenario: Benchmark reports average return and hit rate
- **WHEN** the PEAD timing-variant run completes
- **THEN** the output includes always-buy hit rate, average gross return, average net return, and uplift versus the model-gated strategy for the configured horizon

#### Scenario: Benchmark uses same transaction cost assumptions
- **WHEN** `ptc` is configured for the PEAD timing-variant run
- **THEN** the always-buy benchmark applies the same per-leg transaction cost assumptions as the model-gated strategy
````

## File: openspec/changes/archive/2026-04-22-pead-t3-entry-tp1-exits/specs/pre-earnings-features/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Build a feature vector per earnings event from T-7 to T-1 daily bars
The feature module SHALL produce a single feature vector per earnings event by computing summary statistics over the 7 trading days ending at T-3 close (inclusive). All features MUST use only data available at T-3 close with no forward-looking fields relative to the T-3 entry decision.

#### Scenario: Feature vector produced for each event
- **WHEN** `build_features(events_df, bars_dict)` is called with a valid events DataFrame and OHLCV bar data
- **THEN** the function returns a DataFrame with one row per event and one column per feature, indexed by `earnings_date`

#### Scenario: No forward-looking data used
- **WHEN** features are computed for an event with earnings date T and entry decision time T-3 close
- **THEN** no bar after T-3 appears in the feature computation window

### Requirement: Price drift features (T-7 to T-1)
The module SHALL compute the following price drift features over the 7-day pre-earnings window ending at T-3:

- `drift_7d`: Cumulative simple return from close(T-9) to close(T-3).
- `drift_slope`: Ordinary-least-squares slope of daily closes over the window, normalized by the mean close.
- `up_day_count`: Number of days where `close > close.shift(1)` in the window.
- `down_day_count`: Number of days where `close < close.shift(1)` in the window.

#### Scenario: Drift computed correctly
- **WHEN** close prices over the 7-day window ending at T-3 increase monotonically
- **THEN** `drift_7d` is positive, `up_day_count` equals 6, and `down_day_count` equals 0

#### Scenario: Slope captures convexity
- **WHEN** closes accelerate upward over the window ending at T-3
- **THEN** `drift_slope` is positive and larger than for a linear price path with the same total drift

### Requirement: Volume pressure features (T-7 to T-1)
The module SHALL compute:

- `rel_volume_mean`: Mean daily volume over the window ending at T-3 divided by the symbol's 20-day baseline volume computed from the 20 trading days ending immediately before the feature window begins.
- `down_volume_ratio`: Sum of volume on down days divided by total window volume.

#### Scenario: Volume baseline uses non-overlapping window
- **WHEN** baseline volume is computed for an event
- **THEN** no bar from the 7-day feature window ending at T-3 is included in the 20-day baseline

#### Scenario: Down-volume ratio reflects selling pressure
- **WHEN** all volume in the window occurs on down days
- **THEN** `down_volume_ratio` equals 1.0

### Requirement: Volatility regime features (T-7 to T-1)
The module SHALL compute:

- `atr_ratio`: Mean of `(high - low)` over the window ending at T-3 divided by the mean of `(high - low)` for the 20-day baseline period immediately preceding the feature window.
- `gap_count`: Number of overnight gaps (`abs(open - prev_close) / prev_close > 0.005`) within the window.

#### Scenario: ATR expansion detected
- **WHEN** intraday ranges expand significantly in the 7-day window ending at T-3 relative to the prior 20-day baseline
- **THEN** `atr_ratio` is greater than 1.0

### Requirement: Relative-to-market features (T-7 to T-1)
The module SHALL compute:

- `rel_drift_vs_qqq`: `drift_7d` (symbol) minus the QQQ cumulative return over the same 7-day window ending at T-3, using QQQ bars passed in `bars_dict`.

#### Scenario: Outperformance detected
- **WHEN** GOOGL rises 5% and QQQ rises 2% over the same window ending at T-3
- **THEN** `rel_drift_vs_qqq` equals approximately 0.03

### Requirement: Drop events with insufficient bar history
The module SHALL exclude any event where fewer than 7 valid bars exist in the feature window ending at T-3, and log a warning per dropped event.

#### Scenario: Event dropped on insufficient history
- **WHEN** only 4 bars are available in the feature window ending at T-3 for an event
- **THEN** that event is excluded from the output and a warning is logged
````

## File: openspec/changes/archive/2026-04-22-pead-t3-entry-tp1-exits/.openspec.yaml
````yaml
schema: spec-driven
created: 2026-04-22
````

## File: openspec/changes/archive/2026-04-22-pead-t3-entry-tp1-exits/design.md
````markdown
## Context

The current PEAD research path is built around a single GOOGL pipeline that classifies the sign of the T-1-close to T-open gap, computes features from the 7 trading days ending at T-1, and backtests an overnight trade that enters at T-1 close and exits at T open. The user wants to test a timing variant that enters earlier at T-3 close and exits later at either T+1 open or T+1 close, while otherwise keeping the ML workflow and feature set conceptually the same.

The main constraint is lookahead bias. A T-3 entry cannot legally use T-2 or T-1 data in feature computation. The design therefore needs to separate feature availability from execution timing while keeping the current PEAD pipeline recognizable and small enough to implement quickly.

## Goals / Non-Goals

**Goals:**
- Preserve the existing single-symbol GOOGL PEAD workflow and logistic-regression walk-forward structure.
- Shift the feature availability cutoff so the new T-3 entry remains free of lookahead bias.
- Support two configurable exits for the timing variant: T+1 open and T+1 close.
- Report benchmark metrics that compare model-gated trades against always-buy trades over the same evaluated events and holding window.

**Non-Goals:**
- Changing the earnings calendar source or event classification rules.
- Expanding to multi-symbol PEAD research in this change.
- Redefining the classifier target to the new T-3 to T+1 holding horizon.
- Adding a new model family or changing walk-forward training logic.

## Decisions

### Decision: Shift feature windows to end at T-3 close

**Choice:** Recompute the 7-day feature window as the 7 trading days ending at T-3 close, which effectively shifts the window from T-7..T-1 to T-9..T-3 while keeping the feature count and formulas intact.

**Alternatives considered:**
- Keep the current T-7..T-1 feature window. Rejected because T-2 and T-1 would be unavailable at a T-3 entry decision, creating lookahead bias.
- Shorten the window to T-7..T-3. Rejected because it changes the semantic meaning of the 7-day feature set and makes results harder to compare with the current strategy.

**Rationale:** This is the smallest safe change that preserves the existing feature definitions while moving the decision point earlier.

### Decision: Preserve the current classifier objective for this experiment

**Choice:** Keep the current classifier machinery and label structure intact for this change, and use the new execution timing as a PEAD strategy variant rather than redefining the learning target.

**Alternatives considered:**
- Redefine the label to predict T-3-close to T+1-open or T+1-close returns. Rejected for this change because the user selected the lower-scope path and the extra label redesign would broaden the experiment materially.

**Rationale:** The user explicitly chose the pragmatic variant first. This keeps scope small and makes it possible to test whether the current signal still adds value when traded over a longer window.

### Decision: Derive T-3 and T+1 from the bar index, not the earnings calendar schema

**Choice:** Continue using `earnings_date` and `t_minus_1` from the earnings event table, and derive T-3 and T+1 by walking the symbol's daily bar index inside feature engineering and backtest logic.

**Alternatives considered:**
- Extend the earnings calendar module to precompute `t_minus_3` and `t_plus_1`. Rejected because those values are only needed by this strategy variant and can be derived from already-fetched bars.

**Rationale:** This keeps the earnings calendar capability stable and localizes timing logic to the PEAD research path.

### Decision: Put always-buy benchmark reporting in the PEAD backtest layer

**Choice:** Compute and print always-buy benchmark metrics in the PEAD strategy/backtest/reporting flow using the same evaluated events, entry date, exit date, and transaction cost assumptions as the model-gated strategy.

**Alternatives considered:**
- Add the benchmark to the classifier evaluation helper. Rejected because the benchmark depends on the configured execution horizon, which is strategy-specific rather than classifier-generic.

**Rationale:** The comparison the user wants is about trade execution, not only label classification quality.

## Risks / Trade-offs

- **[Label/execution mismatch]** The classifier still predicts the original PEAD label while the executed trade holds a longer window. → Mitigation: document this explicitly in logs and specs as an exploratory timing variant, and keep the change scoped so a later proposal can realign the label if needed.
- **[More exposure to non-earnings market noise]** T-3 to T+1 holds the position across more non-event price movement than the original overnight trade. → Mitigation: compare against an always-buy baseline over the exact same horizon.
- **[Date derivation edge cases]** Holidays or missing bars can make T-3 or T+1 unavailable for specific events. → Mitigation: skip affected events with a warning and keep benchmark/model comparisons on the same evaluated subset.

## Migration Plan

1. Update PEAD configuration to expose entry and exit timing controls for this variant.
2. Shift feature window computation to the last 7 trading days ending at T-3.
3. Extend the PEAD backtest to derive T-3 and T+1 dates from bars and support both configured exit modes.
4. Add always-buy benchmark summary output to the PEAD run path.
5. Validate the variant on GOOGL and compare reported metrics for T+1 open versus T+1 close.

## Open Questions

- Which exit should be the default for `pead-backtest`: T+1 open, T+1 close, or a configurable switch with no default change?
- Should the logs report both exit horizons in one run, or should each run evaluate only one configured horizon?
````

## File: openspec/changes/archive/2026-04-22-pead-t3-entry-tp1-exits/proposal.md
````markdown
## Why

The current PEAD research path enters at T-1 close and exits at T open, which may capture the earnings gap but miss earlier pre-announcement positioning and post-announcement follow-through. This change adds a new GOOGL PEAD timing variant that enters earlier at T-3 close, exits at T+1 open or T+1 close, and compares model-gated trades against an always-buy baseline on the same horizon.

## What Changes

- Shift PEAD feature computation to a 7-trading-day window ending at T-3 close so the new entry timing remains free of lookahead bias.
- Extend the PEAD backtest to support configurable entry at T-3 close and configurable exits at either T+1 open or T+1 close.
- Add PEAD-specific benchmark metrics that compare the model-gated strategy against an always-buy baseline over the same evaluated events and holding window.
- Update PEAD configuration and run-mode wiring so the timing variant can be executed and reported without changing the rest of the ML pipeline structure.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `pre-earnings-features`: Change the feature availability cutoff from T-1 to T-3 while preserving the 7-day feature horizon and no-lookahead guarantees.
- `pead-backtest`: Change PEAD execution timing to support T-3 entry with T+1 open or T+1 close exits, plus reporting for the configured timing variant.

## Impact

- Affected code: `data/pre_earnings_features.py`, `strategies/pead_backtest.py`, `run.py`, and `config.py`.
- Affected specs: `openspec/specs/pre-earnings-features/spec.md` and `openspec/specs/pead-backtest/spec.md`.
- No new external dependencies are expected.
````

## File: openspec/changes/archive/2026-04-22-pead-t3-entry-tp1-exits/tasks.md
````markdown
## 1. Configuration and Run-Mode Wiring

- [x] 1.1 Add PEAD timing-variant config values for T-3 entry and configurable exit mode (`t_plus_1_open` or `t_plus_1_close`)
- [x] 1.2 Update `run_pead_backtest()` to log the configured entry/exit timing variant and keep the rest of the PEAD pipeline wiring intact

## 2. Feature Timing Shift

- [x] 2.1 Update `build_features()` to compute the 7-trading-day feature window ending at T-3 instead of T-1
- [x] 2.2 Update baseline-volume and baseline-range windows so they remain non-overlapping relative to the shifted T-3 feature window
- [x] 2.3 Update feature-window validation and warnings to enforce no-lookahead relative to the T-3 decision time

## 3. PEAD Backtest Timing Variant

- [x] 3.1 Extend the PEAD backtest to derive T-3 and T+1 dates from the symbol's daily bar index for each evaluated event
- [x] 3.2 Implement configurable exits at T+1 open and T+1 close using the configured PEAD exit mode
- [x] 3.3 Keep transaction-cost handling and per-trade records consistent with the new entry/exit prices
- [x] 3.4 Skip events with missing T-3 or T+1 bars and log warnings without breaking the run

## 4. Benchmark Reporting

- [x] 4.1 Compute always-buy benchmark metrics on the same evaluated event subset as the model-gated PEAD strategy
- [x] 4.2 Report always-buy hit rate, average gross return, average net return, and model-versus-benchmark uplift for the configured horizon

## 5. Validation

- [x] 5.1 Run `python run.py --mode pead-backtest` for the T-3 to T+1 open variant and confirm the pipeline completes end to end
- [x] 5.2 Run the PEAD timing variant with the T+1 close exit and confirm both exit modes produce valid trade records and benchmark metrics
- [x] 5.3 Verify the shifted feature window uses only bars available by T-3 for at least one sampled earnings event
````

## File: openspec/changes/archive/2026-04-23-pead-live-multi-symbol/specs/pead-live-trader/spec.md
````markdown
## ADDED Requirements

### Requirement: Daily cronjob executes PEAD trading logic

The system SHALL run PEAD live execution as a daily cronjob. At each execution, the system SHALL:
1. Check each symbol (NXPI, AMD, AVGO) to determine if today is T-3 or T+1+ relative to the symbol's nearest upcoming earnings date
2. Execute entry orders for any symbol at T-3, provided a positive classifier prediction exists
3. Execute exit orders for any symbol at T+1 or later, if a position is currently open
4. Log all order execution results

#### Scenario: Entry trigger on T-3
- **WHEN** cronjob runs on a day that is T-3 for a symbol's nearest earnings event AND classifier predicts positive (pred_label == 1)
- **THEN** system SHALL fetch 7-day OHLCV data (T-9 through T-3), place a market BUY order, record entry state with entry_date/entry_price/entry_qty

#### Scenario: Entry skipped on negative prediction
- **WHEN** cronjob runs on T-3 for a symbol AND classifier predicts negative (pred_label == 0)
- **THEN** system SHALL not place an order; position entry is skipped for this event

#### Scenario: Exit trigger on T+1 or later
- **WHEN** cronjob runs on a day that is T+1 or later for a symbol's current open earnings event AND a position is currently open
- **THEN** system SHALL place a market SELL order at current market price (immediate execution), log exit price and PnL, clear state entry for that symbol

#### Scenario: Double-trade prevention
- **WHEN** cronjob runs on T-3 for a symbol AND state file already shows an open position for this symbol and the same earnings_date
- **THEN** system SHALL not place another BUY order; only one entry per symbol per earnings event

#### Scenario: Missed cronjob recovery
- **WHEN** cronjob does not run on T+1 (e.g., droplet downtime), but runs on T+2 or later AND a position is still open
- **THEN** system SHALL execute the exit order immediately on the first available execution, preventing positions from lingering past intended exit date

### Requirement: Classifier integration for entry prediction

The system SHALL use a pre-trained, frozen classifier to generate predictions for live trades. For each symbol on T-3:
1. Load the latest trained classifier (no retraining during live cycle)
2. Extract 7-day pre-earnings features (T-9 through T-3)
3. Generate pred_label (0 or 1) and prob_positive probability
4. Use pred_label to gate entry: only execute if pred_label == 1

#### Scenario: Load classifier
- **WHEN** daily cronjob initializes
- **THEN** system SHALL load the most recent trained classifier model

#### Scenario: Predict for T-3 features
- **WHEN** on T-3 execution and need to decide whether to enter
- **THEN** system SHALL extract 7-day momentum/volatility/QQQ correlation features, invoke classifier.predict(), receive pred_label and prob_positive

#### Scenario: Entry gated on positive prediction
- **WHEN** classifier returns pred_label == 1
- **THEN** entry order proceeds to execution

#### Scenario: Entry blocked on negative prediction
- **WHEN** classifier returns pred_label == 0
- **THEN** entry order is not placed; day is recorded as "skipped"

### Requirement: Market order execution with Alpaca API

The system SHALL submit market orders via Alpaca's trading API (paper trading account). For each order:
1. Calculate position size as `(account_equity * 0.10) / current_price` for entry orders
2. Submit market order (buy on entry, sell on exit) with time_in_force = Day
3. Capture order ID, fill price, and fill timestamp
4. Handle errors (insufficient buying power, API rate limits) by logging and deferring to next cronjob run

#### Scenario: Calculate entry position size
- **WHEN** entry order is ready to submit
- **THEN** system SHALL read account equity, multiply by 0.10 (10% position size), divide by T-3 close price to get share count, round down to integer

#### Scenario: Submit entry market order
- **WHEN** position size is calculated
- **THEN** system SHALL submit market BUY order via AlpacaLiveTraderBase, capturing order_id and requested fill price

#### Scenario: Submit exit market order
- **WHEN** T+1+ exit is triggered
- **THEN** system SHALL submit market SELL order via AlpacaLiveTraderBase for the full open position quantity, capturing order_id and fill price

#### Scenario: Handle Alpaca errors gracefully
- **WHEN** order submission fails (e.g., API down, insufficient buying power)
- **THEN** system SHALL log error, not crash, continue to next symbol, retry on next cronjob run

### Requirement: Earnings date fetching and T-N offset calculation

The system SHALL fetch the nearest upcoming earnings date for each symbol using yfinance, then calculate T-3 and T+1 offsets accounting for NYSE trading calendar (exclude weekends, US federal holidays).

#### Scenario: Fetch nearest earnings date
- **WHEN** cronjob runs
- **THEN** system SHALL call fetch_earnings_events(symbol) to retrieve the next upcoming earnings date for each symbol (NXPI, AMD, AVGO)

#### Scenario: Calculate T-3 from earnings date
- **WHEN** earnings_date is known
- **THEN** system SHALL find the trading day exactly 3 trading days before earnings_date (skip weekends and US holidays), call this T-3

#### Scenario: Calculate T+1 from earnings date
- **WHEN** earnings_date is known
- **THEN** system SHALL find the trading day exactly 1 trading day after earnings_date, call this T+1

#### Scenario: Handle holiday edge cases
- **WHEN** earnings_date or T-3/T+1 calculation crosses a US federal holiday or weekend
- **THEN** system SHALL skip non-trading days and use NYSE trading calendar to find the correct trading day offset

### Requirement: PnL calculation at exit

The system SHALL calculate and record the profit/loss for each trade at exit time using actual execution prices.

#### Scenario: Calculate net PnL in dollars
- **WHEN** exit order executes on T+1
- **THEN** system SHALL compute: pnl_dollars = (exit_price - entry_price) * qty_shares - (2 * 0.001 * position_value) [accounting for entry and exit transaction costs of 0.1% each]

#### Scenario: Calculate PnL percentage
- **WHEN** exit order executes
- **THEN** system SHALL compute: pnl_pct = pnl_dollars / (entry_price * qty_shares)

#### Scenario: Record PnL in trade log
- **WHEN** exit order executes with known entry_price, exit_price, and qty
- **THEN** system SHALL append pnl_dollars and pnl_pct to the trade log entry
````

## File: openspec/changes/archive/2026-04-23-pead-live-multi-symbol/specs/pead-state-manager/spec.md
````markdown
## ADDED Requirements

### Requirement: State file structure and initialization

The state file (`output/pead_live_state.json`) SHALL be a JSON document tracking current open positions per symbol. Structure: `{symbol: {earnings_date, entry_date, entry_price, entry_qty, created_at}}`. The state file SHALL be initialized as empty on first run or if no positions are open.

#### Scenario: Load state file on startup
- **WHEN** cronjob starts and state file exists
- **THEN** system SHALL read and parse the JSON file; if parsing fails, log error and treat as empty state

#### Scenario: Initialize state file if missing
- **WHEN** state file does not exist
- **THEN** system SHALL create an empty state file `{}`

#### Scenario: State structure for single open position
- **WHEN** one symbol has an open position for current earnings event
- **THEN** state file SHALL contain: `{"NXPI": {"earnings_date": "2026-04-30", "entry_date": "2026-04-27", "entry_price": 125.50, "entry_qty": 80, "created_at": "2026-04-27T16:00:00Z"}}`

#### Scenario: State structure for multiple open positions
- **WHEN** multiple symbols have open positions simultaneously
- **THEN** state file SHALL contain entries for each symbol independently: `{"NXPI": {...}, "AMD": {...}, "AVGO": {...}}`

### Requirement: Record new position state on entry

When an entry order executes, the system SHALL write a new state entry with entry details and timestamp.

#### Scenario: Write entry state after buy order
- **WHEN** entry market order executes on T-3
- **THEN** system SHALL append/update state entry: `state[symbol] = {earnings_date, entry_date: today, entry_price: filled_price, entry_qty: filled_qty, created_at: timestamp}`

#### Scenario: Entry state persists until exit
- **WHEN** entry state is recorded and position is held through T+1
- **THEN** state entry SHALL remain in the state file until exit order executes

### Requirement: Idempotency check before entry

Before placing an entry order, the system SHALL check if a position already exists for this symbol and earnings date, and skip if already present.

#### Scenario: Skip entry if already in state
- **WHEN** cronjob runs on T-3 AND symbol already exists in state file with the same earnings_date
- **THEN** system SHALL not place another BUY order; record as "skipped (already entered)"

#### Scenario: Allow entry if earnings event is different
- **WHEN** cronjob runs on T-3 for earnings event E2 AND symbol exists in state but for a previous earnings event E1
- **THEN** this would indicate a failed exit (shouldn't happen); log warning and do not enter (state cleanup required manually)

### Requirement: Delete state entry on position exit

After a position exits, the system SHALL delete the corresponding state entry, resetting to clean slate for the next earnings event.

#### Scenario: Delete entry on successful exit
- **WHEN** exit market order executes on T+1
- **THEN** system SHALL delete `state[symbol]`, leaving state file clean for next earnings event

#### Scenario: Clean state for future events
- **WHEN** position is exited and state entry is deleted
- **THEN** next earnings event for the same symbol can re-enter without interference

### Requirement: Auto-cleanup of stale state entries

The system SHALL automatically remove state entries older than 30 days, in case a position was never exited (e.g., due to manual intervention or error).

#### Scenario: Cleanup entries older than 30 days
- **WHEN** cronjob runs and detects a state entry with created_at timestamp > 30 days ago
- **THEN** system SHALL delete that entry, log warning: "Cleaned up stale NXPI position from 2026-03-25"

#### Scenario: Do not cleanup recent entries
- **WHEN** state entry has created_at < 30 days ago
- **THEN** entry SHALL remain in the state file

### Requirement: Atomic read-modify-write for state file

State file operations (read, check, update, write) SHALL be performed atomically to prevent corruption or lost updates if multiple cronjobs run simultaneously.

#### Scenario: Atomic entry write
- **WHEN** placing an entry order
- **THEN** system SHALL: load state file, check if symbol exists, add/update entry, write atomically (not partial writes)

#### Scenario: Atomic entry delete
- **WHEN** exiting a position
- **THEN** system SHALL: load state file, delete symbol entry, write atomically

#### Scenario: Handle concurrent writes
- **WHEN** two cronjob instances try to update state simultaneously
- **THEN** system SHALL use file locking or atomic operations to ensure one write completes before the other starts (no corruption)

### Requirement: Human-readable state file format

The state file format SHALL be plain JSON, suitable for manual inspection and debugging.

#### Scenario: State file is readable without special tools
- **WHEN** cronjob writes state file
- **THEN** a human can open the file in a text editor and understand the current position(s)

#### Scenario: Pretty-printed JSON for clarity
- **WHEN** state file is written
- **THEN** JSON SHALL be formatted with indentation (not minified) for readability
````

## File: openspec/changes/archive/2026-04-23-pead-live-multi-symbol/specs/pead-trade-logger/spec.md
````markdown
## ADDED Requirements

### Requirement: Trade log file structure and initialization

The trade log (`output/pead_live_trades.csv`) SHALL be an append-only CSV file with columns: symbol, earnings_date, entry_date, exit_date, entry_price, exit_price, qty, pnl, pnl_pct, timestamp. The file SHALL be initialized with a header row on first write if it does not exist.

#### Scenario: Initialize trade log with header
- **WHEN** trade log does not exist and first trade is recorded
- **THEN** system SHALL create the file with header row: `symbol,earnings_date,entry_date,exit_date,entry_price,exit_price,qty,pnl,pnl_pct,timestamp`

#### Scenario: Load existing trade log
- **WHEN** trade log already exists
- **THEN** system SHALL append new trades to the existing file, preserving all previous records

#### Scenario: Trade log structure for single trade
- **WHEN** one trade completes (entry + exit)
- **THEN** trade log SHALL contain one row with all fields populated: `NXPI,2026-04-30,2026-04-27,2026-04-28,125.50,128.60,80,240.00,0.0238,2026-04-28T16:00:00Z`

### Requirement: Record trade entry event

When an entry order executes, the system SHALL begin recording trade details (capture symbol, earnings_date, entry_date, entry_price, entry_qty).

#### Scenario: Capture entry details on order execution
- **WHEN** entry market order executes on T-3
- **THEN** system SHALL store: symbol, earnings_date, entry_date=today, entry_price=filled_price, qty=filled_qty, entry_timestamp

#### Scenario: Hold entry details until exit
- **WHEN** entry is recorded and position held through T+1
- **THEN** entry details SHALL be retained in memory or temporary state, waiting for exit to complete the trade record

### Requirement: Record trade exit and compute PnL

When an exit order executes on T+1+, the system SHALL complete the trade record by adding exit details and computed PnL, then append one row to the trade log CSV.

#### Scenario: Capture exit details on order execution
- **WHEN** exit market order executes on T+1
- **THEN** system SHALL capture: exit_date=today, exit_price=filled_price, exit_timestamp

#### Scenario: Compute net PnL with transaction costs
- **WHEN** exit order executes
- **THEN** system SHALL compute:
  - gross_pnl_pct = (exit_price - entry_price) / entry_price
  - net_pnl_pct = gross_pnl_pct - 0.002 (entry cost 0.1% + exit cost 0.1%)
  - pnl_dollars = net_pnl_pct * entry_price * qty

#### Scenario: Append completed trade to log
- **WHEN** all trade details and PnL are computed
- **THEN** system SHALL append one row to the CSV file: `symbol,earnings_date,entry_date,exit_date,entry_price,exit_price,qty,pnl,pnl_pct,timestamp`

#### Scenario: Trade log records multiple trades chronologically
- **WHEN** multiple trades complete over time
- **THEN** trade log SHALL contain multiple rows (one per trade), appended in chronological order of exit timestamp

### Requirement: Append-only semantics for trade log

The trade log SHALL never be modified or overwritten once written. All operations are append-only to maintain audit trail integrity.

#### Scenario: Append new trade without modifying existing records
- **WHEN** a new trade completes and is logged
- **THEN** system SHALL append a new row; no existing rows are modified or deleted

#### Scenario: Trade log grows monotonically
- **WHEN** multiple trades are recorded over weeks/months
- **THEN** trade log file size increases monotonically; no truncation or reordering

### Requirement: Human-readable trade log format

Trade log format SHALL be plain CSV, easily imported into analysis tools (pandas, Excel, R) for performance analysis and audit.

#### Scenario: Trade log is queryable via pandas
- **WHEN** analyst reads the trade log
- **THEN** they can load it in pandas: `pd.read_csv('output/pead_live_trades.csv')` and analyze by symbol, earnings_date, PnL, hit rate, etc.

#### Scenario: Trade log is readable in Excel
- **WHEN** trade log is opened in Excel or Google Sheets
- **THEN** columns are labeled clearly and values are formatted for easy interpretation

### Requirement: Timestamp precision for audit trail

Each trade record SHALL include a precise timestamp (ISO 8601 format with seconds precision, UTC) to enable accurate sequencing and audit of events.

#### Scenario: Timestamp on trade exit
- **WHEN** exit order executes and trade is logged
- **THEN** timestamp column SHALL contain the exact exit order execution time in ISO 8601 format (e.g., `2026-04-28T16:00:30Z`)

#### Scenario: Timestamp enables event sequencing
- **WHEN** multiple trades are logged on the same day
- **THEN** their timestamps enable precise ordering of events

### Requirement: Record skipped entry events (for analysis)

When an entry is skipped due to negative classifier prediction, the system MAY optionally log a "skipped" record for analysis purposes (to compute true false-negative rate).

#### Scenario: Optional logging of skipped entries
- **WHEN** classifier predicts negative (pred_label == 0) on T-3
- **THEN** system MAY append a record to the trade log with fields: symbol, earnings_date, entry_date, exit_date=NULL, entry_price=NULL, exit_price=NULL, qty=0, pnl=0, pnl_pct=0, timestamp=T-3_time, plus a note "skipped_pred=0"
````

## File: openspec/changes/archive/2026-04-23-pead-live-multi-symbol/.openspec.yaml
````yaml
schema: spec-driven
created: 2026-04-22
````

## File: openspec/changes/archive/2026-04-23-pead-live-multi-symbol/design.md
````markdown
## Context

Currently, PEAD backtest is offline—run manually, analyze results after-the-fact. The classifier has been trained and validated on 2016–2025 historical data showing strong alpha in semiconductors (NXPI 92% hit rate, AMD 75%, AVGO 70%). Live execution faces two operational challenges:

1. **Timing precision**: Entry must trigger at T-3 close, exit at T+1 open (or later if cronjob fails). Multiple symbols have non-overlapping earnings dates, so cronjob must check readiness for each symbol daily.
2. **Idempotency**: Without state tracking, a retry or double-run could place duplicate orders. We need lightweight tracking to answer "did we already trade this event?"

Existing infrastructure available:
- `AlpacaLiveTraderBase` for Alpaca order submission (paper trading)
- `fetch_earnings_events()` to get earnings dates from yfinance
- `fetch_bars()` to get OHLCV data
- Trained classifier model for predictions

## Goals / Non-Goals

**Goals:**
- Daily cronjob that checks all three symbols and triggers entry/exit as calendar dates arrive
- Prevents double-trades for the same symbol/earnings-event pair
- Market orders for entry (T-3) and exit (T+1+), using current market price for PnL
- Full audit trail of all trades (entry price, exit price, PnL, timestamp)
- Clean state after each event (no carryover between earnings events)
- Graceful handling of missed cronjobs (execute exit on next available T+1+)
- No manual intervention needed after initial setup

**Non-Goals:**
- Model retraining during live cycle (separate weekly batch job, out of scope)
- Real (non-paper) trading
- Dynamic position sizing based on market conditions
- Sophisticated exit strategies (profit targets, stop losses)
- Cross-symbol correlation handling
- Integration with other strategies

## Decisions

### Decision 1: State Storage → JSON File (not database)
**Choice**: Single JSON file per symbol (`output/pead_live_state.json`), structured as `{symbol: {earnings_date, entry_date, entry_price, entry_qty, ...}}`.

**Rationale**: 
- Simple, human-readable, easy to inspect/debug
- No extra dependencies (sqlite, redis)
- Small data volume (3 symbols × 1 position each)
- File-based state survives cronjob restarts naturally

**Alternatives considered**:
- CSV file: More awkward to merge/update (would need read-modify-write)
- SQLite: Overkill for 3 symbols + 1 position each
- Redis: Adds operational complexity (another service)

### Decision 2: State Lifecycle → Delete After Exit
**Choice**: After exiting a position (T+1 or later), delete the state entry. Next earnings event gets a clean state.

**Rationale**:
- Simplifies idempotency check: "if symbol in state, position is open"
- No need to track closed positions in state file (that's what trades log does)
- Clean slate semantics match trading intent

### Decision 3: Trade Logging → Append-Only CSV
**Choice**: Single `output/pead_live_trades.csv` with columns: `symbol, earnings_date, entry_date, exit_date, entry_price, exit_price, qty, pnl, pnl_pct, timestamp`.

**Rationale**:
- Audit trail is immutable and queryable
- Easy to import into analysis tools (pandas, Excel)
- Append-only prevents accidental overwrites
- Decoupled from state (state is ephemeral, log is permanent)

### Decision 4: Order Type → Market Orders for Both Entry/Exit
**Choice**: Use market orders (vs limit orders) for both T-3 entry and T+1 exit.

**Rationale**:
- Simplicity: no need to guess fill prices
- Backtest assumes T-3 close/T+1 open prices (market order aligns with that)
- Given semicon volatility, slippage on market orders is acceptable cost
- Live execution will reveal if slippage kills alpha (if so, can switch to limit orders in future)

**Trade-off**: May experience slippage vs theoretical backtest prices. Mitigation: log actual fill prices; compare to backtest assumptions in weekly reviews.

### Decision 5: Exit Timing → `if today >= T+1`
**Choice**: Exit triggers when `today >= T+1 AND position is open AND earnings_date matches`. Handles missed cronjobs gracefully.

**Rationale**:
- If droplet was down on T+1, position still exits on next cronjob run
- Avoids lingering positions past intended exit date
- Simple to implement (just one inequality check)

### Decision 6: Entry Decision → Frozen Classifier, No Retraining
**Choice**: Use pre-trained classifier for live predictions. Retraining happens in separate weekly batch job after T+1 closes.

**Rationale**:
- Live cycle should be stable (no model churn day-to-day)
- Retraining needs full event data (only available after T+1 close)
- Weekly cadence (5 earnings events/year × 3 symbols = ~15 events/year) doesn't warrant daily updates
- Backtest already validated walk-forward performance; retrain weekly to stay current

## Risks / Trade-offs

**[Risk] Alpaca API rate limits or outages** → Mitigation: Catch exceptions, log errors, rely on next cronjob run. No exponential backoff needed for daily cron (single attempt).

**[Risk] Earnings date fetch fails (yfinance down)** → Mitigation: Cache earnings dates in state file; skip day if fetch fails but use last known dates.

**[Risk] State file corruption** → Mitigation: Always back up before write; validate JSON before loading; human-inspectable format aids recovery.

**[Risk] Slippage on market orders reduces alpha** → Mitigation: Log actual fill prices; weekly review will show if live returns match backtest. If not, switch to limit orders.

**[Risk] Model degradation over time** → Mitigation: Weekly retraining job updates model. If performance drops >10%, manual intervention to investigate.

**[Risk] Simultaneous cronjob runs (e.g., manual + scheduled)** → Mitigation: Load/check/write state atomically; OS file locking provides basic protection. For higher safety, add timestamp-based conflict detection.

## Migration Plan

1. **Develop locally** with paper trading on test symbols
2. **Deploy to DigitalOcean droplet** as new cron job entry
3. **Monitor first week** of live execution (observe fills, PnL, log quality)
4. **Verify backtest assumptions**: Compare actual T-3/T+1 fills to historical bar data; check if slippage is acceptable
5. **Scale to production** once confidence is built

Rollback: Simply disable cron job entry. Existing state file can be inspected/manually cleaned up if needed.

## Open Questions

1. How often does yfinance earnings data refresh? Should we cache and validate?
2. Should we add Slack/email alerts on entry/exit (for visibility)?
3. Weekly retraining job: separate script or integrated into cronjob logic?
````

## File: openspec/changes/archive/2026-04-23-pead-live-multi-symbol/proposal.md
````markdown
## Why

Post-Earnings Announcements Drift (PEAD) backtests show strong alpha in semiconductors (NXPI, AMD, AVGO with 70-92% hit rates). The current system only backtests—we need live paper trading execution to validate signals in real market conditions and build operational confidence before deploying real capital.

## What Changes

- **Daily cronjob system** for PEAD multi-symbol live execution (NXPI, AMD, AVGO)
- **Entry logic** triggers at T-3 (3 days before earnings, using frozen pre-trained classifier)
- **Exit logic** triggers at T+1 or later (if cronjob missed), exits immediately at market price
- **State tracking** prevents double-trades for the same symbol/earnings-event combination
- **Trade logging** captures entry/exit details and PnL for audit trail
- **Clean-slate design** — after each event closes, position state is reset for next earnings
- **Robustness** — handles dropped cronjobs gracefully with `today >= T+1` exit condition

## Capabilities

### New Capabilities
- `pead-live-trader`: Daily cronjob-driven live execution engine; fetches earnings dates, checks T-3/T+1 triggers, places Alpaca market orders, coordinates symbol state
- `pead-state-manager`: JSON-based state file tracking current positions per symbol (earnings_date, entry_price, entry_qty); prevents double-trades; auto-cleanup after 30 days
- `pead-trade-logger`: Append-only CSV journal (symbol, earnings_date, entry_date, exit_date, entry_price, exit_price, qty, pnl, pnl_pct, timestamp)

### Modified Capabilities
- `pead-classifier`: Freeze trained model for live predictions (no retraining during live cycle; separate weekly batch job handles retraining after T+1 closes)

## Impact

- **New files**: `core/pead_live_trader.py`, `scripts/pead_daily_cronjob.py`
- **Modified files**: `run.py` (add `--mode pead-live` entry point), `config.py` (add PEAD live parameters)
- **Output artifacts**: `output/pead_live_state.json`, `output/pead_live_trades.csv`
- **Alpaca integration**: Uses existing `AlpacaLiveTraderBase` for order submission
- **Dependencies**: None new (uses existing alpaca, pandas, yfinance)
- **Breaking changes**: None; backtest system unchanged
````

## File: openspec/changes/archive/2026-04-23-pead-live-multi-symbol/tasks.md
````markdown
## 1. State Manager Implementation

- [x] 1.1 Create `core/pead_state_manager.py` with `PEADStateManager` class
- [x] 1.2 Implement `load_state()` method to read JSON state file with error handling
- [x] 1.3 Implement `save_state()` method with atomic writes (file locking)
- [x] 1.4 Implement `add_position(symbol, earnings_date, entry_date, entry_price, entry_qty)` to record new entry
- [x] 1.5 Implement `remove_position(symbol)` to delete position after exit (clean slate)
- [x] 1.6 Implement `get_position(symbol)` to check if symbol has open position
- [x] 1.7 Implement `cleanup_stale_entries(days=30)` to remove entries older than 30 days
- [x] 1.8 Implement `already_traded(symbol, earnings_date)` idempotency check
- [x] 1.9 Add comprehensive logging for all state operations

## 2. Trade Logger Implementation

- [x] 2.1 Create `core/pead_trade_logger.py` with `PEADTradeLogger` class
- [x] 2.2 Implement `initialize_log()` to create CSV header if file doesn't exist
- [x] 2.3 Implement `log_trade(symbol, earnings_date, entry_date, exit_date, entry_price, exit_price, qty, pnl, pnl_pct)` to append trade row
- [x] 2.4 Implement PnL computation with transaction cost deduction (0.1% per leg = 0.2% total)
- [x] 2.5 Implement CSV writing with proper escaping and timestamp formatting (ISO 8601 UTC)
- [x] 2.6 Implement optional `log_skipped_entry(symbol, earnings_date, entry_date, reason)` for analysis
- [x] 2.7 Add error handling for file I/O and disk space issues

## 3. Earnings Calendar and T-N Utilities

- [x] 3.1 Create `data/pead_calendar.py` utility module
- [x] 3.2 Implement `get_trading_dates(start, end)` using NYSE calendar (accounts for holidays/weekends)
- [x] 3.3 Implement `calculate_offset_trading_date(anchor_date, offset)` to compute T-3, T+1 offsets
- [x] 3.4 Implement `is_today_entry_date(symbol, earnings_dates_dict)` to check if today is T-3 for any symbol
- [x] 3.5 Implement `is_today_exit_date(symbol, earnings_dates_dict)` to check if today is T+1+ for any symbol
- [x] 3.6 Implement `fetch_nearest_earnings(symbol)` wrapper around `fetch_earnings_events()`
- [x] 3.7 Add caching for earnings dates to avoid repeated yfinance calls within same cronjob execution

## 4. Classifier Integration for Live Predictions

- [x] 4.1 Identify pre-trained classifier model location/format (from backtest)
- [x] 4.2 Create `strategies/pead_classifier_live.py` wrapper for frozen model
- [x] 4.3 Implement `load_classifier()` to deserialize trained model
- [x] 4.4 Implement `predict_entry(features)` to generate pred_label and prob_positive
- [x] 4.5 Implement feature extraction for 7-day pre-earnings window (reuse from backtest)
- [x] 4.6 Add logging of classifier predictions for audit trail
- [x] 4.7 Test that live predictions match backtest predictions on historical data (validation)

## 5. Alpaca Order Execution

- [x] 5.1 Create `strategies/pead_live_trader.py` with `PEADLiveTrader` class extending `AlpacaLiveTraderBase`
- [x] 5.2 Implement `calculate_position_size(account_equity, entry_price, position_size_pct=0.10)` for entry qty
- [x] 5.3 Implement `place_entry_order(symbol, qty)` to submit market BUY order via Alpaca
- [x] 5.4 Implement `place_exit_order(symbol, qty)` to submit market SELL order via Alpaca
- [x] 5.5 Implement `get_current_price(symbol)` to fetch real-time market price for PnL calculation
- [x] 5.6 Implement error handling for Alpaca API failures (rate limits, insufficient buying power, API down)
- [x] 5.7 Implement order result capture (order_id, fill_price, fill_timestamp) from Alpaca responses
- [x] 5.8 Add detailed logging of all order submissions and fills

## 6. Daily Cronjob Logic

- [x] 6.1 Create `scripts/pead_live_cronjob.py` as the main cronjob entry point
- [x] 6.2 Implement main loop: `for symbol in [NXPI, AMD, AVGO]:`
- [x] 6.3 For each symbol:
  - [x] 6.3.1 Fetch nearest earnings date
  - [x] 6.3.2 Calculate T-3 and T+1 trading dates
  - [x] 6.3.3 Check if today == T-3; if yes, execute entry logic
  - [x] 6.3.4 Check if today >= T+1; if yes, execute exit logic
- [x] 6.4 Implement entry logic: check prediction, place order, update state, log result
- [x] 6.5 Implement exit logic: get current price, calculate PnL, place order, update state, log trade
- [x] 6.6 Implement error handling: catch all exceptions, log, continue to next symbol
- [x] 6.7 Add summary logging at end of cronjob execution (e.g., "Entry fired for NXPI, exit skipped for AMD, error on AVGO")

## 7. Integration with Existing run.py

- [x] 7.1 Add `--mode pead-live` option to `run.py` argument parser
- [x] 7.2 Implement `run_pead_live()` function in `run.py`
- [x] 7.3 Set up logging configuration for pead-live mode (log to file + stdout)
- [x] 7.4 Call `PEADLiveTrader.run_daily_execution()` or equivalent main function
- [x] 7.5 Update README.md with usage instructions for `python run.py --mode pead-live`

## 8. Configuration and Parameters

- [x] 8.1 Add PEAD live parameters to `config.py`:
  - [x] 8.1.1 `PEAD_LIVE_SYMBOLS = ["NXPI", "AMD", "AVGO"]`
  - [x] 8.1.2 `PEAD_LIVE_POSITION_SIZE = 0.10` (10% of capital)
  - [x] 8.1.3 `PEAD_LIVE_PTC = 0.001` (0.1% per leg)
  - [x] 8.1.4 `PEAD_LIVE_STATE_FILE = "output/pead_live_state.json"`
  - [x] 8.1.5 `PEAD_LIVE_LOG_FILE = "output/pead_live_trades.csv"`
  - [x] 8.1.6 `PEAD_LIVE_STALE_DAYS = 30`
- [x] 8.2 Make configuration parameters easily modifiable

## 9. Testing and Validation

- [ ] 9.1 Unit test `PEADStateManager`: load/save, idempotency checks, cleanup
- [ ] 9.2 Unit test `PEADTradeLogger`: CSV format, PnL calculation, append semantics
- [ ] 9.3 Unit test `calculate_offset_trading_date()`: T-3, T+1 calculations, holiday handling
- [ ] 9.4 Unit test classifier prediction wrapper: loads model, returns pred_label/prob
- [ ] 9.5 Integration test: simulate one full entry/exit cycle (mock Alpaca API)
- [ ] 9.6 Manual test on paper trading: dry-run with real Alpaca API (no real execution, observe logs)
- [ ] 9.7 Validate that live predictions match historical backtest on same data

## 10. Documentation and Deployment

- [ ] 10.1 Update README.md with new `--mode pead-live` instructions
- [ ] 10.2 Document cronjob setup: example crontab entry for daily 8am ET execution
- [ ] 10.3 Document state file format and manual inspection procedures
- [ ] 10.4 Document trade log schema and how to analyze results
- [ ] 10.5 Create deployment checklist for DigitalOcean droplet
- [ ] 10.6 Add comments to all new modules explaining key design decisions
- [ ] 10.7 Write runbook for troubleshooting common issues (missed orders, state corruption, etc.)

## 11. Weekly Model Retraining (Separate Job, Lower Priority)

- [ ] 11.1 Design weekly retraining job (runs Sunday evening, retrain on all accumulated T+1 results)
- [ ] 11.2 Note: This is a separate cronjob entry; scope it for future implementation if needed
````

## File: openspec/changes/archive/2026-04-24-pead-configurable-entry-offset/specs/data-layer/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Fetch daily OHLCV bars for a symbol universe
The system SHALL fetch historical daily bar data for a list of symbols using alpaca-py `StockHistoricalDataClient`, returning a dict mapping each symbol to a pandas DataFrame with columns: `open`, `high`, `low`, `close`, `volume` indexed by date. The function SHALL accept an optional `symbols` parameter allowing single-symbol fetches (for example `["QQQ"]`) in addition to the existing multi-symbol use case. Date-range behavior SHALL be inclusive of the requested end date for daily bars, and returned OHLCV rows SHALL be preserved even when first-row derived return fields are NaN.

#### Scenario: Successful multi-symbol fetch
- **WHEN** `fetch_bars(symbols, start, end, timeframe)` is called with a list of valid symbols and a date range
- **THEN** the function returns a dict where each key is a symbol string and each value is a DataFrame with OHLCV columns indexed by UTC date

#### Scenario: Single-symbol fetch for benchmark
- **WHEN** `fetch_bars(["QQQ"], start, end)` is called
- **THEN** the function returns a dict with a single key `"QQQ"` and a valid OHLCV DataFrame

#### Scenario: Inclusive end date for daily bars
- **WHEN** `fetch_bars(["NXPI"], "2026-04-14", "2026-04-23")` is called and provider data exists for 2026-04-23
- **THEN** the returned DataFrame includes the 2026-04-23 daily bar

#### Scenario: Symbol with no data in range
- **WHEN** a symbol is requested but has no data in the given date range
- **THEN** the function raises a descriptive `ValueError` identifying the missing symbol

#### Scenario: Credentials loaded from .env
- **WHEN** `fetch_bars()` is called and a `.env` file with valid credentials exists
- **THEN** the `StockHistoricalDataClient` authenticates successfully and returns data

#### Scenario: Missing credentials
- **WHEN** `APCA_API_KEY_ID` or `APCA_API_SECRET_KEY` is not set in the environment
- **THEN** the function raises a `EnvironmentError` before making any API calls

#### Scenario: Returns column present after fetch
- **WHEN** `fetch_bars()` returns successfully
- **THEN** each symbol DataFrame contains a `return` column, and OHLCV rows are not dropped solely because first-row `return` is NaN
````

## File: openspec/changes/archive/2026-04-24-pead-configurable-entry-offset/specs/live-trader/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Weekly rebalance trigger
The PEAD live execution flow SHALL evaluate entry for each symbol using configurable entry offset `PEAD_ENTRY_OFFSET_DAYS`, where entry date is `T-E` and required feature bars are available by `T-(E+1)` close. The system SHALL NOT attempt entry prediction when the required anchor bar is not yet available, and SHALL log an explicit skip reason.

#### Scenario: Entry evaluated with available anchor bars
- **WHEN** live execution runs for symbol S and all bars through `T-(E+1)` are available
- **THEN** prediction is computed and entry order logic is evaluated for date `T-E`

#### Scenario: Entry skipped when anchor bar unavailable
- **WHEN** live execution runs before the required anchor bar has finalized for symbol S
- **THEN** no prediction or order is attempted for that symbol and logs record `missing feature-anchor bar`

#### Scenario: Existing order safety behavior preserved
- **WHEN** live execution runs outside supported order timing or data preconditions
- **THEN** no new entry order is submitted
````

## File: openspec/changes/archive/2026-04-24-pead-configurable-entry-offset/specs/pead-backtest/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Event-driven backtest simulating overnight entry at T-1 close
The PEAD backtest SHALL support a configurable entry offset `PEAD_ENTRY_OFFSET_DAYS` and SHALL enter a long position at `open(T-E)` for each event where `pred_label == 1`, where E is the configured entry offset. The backtest SHALL exit at either T+1 open or T+1 close according to configured exit mode. Each trade is independent; no portfolio is held between events.

#### Scenario: Trade entered at T-3 open
- **WHEN** `pred_label == 1` and `PEAD_ENTRY_OFFSET_DAYS=3`
- **THEN** a long entry is recorded at `open(T-3)` with configured position size as a fraction of capital

#### Scenario: Trade exited at T+1 open
- **WHEN** a trade is open and the configured exit mode is `t_plus_1_open`
- **THEN** the position is closed at `open(T+1)` and PnL is recorded from `open(T-E)` to `open(T+1)`

#### Scenario: Trade exited at T+1 close
- **WHEN** a trade is open and the configured exit mode is `t_plus_1_close`
- **THEN** the position is closed at `close(T+1)` and PnL is recorded from `open(T-E)` to `close(T+1)`

#### Scenario: No trade on predicted-negative event
- **WHEN** `pred_label == 0` for an event
- **THEN** no entry or exit is simulated and capital is unchanged

### Requirement: Invocable via `python run.py --mode pead-backtest`
The main entry point SHALL support `--mode pead-backtest` as the PEAD timing-variant runner that executes the full pipeline: fetch earnings events -> fetch bars -> build features using bars available by `T-(E+1)` where E is `PEAD_ENTRY_OFFSET_DAYS` -> walk-forward predict -> backtest the configured entry/exit horizon -> print summary.

#### Scenario: pead-backtest mode runs end to end
- **WHEN** `python run.py --mode pead-backtest` is invoked
- **THEN** the full configured timing-variant pipeline completes without error and prints a PEAD risk summary

#### Scenario: Existing non-PEAD modes unaffected
- **WHEN** `python run.py --mode backtest` or `--mode live` is invoked
- **THEN** behavior is identical to before this change
````

## File: openspec/changes/archive/2026-04-24-pead-configurable-entry-offset/specs/pead-entry-timing-config/spec.md
````markdown
## ADDED Requirements

### Requirement: Configurable PEAD entry offset for backtest and live execution
The system SHALL expose a configuration parameter `PEAD_ENTRY_OFFSET_DAYS` representing the entry day offset in trading days before earnings day T. The value MUST be a positive integer and SHALL be interpreted consistently by backtest and live code paths.

#### Scenario: Valid offset accepted
- **WHEN** `PEAD_ENTRY_OFFSET_DAYS=3` is configured
- **THEN** both backtest and live logic treat entry day as T-3

#### Scenario: Invalid offset rejected
- **WHEN** `PEAD_ENTRY_OFFSET_DAYS` is set to 0, a negative number, or a non-integer value
- **THEN** the system raises a configuration validation error before any trading or backtest execution begins

### Requirement: Derived feature anchor from configured entry offset
For an entry offset E, the feature window anchor SHALL be T-(E+1), and the 7-day feature window SHALL cover the 7 trading days ending at that anchor date (inclusive).

#### Scenario: T-3 open entry derives T-4 anchor
- **WHEN** `PEAD_ENTRY_OFFSET_DAYS=3`
- **THEN** feature anchor is T-4 and the feature window is T-10 through T-4

#### Scenario: T-5 open entry derives T-6 anchor
- **WHEN** `PEAD_ENTRY_OFFSET_DAYS=5`
- **THEN** feature anchor is T-6 and the feature window is the 7 trading days ending at T-6

### Requirement: Runtime visibility of effective timing configuration
The system SHALL log the effective entry offset, derived feature anchor offset, and resolved entry/exit dates for each run.

#### Scenario: Effective timing is logged
- **WHEN** a PEAD backtest or live run starts
- **THEN** logs include `entry_offset_days`, `feature_anchor_offset_days`, and configured exit mode
````

## File: openspec/changes/archive/2026-04-24-pead-configurable-entry-offset/specs/pre-earnings-features/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Build a feature vector per earnings event from T-7 to T-1 daily bars
The feature module SHALL produce a single feature vector per earnings event by computing summary statistics over a 7-trading-day window ending at a configurable feature anchor derived from `PEAD_ENTRY_OFFSET_DAYS`. For entry offset E, the feature anchor MUST be T-(E+1), and all features MUST use only data available by the anchor close with no forward-looking fields relative to the entry decision time.

#### Scenario: Feature vector produced for each event
- **WHEN** `build_features(events_df, bars_dict, entry_offset_days=3)` is called with a valid events DataFrame and OHLCV bar data
- **THEN** the function returns a DataFrame with one row per event and one column per feature, indexed by `earnings_date`

#### Scenario: No forward-looking data used
- **WHEN** features are computed for an event with earnings date T and entry offset E
- **THEN** no bar after T-(E+1) appears in the feature computation window

### Requirement: Price drift features (T-7 to T-1)
The module SHALL compute the following price drift features over the 7-day pre-earnings window ending at the derived anchor date T-(E+1):

- `drift_7d`: Cumulative simple return from the first close in the window to the anchor close.
- `drift_slope`: Ordinary-least-squares slope of daily closes over the window, normalized by the mean close.
- `up_day_count`: Number of days where `close > close.shift(1)` in the window.
- `down_day_count`: Number of days where `close < close.shift(1)` in the window.

#### Scenario: Drift computed correctly
- **WHEN** close prices over the 7-day window ending at T-(E+1) increase monotonically
- **THEN** `drift_7d` is positive, `up_day_count` equals 6, and `down_day_count` equals 0

#### Scenario: Slope captures convexity
- **WHEN** closes accelerate upward over the window ending at T-(E+1)
- **THEN** `drift_slope` is positive and larger than for a linear price path with the same total drift

### Requirement: Volume pressure features (T-7 to T-1)
The module SHALL compute:

- `rel_volume_mean`: Mean daily volume over the window ending at T-(E+1) divided by the symbol's 20-day baseline volume computed from the 20 trading days ending immediately before the feature window begins.
- `down_volume_ratio`: Sum of volume on down days divided by total window volume.

#### Scenario: Volume baseline uses non-overlapping window
- **WHEN** baseline volume is computed for an event
- **THEN** no bar from the 7-day feature window ending at T-(E+1) is included in the 20-day baseline

#### Scenario: Down-volume ratio reflects selling pressure
- **WHEN** all volume in the window occurs on down days
- **THEN** `down_volume_ratio` equals 1.0

### Requirement: Volatility regime features (T-7 to T-1)
The module SHALL compute:

- `atr_ratio`: Mean of `(high - low)` over the window ending at T-(E+1) divided by the mean of `(high - low)` for the 20-day baseline period immediately preceding the feature window.
- `gap_count`: Number of overnight gaps (`abs(open - prev_close) / prev_close > 0.005`) within the window.

#### Scenario: ATR expansion detected
- **WHEN** intraday ranges expand significantly in the 7-day window ending at T-(E+1) relative to the prior 20-day baseline
- **THEN** `atr_ratio` is greater than 1.0

### Requirement: Relative-to-market features (T-7 to T-1)
The module SHALL compute:

- `rel_drift_vs_qqq`: `drift_7d` (symbol) minus the QQQ cumulative return over the same 7-day window ending at T-(E+1), using QQQ bars passed in `bars_dict`.

#### Scenario: Outperformance detected
- **WHEN** the symbol rises 5% and QQQ rises 2% over the same window ending at T-(E+1)
- **THEN** `rel_drift_vs_qqq` equals approximately 0.03

### Requirement: Target label computation
The module SHALL compute the binary target label alongside features:

- `y`: 1 if `open(T) / close(T-1) - 1 > 0.0`, else 0.
- `gap_return`: Continuous gap return `open(T) / close(T-1) - 1` (stored for evaluation, not used as training label).

#### Scenario: Positive gap labeled correctly
- **WHEN** T open is higher than T-1 close
- **THEN** `y = 1` and `gap_return > 0`

#### Scenario: No-gap or negative gap labeled correctly
- **WHEN** T open equals or is below T-1 close
- **THEN** `y = 0` and `gap_return <= 0`

### Requirement: Drop events with insufficient bar history
The module SHALL exclude any event where fewer than 7 valid bars exist in the feature window ending at T-(E+1), and log a warning per dropped event.

#### Scenario: Event dropped on insufficient history
- **WHEN** only 4 bars are available in the feature window ending at T-(E+1) for an event
- **THEN** that event is excluded from the output and a warning is logged
````

## File: openspec/changes/archive/2026-04-24-pead-configurable-entry-offset/.openspec.yaml
````yaml
schema: spec-driven
created: 2026-04-23
````

## File: openspec/changes/archive/2026-04-24-pead-configurable-entry-offset/design.md
````markdown
## Context

The PEAD system currently mixes a fixed T-3 entry concept with daily-bar availability constraints. In live mode, when the job runs before a T-3 daily bar is finalized, feature generation can fail because the required anchor bar is absent. This surfaced as event drops for near-term earnings symbols.

The user wants two things:
1. A coherent timing model for T-3 open entry, which implies features must stop at T-4 close (window T-10..T-4).
2. Configurable entry offsets so strategy variants (T-4, T-5, etc.) can be tested without code rewrites.

This change introduces one timing contract used by both backtest and live: entry offset is configurable, and feature window is derived from offset deterministically.

## Goals / Non-Goals

**Goals:**
- Define a single timing model shared by backtest and live PEAD flows.
- Support configurable entry offsets through config, with offset-specific feature windows.
- Eliminate impossible decision timing (for example requiring a bar that does not exist yet at decision time).
- Preserve classifier pipeline compatibility by keeping feature names stable while changing date anchoring.
- Make runtime behavior explicit in logs and docs.

**Non-Goals:**
- Re-architecting the model family or introducing a new model type.
- Introducing intraday minute-bar feature engineering in this change.
- Implementing full hyperparameter/offset grid optimization tooling.

## Decisions

1. Decision: Introduce config-driven entry offset as the source of truth.
- Choice: Add PEAD entry offset config values and propagate through feature builder, backtest, and live execution.
- Why: Hardcoded timing creates fragile behavior and blocks strategy iteration.
- Alternative considered: Keep fixed T-3 and add ad-hoc exceptions in live mode.
- Why rejected: Preserves incoherent semantics and accumulates timing bugs.

2. Decision: Define feature window relative to entry offset, not fixed named dates.
- Choice: For entry offset E (positive integer days before earnings), feature window is 7 trading days ending at E+1 (for T-3 open, end at T-4; window T-10..T-4).
- Why: Guarantees every feature bar is known before entry execution.
- Alternative considered: Keep T-3 feature anchor and delay decisions until next day.
- Why rejected: Violates intended entry timing and produces post-hoc decisions.

3. Decision: Use open-entry semantics in backtest/live for offset-driven entry day.
- Choice: Entry execution uses entry-day open price, with exit mode remaining configurable (T+1 open/close).
- Why: Aligns with user intent for "decide at T-3 open" and avoids requiring same-day close data.
- Alternative considered: Entry-at-close semantics with post-close trigger.
- Why rejected: Contradicts requested timing variant and daytime cron usage.

4. Decision: Keep data-layer daily fetch inclusive and avoid dropping first bar in requested range.
- Choice: Maintain inclusive end-date fetch and preserve OHLCV rows even if return is NaN on first row.
- Why: Offset-derived windows require precise boundaries; dropping a boundary bar causes false "missing bar" failures.
- Alternative considered: Compute returns externally and keep current drop behavior.
- Why rejected: Unnecessary complexity and repeated edge-case handling downstream.

## Risks / Trade-offs

- [Risk] Timing model changes alter historical backtest performance and comparability with archived results.
  -> Mitigation: Log entry offset and derived window dates for each run; document baseline shift in README.

- [Risk] Offset generalization can introduce off-by-one errors around holidays.
  -> Mitigation: Centralize offset date derivation in `data/pead_calendar.py` and add unit tests for known holiday weeks.

- [Risk] Existing trained models may degrade if retrained under new timing semantics.
  -> Mitigation: Keep model artifact versioning and include a retrain step in tasks after timing migration.

- [Risk] Different data plans (IEX/SIP limits) can still cause missing-recent-bar errors.
  -> Mitigation: Keep descriptive logging and explicit skip reasons; document required market-data subscription behavior.
````

## File: openspec/changes/archive/2026-04-24-pead-configurable-entry-offset/proposal.md
````markdown
## Why

The current PEAD live path fails on entry day because the decision timing and available bar data are inconsistent: we trigger on T-3 while the model expects a fully available T-3 daily bar. This creates impossible behavior ("decide T-3" only after T-3 has passed) and causes dropped events in live runs.

We also need entry timing to be strategy-configurable instead of hardcoded so we can test and compare variants (for example T-3 open, T-4 open, T-5 open) without rewriting feature logic and backtest/live orchestration each time.

## What Changes

- Add configurable PEAD entry timing via config (`PEAD_ENTRY_OFFSET_DAYS`) and derive the feature window from that offset.
- Redefine default live/backtest semantics to support T-3 open entry by using only bars available by T-4 close (feature window T-10..T-4).
- Generalize feature engineering to compute windows from `entry_offset_days` (not fixed T-3 assumptions).
- Update backtest entry/exit pricing logic to use configurable entry anchor and keep configurable exit mode.
- Update live cronjob trigger logic to evaluate entry on entry-day open semantics and avoid impossible "predict after the fact" paths.
- Update logging and docs to print the configured entry/feature window so runtime behavior is explicit.

## Capabilities

### New Capabilities
- `pead-entry-timing-config`: Config-driven PEAD entry timing and derived feature window rules shared by backtest and live execution.

### Modified Capabilities
- `pre-earnings-features`: Requirement changes from fixed T-3 feature anchoring to offset-driven window generation.
- `pead-backtest`: Requirement changes from fixed T-3 close entry to configurable entry offset with open-entry semantics.
- `live-trader`: Requirement changes to ensure PEAD live entry decisions align with data actually available at decision time.
- `data-layer`: Requirement changes to enforce inclusive date windows for daily bars used in offset-derived feature windows.

## Impact

- Affected code:
  - `config.py`
  - `data/pre_earnings_features.py`
  - `data/pead_calendar.py`
  - `data/alpaca_data.py`
  - `strategies/pead_backtest.py`
  - `scripts/pead_live_cronjob.py`
  - `run.py`
- New/updated OpenSpec files under this change for one new capability and multiple modified capabilities.
- Backtest outputs will change because entry/feature timing changes.
- README and runbook sections for PEAD timing must be updated to describe configurable entry offsets.
````

## File: openspec/changes/archive/2026-04-24-pead-configurable-entry-offset/tasks.md
````markdown
## 1. Configuration and Timing Contract

- [x] 1.1 Add `PEAD_ENTRY_OFFSET_DAYS` validation (positive integer) in `config.py`
- [x] 1.2 Add helper(s) in `data/pead_calendar.py` to derive entry day `T-E` and feature anchor day `T-(E+1)`
- [x] 1.3 Update run/startup logging to print effective timing config (`entry_offset_days`, anchor offset, exit mode)

## 2. Data-Layer Boundary Fixes

- [x] 2.1 Ensure `data.alpaca_data.fetch_bars()` treats daily end date as inclusive
- [x] 2.2 Preserve OHLCV rows when first-row `return` is NaN (no blanket drop on return NaN)
- [x] 2.3 Add/adjust tests for inclusive end-date behavior and row preservation

## 3. Feature Engineering Generalization

- [x] 3.1 Update `build_features()` to accept `entry_offset_days` and derive anchor date from it
- [x] 3.2 Shift default T-3-open semantics to feature window `T-10..T-4` when `entry_offset_days=3`
- [x] 3.3 Keep feature column schema unchanged while using offset-derived windows
- [x] 3.4 Update warnings/errors to report missing bars in terms of derived anchor dates
- [x] 3.5 Add unit tests for offset variants (T-3, T-4, T-5) and no-lookahead guarantees

## 4. Backtest Timing Migration

- [x] 4.1 Update PEAD backtest entry pricing to use `open(T-E)` instead of fixed `close(T-3)`
- [x] 4.2 Keep exit modes (`t_plus_1_open`, `t_plus_1_close`) and ensure PnL uses new entry price basis
- [x] 4.3 Update event filtering to skip when `T-E`, `T-(E+1)`, or exit bars are unavailable
- [x] 4.4 Update backtest reporting to include configured entry offset and derived timing window

## 5. Live Cronjob Timing Migration

- [x] 5.1 Replace hardcoded T-3 checks in `scripts/pead_live_cronjob.py` with `PEAD_ENTRY_OFFSET_DAYS`
- [x] 5.2 Only build prediction features when bars through `T-(E+1)` are available
- [x] 5.3 For `entry_offset_days=3`, ensure live logic reflects T-3-open semantics using `T-10..T-4` features
- [x] 5.4 Keep idempotency/state handling correct under configurable entry offset
- [x] 5.5 Improve skip logging to distinguish timing-unavailable vs. true data-missing cases

## 6. End-to-End Validation

- [x] 6.1 Run `python run.py --mode pead-backtest` with `PEAD_ENTRY_OFFSET_DAYS=3` and confirm end-to-end success
- [x] 6.2 Run backtest with at least one alternate offset (for example 4 or 5) and confirm logic remains valid
- [x] 6.3 Run `python run.py --mode pead-live` in paper mode and verify no impossible post-hoc prediction behavior
- [x] 6.4 Confirm live logs clearly show effective timing configuration and entry/skip reasons per symbol

## 7. Documentation

- [x] 7.1 Update README PEAD section with entry-offset configuration and timing semantics
- [x] 7.2 Document how to test alternate entry offsets (T-3, T-4, T-5) safely
- [x] 7.3 Document migration note that prior backtest results are not directly comparable after timing change
````

## File: openspec/changes/archive/2026-04-30-fix-momentum-live-cash-constrained-moc-rebalance/specs/live-trader/spec.md
````markdown
## ADDED Requirements

### Requirement: MOC rebalance budget excludes exiting positions
For live MOC rebalances with a capital cap, the system SHALL compute retained strategy exposure using only currently held symbols that remain in the target set, and SHALL exclude positions already marked for sale from capital-cap accounting.

#### Scenario: Capital cap ignores positions already scheduled to exit
- **WHEN** the strategy currently holds `AAPL`, `META`, and `NVDA`, `META` is no longer in the target set, and a capital cap is configured
- **THEN** the rebalance computes retained exposure from `AAPL` and `NVDA` only and does not count `META` against remaining buy budget

### Requirement: Live rebalance logs skipped buys for auditability
The live trader SHALL write an explicit log entry when a target buy is skipped because pre-close available cash cannot fund at least one whole share.

#### Scenario: Insufficient-cash skip is logged
- **WHEN** symbol S is a new target entry and the remaining buy budget is less than the reference price of one share of S
- **THEN** the rebalance submits no buy order for S and logs the symbol, remaining cash, and insufficient-cash skip reason
````

## File: openspec/changes/archive/2026-04-30-fix-momentum-live-cash-constrained-moc-rebalance/specs/momentum-strategy/spec.md
````markdown
## ADDED Requirements

### Requirement: Live rebalance preserves ranked replacement order
The live momentum rebalance SHALL preserve the momentum-ranked target order returned by the signal, SHALL submit sell orders for dropped strategy holdings regardless of unrealized gain or loss, and SHALL evaluate new replacement buys in that same rank order.

#### Scenario: Dropped symbol is sold even when losing
- **WHEN** symbol S is currently held by the live momentum strategy, is no longer in the target list, and has a negative unrealized PnL
- **THEN** the rebalance submits a sell order for S and does not retain it solely because it is at a loss

#### Scenario: New entries are evaluated in momentum rank order
- **WHEN** the live target ranking is `[AAPL, AMZN, NVDA]`, `AAPL` is already held, and `AMZN` and `NVDA` are new entries
- **THEN** the rebalance evaluates `AMZN` before `NVDA` when allocating limited buy cash

### Requirement: Live MOC buys use only pre-close available cash
The live momentum rebalance SHALL compute buy budget only from cash available before the close, SHALL NOT treat same-day MOC sale proceeds as available for new buys, and SHALL size buys only across new target entries.

#### Scenario: Same-day MOC sale proceeds are excluded from buy budget
- **WHEN** symbol `META` is scheduled for a same-day MOC sell and `AMZN` is a new target entry
- **THEN** the rebalance computes the `AMZN` buy budget without including expected proceeds from the `META` sell order

#### Scenario: Buy sizing uses only remaining new-entry slots
- **WHEN** there are two new target entries remaining and the live trader has `$1,000` of pre-close available cash
- **THEN** the next buy decision is sized from the remaining cash divided by the remaining unfunded new entries rather than by all target holdings

### Requirement: Insufficient-cash buys are skipped explicitly
The live momentum rebalance SHALL skip a target buy when remaining buy budget cannot fund at least one whole share and SHALL log the skipped symbol and reason explicitly.

#### Scenario: Buy skipped because one share cannot be funded
- **WHEN** `AMZN` is a new target entry, the remaining buy budget is below the reference price of one share, and no fractional shares are supported
- **THEN** no buy order is submitted for `AMZN` and logs record that the buy was skipped due to insufficient available cash before the close
````

## File: openspec/changes/archive/2026-04-30-fix-momentum-live-cash-constrained-moc-rebalance/.openspec.yaml
````yaml
schema: spec-driven
created: 2026-04-30
````

## File: openspec/changes/archive/2026-04-30-fix-momentum-live-cash-constrained-moc-rebalance/design.md
````markdown
## Context

The live momentum trader submits Market-on-Close orders to match the backtest's close-execution assumption, but the current rebalance logic sizes buys from the account cash snapshot without distinguishing between already-available cash and proceeds from same-day MOC sells. As a result, replacement buys can be silently skipped or sized inconsistently, and buy priority across multiple new entries is undefined.

The change is confined to the weekly live momentum rebalance flow. It does not alter the signal definition, the MOC execution choice, or the rule that dropped symbols are sold regardless of unrealized gain or loss.

## Goals / Non-Goals

**Goals:**
- Keep MOC orders as the live execution model.
- Define a deterministic rebalance flow that always sells dropped symbols and funds new buys only from cash available before the close.
- Preserve momentum rank order when multiple new entries compete for limited cash.
- Make skipped buys and capital-cap behavior explicit in logs.

**Non-Goals:**
- Changing live execution from MOC to DAY orders.
- Reusing same-day MOC sale proceeds for new buys.
- Adding loss-aware sell filters or partial-position resizing.
- Changing the backtest strategy semantics.

## Decisions

### Decision: Treat same-day MOC sale proceeds as unavailable for buys

The rebalance will submit sells first for dropped symbols, but the buy budget will be computed strictly from currently available account cash. Same-day MOC sale proceeds are excluded because they are not available until the close.

Alternatives considered:
- Assume sell proceeds are reusable in the same rebalance run. Rejected because it conflicts with MOC timing.
- Switch to DAY orders so proceeds may become available sooner. Rejected because the change intent is to keep close-price execution.

### Decision: Buy only new entries and process them in signal rank order

The rebalance will preserve the ranked target list returned by the signal and iterate new entries in that order. This gives deterministic behavior when available cash can fund only a subset of replacements.

Alternatives considered:
- Convert targets to a set and lose ordering. Rejected because buy priority becomes arbitrary.
- Split cash equally across all targets, including symbols already held. Rejected because unchanged holdings are not resized in this live model.

### Decision: Allocate remaining cash progressively across remaining buy slots

For each new entry in rank order, the trader will compute a per-symbol budget from remaining buy cash divided by remaining unfunded entries. This preserves rank priority without overcommitting the first symbol.

Alternatives considered:
- Spend all remaining cash on the highest-ranked new entry. Rejected because it over-concentrates replacement buys.
- Precompute fixed equal allocations before filtering skipped names. Rejected because later entries would not benefit from cash released by earlier skips.

### Decision: Capital-cap accounting excludes positions already marked for sale

When `max_capital` is set, the trader will estimate currently retained exposure using only positions that remain in the target set. Positions already marked for sale will not count against the remaining budget.

Alternatives considered:
- Count all currently held strategy positions, including outgoing names. Rejected because it artificially suppresses buys during rotations.

### Decision: Log skipped buys explicitly

If remaining buy budget cannot fund at least one share of a target symbol, the trader will skip the order and write an explicit log entry with symbol, reference price, and remaining cash.

Alternatives considered:
- Silently skip zero-quantity buys. Rejected because it obscures whether skipped entries were intentional or a bug.

## Risks / Trade-offs

- Cash-constrained rotations may leave the portfolio temporarily underinvested -> This is accepted as the correct consequence of keeping MOC and refusing to rely on same-day sale proceeds.
- Using recent close prices for share sizing can differ slightly from the closing-auction fill -> Existing MOC design already accepts this approximation for order sizing.
- Rank-priority buys may still leave lower-ranked targets unfunded for a week -> Explicit logging will make these tradeoffs visible for later tuning.

## Migration Plan

1. Update live momentum rebalance logic to preserve ranked targets, compute retained exposure, and process new buys from available cash only.
2. Add or update focused tests covering sell-first behavior, rank-ordered buys, capital-cap accounting, and explicit skipped-buy logging.
3. Run the weekly rebalance test slice and any momentum-specific unit tests.
4. Deploy with no config migration; rollback is limited to restoring the prior rebalance method.

## Open Questions

None.
````

## File: openspec/changes/archive/2026-04-30-fix-momentum-live-cash-constrained-moc-rebalance/proposal.md
````markdown
## Why

The live momentum rebalance currently submits MOC sells and then sizes buys from the account cash snapshot taken before the close. This can skip legitimate replacement buys because same-day MOC sale proceeds are not available yet, while also obscuring the intended buy-priority and skip behavior.

## What Changes

- Clarify that the live momentum rebalance treats same-day MOC sale proceeds as unavailable for new buys.
- Preserve the existing behavior that dropped symbols are sold regardless of gain or loss.
- Define buy selection for new target entries using momentum rank order and only currently available cash.
- Require explicit logging when a target buy is skipped because cash is insufficient to purchase at least one share.
- Clarify that capital-cap calculations exclude positions already marked for sale and apply only to retained holdings plus new buys.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `momentum-strategy`: Change live rebalance behavior so new entries are funded only from currently available cash, prioritized by momentum rank, while dropped holdings are always sold.
- `live-trader`: Clarify how MOC order timing interacts with rebalance cash availability, buy skipping, and capital-cap accounting.

## Impact

- Affected code: `strategies/momentum.py`, and potentially shared live-order helper logic in `core/live_trader_base.py` if logging or position metadata access needs adjustment.
- Affected behavior: weekly live M7 rebalance order generation, skipped-buy logging, and capital-cap accounting.
- No new external dependencies or APIs.
````

## File: openspec/changes/archive/2026-04-30-fix-momentum-live-cash-constrained-moc-rebalance/tasks.md
````markdown
## 1. Rebalance Logic

- [x] 1.1 Update `LiveMomentumTrader.rebalance()` to preserve ranked targets, identify dropped holdings, and submit sells for dropped symbols regardless of unrealized PnL.
- [x] 1.2 Change live buy-budget calculation to use only currently available cash, excluding same-day MOC sale proceeds and excluding positions marked for sale from capital-cap accounting.
- [x] 1.3 Implement rank-ordered new-entry buys using remaining cash divided across remaining buy slots, and log explicit insufficient-cash skips when fewer than one whole share can be purchased.

## 2. Focused Validation

- [x] 2.1 Add or update tests covering sell-first behavior, rank-ordered replacement buys, and insufficient-cash skip logging.
- [x] 2.2 Add or update tests covering capital-cap accounting that ignores positions already scheduled to exit.
- [x] 2.3 Run the relevant momentum and live-rebalance test slice and confirm the new behavior passes.
````

## File: openspec/changes/archive/2026-05-05-account-separation-v1-v2/specs/data-layer/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Fetch daily OHLCV bars for a symbol universe
The system SHALL fetch historical daily bar data for a list of symbols using alpaca-py `StockHistoricalDataClient`, returning a dict mapping each symbol to a pandas DataFrame with columns `open`, `high`, `low`, `close`, `volume` indexed by date. The function SHALL support profile-aware authentication and SHALL default to profile `v1` when no profile is provided.

#### Scenario: Successful multi-symbol fetch with default profile
- **WHEN** `fetch_bars(symbols, start, end, timeframe)` is called without an explicit profile
- **THEN** the request authenticates with profile `v1` credentials and returns symbol-keyed OHLCV DataFrames

#### Scenario: Successful fetch with explicit v2 profile
- **WHEN** `fetch_bars(symbols, start, end, timeframe, profile="v2")` is called with valid V2 credentials
- **THEN** the request authenticates with `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY`

#### Scenario: Backtest data fetch uses v1 by default
- **WHEN** backtest workflows call `fetch_bars()` without profile overrides
- **THEN** data-layer authentication uses profile `v1`

#### Scenario: Missing profile credentials
- **WHEN** required environment variables for the selected profile are not set
- **THEN** the function raises `EnvironmentError` before making any API call and names the missing profile variables

## ADDED Requirements

### Requirement: Profile-aware data credential naming
The data layer SHALL resolve credentials from profile-prefixed environment variables using the following names:
- For `v1`: `V1_APCA_API_KEY_ID`, `V1_APCA_API_SECRET_KEY`
- For `v2`: `V2_APCA_API_KEY_ID`, `V2_APCA_API_SECRET_KEY`

#### Scenario: V2 key naming is normalized
- **WHEN** profile `v2` is selected for a data request
- **THEN** the system reads `V2_APCA_API_KEY_ID` and SHALL NOT require `V2_APCA_API_KEY`
````

## File: openspec/changes/archive/2026-05-05-account-separation-v1-v2/specs/live-trader/spec.md
````markdown
## ADDED Requirements

### Requirement: Profile-aware Alpaca live trader authentication
The live trader base SHALL authenticate Alpaca trading clients using a required profile identifier for live strategy flows. Supported profiles are `v1` and `v2`, each mapped to profile-prefixed environment variables.

#### Scenario: Momentum live trader uses v1 profile
- **WHEN** weekly momentum live rebalance initializes its trading client
- **THEN** it authenticates using `V1_APCA_API_KEY_ID` and `V1_APCA_API_SECRET_KEY`

#### Scenario: Missing live profile credentials fail fast
- **WHEN** the selected profile credentials are missing at trader initialization time
- **THEN** initialization fails with an error that identifies the missing profile variable names

### Requirement: Live momentum routing is explicit
The live momentum execution flow SHALL pass profile `v1` explicitly when constructing the shared live trader base.

#### Scenario: Momentum account routing is deterministic
- **WHEN** momentum live rebalance is executed from supported entrypoints
- **THEN** all order placement calls route through a `TradingClient` initialized with profile `v1`
````

## File: openspec/changes/archive/2026-05-05-account-separation-v1-v2/specs/pead-live-trader/spec.md
````markdown
## ADDED Requirements

### Requirement: PEAD live trading uses V2 profile
The PEAD live trader SHALL initialize Alpaca trading access with profile `v2` so PEAD orders are isolated from momentum account activity.

#### Scenario: PEAD live trader authenticates with V2 credentials
- **WHEN** PEAD live cronjob creates `PEADLiveTrader`
- **THEN** the trading client is authenticated with `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY`

### Requirement: PEAD live data fetches are profile-selectable
PEAD live execution paths that fetch bars SHALL support explicit profile selection. If no profile is provided for general data calls, the system SHALL use default `v1` behavior.

#### Scenario: PEAD live can request v2 market data explicitly
- **WHEN** PEAD live flow calls the data layer with `profile="v2"`
- **THEN** the request authenticates using V2 profile credentials

#### Scenario: Default data profile remains v1
- **WHEN** data fetches are called without explicit profile override
- **THEN** data layer authentication uses profile `v1`
````

## File: openspec/changes/archive/2026-05-05-account-separation-v1-v2/.openspec.yaml
````yaml
schema: spec-driven
created: 2026-05-05
````

## File: openspec/changes/archive/2026-05-05-account-separation-v1-v2/design.md
````markdown
## Context

The repository currently initializes Alpaca trading and market-data clients from one shared credential pair. This was sufficient when all strategies used one paper account, but the operating model now requires hard separation: momentum weekly live trading runs on V1, while PEAD live trading runs on V2.

The account split must be explicit in code to avoid accidental cross-account order placement. At the same time, existing backtests should remain simple and continue to use V1 credentials by default for data fetches.

## Goals / Non-Goals

**Goals:**
- Introduce a profile-aware credential model for Alpaca trading and data clients.
- Make live strategy account routing explicit and deterministic:
  - Momentum live -> v1
  - PEAD live -> v2
- Normalize V2 variable naming to `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY`.
- Preserve backward usability for backtests by defaulting data-only fetches to profile v1.
- Provide precise startup failures when required profile credentials are missing.

**Non-Goals:**
- No strategy logic changes for signal generation, ranking, or PEAD entry/exit rules.
- No migration to live-money trading accounts.
- No change to portfolio sizing formulas or transaction-cost assumptions.

## Decisions

### Decision: Introduce profile-based credential resolution
Use named profiles (`v1`, `v2`) rather than one global credential pair. Both trading and data client builders resolve keys by profile.

Rationale:
- Prevents accidental account mixing.
- Keeps flow ownership obvious and testable.
- Supports future profile expansion without redesign.

Alternatives considered:
- Process-level environment variable swapping before each script run. Rejected due to fragility and poor testability.
- Hardcoded strategy-specific keys. Rejected for security and maintainability reasons.

### Decision: Keep data-layer default profile as v1
Data fetching APIs default to profile `v1` unless caller explicitly sets another profile.

Rationale:
- Matches current backtest expectation and user preference.
- Minimizes call-site churn for non-live workflows.

Alternatives considered:
- Require explicit profile at every call site. Rejected due to unnecessary verbosity and migration burden.

### Decision: Enforce live routing at strategy entrypoints
Live momentum constructors/entrypoints pass profile `v1`; PEAD live constructors/entrypoints pass profile `v2`.

Rationale:
- Puts account selection where execution intent is defined.
- Prevents accidental fallback to wrong profile.

Alternatives considered:
- Select profile only in shared base classes by runtime mode. Rejected because mode alone cannot infer strategy ownership.

### Decision: Normalize V2 env names to API_KEY_ID format
Adopt `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY` for consistency with V1 naming and existing Alpaca naming style.

Rationale:
- Reduces confusion and avoids conditional naming logic.

Alternatives considered:
- Keep `V2_APCA_API_KEY` while introducing alias handling. Rejected to avoid long-term ambiguity.

## Risks / Trade-offs

- [Risk] Profile defaults could hide missing explicit routing in new live flows.
  Mitigation: Require explicit profile in live trader constructors and add tests asserting v1/v2 routing.

- [Risk] Environment migration mistakes (old V2 variable name still present).
  Mitigation: Add clear startup validation and error text naming the exact missing variables.

- [Risk] PEAD live and PEAD training/fallback data fetches may need different profiles over time.
  Mitigation: Keep data APIs profile-overridable so call sites can opt into v2 explicitly where needed.

## Migration Plan

1. Add profile-aware credential resolvers for trading and data clients.
2. Update live strategy constructors and script entrypoints to pass explicit profiles.
3. Update environment documentation and examples to use `V2_APCA_API_KEY_ID`.
4. Add/adjust tests for default-v1 data behavior and live routing behavior.
5. Deploy with both V1 and V2 credentials present and verify account-specific order placement in paper dashboards.

Rollback:
- Revert to prior shared-credential behavior by removing profile arguments and restoring single-variable resolution.
- Keep previous .env key names only if rollback requires temporary compatibility.

## Open Questions

- Should PEAD classifier fallback training in live mode continue to use default v1 data or explicitly use v2 for consistency with PEAD live execution?
- Should we keep temporary compatibility aliases for the legacy `V2_APCA_API_KEY` name during one transition release?
````

## File: openspec/changes/archive/2026-05-05-account-separation-v1-v2/proposal.md
````markdown
## Why

The project now runs two distinct paper accounts: V1 for momentum and V2 for PEAD. Today, live trading and data clients still rely on one shared credential pair, which risks sending orders to the wrong account and makes strategy isolation fragile.

## What Changes

- Introduce profile-aware Alpaca credential resolution for both trading and data clients.
- Enforce strategy-to-profile mapping in live flows:
  - Momentum weekly live rebalance uses profile v1.
  - PEAD live cronjob uses profile v2.
- Normalize V2 environment variable naming to `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY`.
- Keep backtests and general data-only fetches on default profile v1 unless explicitly overridden.
- Add validation and error messages that clearly identify missing profile-specific credentials.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `data-layer`: Add profile-aware data client authentication with default v1 behavior for backtests and data-only fetches.
- `live-trader`: Add profile-aware trading client authentication and require momentum live flow to use v1 credentials.
- `pead-live-trader`: Require PEAD live flow to use v2 credentials and preserve existing PEAD execution behavior.

## Impact

- Affected code:
  - Credential loading and client creation in core live trading base and data layer.
  - Live entrypoints and strategy constructors for momentum and PEAD.
  - Environment configuration documentation and startup validation.
  - Tests covering credential resolution and live profile routing.
- External systems:
  - Alpaca paper accounts for V1 and V2.
- Operational impact:
  - Reduces cross-strategy account contamination risk and makes account ownership explicit by flow.
````

## File: openspec/changes/archive/2026-05-05-account-separation-v1-v2/tasks.md
````markdown
## 1. Credential Profile Foundation

- [x] 1.1 Add a shared credential-resolution utility that maps profile `v1` and `v2` to profile-prefixed environment variables and raises clear errors on missing keys.
- [x] 1.2 Normalize environment handling to use `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY` for V2.
- [x] 1.3 Add unit tests for profile resolution success and missing-variable failure paths.

## 2. Data Layer Profile Routing

- [x] 2.1 Update data client construction to accept a profile parameter and default to `v1` when omitted.
- [x] 2.2 Extend `fetch_bars()` and related internal helpers to pass profile through to authentication.
- [x] 2.3 Add tests verifying default `v1` data fetch behavior and explicit `v2` profile behavior.

## 3. Live Trader Profile Routing

- [x] 3.1 Update the live trader base class to accept a required profile for live strategy initialization and use profile-specific trading credentials.
- [x] 3.2 Update `LiveMomentumTrader` and momentum live entrypoints to pass profile `v1` explicitly.
- [x] 3.3 Update `PEADLiveTrader` and PEAD live entrypoints to pass profile `v2` explicitly.
- [x] 3.4 Add tests asserting momentum routes to v1 and PEAD routes to v2, including missing-credential fail-fast behavior.

## 4. Backtest Compatibility and Call-Site Audit

- [x] 4.1 Verify backtest and data-only call sites continue to use implicit default `v1` profile without behavior regression.
- [x] 4.2 Audit PEAD live data-fetch call sites and apply explicit `v2` only where intended, leaving non-live training/backtest flows on default `v1`.
- [x] 4.3 Confirm no remaining live path depends on legacy shared `APCA_API_KEY_ID` variables.

## 5. Documentation and Operational Readiness

- [x] 5.1 Update `.env` examples and README instructions to document V1/V2 profile variables and account ownership by strategy.
- [x] 5.2 Add a migration note for renaming V2 key variable from `V2_APCA_API_KEY` to `V2_APCA_API_KEY_ID`.
- [x] 5.3 Run targeted tests and one dry-run startup check for both live entrypoints to validate profile wiring before deployment.
````

## File: openspec/specs/backtest-engine/spec.md
````markdown
## ADDED Requirements

### Requirement: Event-driven iteration over time bars
The backtest engine SHALL iterate over each time bar in chronological order, evaluating strategy signals and simulating order execution at each bar.

#### Scenario: Bar-by-bar event loop
- **WHEN** `run_backtest()` is called
- **THEN** the engine processes each bar from index `lookback` to `len(data)-1` in order, calling `on_bar(bar)` exactly once per bar

### Requirement: Simulated order execution with transaction costs
The engine SHALL simulate buy and sell orders using the closing price at the signal bar, applying configurable fixed transaction cost (`ftc`) and proportional transaction cost (`ptc`).

#### Scenario: Buy order reduces cash balance
- **WHEN** a buy order is placed for N units at price P with ptc=0.001 and ftc=0
- **THEN** cash decreases by `N * P * (1 + ptc) + ftc`

#### Scenario: Sell order increases cash balance
- **WHEN** a sell order is placed for N units at price P with ptc=0.001 and ftc=0
- **THEN** cash increases by `N * P * (1 - ptc) - ftc`

### Requirement: Multi-symbol portfolio state tracking
The engine SHALL maintain portfolio state across multiple symbols: cash balance, units held per symbol, and current position per symbol.

#### Scenario: Portfolio state initialized correctly
- **WHEN** a backtest is instantiated with `initial_amount=10000`
- **THEN** cash equals 10000, units_held is an empty dict, and all positions are neutral (0)

#### Scenario: Portfolio state updated after trade
- **WHEN** a buy order is executed for symbol S
- **THEN** `units_held[S]` reflects the purchased units and cash reflects the deducted amount

### Requirement: Equity curve recorded at each rebalance
The engine SHALL record total portfolio value (cash + mark-to-market holdings) at each rebalance event, producing an equity curve as a pandas Series indexed by date.

#### Scenario: Equity curve length matches rebalance count
- **WHEN** backtest runs over a period with W weekly rebalances
- **THEN** the equity curve has exactly W+1 entries (including initial value)

### Requirement: Final close-out and summary
The engine SHALL close all open positions at the last bar and print a summary: final balance, net performance (%), number of trades, and call `calculate_risk_metrics()`.

#### Scenario: Close-out at end of backtest
- **WHEN** the event loop reaches the final bar
- **THEN** all positions are liquidated at the last closing price and the final cash balance reflects all proceeds
````

## File: openspec/specs/earnings-calendar/spec.md
````markdown
## ADDED Requirements

### Requirement: Fetch earnings event dates for a symbol via yfinance
The earnings calendar module SHALL fetch historical earnings dates for a given symbol using `yfinance.Ticker(symbol).get_earnings_dates(limit)`, returning a structured DataFrame with columns: `earnings_date` (date), `release_time` (`AMC` or `BMO`), and `symbol`.

#### Scenario: Successful fetch for GOOGL
- **WHEN** `fetch_earnings_events("GOOGL", start="2018-01-01")` is called
- **THEN** the function returns a DataFrame with at least one row per quarterly earnings event since 2018, each with a non-null `earnings_date` and `release_time` value

#### Scenario: Events before start date are excluded
- **WHEN** `fetch_earnings_events("GOOGL", start="2022-01-01")` is called
- **THEN** no events with `earnings_date` before 2022-01-01 appear in the result

### Requirement: Classify each event as AMC or BMO
The module SHALL classify each earnings event as `AMC` (after market close, release time after 16:00 ET) or `BMO` (before market open, release time before 09:30 ET) based on the yfinance timestamp field. Events with ambiguous or null timestamps SHALL be excluded and logged.

#### Scenario: After-close event classified as AMC
- **WHEN** yfinance reports a release time of 17:00 ET for an earnings event
- **THEN** the event is tagged `release_time = "AMC"`

#### Scenario: Pre-open event classified as BMO
- **WHEN** yfinance reports a release time of 07:00 ET for an earnings event
- **THEN** the event is tagged `release_time = "BMO"`

#### Scenario: Ambiguous timestamp excluded
- **WHEN** yfinance returns a null or mid-day timestamp for an event
- **THEN** the event is excluded from the result and a warning is logged identifying the event date and symbol

### Requirement: Filter to AMC events only for Phase 1
The module SHALL support a `timing` parameter that, when set to `"AMC"`, returns only after-close events. This is the required filter for Phase 1 of the strategy.

#### Scenario: AMC filter applied
- **WHEN** `fetch_earnings_events("GOOGL", timing="AMC")` is called
- **THEN** the returned DataFrame contains only rows where `release_time == "AMC"`

#### Scenario: No filter returns all classified events
- **WHEN** `fetch_earnings_events("GOOGL", timing=None)` is called
- **THEN** the returned DataFrame contains both AMC and BMO events (ambiguous excluded)

### Requirement: Return T-1 trading date for each event
The module SHALL compute and include a `t_minus_1` column representing the last trading day before `earnings_date`, using the NYSE calendar. This is the entry date for the strategy.

#### Scenario: T-1 is the trading day before earnings
- **WHEN** earnings date is a Wednesday
- **THEN** `t_minus_1` is the prior Tuesday (assuming no holiday)

#### Scenario: T-1 skips non-trading days
- **WHEN** earnings date is a Monday
- **THEN** `t_minus_1` is the prior Friday

### Requirement: Raise on empty result set
The module SHALL raise a descriptive `ValueError` if the fetched and filtered event set is empty after all exclusions.

#### Scenario: Empty result after filtering raises error
- **WHEN** `fetch_earnings_events("GOOGL", start="2030-01-01")` is called and no future events exist
- **THEN** a `ValueError` is raised with a message identifying the symbol and filter parameters
````

## File: openspec/specs/ml-classifier/spec.md
````markdown
## ADDED Requirements

### Requirement: Walk-forward event-level cross-validation
The ML classifier module SHALL train and evaluate using a strictly chronological, expanding-window walk-forward protocol. Events MUST be sorted by `earnings_date` before splitting. Random shuffling is prohibited.

#### Scenario: Walk-forward produces one prediction per test event
- **WHEN** `walk_forward_predict(features_df, min_train=20)` is called
- **THEN** the function returns a Series of predicted probabilities indexed by `earnings_date`, with one prediction per event from position `min_train` onward

#### Scenario: No future data leaks into training
- **WHEN** predicting the probability for event at index N
- **THEN** only events at indices 0 through N-1 are used for training

#### Scenario: Insufficient training data skips prediction
- **WHEN** fewer than `min_train` events precede the current event
- **THEN** no prediction is made for that event and it is excluded from evaluation

### Requirement: Logistic regression as Phase 1 baseline model
The module SHALL use `sklearn.linear_model.LogisticRegression` with standardized features (`sklearn.preprocessing.StandardScaler` fit on training fold only) as the primary classifier. Scaler MUST be fit exclusively on training data and applied to test data without re-fitting.

#### Scenario: Scaler fit on training fold only
- **WHEN** walk-forward prediction is run for fold N
- **THEN** the StandardScaler is fit on events 0..N-1 and applied (not re-fit) to event N

#### Scenario: Model coefficients logged per fold
- **WHEN** verbose mode is enabled
- **THEN** feature names and their logistic regression coefficients are logged after each fold fit

### Requirement: Prediction output includes probability and binary label
The module SHALL return both predicted probability (`prob_positive`) and thresholded binary label (`pred_label`) for each test event. Default threshold is 0.5; configurable via parameter.

#### Scenario: Probability output is in [0, 1]
- **WHEN** `walk_forward_predict` returns predictions
- **THEN** all `prob_positive` values are between 0.0 and 1.0 inclusive

#### Scenario: Custom threshold applied
- **WHEN** `threshold=0.60` is passed
- **THEN** `pred_label = 1` only for events where `prob_positive >= 0.60`

### Requirement: Evaluation report with hit rate, expectancy, and calibration
The module SHALL compute and return an evaluation report covering:

- `hit_rate`: Fraction of predicted positive events where `y == 1`.
- `baseline_rate`: Unconditional fraction of positive-gap events in the full sample.
- `avg_gap_return`: Mean `gap_return` across all predicted-positive events.
- `avg_gap_return_negative`: Mean `gap_return` across predicted-negative events (for comparison).
- `n_trades`: Count of events where `pred_label == 1`.
- `n_total`: Total events evaluated.

#### Scenario: Hit rate exceeds baseline rate to indicate edge
- **WHEN** the classifier has predictive power
- **THEN** `hit_rate > baseline_rate`

#### Scenario: Evaluation report prints to log
- **WHEN** `print_eval_report(report)` is called
- **THEN** all metrics are printed with labels to stdout

### Requirement: Feature importance logging for logistic regression
The module SHALL log sorted feature coefficients (by absolute magnitude) after fitting on the full training set, to validate whether the pre-earnings flow hypothesis is reflected in the model weights.

#### Scenario: Top features logged
- **WHEN** the final fold is fit
- **THEN** feature names ranked by absolute coefficient magnitude are logged in descending order
````

## File: openspec/specs/pead-backtest/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Event-driven backtest simulating overnight entry at T-1 close
The PEAD backtest SHALL support a configurable entry offset `PEAD_ENTRY_OFFSET_DAYS` and SHALL enter a long position at `open(T-E)` for each event where `pred_label == 1`, where E is the configured entry offset. The backtest SHALL exit at either T+1 open or T+1 close according to configured exit mode. Each trade is independent; no portfolio is held between events.

#### Scenario: Trade entered at T-3 open
- **WHEN** `pred_label == 1` and `PEAD_ENTRY_OFFSET_DAYS=3`
- **THEN** a long entry is recorded at `open(T-3)` with configured position size as a fraction of capital

#### Scenario: Trade exited at T+1 open
- **WHEN** a trade is open and the configured exit mode is `t_plus_1_open`
- **THEN** the position is closed at `open(T+1)` and PnL is recorded from `open(T-E)` to `open(T+1)`

#### Scenario: Trade exited at T+1 close
- **WHEN** a trade is open and the configured exit mode is `t_plus_1_close`
- **THEN** the position is closed at `close(T+1)` and PnL is recorded from `open(T-E)` to `close(T+1)`

#### Scenario: No trade on predicted-negative event
- **WHEN** `pred_label == 0` for an event
- **THEN** no entry or exit is simulated and capital is unchanged

### Requirement: Invocable via `python run.py --mode pead-backtest`
The main entry point SHALL support `--mode pead-backtest` as the PEAD timing-variant runner that executes the full pipeline: fetch earnings events -> fetch bars -> build features using bars available by `T-(E+1)` where E is `PEAD_ENTRY_OFFSET_DAYS` -> walk-forward predict -> backtest the configured entry/exit horizon -> print summary.

#### Scenario: pead-backtest mode runs end to end
- **WHEN** `python run.py --mode pead-backtest` is invoked
- **THEN** the full configured timing-variant pipeline completes without error and prints a PEAD risk summary

#### Scenario: Existing non-PEAD modes unaffected
- **WHEN** `python run.py --mode backtest` or `--mode live` is invoked
- **THEN** behavior is identical to before this change
````

## File: openspec/specs/pead-entry-timing-config/spec.md
````markdown
## ADDED Requirements

### Requirement: Configurable PEAD entry offset for backtest and live execution
The system SHALL expose a configuration parameter `PEAD_ENTRY_OFFSET_DAYS` representing the entry day offset in trading days before earnings day T. The value MUST be a positive integer and SHALL be interpreted consistently by backtest and live code paths.

#### Scenario: Valid offset accepted
- **WHEN** `PEAD_ENTRY_OFFSET_DAYS=3` is configured
- **THEN** both backtest and live logic treat entry day as T-3

#### Scenario: Invalid offset rejected
- **WHEN** `PEAD_ENTRY_OFFSET_DAYS` is set to 0, a negative number, or a non-integer value
- **THEN** the system raises a configuration validation error before any trading or backtest execution begins

### Requirement: Derived feature anchor from configured entry offset
For an entry offset E, the feature window anchor SHALL be T-(E+1), and the 7-day feature window SHALL cover the 7 trading days ending at that anchor date (inclusive).

#### Scenario: T-3 open entry derives T-4 anchor
- **WHEN** `PEAD_ENTRY_OFFSET_DAYS=3`
- **THEN** feature anchor is T-4 and the feature window is T-10 through T-4

#### Scenario: T-5 open entry derives T-6 anchor
- **WHEN** `PEAD_ENTRY_OFFSET_DAYS=5`
- **THEN** feature anchor is T-6 and the feature window is the 7 trading days ending at T-6

### Requirement: Runtime visibility of effective timing configuration
The system SHALL log the effective entry offset, derived feature anchor offset, and resolved entry/exit dates for each run.

#### Scenario: Effective timing is logged
- **WHEN** a PEAD backtest or live run starts
- **THEN** logs include `entry_offset_days`, `feature_anchor_offset_days`, and configured exit mode
````

## File: openspec/specs/pead-state-manager/spec.md
````markdown
## ADDED Requirements

### Requirement: State file structure and initialization

The state file (`output/pead_live_state.json`) SHALL be a JSON document tracking current open positions per symbol. Structure: `{symbol: {earnings_date, entry_date, entry_price, entry_qty, created_at}}`. The state file SHALL be initialized as empty on first run or if no positions are open.

#### Scenario: Load state file on startup
- **WHEN** cronjob starts and state file exists
- **THEN** system SHALL read and parse the JSON file; if parsing fails, log error and treat as empty state

#### Scenario: Initialize state file if missing
- **WHEN** state file does not exist
- **THEN** system SHALL create an empty state file `{}`

#### Scenario: State structure for single open position
- **WHEN** one symbol has an open position for current earnings event
- **THEN** state file SHALL contain: `{"NXPI": {"earnings_date": "2026-04-30", "entry_date": "2026-04-27", "entry_price": 125.50, "entry_qty": 80, "created_at": "2026-04-27T16:00:00Z"}}`

#### Scenario: State structure for multiple open positions
- **WHEN** multiple symbols have open positions simultaneously
- **THEN** state file SHALL contain entries for each symbol independently: `{"NXPI": {...}, "AMD": {...}, "AVGO": {...}}`

### Requirement: Record new position state on entry

When an entry order executes, the system SHALL write a new state entry with entry details and timestamp.

#### Scenario: Write entry state after buy order
- **WHEN** entry market order executes on T-3
- **THEN** system SHALL append/update state entry: `state[symbol] = {earnings_date, entry_date: today, entry_price: filled_price, entry_qty: filled_qty, created_at: timestamp}`

#### Scenario: Entry state persists until exit
- **WHEN** entry state is recorded and position is held through T+1
- **THEN** state entry SHALL remain in the state file until exit order executes

### Requirement: Idempotency check before entry

Before placing an entry order, the system SHALL check if a position already exists for this symbol and earnings date, and skip if already present.

#### Scenario: Skip entry if already in state
- **WHEN** cronjob runs on T-3 AND symbol already exists in state file with the same earnings_date
- **THEN** system SHALL not place another BUY order; record as "skipped (already entered)"

#### Scenario: Allow entry if earnings event is different
- **WHEN** cronjob runs on T-3 for earnings event E2 AND symbol exists in state but for a previous earnings event E1
- **THEN** this would indicate a failed exit (shouldn't happen); log warning and do not enter (state cleanup required manually)

### Requirement: Delete state entry on position exit

After a position exits, the system SHALL delete the corresponding state entry, resetting to clean slate for the next earnings event.

#### Scenario: Delete entry on successful exit
- **WHEN** exit market order executes on T+1
- **THEN** system SHALL delete `state[symbol]`, leaving state file clean for next earnings event

#### Scenario: Clean state for future events
- **WHEN** position is exited and state entry is deleted
- **THEN** next earnings event for the same symbol can re-enter without interference

### Requirement: Auto-cleanup of stale state entries

The system SHALL automatically remove state entries older than 30 days, in case a position was never exited (e.g., due to manual intervention or error).

#### Scenario: Cleanup entries older than 30 days
- **WHEN** cronjob runs and detects a state entry with created_at timestamp > 30 days ago
- **THEN** system SHALL delete that entry, log warning: "Cleaned up stale NXPI position from 2026-03-25"

#### Scenario: Do not cleanup recent entries
- **WHEN** state entry has created_at < 30 days ago
- **THEN** entry SHALL remain in the state file

### Requirement: Atomic read-modify-write for state file

State file operations (read, check, update, write) SHALL be performed atomically to prevent corruption or lost updates if multiple cronjobs run simultaneously.

#### Scenario: Atomic entry write
- **WHEN** placing an entry order
- **THEN** system SHALL: load state file, check if symbol exists, add/update entry, write atomically (not partial writes)

#### Scenario: Atomic entry delete
- **WHEN** exiting a position
- **THEN** system SHALL: load state file, delete symbol entry, write atomically

#### Scenario: Handle concurrent writes
- **WHEN** two cronjob instances try to update state simultaneously
- **THEN** system SHALL use file locking or atomic operations to ensure one write completes before the other starts (no corruption)

### Requirement: Human-readable state file format

The state file format SHALL be plain JSON, suitable for manual inspection and debugging.

#### Scenario: State file is readable without special tools
- **WHEN** cronjob writes state file
- **THEN** a human can open the file in a text editor and understand the current position(s)

#### Scenario: Pretty-printed JSON for clarity
- **WHEN** state file is written
- **THEN** JSON SHALL be formatted with indentation (not minified) for readability
````

## File: openspec/specs/pead-trade-logger/spec.md
````markdown
## ADDED Requirements

### Requirement: Trade log file structure and initialization

The trade log (`output/pead_live_trades.csv`) SHALL be an append-only CSV file with columns: symbol, earnings_date, entry_date, exit_date, entry_price, exit_price, qty, pnl, pnl_pct, timestamp. The file SHALL be initialized with a header row on first write if it does not exist.

#### Scenario: Initialize trade log with header
- **WHEN** trade log does not exist and first trade is recorded
- **THEN** system SHALL create the file with header row: `symbol,earnings_date,entry_date,exit_date,entry_price,exit_price,qty,pnl,pnl_pct,timestamp`

#### Scenario: Load existing trade log
- **WHEN** trade log already exists
- **THEN** system SHALL append new trades to the existing file, preserving all previous records

#### Scenario: Trade log structure for single trade
- **WHEN** one trade completes (entry + exit)
- **THEN** trade log SHALL contain one row with all fields populated: `NXPI,2026-04-30,2026-04-27,2026-04-28,125.50,128.60,80,240.00,0.0238,2026-04-28T16:00:00Z`

### Requirement: Record trade entry event

When an entry order executes, the system SHALL begin recording trade details (capture symbol, earnings_date, entry_date, entry_price, entry_qty).

#### Scenario: Capture entry details on order execution
- **WHEN** entry market order executes on T-3
- **THEN** system SHALL store: symbol, earnings_date, entry_date=today, entry_price=filled_price, qty=filled_qty, entry_timestamp

#### Scenario: Hold entry details until exit
- **WHEN** entry is recorded and position held through T+1
- **THEN** entry details SHALL be retained in memory or temporary state, waiting for exit to complete the trade record

### Requirement: Record trade exit and compute PnL

When an exit order executes on T+1+, the system SHALL complete the trade record by adding exit details and computed PnL, then append one row to the trade log CSV.

#### Scenario: Capture exit details on order execution
- **WHEN** exit market order executes on T+1
- **THEN** system SHALL capture: exit_date=today, exit_price=filled_price, exit_timestamp

#### Scenario: Compute net PnL with transaction costs
- **WHEN** exit order executes
- **THEN** system SHALL compute:
  - gross_pnl_pct = (exit_price - entry_price) / entry_price
  - net_pnl_pct = gross_pnl_pct - 0.002 (entry cost 0.1% + exit cost 0.1%)
  - pnl_dollars = net_pnl_pct * entry_price * qty

#### Scenario: Append completed trade to log
- **WHEN** all trade details and PnL are computed
- **THEN** system SHALL append one row to the CSV file: `symbol,earnings_date,entry_date,exit_date,entry_price,exit_price,qty,pnl,pnl_pct,timestamp`

#### Scenario: Trade log records multiple trades chronologically
- **WHEN** multiple trades complete over time
- **THEN** trade log SHALL contain multiple rows (one per trade), appended in chronological order of exit timestamp

### Requirement: Append-only semantics for trade log

The trade log SHALL never be modified or overwritten once written. All operations are append-only to maintain audit trail integrity.

#### Scenario: Append new trade without modifying existing records
- **WHEN** a new trade completes and is logged
- **THEN** system SHALL append a new row; no existing rows are modified or deleted

#### Scenario: Trade log grows monotonically
- **WHEN** multiple trades are recorded over weeks/months
- **THEN** trade log file size increases monotonically; no truncation or reordering

### Requirement: Human-readable trade log format

Trade log format SHALL be plain CSV, easily imported into analysis tools (pandas, Excel, R) for performance analysis and audit.

#### Scenario: Trade log is queryable via pandas
- **WHEN** analyst reads the trade log
- **THEN** they can load it in pandas: `pd.read_csv('output/pead_live_trades.csv')` and analyze by symbol, earnings_date, PnL, hit rate, etc.

#### Scenario: Trade log is readable in Excel
- **WHEN** trade log is opened in Excel or Google Sheets
- **THEN** columns are labeled clearly and values are formatted for easy interpretation

### Requirement: Timestamp precision for audit trail

Each trade record SHALL include a precise timestamp (ISO 8601 format with seconds precision, UTC) to enable accurate sequencing and audit of events.

#### Scenario: Timestamp on trade exit
- **WHEN** exit order executes and trade is logged
- **THEN** timestamp column SHALL contain the exact exit order execution time in ISO 8601 format (e.g., `2026-04-28T16:00:30Z`)

#### Scenario: Timestamp enables event sequencing
- **WHEN** multiple trades are logged on the same day
- **THEN** their timestamps enable precise ordering of events

### Requirement: Record skipped entry events (for analysis)

When an entry is skipped due to negative classifier prediction, the system MAY optionally log a "skipped" record for analysis purposes (to compute true false-negative rate).

#### Scenario: Optional logging of skipped entries
- **WHEN** classifier predicts negative (pred_label == 0) on T-3
- **THEN** system MAY append a record to the trade log with fields: symbol, earnings_date, entry_date, exit_date=NULL, entry_price=NULL, exit_price=NULL, qty=0, pnl=0, pnl_pct=0, timestamp=T-3_time, plus a note "skipped_pred=0"
````

## File: openspec/specs/pre-earnings-features/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Build a feature vector per earnings event from T-7 to T-1 daily bars
The feature module SHALL produce a single feature vector per earnings event by computing summary statistics over a 7-trading-day window ending at a configurable feature anchor derived from `PEAD_ENTRY_OFFSET_DAYS`. For entry offset E, the feature anchor MUST be T-(E+1), and all features MUST use only data available by the anchor close with no forward-looking fields relative to the entry decision time.

#### Scenario: Feature vector produced for each event
- **WHEN** `build_features(events_df, bars_dict, entry_offset_days=3)` is called with a valid events DataFrame and OHLCV bar data
- **THEN** the function returns a DataFrame with one row per event and one column per feature, indexed by `earnings_date`

#### Scenario: No forward-looking data used
- **WHEN** features are computed for an event with earnings date T and entry offset E
- **THEN** no bar after T-(E+1) appears in the feature computation window

### Requirement: Price drift features (T-7 to T-1)
The module SHALL compute the following price drift features over the 7-day pre-earnings window ending at the derived anchor date T-(E+1):

- `drift_7d`: Cumulative simple return from the first close in the window to the anchor close.
- `drift_slope`: Ordinary-least-squares slope of daily closes over the window, normalized by the mean close.
- `up_day_count`: Number of days where `close > close.shift(1)` in the window.
- `down_day_count`: Number of days where `close < close.shift(1)` in the window.

#### Scenario: Drift computed correctly
- **WHEN** close prices over the 7-day window ending at T-(E+1) increase monotonically
- **THEN** `drift_7d` is positive, `up_day_count` equals 6, and `down_day_count` equals 0

#### Scenario: Slope captures convexity
- **WHEN** closes accelerate upward over the window ending at T-(E+1)
- **THEN** `drift_slope` is positive and larger than for a linear price path with the same total drift

### Requirement: Volume pressure features (T-7 to T-1)
The module SHALL compute:

- `rel_volume_mean`: Mean daily volume over the window ending at T-(E+1) divided by the symbol's 20-day baseline volume computed from the 20 trading days ending immediately before the feature window begins.
- `down_volume_ratio`: Sum of volume on down days divided by total window volume.

#### Scenario: Volume baseline uses non-overlapping window
- **WHEN** baseline volume is computed for an event
- **THEN** no bar from the 7-day feature window ending at T-(E+1) is included in the 20-day baseline

#### Scenario: Down-volume ratio reflects selling pressure
- **WHEN** all volume in the window occurs on down days
- **THEN** `down_volume_ratio` equals 1.0

### Requirement: Volatility regime features (T-7 to T-1)
The module SHALL compute:

- `atr_ratio`: Mean of `(high - low)` over the window ending at T-(E+1) divided by the mean of `(high - low)` for the 20-day baseline period immediately preceding the feature window.
- `gap_count`: Number of overnight gaps (`abs(open - prev_close) / prev_close > 0.005`) within the window.

#### Scenario: ATR expansion detected
- **WHEN** intraday ranges expand significantly in the 7-day window ending at T-(E+1) relative to the prior 20-day baseline
- **THEN** `atr_ratio` is greater than 1.0

### Requirement: Relative-to-market features (T-7 to T-1)
The module SHALL compute:

- `rel_drift_vs_qqq`: `drift_7d` (symbol) minus the QQQ cumulative return over the same 7-day window ending at T-(E+1), using QQQ bars passed in `bars_dict`.

#### Scenario: Outperformance detected
- **WHEN** the symbol rises 5% and QQQ rises 2% over the same window ending at T-(E+1)
- **THEN** `rel_drift_vs_qqq` equals approximately 0.03

### Requirement: Target label computation
The module SHALL compute the binary target label alongside features:

- `y`: 1 if `open(T) / close(T-1) - 1 > 0.0`, else 0.
- `gap_return`: Continuous gap return `open(T) / close(T-1) - 1` (stored for evaluation, not used as training label).

#### Scenario: Positive gap labeled correctly
- **WHEN** T open is higher than T-1 close
- **THEN** `y = 1` and `gap_return > 0`

#### Scenario: No-gap or negative gap labeled correctly
- **WHEN** T open equals or is below T-1 close
- **THEN** `y = 0` and `gap_return <= 0`

### Requirement: Drop events with insufficient bar history
The module SHALL exclude any event where fewer than 7 valid bars exist in the feature window ending at T-(E+1), and log a warning per dropped event.

#### Scenario: Event dropped on insufficient history
- **WHEN** only 4 bars are available in the feature window ending at T-(E+1) for an event
- **THEN** that event is excluded from the output and a warning is logged
````

## File: openspec/specs/risk-analytics/spec.md
````markdown
## ADDED Requirements

### Requirement: Compute annualized Sharpe ratio from equity curve
The risk module SHALL compute the annualized Sharpe ratio from a weekly equity curve using the formula: `mean(weekly_returns) / std(weekly_returns) * sqrt(52)`, assuming risk-free rate of 0.

#### Scenario: Sharpe ratio computed correctly
- **WHEN** `sharpe_ratio(equity_curve, periods_per_year=52)` is called with a pandas Series of weekly portfolio values
- **THEN** it returns a float representing the annualized Sharpe ratio

#### Scenario: Flat equity curve returns zero Sharpe
- **WHEN** all equity values are equal (zero volatility)
- **THEN** the function returns 0.0 (not NaN or error)

### Requirement: Compute maximum drawdown
The risk module SHALL compute maximum drawdown as the largest peak-to-trough decline in the equity curve, expressed as a percentage: `(trough - peak) / peak * 100`.

#### Scenario: Maximum drawdown computed
- **WHEN** `max_drawdown(equity_curve)` is called
- **THEN** it returns a negative float representing the worst percentage decline from any peak

#### Scenario: Always-rising equity has zero drawdown
- **WHEN** the equity curve is monotonically increasing
- **THEN** `max_drawdown` returns 0.0

### Requirement: Compute Calmar ratio
The risk module SHALL compute the Calmar ratio as `annualized_return / abs(max_drawdown)`, where annualized return is `(final_value / initial_value) ^ (periods_per_year / n_periods) - 1`.

#### Scenario: Calmar ratio computed
- **WHEN** `calmar_ratio(equity_curve, periods_per_year=52)` is called
- **THEN** it returns a positive float when the strategy is profitable

### Requirement: Print risk summary
The risk module SHALL provide a `print_summary(equity_curve)` function that prints Sharpe ratio, maximum drawdown, Calmar ratio, total return (%), and number of periods to stdout.

#### Scenario: Summary printed after backtest
- **WHEN** `print_summary(equity_curve)` is called
- **THEN** all four metrics are printed with labels and rounded to 2 decimal places

### Requirement: Plot equity curve
The risk module SHALL provide a `plot_equity_curve(equity_curve, title)` function that renders a matplotlib line chart of portfolio value over time.

#### Scenario: Plot generated without error
- **WHEN** `plot_equity_curve(equity_curve, title="M7 Momentum")` is called
- **THEN** a matplotlib figure is created and displayed (or saved if a path is provided)
````

## File: openspec/config.yaml
````yaml
schema: spec-driven

# Project context (optional)
# This is shown to AI when creating artifacts.
# Add your tech stack, conventions, style guides, domain knowledge, etc.
# Example:
#   context: |
#     Tech stack: TypeScript, React, Node.js
#     We use conventional commits
#     Domain: e-commerce platform

# Per-artifact rules (optional)
# Add custom rules for specific artifacts.
# Example:
#   rules:
#     proposal:
#       - Keep proposals under 500 words
#       - Always include a "Non-goals" section
#     tasks:
#       - Break tasks into chunks of max 2 hours
````

## File: risk/__init__.py
````python

````

## File: strategies/__init__.py
````python

````

## File: strategies/pead_backtest.py
````python
"""Event-driven backtest for PEAD strategy.

Simulates entry at open(T-E) and exit at the configured T+1 horizon based on
classifier predictions, with transaction cost modeling.
"""
⋮----
log = logging.getLogger(__name__)
⋮----
def _to_naive_midnight(series_or_index: pd.Series | pd.Index) -> pd.Series | pd.DatetimeIndex
⋮----
"""Normalize datetime values to tz-naive midnight for key-safe joins."""
values = pd.to_datetime(series_or_index)
⋮----
values = values.dt.tz_localize(None)
⋮----
idx = pd.DatetimeIndex(values)
⋮----
idx = idx.tz_localize(None)
⋮----
"""Return the trading day at a relative offset from anchor, or None if unavailable."""
⋮----
anchor_idx = trading_dates.get_loc(anchor)
shifted_idx = anchor_idx + offset
⋮----
class PEADBacktest
⋮----
"""Event-driven backtest for Post-Earnings Announcements Drift strategy.

    Simulates offset-driven positions: buy at open(T-E), sell at T+1 open/close.
    """
⋮----
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
⋮----
# Ensure datetime indices
# Normalize to date-only so timestamps from different sources (e.g. 16:00
# earnings events vs 00:00 bars) align on calendar day keys.
⋮----
def run(self) -> tuple[pd.Series, pd.DataFrame]
⋮----
"""Run backtest and return equity curve and trades.

        Returns
        -------
        tuple[pd.Series, pd.DataFrame]
            - equity_curve: Series indexed by earnings_date with account value
            - trades_df: DataFrame with per-trade records
        """
bars = self.bars_dict[self.symbol].copy()
⋮----
equity = self.initial_amount
equity_curve_values = [equity]
equity_curve_dates = [pd.Timestamp(self.events_df.iloc[0]["earnings_date"]) - pd.Timedelta(days=1)]
trades = []
evaluated_events = []
⋮----
event_ts = pd.Timestamp(event["earnings_date"])
t_minus_1_ts = pd.Timestamp(event["t_minus_1"])
earnings_date = event_ts.date()
⋮----
# Check if we have a prediction for this event
⋮----
pred = self.predictions_df.loc[event_ts]
⋮----
# Derive entry and feature-anchor dates from the trading calendar, not from
# available bar rows, so missing bars are detected as missing data rather than
# silently changing the intended offsets.
entry_ts = get_entry_trading_date(event_ts, self.entry_offset_days)
⋮----
feature_anchor_ts = get_feature_anchor_trading_date(event_ts, self.entry_offset_days)
⋮----
exit_ts = calculate_offset_trading_date(event_ts, 1)
⋮----
entry_price = float(bars.loc[entry_ts, "open"])
⋮----
exit_field = "open" if self.exit_mode == "t_plus_1_open" else "close"
exit_price = float(bars.loc[exit_ts, exit_field])
⋮----
gross_return = (exit_price - entry_price) / entry_price if entry_price > 0 else 0.0
net_return = gross_return - 2 * self.ptc
⋮----
# No model-gated trade for predicted-negative events.
⋮----
# Calculate position
position_value = equity * self.position_size
⋮----
# PnL
pnl = position_value * net_return
⋮----
# Update equity
⋮----
# Record trade
⋮----
# Add to equity curve
⋮----
# Build equity curve
⋮----
# Build trades DataFrame
⋮----
benchmark_df = pd.DataFrame(evaluated_events)
⋮----
model_df = benchmark_df[benchmark_df["pred_label"] == 1].copy()
model_avg_gross = model_df["gross_return"].mean() if not model_df.empty else 0.0
model_avg_net = model_df["net_return"].mean() if not model_df.empty else 0.0
model_hit_rate = (model_df["gross_return"] > 0).mean() if not model_df.empty else 0.0
always_buy_avg_gross = benchmark_df["gross_return"].mean()
always_buy_avg_net = benchmark_df["net_return"].mean()
always_buy_hit_rate = (benchmark_df["gross_return"] > 0).mean()
⋮----
# Compute risk metrics
# For event-driven PEAD trades, compute Sharpe from actual trade returns only
# (not the equity curve with flats), without annualization.
⋮----
trade_returns = self.trades_df["net_return"].values
sharpe = sharpe_ratio_from_returns(trade_returns, periods_per_year=None)
⋮----
sharpe = 0.0
````

## File: strategies/pead_classifier_live.py
````python
"""PEAD live classifier wrapper.

Uses a frozen trained model for live entry predictions.
Falls back to training on historical data if no saved model exists.
"""
⋮----
log = logging.getLogger(__name__)
⋮----
class PEADClassifierLive
⋮----
"""Live PEAD classifier using frozen trained model."""
FEATURE_COLS = FEATURE_COLS
⋮----
def __init__(self, symbol: str, model_path: str | None = None)
⋮----
"""Initialize classifier.
        
        Parameters
        ----------
        symbol : str
            Symbol whose classifier should be loaded.
        model_path : str | None
            Optional explicit model path override.
        """
⋮----
@staticmethod
    def get_model_path(symbol: str) -> str
⋮----
"""Return the on-disk model path for a symbol-specific classifier."""
⋮----
def load_classifier(self) -> None
⋮----
"""Load pre-trained classifier from pickle file."""
⋮----
saved_data = pickle.load(f)
⋮----
"""Train classifier on historical data (on-demand fallback).
        
        Parameters
        ----------
        symbol : str
            Stock symbol
        start_date : str
            Training period start (YYYY-MM-DD)
        end_date : str
            Training period end (YYYY-MM-DD)
        min_train : int
            Minimum training events
        """
⋮----
# Fetch earnings events
events_df = fetch_earnings_events(
⋮----
# Fetch bars
bars_dict = fetch_bars(
⋮----
# Build features
features_df = build_features(
⋮----
# Train on all historical data
X = features_df[self.FEATURE_COLS].values
y = features_df["y"].values
⋮----
X_scaled = self.scaler.fit_transform(X)
⋮----
# Save model
⋮----
def save_classifier(self) -> None
⋮----
"""Save trained model to pickle file."""
⋮----
def predict_entry(self, features: dict[str, float]) -> tuple[int, float]
⋮----
"""Generate entry prediction (pred_label, prob_positive).
        
        Parameters
        ----------
        features : dict[str, float]
            Feature dict with keys matching FEATURE_COLS
            
        Returns
        -------
        tuple[int, float]
            (pred_label: 0 or 1, prob_positive: probability)
            
        Raises
        ------
        ValueError
            If model is not trained
        """
⋮----
# Extract features in correct order
X = np.array([[features.get(col, 0.0) for col in self.FEATURE_COLS]])
⋮----
# Scale
X_scaled = self.scaler.transform(X)
⋮----
# Predict
⋮----
probs = self.model.predict_proba(X_scaled)
prob_positive = probs[0, 1]
⋮----
prob_positive = float(self.model.predict(X_scaled)[0])
⋮----
pred_label = 1 if prob_positive >= 0.5 else 0
⋮----
def ensure_trained(self) -> None
⋮----
"""Train and save the symbol model if it is missing on disk."""
````

## File: strategies/pead_classifier.py
````python
"""ML classifier for earnings gap predictions using walk-forward cross-validation.

Implements event-level expanding-window walk-forward validation with logistic
regression (Phase 1) or configurable classifiers (Phase 2).
"""
⋮----
log = logging.getLogger(__name__)
⋮----
FEATURE_COLS = [
⋮----
"""Run expanding-window walk-forward prediction.

    Parameters
    ----------
    features_df : pd.DataFrame
        Features DataFrame indexed by earnings_date with columns:
        drift_7d, drift_slope, up_day_count, down_day_count, rel_volume_mean,
        down_volume_ratio, atr_ratio, gap_count, rel_drift_vs_qqq, y, gap_return.
    min_train : int
        Minimum number of training events before making first prediction.
    threshold : float
        Probability threshold for binary prediction (default 0.5).
    model_cls : type or None
        Classifier class (e.g., LogisticRegression). Default: LogisticRegression.
    verbose : bool
        If True, log feature coefficients after each fold fit.

    Returns
    -------
    pd.DataFrame
        Predictions DataFrame with columns:
        - earnings_date: event date (index)
        - prob_positive: predicted probability of positive gap
        - pred_label: thresholded prediction (0 or 1)
        - y: actual target label
        - gap_return: actual gap return

    Notes
    -----
    - Predictions only available from position min_train onward.
    - Earlier events are in-sample training only.
    """
features_df = features_df.sort_index().copy()
⋮----
model_cls = LogisticRegression
⋮----
X = features_df[FEATURE_COLS].values
y = features_df["y"].values
gap_returns = features_df["gap_return"].values
dates = features_df.index
⋮----
predictions = []
⋮----
# Walk-forward loop
⋮----
train_idx = test_idx - 1  # Expanding window: 0..test_idx-1 for training
train_size = train_idx + 1
⋮----
# Ensure we have at least min_train events for training
⋮----
# Split data
⋮----
X_test = X[test_idx : test_idx + 1]
⋮----
# Fit scaler on training data only
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
⋮----
# Train model
model = model_cls(random_state=42, max_iter=1000)
⋮----
# Log coefficients if verbose
⋮----
coefs = model.coef_[0]
abs_coefs = np.abs(coefs)
sorted_idx = np.argsort(-abs_coefs)
⋮----
# Predict
⋮----
probs = model.predict_proba(X_test_scaled)
prob_positive = probs[0, 1]  # Probability of class 1
⋮----
# Fallback for models without predict_proba
prob_positive = float(model.predict(X_test_scaled)[0])
⋮----
pred_label = 1 if prob_positive >= threshold else 0
⋮----
result = pd.DataFrame(predictions)
⋮----
def evaluate(predictions_df: pd.DataFrame) -> dict[str, Any]
⋮----
"""Evaluate classifier predictions.

    Parameters
    ----------
    predictions_df : pd.DataFrame
        Predictions DataFrame with columns: pred_label, y, gap_return.

    Returns
    -------
    dict
        Report with keys:
        - hit_rate: proportion of correct predictions among all events
        - baseline_rate: proportion of positive events in full data
        - n_trades: number of predicted-positive events
        - avg_gap_return: mean gap return for predicted-positive events
        - avg_gap_return_negative: mean gap return for predicted-negative events
        - n_total: total number of events
    """
correct = (predictions_df["pred_label"] == predictions_df["y"]).sum()
hit_rate = correct / len(predictions_df) if len(predictions_df) > 0 else 0.0
baseline_rate = predictions_df["y"].mean()
⋮----
n_trades = (predictions_df["pred_label"] == 1).sum()
n_total = len(predictions_df)
⋮----
avg_gap_return = predictions_df[predictions_df["pred_label"] == 1]["gap_return"].mean()
⋮----
avg_gap_return = 0.0
⋮----
n_negative_pred = (predictions_df["pred_label"] == 0).sum()
⋮----
avg_gap_return_negative = predictions_df[predictions_df["pred_label"] == 0][
⋮----
avg_gap_return_negative = 0.0
⋮----
def print_eval_report(report: dict[str, Any]) -> None
⋮----
"""Print evaluation report to stdout.

    Parameters
    ----------
    report : dict
        Dictionary returned by evaluate().
    """
⋮----
"""Fit a final classifier on the full feature set for later live inference."""
⋮----
X_scaled = scaler.fit_transform(X)
⋮----
def save_trained_classifier(model: Any, scaler: StandardScaler, model_path: str | Path) -> None
⋮----
"""Persist a trained classifier/scaler pair to disk."""
path = Path(model_path)
````

## File: tests/test_alpaca_credentials.py
````python
class ResolveAlpacaCredentialsTests(unittest.TestCase)
⋮----
def test_resolves_v1_credentials(self)
⋮----
def test_resolves_v2_credentials(self)
⋮----
def test_raises_for_unknown_profile(self)
⋮----
def test_raises_when_required_variables_are_missing(self)
````

## File: tests/test_live_trader_profiles.py
````python
class LiveTraderProfileTests(unittest.TestCase)
⋮----
@patch("core.live_trader_base.TradingClient")
@patch("core.live_trader_base.resolve_alpaca_credentials", return_value=("api", "secret"))
    def test_live_trader_base_uses_requested_profile(self, mock_resolve, mock_client)
⋮----
@patch("core.live_trader_base.resolve_alpaca_credentials", side_effect=EnvironmentError("missing creds"))
    def test_live_trader_base_fails_fast_on_missing_profile_credentials(self, mock_resolve)
⋮----
@patch("core.live_trader_base.AlpacaLiveTraderBase.__init__", return_value=None)
    def test_live_momentum_trader_defaults_to_v1_profile(self, mock_base_init)
⋮----
@patch("strategies.pead_live_trader.AlpacaLiveTraderBase.__init__", return_value=None)
    def test_pead_live_trader_defaults_to_v2_profile(self, mock_base_init)
````

## File: tests/test_momentum_live_rebalance.py
````python
# risk.metrics imports matplotlib at module import time; stub it for unit tests.
⋮----
def _price_df(price: float) -> pd.DataFrame
⋮----
class LiveMomentumTraderRebalanceTests(unittest.TestCase)
⋮----
trader = LiveMomentumTrader(symbols=["AAPL", "AMZN", "META", "NVDA"], max_capital=None)
⋮----
# Sell dropped holding first, then buy ranked replacement that can be funded.
⋮----
# AMZN should be explicitly skipped due to insufficient pre-close cash.
⋮----
trader = LiveMomentumTrader(symbols=["AAPL", "AMZN", "META"], max_capital=1000.0)
⋮----
# META is sold, and AMZN buy sizing uses cap minus retained (AAPL) value: (1000 - 100) / 100 = 9 shares.
⋮----
trader = LiveMomentumTrader(symbols=["AAPL"], max_capital=1000.0)
````

## File: tests/test_pead_backtest.py
````python
class PEADBacktestTimingTests(unittest.TestCase)
⋮----
def setUp(self) -> None
⋮----
dates = pd.bdate_range("2026-01-05", periods=10)
⋮----
def test_backtest_uses_open_price_for_offset_entry(self)
⋮----
backtest = PEADBacktest(
⋮----
def test_backtest_skips_when_feature_anchor_bar_missing(self)
⋮----
bars = self.bars.drop(self.bars.index[2])
````

## File: tests/test_pead_calendar.py
````python
class PEADCalendarTests(unittest.TestCase)
⋮----
def test_get_trading_dates_excludes_good_friday(self)
⋮----
trading_dates = get_trading_dates("2025-04-14", "2025-04-22")
date_labels = set(trading_dates.strftime("%Y-%m-%d"))
⋮----
def test_offset_helpers_skip_good_friday(self)
⋮----
earnings_date = "2025-04-22"
⋮----
def test_current_market_date_uses_new_york_timezone(self)
⋮----
now_utc = datetime(2026, 4, 24, 1, 50, tzinfo=timezone.utc)
````

## File: tests/test_pre_earnings_features.py
````python
class BuildFeaturesTimingTests(unittest.TestCase)
⋮----
def setUp(self) -> None
⋮----
closes = [float(100 + idx) for idx in range(len(self.dates))]
⋮----
def test_build_features_uses_t4_anchor_for_t3_open_entry(self)
⋮----
features = build_features(
⋮----
expected_window = self.bars.iloc[5:12]
expected_drift = (
⋮----
def test_build_features_supports_alternate_offsets_without_schema_changes(self)
⋮----
features_t4 = build_features(
features_t5 = build_features(
⋮----
def test_build_features_inference_respects_explicit_feature_anchor(self)
⋮----
bars = self.bars.copy()
⋮----
qqq = self.qqq.copy()
⋮----
events = pd.DataFrame(
⋮----
expected_window = bars.iloc[5:12]
````

## File: .gitignore
````
*.vscode/*
*.env
*.pyc

# Generated output — logs, plots, backtest artifacts
output/*
!output/.gitkeep
__pycache__/
````

## File: core/backtest_base.py
````python
log = logging.getLogger(__name__)
⋮----
class AlpacaBacktestBase
⋮----
"""Event-driven backtesting base class for multi-symbol portfolios.

    Subclasses must implement ``on_bar(bar)`` with the strategy signal logic.
    The event loop calls ``on_bar`` at each bar and detects Friday rebalances.

    Parameters
    ----------
    data : dict[str, pd.DataFrame]
        Mapping of symbol → OHLCV+return DataFrame (aligned on a common date index).
    initial_amount : float
        Starting capital in USD.
    ftc : float
        Fixed transaction cost per trade (USD).
    ptc : float
        Proportional transaction cost per trade (fraction, e.g. 0.001 = 0.1%).
    verbose : bool
        If True, print each order to stdout.
    """
⋮----
# Build a shared date index (intersection of all symbols)
dates = None
⋮----
dates = df.index if dates is None else dates.intersection(df.index)
⋮----
# Portfolio state
⋮----
self.units_held: dict[str, float] = {}   # symbol → float shares
⋮----
self.equity_curve: list[tuple] = []      # [(date, value), ...]
⋮----
# ------------------------------------------------------------------
# Price helpers
⋮----
def _price(self, symbol: str, bar: int) -> float
⋮----
"""Return closing price of symbol at bar index."""
date = self.dates[bar]
⋮----
def _date(self, bar: int) -> pd.Timestamp
⋮----
# Order simulation
⋮----
def place_buy_order(self, symbol: str, bar: int, amount: float) -> None
⋮----
"""Buy as many whole shares of symbol as possible with given amount."""
price = self._price(symbol, bar)
units = int(amount / price)
⋮----
cost = units * price * (1 + self.ptc) + self.ftc
⋮----
def place_sell_order(self, symbol: str, bar: int, units: float) -> None
⋮----
"""Sell a given number of units of symbol."""
⋮----
proceeds = units * price * (1 - self.ptc) - self.ftc
⋮----
# Portfolio valuation
⋮----
def get_portfolio_value(self, bar: int) -> float
⋮----
"""Total portfolio value: cash + mark-to-market holdings."""
mtm = sum(
⋮----
# Close-out
⋮----
def close_out(self, bar: int) -> None
⋮----
"""Liquidate all positions at the final bar and record last equity value."""
⋮----
final_value = self.get_portfolio_value(bar)
⋮----
perf = (self.cash - self.initial_amount) / self.initial_amount * 100
⋮----
# Event loop
⋮----
def on_bar(self, bar: int) -> None:  # pragma: no cover
⋮----
"""Override in subclass: called on each bar (Monday only for rebalance)."""
⋮----
def run_backtest(self) -> pd.Series | None
⋮----
"""Main event loop. Iterates over all bars, calls on_bar on Mondays."""
⋮----
# Record starting value
⋮----
if date.weekday() == 0:  # Monday (Mon=0 … Fri=4)
⋮----
value = self.get_portfolio_value(bar)
````

## File: openspec/specs/momentum-strategy/spec.md
````markdown
## ADDED Requirements

### Requirement: Rank symbols by N-day simple return
The strategy SHALL compute the N-day simple price return for each symbol at each rebalance bar and rank symbols from highest to lowest return.

#### Scenario: Returns computed at each rebalance
- **WHEN** the rebalance event fires at bar T
- **THEN** each symbol's score is `(close[T] - close[T-N]) / close[T-N]` where N is the configured lookback window

#### Scenario: Symbols ranked correctly
- **WHEN** NVDA has return=0.42, META=0.28, AAPL=0.05, others negative
- **THEN** ranking is NVDA(1), META(2), AAPL(3), ... in descending order

### Requirement: Go long top-N symbols equal-weight
The strategy SHALL enter long positions in the top `top_n` ranked symbols, allocating equal weight (1/top_n of available capital) to each. Symbols outside the top-N SHALL be sold if currently held.

#### Scenario: Equal-weight allocation
- **WHEN** top_n=3 and available capital is $9000
- **THEN** each of the 3 selected symbols receives $3000 of capital

#### Scenario: Dropped symbol is sold
- **WHEN** symbol S was in the top-N at the previous rebalance but is no longer in the top-N at the current rebalance
- **THEN** all units of S are sold at the current closing price

#### Scenario: New symbol enters top-N
- **WHEN** symbol S enters the top-N at the current rebalance and is not currently held
- **THEN** a buy order is placed for S using its equal-weight capital allocation

### Requirement: Rebalance only on weekly frequency
The strategy SHALL only execute rebalance logic on the last trading day of each calendar week (Friday, or Thursday if Friday is a holiday).

#### Scenario: Rebalance fires on Friday
- **WHEN** the current bar's date is a Friday
- **THEN** the full ranking and rebalance logic executes

#### Scenario: No trades on non-rebalance days
- **WHEN** the current bar's date is Monday through Thursday
- **THEN** no orders are placed and portfolio state is unchanged

### Requirement: Configurable parameters
The strategy SHALL accept `lookback` (int, days), `top_n` (int), `symbols` (list of str), `start` (str date), `end` (str date), `initial_amount` (float), `ftc` (float), and `ptc` (float) as constructor parameters.

#### Scenario: Default parameters produce valid backtest
- **WHEN** strategy is instantiated with symbols=M7, lookback=60, top_n=3, initial_amount=10000
- **THEN** backtest runs without error over the configured date range

### Requirement: Live rebalance preserves ranked replacement order
The live momentum rebalance SHALL preserve the momentum-ranked target order returned by the signal, SHALL submit sell orders for dropped strategy holdings regardless of unrealized gain or loss, and SHALL evaluate new replacement buys in that same rank order.

#### Scenario: Dropped symbol is sold even when losing
- **WHEN** symbol S is currently held by the live momentum strategy, is no longer in the target list, and has a negative unrealized PnL
- **THEN** the rebalance submits a sell order for S and does not retain it solely because it is at a loss

#### Scenario: New entries are evaluated in momentum rank order
- **WHEN** the live target ranking is `[AAPL, AMZN, NVDA]`, `AAPL` is already held, and `AMZN` and `NVDA` are new entries
- **THEN** the rebalance evaluates `AMZN` before `NVDA` when allocating limited buy cash

### Requirement: Live MOC buys use only pre-close available cash
The live momentum rebalance SHALL compute buy budget only from cash available before the close, SHALL NOT treat same-day MOC sale proceeds as available for new buys, and SHALL size buys only across new target entries.

#### Scenario: Same-day MOC sale proceeds are excluded from buy budget
- **WHEN** symbol `META` is scheduled for a same-day MOC sell and `AMZN` is a new target entry
- **THEN** the rebalance computes the `AMZN` buy budget without including expected proceeds from the `META` sell order

#### Scenario: Buy sizing uses only remaining new-entry slots
- **WHEN** there are two new target entries remaining and the live trader has `$1,000` of pre-close available cash
- **THEN** the next buy decision is sized from the remaining cash divided by the remaining unfunded new entries rather than by all target holdings

### Requirement: Insufficient-cash buys are skipped explicitly
The live momentum rebalance SHALL skip a target buy when remaining buy budget cannot fund at least one whole share and SHALL log the skipped symbol and reason explicitly.

#### Scenario: Buy skipped because one share cannot be funded
- **WHEN** `AMZN` is a new target entry, the remaining buy budget is below the reference price of one share, and no fractional shares are supported
- **THEN** no buy order is submitted for `AMZN` and logs record that the buy was skipped due to insufficient available cash before the close
````

## File: openspec/specs/pead-live-trader/spec.md
````markdown
## ADDED Requirements

### Requirement: Daily cronjob executes PEAD trading logic

The system SHALL run PEAD live execution as a daily cronjob. At each execution, the system SHALL:
1. Check each symbol (NXPI, AMD, AVGO) to determine if today is T-3 or T+1+ relative to the symbol's nearest upcoming earnings date
2. Execute entry orders for any symbol at T-3, provided a positive classifier prediction exists
3. Execute exit orders for any symbol at T+1 or later, if a position is currently open
4. Log all order execution results

#### Scenario: Entry trigger on T-3
- **WHEN** cronjob runs on a day that is T-3 for a symbol's nearest earnings event AND classifier predicts positive (pred_label == 1)
- **THEN** system SHALL fetch 7-day OHLCV data (T-9 through T-3), place a market BUY order, record entry state with entry_date/entry_price/entry_qty

#### Scenario: Entry skipped on negative prediction
- **WHEN** cronjob runs on T-3 for a symbol AND classifier predicts negative (pred_label == 0)
- **THEN** system SHALL not place an order; position entry is skipped for this event

#### Scenario: Exit trigger on T+1 or later
- **WHEN** cronjob runs on a day that is T+1 or later for a symbol's current open earnings event AND a position is currently open
- **THEN** system SHALL place a market SELL order at current market price (immediate execution), log exit price and PnL, clear state entry for that symbol

#### Scenario: Double-trade prevention
- **WHEN** cronjob runs on T-3 for a symbol AND state file already shows an open position for this symbol and the same earnings_date
- **THEN** system SHALL not place another BUY order; only one entry per symbol per earnings event

#### Scenario: Missed cronjob recovery
- **WHEN** cronjob does not run on T+1 (e.g., droplet downtime), but runs on T+2 or later AND a position is still open
- **THEN** system SHALL execute the exit order immediately on the first available execution, preventing positions from lingering past intended exit date

### Requirement: Classifier integration for entry prediction

The system SHALL use a pre-trained, frozen classifier to generate predictions for live trades. For each symbol on T-3:
1. Load the latest trained classifier (no retraining during live cycle)
2. Extract 7-day pre-earnings features (T-9 through T-3)
3. Generate pred_label (0 or 1) and prob_positive probability
4. Use pred_label to gate entry: only execute if pred_label == 1

#### Scenario: Load classifier
- **WHEN** daily cronjob initializes
- **THEN** system SHALL load the most recent trained classifier model

#### Scenario: Predict for T-3 features
- **WHEN** on T-3 execution and need to decide whether to enter
- **THEN** system SHALL extract 7-day momentum/volatility/QQQ correlation features, invoke classifier.predict(), receive pred_label and prob_positive

#### Scenario: Entry gated on positive prediction
- **WHEN** classifier returns pred_label == 1
- **THEN** entry order proceeds to execution

#### Scenario: Entry blocked on negative prediction
- **WHEN** classifier returns pred_label == 0
- **THEN** entry order is not placed; day is recorded as "skipped"

### Requirement: Market order execution with Alpaca API

The system SHALL submit market orders via Alpaca's trading API (paper trading account). For each order:
1. Calculate position size as `(account_equity * 0.10) / current_price` for entry orders
2. Submit market order (buy on entry, sell on exit) with time_in_force = Day
3. Capture order ID, fill price, and fill timestamp
4. Handle errors (insufficient buying power, API rate limits) by logging and deferring to next cronjob run

#### Scenario: Calculate entry position size
- **WHEN** entry order is ready to submit
- **THEN** system SHALL read account equity, multiply by 0.10 (10% position size), divide by T-3 close price to get share count, round down to integer

#### Scenario: Submit entry market order
- **WHEN** position size is calculated
- **THEN** system SHALL submit market BUY order via AlpacaLiveTraderBase, capturing order_id and requested fill price

#### Scenario: Submit exit market order
- **WHEN** T+1+ exit is triggered
- **THEN** system SHALL submit market SELL order via AlpacaLiveTraderBase for the full open position quantity, capturing order_id and fill price

#### Scenario: Handle Alpaca errors gracefully
- **WHEN** order submission fails (e.g., API down, insufficient buying power)
- **THEN** system SHALL log error, not crash, continue to next symbol, retry on next cronjob run

### Requirement: Earnings date fetching and T-N offset calculation

The system SHALL fetch the nearest upcoming earnings date for each symbol using yfinance, then calculate T-3 and T+1 offsets accounting for NYSE trading calendar (exclude weekends, US federal holidays).

#### Scenario: Fetch nearest earnings date
- **WHEN** cronjob runs
- **THEN** system SHALL call fetch_earnings_events(symbol) to retrieve the next upcoming earnings date for each symbol (NXPI, AMD, AVGO)

#### Scenario: Calculate T-3 from earnings date
- **WHEN** earnings_date is known
- **THEN** system SHALL find the trading day exactly 3 trading days before earnings_date (skip weekends and US holidays), call this T-3

#### Scenario: Calculate T+1 from earnings date
- **WHEN** earnings_date is known
- **THEN** system SHALL find the trading day exactly 1 trading day after earnings_date, call this T+1

#### Scenario: Handle holiday edge cases
- **WHEN** earnings_date or T-3/T+1 calculation crosses a US federal holiday or weekend
- **THEN** system SHALL skip non-trading days and use NYSE trading calendar to find the correct trading day offset

### Requirement: PnL calculation at exit

The system SHALL calculate and record the profit/loss for each trade at exit time using actual execution prices.

#### Scenario: Calculate net PnL in dollars
- **WHEN** exit order executes on T+1
- **THEN** system SHALL compute: pnl_dollars = (exit_price - entry_price) * qty_shares - (2 * 0.001 * position_value) [accounting for entry and exit transaction costs of 0.1% each]

#### Scenario: Calculate PnL percentage
- **WHEN** exit order executes
- **THEN** system SHALL compute: pnl_pct = pnl_dollars / (entry_price * qty_shares)

#### Scenario: Record PnL in trade log
- **WHEN** exit order executes with known entry_price, exit_price, and qty
- **THEN** system SHALL append pnl_dollars and pnl_pct to the trade log entry

### Requirement: PEAD live trading uses V2 profile
The PEAD live trader SHALL initialize Alpaca trading access with profile `v2` so PEAD orders are isolated from momentum account activity.

#### Scenario: PEAD live trader authenticates with V2 credentials
- **WHEN** PEAD live cronjob creates `PEADLiveTrader`
- **THEN** the trading client is authenticated with `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY`

### Requirement: PEAD live data fetches are profile-selectable
PEAD live execution paths that fetch bars SHALL support explicit profile selection. If no profile is provided for general data calls, the system SHALL use default `v1` behavior.

#### Scenario: PEAD live can request v2 market data explicitly
- **WHEN** PEAD live flow calls the data layer with `profile="v2"`
- **THEN** the request authenticates using V2 profile credentials

#### Scenario: Default data profile remains v1
- **WHEN** data fetches are called without explicit profile override
- **THEN** data layer authentication uses profile `v1`
````

## File: risk/metrics.py
````python
log = logging.getLogger(__name__)
⋮----
def _to_series(equity_curve: list[tuple] | pd.Series) -> pd.Series
⋮----
"""Normalise equity_curve to a pandas Series indexed by date."""
⋮----
"""Annualised Sharpe ratio (risk-free rate = 0).

    Parameters
    ----------
    equity_curve : list of (date, value) tuples or pd.Series
    periods_per_year : int
        52 for weekly, 252 for daily.

    Returns
    -------
    float
        Annualised Sharpe ratio.  Returns 0.0 if volatility is zero.
    """
s = _to_series(equity_curve)
returns = s.pct_change().dropna()
std = returns.std()
⋮----
"""Sharpe ratio from a list of returns (no annualization for event-driven data).

    Parameters
    ----------
    returns : list of floats or pd.Series
        Individual returns (e.g., per-trade returns).
    periods_per_year : int, optional
        If provided, annualizes the ratio. If None (default), no annualization.
        Use None for event-driven data (e.g., earnings-driven trades).

    Returns
    -------
    float
        Sharpe ratio.  Returns 0.0 if volatility is zero or data has < 2 points.
    """
⋮----
returns = pd.Series(returns)
⋮----
returns = returns.copy()
⋮----
mean_ret = returns.mean()
⋮----
sharpe = float(mean_ret / std)
⋮----
def max_drawdown(equity_curve: list[tuple] | pd.Series) -> float
⋮----
"""Maximum peak-to-trough drawdown as a percentage (negative value).

    Returns
    -------
    float
        e.g. -25.4 means the worst drawdown was -25.4%.
        Returns 0.0 if the curve is monotonically increasing.
    """
⋮----
rolling_max = s.cummax()
drawdown = (s - rolling_max) / rolling_max * 100
⋮----
"""Calmar ratio: annualised return / abs(max drawdown).

    Returns
    -------
    float
        Calmar ratio.  Returns 0.0 if max drawdown is zero.
    """
⋮----
n = len(s)
⋮----
total_return = s.iloc[-1] / s.iloc[0]
ann_return = total_return ** (periods_per_year / n) - 1
mdd = max_drawdown(equity_curve)
⋮----
"""Print a formatted risk summary to stdout."""
⋮----
total_ret = (s.iloc[-1] / s.iloc[0] - 1) * 100
sr = sharpe_ratio(equity_curve, periods_per_year)
⋮----
cr = calmar_ratio(equity_curve, periods_per_year)
⋮----
"""Plot the equity curve using matplotlib."""
````

## File: scripts/pead_live_cronjob.py
````python
"""Daily cronjob for PEAD live trading execution.

Runs daily to check entry and exit conditions for configured symbols.
Entry: T-E open if classifier predicts positive using bars through T-(E+1) close
Exit: T+1 or later if position is open

Usage:
    python scripts/pead_live_cronjob.py
"""
⋮----
log = logging.getLogger(__name__)
⋮----
def setup_logging() -> None
⋮----
"""Configure logging for cronjob."""
log_path = Path("output") / f"pead_live_cronjob_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.log"
⋮----
root = logging.getLogger()
⋮----
fmt = logging.Formatter(
⋮----
fh = logging.FileHandler(log_path)
⋮----
ch = logging.StreamHandler(sys.stdout)
⋮----
def run_daily_execution() -> None
⋮----
"""Execute daily PEAD live trading logic."""
⋮----
feature_anchor_offset_days = config.get_pead_feature_anchor_offset_days()
⋮----
state_manager = PEADStateManager(config.PEAD_LIVE_STATE_FILE)
trade_logger = PEADTradeLogger(config.PEAD_LIVE_LOG_FILE)
trader = PEADLiveTrader(paper=True, position_size_pct=config.PEAD_LIVE_POSITION_SIZE, profile="v2")
summary = {
⋮----
# Clean up stale entries
⋮----
# Fetch earnings dates for all symbols
⋮----
earnings_dates = {}
⋮----
earnings_date = get_cached_earnings(symbol, use_cache=True)
⋮----
# Process each symbol
⋮----
classifier = PEADClassifierLive(symbol=symbol)
⋮----
earnings_date = earnings_dates[symbol]
timing_dates = get_pead_timing_dates(
entry_date = timing_dates["entry_date"]
feature_anchor_date = timing_dates["feature_anchor_date"]
exit_date = timing_dates["exit_date"]
today = get_current_market_date()
⋮----
# Check for ENTRY (if today is T-E)
⋮----
# Check if already traded this event (idempotency)
⋮----
# Fetch 7-day OHLCV ending at feature anchor (for T-3 open: T-10 to T-4)
feature_window_start = calculate_offset_trading_date(feature_anchor_date, -6)
⋮----
bars_dict = fetch_bars(
⋮----
symbol_index = bars_dict[symbol].index
symbol_trading_dates = set(pd.to_datetime(symbol_index).strftime("%Y-%m-%d"))
⋮----
# Build features for this event
# Create minimal events DataFrame for this single event
event_df = pd.DataFrame({
⋮----
features = build_features(
⋮----
# Extract features for prediction
features_row = features.iloc[0]
features_dict = {
⋮----
# Classify
⋮----
# Place entry order
entry_result = trader.place_entry_order(symbol)
⋮----
# Update state
⋮----
# Check for EXIT (if today is T+1 or later)
⋮----
position = state_manager.get_position(symbol)
⋮----
# Verify this is the same earnings event
⋮----
# Get current price for PnL
exit_price = trader.get_current_price(symbol)
⋮----
entry_price = position["entry_price"]
entry_qty = position["entry_qty"]
⋮----
# Place exit order
exit_result = trader.place_exit_order(symbol, entry_qty)
⋮----
# Compute PnL (with transaction costs)
gross_pnl_pct = (fill_price - entry_price) / entry_price if entry_price > 0 else 0.0
net_pnl_pct = gross_pnl_pct - (2 * config.PEAD_LIVE_PTC)
pnl_dollars = net_pnl_pct * entry_price * entry_qty
⋮----
# Log trade
t_plus_1 = calculate_offset_trading_date(earnings_date, 1)
exit_date_str = str(t_plus_1.date()) if t_plus_1 else str(get_current_market_date())
⋮----
# Remove position from state (clean slate)
⋮----
# Summary report
⋮----
# Clear cache for next execution
````

## File: strategies/pead_live_trader.py
````python
"""PEAD live trader for Alpaca paper trading execution.

Handles order placement (entry/exit), position sizing, and market price queries.
Extends AlpacaLiveTraderBase for paper trading via Alpaca API.
"""
⋮----
log = logging.getLogger(__name__)
⋮----
class PEADLiveTrader(AlpacaLiveTraderBase)
⋮----
"""Alpaca-based live trader for PEAD strategy."""
⋮----
def __init__(self, paper: bool = True, position_size_pct: float = 0.10, profile: str = "v2")
⋮----
"""Initialize PEAD live trader.
        
        Parameters
        ----------
        paper : bool
            Must be True (paper trading only)
        position_size_pct : float
            Position size as fraction of account equity (default: 0.10 = 10%)
        profile : str
            Credential profile to use for Alpaca authentication (default: "v2").
        """
⋮----
self.ptc = 0.001  # 0.1% proportional transaction cost per leg
⋮----
def calculate_position_size(self, entry_price: float) -> int
⋮----
"""Calculate number of shares to buy.
        
        Parameters
        ----------
        entry_price : float
            Entry order fill price
            
        Returns
        -------
        int
            Number of shares to buy (rounded down)
        """
⋮----
# Get account equity
account = self.client.get_account()
account_equity = float(account.equity)
⋮----
# Calculate position value
position_value = account_equity * self.position_size_pct
⋮----
# Calculate shares
qty = int(position_value / entry_price)
⋮----
def place_entry_order(self, symbol: str) -> tuple[str, float, int] | None
⋮----
"""Place a market BUY order for entry.
        
        Parameters
        ----------
        symbol : str
            Stock symbol
            
        Returns
        -------
        tuple[str, float, int] or None
            (order_id, fill_price, qty) if successful, else None
        """
⋮----
# Get current price to calculate position size
entry_price = self.get_current_price(symbol)
⋮----
# Calculate position size
qty = self.calculate_position_size(entry_price)
⋮----
# Place market order
request = MarketOrderRequest(
⋮----
order = self.client.submit_order(request)
⋮----
# Capture fill details
fill_price = float(order.filled_avg_price) if order.filled_avg_price else entry_price
filled_qty = int(order.filled_qty) if order.filled_qty else qty
⋮----
def place_exit_order(self, symbol: str, qty: int) -> tuple[str, float] | None
⋮----
"""Place a market SELL order for exit.
        
        Parameters
        ----------
        symbol : str
            Stock symbol
        qty : int
            Shares to sell
            
        Returns
        -------
        tuple[str, float] or None
            (order_id, fill_price) if successful, else None
        """
⋮----
# Get current price
exit_price = self.get_current_price(symbol)
⋮----
fill_price = float(order.filled_avg_price) if order.filled_avg_price else exit_price
⋮----
def get_current_price(self, symbol: str) -> float | None
⋮----
"""Fetch current market price for a symbol.
        
        Parameters
        ----------
        symbol : str
            Stock symbol
            
        Returns
        -------
        float or None
            Current market price, or None if unavailable
        """
⋮----
# Use quotes endpoint to get latest price
quote = self.client.get_latest_trade(symbol)
⋮----
price = float(quote.price)
⋮----
def get_order_details(self, order_id: str) -> dict | None
⋮----
"""Get details of a placed order.
        
        Parameters
        ----------
        order_id : str
            Order ID from Alpaca
            
        Returns
        -------
        dict or None
            Order details (status, filled_qty, filled_avg_price, etc.), or None on error
        """
⋮----
order = self.client.get_order_by_id(order_id)
````

## File: tests/test_pead_live_cronjob.py
````python
class PEADLiveCronjobTimingTests(unittest.TestCase)
⋮----
mock_state_manager = mock_state_manager_cls.return_value
⋮----
mock_classifier = mock_classifier_cls.return_value
⋮----
event_df = mock_build_features.call_args.kwargs["events_df"]
````

## File: .repomixignore
````
# Dev tooling
.vscode/
.idea/

# CI/CD
.github/

# Git internals
.git/

# Python cache
__pycache__/
*.pyc

# Logs / temp
logs/
tmp/

# Dependencies
node_modules/

# Others
.env
LICENSE
output/
````

## File: openspec/specs/data-layer/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Fetch daily OHLCV bars for a symbol universe
The system SHALL fetch historical daily bar data for a list of symbols using alpaca-py `StockHistoricalDataClient`, returning a dict mapping each symbol to a pandas DataFrame with columns `open`, `high`, `low`, `close`, `volume` indexed by date. The function SHALL support profile-aware authentication and SHALL default to profile `v1` when no profile is provided.

#### Scenario: Successful multi-symbol fetch with default profile
- **WHEN** `fetch_bars(symbols, start, end, timeframe)` is called without an explicit profile
- **THEN** the request authenticates with profile `v1` credentials and returns symbol-keyed OHLCV DataFrames

#### Scenario: Successful fetch with explicit v2 profile
- **WHEN** `fetch_bars(symbols, start, end, timeframe, profile="v2")` is called with valid V2 credentials
- **THEN** the request authenticates with `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY`

#### Scenario: Backtest data fetch uses v1 by default
- **WHEN** backtest workflows call `fetch_bars()` without profile overrides
- **THEN** data-layer authentication uses profile `v1`

#### Scenario: Missing profile credentials
- **WHEN** required environment variables for the selected profile are not set
- **THEN** the function raises `EnvironmentError` before making any API call and names the missing profile variables

## ADDED Requirements

### Requirement: Profile-aware data credential naming
The data layer SHALL resolve credentials from profile-prefixed environment variables using the following names:
- For `v1`: `V1_APCA_API_KEY_ID`, `V1_APCA_API_SECRET_KEY`
- For `v2`: `V2_APCA_API_KEY_ID`, `V2_APCA_API_SECRET_KEY`

#### Scenario: V2 key naming is normalized
- **WHEN** profile `v2` is selected for a data request
- **THEN** the system reads `V2_APCA_API_KEY_ID` and SHALL NOT require `V2_APCA_API_KEY`
````

## File: tests/test_alpaca_data.py
````python
class FetchBarsTests(unittest.TestCase)
⋮----
def _make_bars_response(self) -> SimpleNamespace
⋮----
index = pd.MultiIndex.from_tuples(
df = pd.DataFrame(
⋮----
@patch("data.alpaca_data._get_client")
    def test_fetch_bars_uses_inclusive_end_date_for_daily_requests(self, mock_get_client)
⋮----
mock_client = mock_get_client.return_value
⋮----
request = mock_client.get_stock_bars.call_args.args[0]
⋮----
@patch("data.alpaca_data._get_client")
    def test_fetch_bars_defaults_to_iex_feed(self, mock_get_client)
⋮----
@patch("data.alpaca_data._get_client")
    def test_fetch_bars_honors_feed_override(self, mock_get_client)
⋮----
@patch("data.alpaca_data._get_client")
    def test_fetch_bars_preserves_first_requested_ohlcv_row(self, mock_get_client)
⋮----
result = fetch_bars(["NXPI"], start="2026-04-14", end="2026-04-23")
⋮----
nxpi = result["NXPI"]
⋮----
@patch("data.alpaca_data._get_client")
    def test_fetch_bars_supports_explicit_v2_profile(self, mock_get_client)
````

## File: config.py
````python
def _validate_positive_int(name: str, value: int) -> int
⋮----
# M7 universe
M7_SYMBOLS = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA"]
⋮----
# Strategy parameters
LOOKBACK = 60       # N-day return lookback window
TOP_N = 3           # Number of symbols to hold long
INITIAL_AMOUNT = 10_000.0
FTC = 0.0           # Fixed transaction cost per trade
PTC = 0.0           # Proportional transaction cost per trade
⋮----
# Backtest period
START_DATE = "2020-01-01"
END_DATE = "2025-12-31"
⋮----
# Alpaca profile credentials
V1_APCA_API_KEY_ID = os.environ.get("V1_APCA_API_KEY_ID")
V1_APCA_API_SECRET_KEY = os.environ.get("V1_APCA_API_SECRET_KEY")
V2_APCA_API_KEY_ID = os.environ.get("V2_APCA_API_KEY_ID")
V2_APCA_API_SECRET_KEY = os.environ.get("V2_APCA_API_SECRET_KEY")
⋮----
# PEAD strategy parameters (Post-Earnings Announcements Drift)
PEAD_SYMBOLS = ["NXPI", "AMD", "AVGO"]
PEAD_START_DATE = "2016-01-01"
PEAD_END_DATE = "2025-12-31"
PEAD_POSITION_SIZE = 0.10        # 10% of capital per trade
PEAD_PTC = 0.001                 # 0.1% proportional transaction cost per leg
PEAD_MIN_TRAIN = 20              # Minimum events for training seed
PEAD_ENTRY_OFFSET_DAYS = _validate_positive_int("PEAD_ENTRY_OFFSET_DAYS", 3)
PEAD_EXIT_MODE = "t_plus_1_open"  # Options: t_plus_1_open, t_plus_1_close
⋮----
def get_pead_feature_anchor_offset_days() -> int
⋮----
"""Return the trading-day offset for the last fully known feature bar."""
⋮----
# PEAD live trading parameters
PEAD_LIVE_SYMBOLS = list(PEAD_SYMBOLS)
PEAD_LIVE_POSITION_SIZE = 0.10   # 10% of account equity per trade
PEAD_LIVE_PTC = 0.001            # 0.1% proportional transaction cost per leg
PEAD_LIVE_STATE_FILE = "output/pead_live_state.json"
PEAD_LIVE_LOG_FILE = "output/pead_live_trades.csv"
PEAD_LIVE_STALE_DAYS = 30        # Auto-cleanup entries older than this many days
````

## File: core/live_trader_base.py
````python
log = logging.getLogger(__name__)
⋮----
class AlpacaLiveTraderBase
⋮----
"""Base class for Alpaca paper trading execution.

    Parameters
    ----------
    paper : bool
        Must be True.  Raises ``ValueError`` if False.
    profile : str
        Credential profile to use for Alpaca authentication.
    """
⋮----
def __init__(self, paper: bool = True, profile: str = "v1") -> None
⋮----
# ------------------------------------------------------------------
# Positions
⋮----
def get_current_positions(self) -> dict[str, float]
⋮----
"""Return current open positions as {symbol: qty}."""
positions = self.client.get_all_positions()
⋮----
# Order submission
⋮----
def submit_order(self, symbol: str, side: OrderSide, qty: float) -> None
⋮----
"""Submit a market order and log the result.

        Parameters
        ----------
        symbol : str
        side : OrderSide
            ``OrderSide.BUY`` or ``OrderSide.SELL``.
        qty : float
            Number of whole shares.
        """
qty = int(qty)
⋮----
request = MarketOrderRequest(
order = self.client.submit_order(request)
⋮----
# Market-hours check
⋮----
def _warn_if_outside_hours(self) -> None
⋮----
clock = self.client.get_clock()
⋮----
next_open = getattr(clock, "next_open", None)
next_open_msg = str(next_open) if next_open is not None else "unknown"
````

## File: strategies/momentum.py
````python
log = logging.getLogger(__name__)
⋮----
class CrossSectionalMomentum(AlpacaBacktestBase)
⋮----
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
⋮----
self._holdings: set[str] = set()   # currently held symbols
⋮----
# ------------------------------------------------------------------
# Signal
⋮----
def compute_scores(self, bar: int) -> pd.Series
⋮----
"""Compute N-day simple price return for each symbol at bar.

        Returns
        -------
        pd.Series
            Symbols ranked descending by return score.
        """
⋮----
scores: dict[str, float] = {}
date_now = self.dates[bar]
date_prev = self.dates[bar - self.lookback]
⋮----
price_now = float(df.loc[date_now, "close"])
price_prev = float(df.loc[date_prev, "close"])
⋮----
# Event handler
⋮----
def on_bar(self, bar: int) -> None
⋮----
"""Rebalance portfolio on Fridays based on momentum signal."""
scores = self.compute_scores(bar)
⋮----
# Cash-out rule: only consider symbols with positive momentum
positive = scores[scores > 0]
target = set(positive.head(self.top_n).index)
⋮----
# 1. Sell symbols no longer in target (dropped or all momentum negative)
⋮----
units = self.units_held.get(symbol, 0.0)
⋮----
# 2. Buy new entries equal-weight (skip if no positive-momentum symbols)
new_entries = target - self._holdings
⋮----
allocation = self.cash / len(new_entries)
⋮----
# Run override (adds risk summary + plot)
⋮----
def run_backtest(self, save_path: str | None = None) -> pd.Series
⋮----
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
⋮----
equity = pd.Series(
⋮----
# ---------------------------------------------------------------------------
# Live paper trader
⋮----
class LiveMomentumTrader(AlpacaLiveTraderBase)
⋮----
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
⋮----
def _last_completed_utc_day(self) -> datetime
⋮----
"""Return the latest fully completed UTC calendar day for daily bars."""
⋮----
def compute_signal(self) -> list[str]
⋮----
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
⋮----
data = fetch_bars(self.symbols, start, end, profile=self.profile)
⋮----
price_now = float(df["close"].iloc[-1])
price_prev = float(df["close"].iloc[-(self.lookback + 1)])
⋮----
ranked = sorted(scores, key=lambda s: scores[s], reverse=True)
positive_ranked = [symbol for symbol in ranked if scores[symbol] > 0]
⋮----
# Rebalance
⋮----
def rebalance(self) -> None
⋮----
"""Execute a full signal → order cycle.

        Computes the momentum signal, diffs against current positions,
        and submits market orders for changes.
        """
⋮----
ranked_target = self.compute_signal()
target = set(ranked_target)
⋮----
current = self.get_current_positions()
⋮----
strategy_held = {symbol for symbol in current if symbol in self.symbols}
retained_held = {symbol for symbol in strategy_held if symbol in target}
⋮----
# Sell dropped holdings regardless of unrealized PnL.
⋮----
qty = current[symbol]
⋮----
# Fetch recent prices for target and currently held universe symbols.
# Used for share sizing and optional capital-cap accounting.
symbols_for_prices = sorted(set(ranked_target) | strategy_held)
⋮----
start = (last_complete_day_utc - timedelta(days=5)).strftime("%Y-%m-%d")
price_data = (
⋮----
# Estimate available capital
account = self.client.get_account()
available_cash = float(getattr(account, "cash", 0.0) or 0.0)
⋮----
deployable_cash = available_cash / 2.0
⋮----
retained_value = 0.0
⋮----
px = float(price_data[symbol]["close"].iloc[-1])
⋮----
remaining_budget = max(self.max_capital - retained_value, 0.0)
deployable_cash = min(available_cash, remaining_budget)
⋮----
# Buy new entries in rank order using remaining cash and remaining slots.
new_entries = [symbol for symbol in ranked_target if symbol not in current or current[symbol] == 0]
remaining_cash = deployable_cash
remaining_slots = len(new_entries)
⋮----
price = float(price_data[symbol]["close"].iloc[-1])
per_symbol_budget = remaining_cash / remaining_slots
qty = math.floor(per_symbol_budget / price)
````

## File: data/alpaca_data.py
````python
log = logging.getLogger(__name__)
⋮----
def _get_retry_config() -> tuple[int, float]
⋮----
"""Return retry settings for transient Alpaca data fetch errors.

    Environment overrides:
    - APCA_DATA_RETRY_COUNT (default: 10, minimum: 0)
    - APCA_DATA_RETRY_DELAY_SEC (default: 60.0, minimum: 1.0)
    """
retry_count = int(os.environ.get("APCA_DATA_RETRY_COUNT", "10"))
retry_delay_sec = float(os.environ.get("APCA_DATA_RETRY_DELAY_SEC", "60.0"))
⋮----
def _get_stock_bars_with_retry(client: StockHistoricalDataClient, request: StockBarsRequest)
⋮----
"""Fetch bars with retries for transient transport-level failures."""
⋮----
last_error: Exception | None = None
⋮----
# retry_count means retries after the first failed attempt.
total_attempts = retry_count + 1
⋮----
last_error = err
retries_used = attempt - 1
⋮----
def _resolve_stock_feed() -> str
⋮----
"""Resolve stock data feed for Alpaca bars requests.

    Defaults to IEX so paper/free subscriptions can query recent data.
    Set APCA_STOCK_FEED or APCA_DATA_FEED to override (e.g., sip, delayed_sip).
    """
⋮----
def _get_client(profile: str = "v1") -> StockHistoricalDataClient
⋮----
"""Build an authenticated StockHistoricalDataClient for a named profile."""
⋮----
"""Fetch historical OHLCV bars for a list of symbols.

    Parameters
    ----------
    symbols : list[str]
        Ticker symbols to fetch.
    start : str
        Start date, e.g. '2019-01-01'.
    end : str
        End date, e.g. '2024-12-31'.
    timeframe : TimeFrame
        Bar timeframe (default: daily).
    profile : str
        Credential profile to use for Alpaca authentication (default: "v1").

    Returns
    -------
    dict[str, pd.DataFrame]
        Mapping of symbol → DataFrame with columns [open, high, low, close, volume, return],
        indexed by date (UTC).

    Raises
    ------
    EnvironmentError
        If Alpaca credentials are not set.
    ValueError
        If any symbol has no data in the requested range.
    """
client = _get_client(profile=profile)
⋮----
start_dt = datetime.strptime(start, "%Y-%m-%d")
# Alpaca's `end` is exclusive for bar queries; add one day so caller's
# YYYY-MM-DD end date remains inclusive at day granularity.
end_dt = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
⋮----
request = StockBarsRequest(
⋮----
bars = _get_stock_bars_with_retry(client, request)
df_all = bars.df  # MultiIndex: (symbol, timestamp)
⋮----
result: dict[str, pd.DataFrame] = {}
⋮----
df = df_all.loc[symbol].copy()
df.index = pd.to_datetime(df.index).tz_localize(None)  # strip tz for simplicity
⋮----
# Keep only OHLCV columns
df = df[["open", "high", "low", "close", "volume"]]
⋮----
# Compute log returns while preserving the first requested OHLCV bar.
````

## File: openspec/specs/live-trader/spec.md
````markdown
## MODIFIED Requirements

### Requirement: Weekly rebalance trigger
The PEAD live execution flow SHALL evaluate entry for each symbol using configurable entry offset `PEAD_ENTRY_OFFSET_DAYS`, where entry date is `T-E` and required feature bars are available by `T-(E+1)` close. The system SHALL NOT attempt entry prediction when the required anchor bar is not yet available, and SHALL log an explicit skip reason.

#### Scenario: Entry evaluated with available anchor bars
- **WHEN** live execution runs for symbol S and all bars through `T-(E+1)` are available
- **THEN** prediction is computed and entry order logic is evaluated for date `T-E`

#### Scenario: Entry skipped when anchor bar unavailable
- **WHEN** live execution runs before the required anchor bar has finalized for symbol S
- **THEN** no prediction or order is attempted for that symbol and logs record `missing feature-anchor bar`

#### Scenario: Existing order safety behavior preserved
- **WHEN** live execution runs outside supported order timing or data preconditions
- **THEN** no new entry order is submitted

### Requirement: MOC rebalance budget excludes exiting positions
For live MOC rebalances with a capital cap, the system SHALL compute retained strategy exposure using only currently held symbols that remain in the target set, and SHALL exclude positions already marked for sale from capital-cap accounting.

#### Scenario: Capital cap ignores positions already scheduled to exit
- **WHEN** the strategy currently holds `AAPL`, `META`, and `NVDA`, `META` is no longer in the target set, and a capital cap is configured
- **THEN** the rebalance computes retained exposure from `AAPL` and `NVDA` only and does not count `META` against remaining buy budget

### Requirement: Live rebalance logs skipped buys for auditability
The live trader SHALL write an explicit log entry when a target buy is skipped because pre-close available cash cannot fund at least one whole share.

#### Scenario: Insufficient-cash skip is logged
- **WHEN** symbol S is a new target entry and the remaining buy budget is less than the reference price of one share of S
- **THEN** the rebalance submits no buy order for S and logs the symbol, remaining cash, and insufficient-cash skip reason

## ADDED Requirements

### Requirement: Profile-aware Alpaca live trader authentication
The live trader base SHALL authenticate Alpaca trading clients using a required profile identifier for live strategy flows. Supported profiles are `v1` and `v2`, each mapped to profile-prefixed environment variables.

#### Scenario: Momentum live trader uses v1 profile
- **WHEN** weekly momentum live rebalance initializes its trading client
- **THEN** it authenticates using `V1_APCA_API_KEY_ID` and `V1_APCA_API_SECRET_KEY`

#### Scenario: Missing live profile credentials fail fast
- **WHEN** the selected profile credentials are missing at trader initialization time
- **THEN** initialization fails with an error that identifies the missing profile variable names

### Requirement: Live momentum routing is explicit
The live momentum execution flow SHALL pass profile `v1` explicitly when constructing the shared live trader base.

#### Scenario: Momentum account routing is deterministic
- **WHEN** momentum live rebalance is executed from supported entrypoints
- **THEN** all order placement calls route through a `TradingClient` initialized with profile `v1`
````

## File: environment.yml
````yaml
name: strategy-lab
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.12
  - pip
  - numpy
  - pandas
  - scipy
  - scikit-learn
  - matplotlib
  - python-dotenv
  - pip:
      - alpaca-py
      - yfinance
      - lxml
````

## File: run.py
````python
"""
run.py — Entry point for Momentum Backtest, Live Trading, and PEAD Strategies.

Usage:
    conda activate strategy-lab
    python run.py --mode backtest                           # M7 momentum backtest
    python run.py --mode live                               # M7 live paper rebalance
    python run.py --mode live --capital-cap 30000           # M7 live with capital limit
    python run.py --mode pead-backtest                      # PEAD earnings prediction backtest
    python run.py --mode pead-live                          # PEAD daily live trading (cronjob)
"""
⋮----
def _setup_logging(log_path: str) -> logging.Logger
⋮----
"""Configure the root logger (stdout + file) so all module loggers propagate here."""
⋮----
root = logging.getLogger()
# Guard: don't add duplicate handlers if called more than once in a session
⋮----
# Suppress noisy third-party debug logs
⋮----
fmt = logging.Formatter("[%(asctime)s UTC] %(levelname)s %(name)s — %(message)s",
⋮----
fh = logging.FileHandler(log_path)
⋮----
ch = logging.StreamHandler(sys.stdout)
⋮----
def _setup_live_logging() -> logging.Logger
⋮----
def _setup_backtest_logging() -> logging.Logger
⋮----
ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
⋮----
def run_backtest() -> None
⋮----
log = _setup_backtest_logging()
⋮----
data = fetch_bars(
⋮----
strategy = CrossSectionalMomentum(
⋮----
except Exception:  # noqa: BLE001
⋮----
def run_live_rebalance(capital_cap: float | None = None) -> None
⋮----
trader = LiveMomentumTrader(
⋮----
def _setup_pead_logging() -> logging.Logger
⋮----
def run_pead_backtest() -> None
⋮----
"""Run PEAD ML backtest pipeline for each configured PEAD symbol."""
log = _setup_pead_logging()
⋮----
feature_anchor_offset_days = config.get_pead_feature_anchor_offset_days()
⋮----
events = fetch_earnings_events(
⋮----
bars = fetch_bars(
⋮----
features = build_features(
⋮----
predictions = walk_forward_predict(
⋮----
backtest = PEADBacktest(
⋮----
model_path = PEADClassifierLive.get_model_path(symbol)
⋮----
report = evaluate(predictions)
⋮----
date_label = str(date)[:10]
⋮----
def _setup_pead_live_logging() -> logging.Logger
⋮----
def run_pead_live() -> None
⋮----
"""Run PEAD live paper trading daily cronjob."""
log = _setup_pead_live_logging()
⋮----
# Import and run cronjob
⋮----
def main() -> None
⋮----
parser = argparse.ArgumentParser(description="Run momentum backtest, live paper rebalance, PEAD ML backtest, or PEAD live trading.")
⋮----
def _positive_float(value: str) -> float
⋮----
parsed = float(value)
⋮----
args = parser.parse_args()
⋮----
log = _setup_live_logging()
````

## File: scripts/weekly_live_rebalance.py
````python
#!/usr/bin/env python3
"""Run one weekly live paper rebalance with optional safety guards.

Examples:
    python scripts/weekly_live_rebalance.py
    python scripts/weekly_live_rebalance.py --capital-cap 30000
    python scripts/weekly_live_rebalance.py --force
"""
⋮----
def _setup_logging(log_path: Path) -> logging.Logger
⋮----
"""Configure the root logger (stdout + file) so all module loggers propagate here."""
⋮----
root = logging.getLogger()
⋮----
# Suppress noisy third-party debug logs
⋮----
fmt = logging.Formatter("[%(asctime)s UTC] %(levelname)s %(name)s — %(message)s",
# File handler — append so history is preserved
fh = logging.FileHandler(log_path)
⋮----
# Console handler
ch = logging.StreamHandler(sys.stdout)
⋮----
def _parse_args() -> argparse.Namespace
⋮----
parser = argparse.ArgumentParser(description="Weekly live rebalance runner.")
⋮----
def _positive_float(value: str) -> float
⋮----
parsed = float(value)
⋮----
def main() -> int
⋮----
args = _parse_args()
⋮----
repo_root = Path(__file__).resolve().parents[1]
⋮----
log = _setup_logging(repo_root / "output" / "live_rebalance.log")
⋮----
# Monday-only safety guard in UTC. Cron: 45 19 * * 1 (19:45 UTC / 2:45 PM ET)
# — submits MOC orders with a 5-min buffer before the 19:50 UTC Alpaca MOC cutoff.
now_utc = datetime.now(timezone.utc)
⋮----
total_attempts = retry_count + 1
worst_case_wait_min = (retry_count * retry_delay_sec) / 60.0
⋮----
trader = LiveMomentumTrader(
⋮----
except Exception:  # noqa: BLE001
````

## File: README.md
````markdown
# alpaca-lab

Repository to practice common rule-based strategies.

## Run Modes

Activate the project environment first:

```bash
conda activate strategy-lab
```

## Account Profiles

This repository uses two Alpaca paper-account credential profiles:
- `v1`: momentum strategy (live weekly rebalance)
- `v2`: PEAD strategy (live daily cronjob)

Data-layer calls default to profile `v1`, which keeps backtests and data-only workflows on V1 unless a call site explicitly passes another profile.

Copy `.env.example` to `.env` and set profile credentials:

```bash
cp .env.example .env
```

Required environment variables:
- `V1_APCA_API_KEY_ID`
- `V1_APCA_API_SECRET_KEY`
- `V2_APCA_API_KEY_ID`
- `V2_APCA_API_SECRET_KEY`

Migration note:
- Previous V2 key name `V2_APCA_API_KEY` has been replaced by `V2_APCA_API_KEY_ID`.

- Backtest:

```bash
python run.py --mode backtest
```

- Live paper rebalance (one-shot):

```bash
python run.py --mode live
```

- Live paper rebalance with max deployable capital cap:

```bash
python run.py --mode live --capital-cap 30000
```

- PEAD ML backtest (GOOGL earnings gap prediction):

```bash
python run.py --mode pead-backtest
```

This mode runs the full pipeline:
1. Fetch earnings events from yfinance
2. Fetch daily bars from Alpaca (GOOGL + QQQ)
3. Build pre-earnings features using the configured entry offset
4. Run walk-forward classification
5. Backtest event-driven entries/exits

Logs are written to `output/pead_backtest_*.log`.

PEAD timing is configurable via `config.PEAD_ENTRY_OFFSET_DAYS`.
- Default: `3`, which means enter at `T-3 open`
- Derived feature anchor: `T-(E+1)` close, so the default feature window is `T-10..T-4`
- Exit timing remains controlled by `config.PEAD_EXIT_MODE`

- PEAD live paper trading (multi-symbol daily cronjob):

```bash
python run.py --mode pead-live
```

This mode runs live paper trading execution for configured symbols (NXPI, AMD, AVGO):
1. Fetch nearest earnings dates for each symbol
2. Check if today is the configured entry day `T-E` or an exit day `T+1+`
3. If today is `T-E`, build features only from bars available through `T-(E+1)` close and evaluate the classifier
4. If T+1+ and position is open: place SELL order (at market price)
5. Log all trades to CSV, track state in JSON file
6. Auto-cleanup stale positions after 30 days

Logs are written to `output/pead_live_*.log`.
State file: `output/pead_live_state.json` (tracks open positions per symbol)
Trade log: `output/pead_live_trades.csv` (permanent audit trail)

### PEAD Daily Automation (DigitalOcean Droplet)

Set up a weekday cronjob to run PEAD live in a New York pre-open window.

Recommended execution window:
- Run between `9:20 AM` and `9:28 AM` America/New_York time
- This is after `T-4` has fully closed and before `T-3` regular session starts
- A single run at `9:25 AM ET` is a practical default

Example crontab entry (DST-safe via `CRON_TZ`):

```cron
CRON_TZ=America/New_York
25 9 * * 1-5 cd /home/chenyang/Git/alpaca-lab && /home/chenyang/miniconda3/envs/strategy-lab/bin/python run.py --mode pead-live >> output/pead_live.log 2>&1
```

**Timing rationale:**
- Running in an ET-defined window prevents timezone drift when the server is in Singapore or UTC
- Supports offset-driven entry-at-open logic because the signal only uses bars available by `T-(E+1)` close
- If today is `T-3` and the run happens after the US close, skip entry and wait for the next valid event (do not force late execution)
- For T+1 exits, if cronjob runs before market close, position is exited at market open
- If cronjob misses T+1 (droplet down), position exits on T+2 when cronjob runs next (handles recovery)

**Testing alternate entry offsets:**
- Default config-driven run: set `PEAD_ENTRY_OFFSET_DAYS` in `config.py`, then run `python run.py --mode pead-backtest`
- One-off alternate offset without editing config permanently:

```bash
conda run -n strategy-lab python -c "import config; config.PEAD_ENTRY_OFFSET_DAYS = 4; import run; run.run_pead_backtest()"
```

- Typical interpretations:
	- `3` => enter at `T-3 open`, feature window ends at `T-4 close`
	- `4` => enter at `T-4 open`, feature window ends at `T-5 close`
	- `5` => enter at `T-5 open`, feature window ends at `T-6 close`

**Migration note:**
- PEAD results produced before this timing change used different entry/feature semantics and are not directly comparable to current runs.

**State file and trade log:**
- State file persists open positions across cronjob runs
- Idempotency check prevents double-trading the same symbol/earnings-event pair
- Trade log is append-only for permanent audit trail
- Auto-cleanup removes stale entries after 30 days

## Weekly Automation (DigitalOcean Droplet)

Comprehensive backtest analysis (2016–2025) reveals **PEAD signal is highly sector-specific**, with semiconductors significantly outperforming mega-cap tech:

#### Semiconductor Universe (6 tested symbols)

| Symbol | Type | Events | Hit Rate | Avg Return | Sharpe | Uplift vs Always-Buy | Signal |
|--------|------|--------|----------|------------|--------|----------------------|--------|
| **NXPI** | Auto/Analog | 16 | 92.31% | 2.66% | 0.87 | **+1.56%** | 🟢 Strongest |
| **AMD** | Processor | 19 | 75.00% | 4.72% | 0.56 | **+1.90%** | 🟢 Excellent |
| **AVGO** | Broadband | 18 | 70.00% | 4.84% | 0.45 | **+1.32%** | 🟢 Excellent |
| **MU** | Memory | 20 | 62.50% | 2.48% | 0.26 | **+0.60%** | 🟡 Good |
| **QCOM** | Mobile SoC | 17 | 42.86% | 0.06% | 0.01 | **+0.78%** | 🟡 Marginal |
| **INTC** | Processor | 18 | 41.67% | -1.23% | -0.19 | **+1.05%** | 🟡 Paradoxical* |

*INTC shows negative returns but still beats always-buy because underlying earnings gap is weaker.

#### Mega-Cap Tech (7 tested symbols)

| Symbol | Events | Hit Rate | Avg Return | Sharpe | Uplift vs Always-Buy | Signal |
|--------|--------|----------|------------|--------|----------------------|--------|
| **GOOGL** | 20 | 56.25% | 1.23% | 0.59 | **+1.03%** | ✓ Only winner |
| **NVDA** | 20 | 60.00% | 2.56% | 0.31 | -0.58% | ✗ |
| **MSFT** | 19 | 52.63% | 2.01% | 0.31 | -0.14% | ✗ |
| **META** | 20 | 56.25% | 1.23% | 0.11 | -0.44% | ✗ |
| **AMZN** | 19 | 47.06% | 0.87% | 0.07 | -0.02% | ✗ |
| **AAPL** | 14 | 50.00% | 0.34% | 0.07 | -0.09% | ✗ |
| **ORCL** | 8 | 37.50% | -0.79% | -0.07 | -3.61% | ✗ Worst |

#### Key Insights

- **Semiconductors dominate**: 6/6 tested show positive uplift vs always-buy (avg +1.04%); mega-caps only 1/7 (avg -0.27%)
- **Highest hit rates in semicon**: NXPI (92%), AMD (75%), AVGO (70%) vs mega-cap range (37–60%)
- **Better risk-adjusted returns**: Semiconductor Sharpe ratios (0.26–0.87) exceed mega-cap tech (0.01–0.59)
- **Sector cyclicality matters**: PEAD drift patterns are predictable in cyclical semicon segment but noise-dominated in mega-cap tech
- **Recommendation**: Focus PEAD portfolio on **NXPI, AMD, AVGO** for highest signal quality and consistent alpha

#### Testing Methodology

- **Entry**: Configurable `T-E open` (default `T-3 open`)
- **Feature window**: 7 trading days ending at `T-(E+1)` close (default `T-10..T-4`)
- **Exit**: T+1 open (next trading day open post-earnings)
- **ML Model**: Walk-forward logistic regression (7-day momentum, volatility, QQQ drift features)
- **Training seed**: Minimum 20 events per stock
- **Transaction costs**: 0.1% per leg
- **Benchmark**: Always-buy comparison on evaluated events

#### Failed Symbols

- **TSM**: Only 7 AMC events in history (below 20-event minimum for training)
- **ADI**: No AMC earnings call data available

## Weekly Automation (DigitalOcean Droplet)

Use the weekly runner:

```bash
python scripts/weekly_live_rebalance.py
```

It includes a Monday-only UTC safety check. If the script is triggered on a non-Monday UTC day, it exits without placing orders.

Optional capital cap:

```bash
python scripts/weekly_live_rebalance.py --capital-cap 30000
```

Alpaca data fetch resilience (used by weekly rebalance bar queries):

- Retries transient connection/timeout errors
- Default policy: `10` retries with `60s` delay between retries
- Worst-case added wait before hard failure: about `10` minutes
- Runtime banner in `output/live_rebalance.log` prints active retry settings each run

Environment overrides:

```bash
export APCA_DATA_RETRY_COUNT=10
export APCA_DATA_RETRY_DELAY_SEC=60
```

Example crontab entry (every Monday pre-close, 3:45 PM ET — 5-min buffer before Alpaca MOC cutoff):

```cron
CRON_TZ=America/New_York
45 15 * * 1 cd /home/chenyang/Git/alpaca-lab && /home/chenyang/miniconda3/envs/strategy-lab/bin/python scripts/weekly_live_rebalance.py --capital-cap 30000 >> output/live_rebalance.log 2>&1
```

This timing submits Market-on-Close (MOC) orders, aligning live execution with the closing price the backtest assumes. 3:45 PM ET is DST-safe when paired with `CRON_TZ=America/New_York` and provides a 5-minute buffer before the NYSE MOC cutoff (3:50 PM ET).
````
