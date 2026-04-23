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
  backtest_base.py
  live_trader_base.py
data/
  __init__.py
  alpaca_data.py
  earnings_calendar.py
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
    pre-earnings-features/
      spec.md
    risk-analytics/
      spec.md
  config.yaml
output/
  .gitkeep
risk/
  __init__.py
  metrics.py
scripts/
  weekly_live_rebalance.py
strategies/
  __init__.py
  momentum.py
  pead_backtest.py
  pead_classifier.py
.gitignore
.repomixignore
config.py
environment.yml
README.md
run.py
```

# Files

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

## File: data/pre_earnings_features.py
````python
"""Pre-earnings feature engineering from T-7 to T-1 daily bars.

Computes features from daily OHLCV bars in the 7-day window preceding each
earnings event, with no forward-looking data.
"""
⋮----
log = logging.getLogger(__name__)
⋮----
"""Build feature vectors from pre-earnings daily bars.

    Parameters
    ----------
    events_df : pd.DataFrame
        Events DataFrame with columns: earnings_date, t_minus_1, symbol.
    bars_dict : dict[str, pd.DataFrame]
        Dict mapping symbol → OHLCV DataFrame indexed by date with columns:
        open, high, low, close, volume.
    symbol : str
        The symbol to analyze (e.g., "GOOGL").
    qqq_symbol : str
        The benchmark symbol for relative features (default "QQQ").

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
        - y: binary label (1 if T open > T-1 close, else 0)
        - gap_return: continuous gap return

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
t_minus_1_date = event["t_minus_1"].date()
⋮----
t_minus_1_ts = pd.Timestamp(t_minus_1_date)
⋮----
t_minus_1_idx = int(trading_dates.get_loc(t_minus_1_ts))  # type: ignore[arg-type]
⋮----
# Feature window: the last 7 trading days ending at T-3 close.
t_minus_3_ts = trading_dates[t_minus_1_idx - 2]
all_bars_before_t3 = bars[bars.index <= t_minus_3_ts].copy()
⋮----
feature_window = all_bars_before_t3.iloc[-7:].copy()
⋮----
# Verify no look-ahead relative to the T-3 entry decision.
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
baseline_end_idx = len(all_bars_before_t3) - 8
⋮----
baseline_window = all_bars_before_t3.iloc[baseline_end_idx - 19:baseline_end_idx + 1].copy()
⋮----
baseline_window = all_bars_before_t3.iloc[:baseline_end_idx + 1].copy()
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
all_qqq_before_t3 = bars_qqq[bars_qqq.index <= t_minus_3_ts].copy()
⋮----
qqq_window = all_qqq_before_t3.iloc[-7:].copy()
qqq_close_t7 = float(qqq_window["close"].iloc[0])
qqq_close_t1 = float(qqq_window["close"].iloc[-1])
qqq_drift = (qqq_close_t1 - qqq_close_t7) / qqq_close_t7 if qqq_close_t7 > 0 else 0.0
rel_drift_vs_qqq = drift_7d - qqq_drift
⋮----
rel_drift_vs_qqq = drift_7d
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
y = 1 if gap_return > 0.0 else 0
⋮----
result = pd.DataFrame(rows)
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
## ADDED Requirements

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
The main entry point SHALL support `--mode pead-backtest` as the PEAD timing-variant runner that executes the full pipeline: fetch earnings events → fetch bars → build features using data available by T-3 → walk-forward predict → backtest the configured entry/exit horizon → print summary.

#### Scenario: pead-backtest mode runs end to end
- **WHEN** `python run.py --mode pead-backtest` is invoked
- **THEN** the full configured timing-variant pipeline completes without error and prints a PEAD risk summary

#### Scenario: Existing non-PEAD modes unaffected
- **WHEN** `python run.py --mode backtest` or `--mode live` is invoked
- **THEN** behavior is identical to before this change
````

## File: openspec/specs/pre-earnings-features/spec.md
````markdown
## ADDED Requirements

### Requirement: Build a feature vector per earnings event from T-7 to T-1 daily bars
The feature module SHALL produce a single feature vector per earnings event by computing summary statistics over the 7 trading days ending at T-3 close (inclusive). All features MUST use only data available at T-3 close with no forward-looking fields relative to the T-3 entry decision time.

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
The module SHALL exclude any event where fewer than 7 valid bars exist in the feature window ending at T-3, and log a warning per dropped event.

#### Scenario: Event dropped on insufficient history
- **WHEN** only 4 bars are available in the feature window ending at T-3 for an event
- **THEN** that event is excluded from the output and a warning is logged
````

## File: strategies/pead_backtest.py
````python
"""Event-driven backtest for PEAD strategy.

Simulates overnight entry at T-1 close and exit at T open based on classifier
predictions, with transaction cost modeling.
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

    Simulates overnight positions: buy at T-1 close, sell at T open.
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
trading_dates = pd.DatetimeIndex(sorted(bars.index.unique()))
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
# Derive entry date from T-1 and exit date from earnings day.
entry_ts = _shift_trading_day(
⋮----
exit_ts = _shift_trading_day(trading_dates, event_ts, 1)
⋮----
entry_price = float(bars.loc[entry_ts, "close"])
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

## File: strategies/pead_classifier.py
````python
"""ML classifier for earnings gap predictions using walk-forward cross-validation.

Implements event-level expanding-window walk-forward validation with logistic
regression (Phase 1) or configurable classifiers (Phase 2).
"""
⋮----
log = logging.getLogger(__name__)
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
# Feature columns (exclude y, gap_return)
feature_cols = [
⋮----
X = features_df[feature_cols].values
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
````

## File: core/__init__.py
````python

````

## File: data/__init__.py
````python

````

## File: data/alpaca_data.py
````python
def _get_client() -> StockHistoricalDataClient
⋮----
"""Build an authenticated StockHistoricalDataClient from environment variables."""
api_key = os.environ.get("APCA_API_KEY_ID")
secret_key = os.environ.get("APCA_API_SECRET_KEY")
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
client = _get_client()
⋮----
request = StockBarsRequest(
⋮----
bars = client.get_stock_bars(request)
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
# Compute log returns and drop NaN
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

## File: openspec/specs/data-layer/spec.md
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

## File: output/.gitkeep
````

````

## File: risk/__init__.py
````python

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

## File: strategies/__init__.py
````python

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
def compute_signal(self) -> list[str]
⋮----
"""Fetch latest data and return top-N positive-momentum symbols.

        Returns
        -------
        list[str]
            Top-N symbols ranked by N-day return, best first.
            If all scores are non-positive, returns an empty list (stay in cash).
        """
end = datetime.today().strftime("%Y-%m-%d")
# Fetch extra days to ensure we have enough trading days
start = (datetime.today() - timedelta(days=self.lookback * 2)).strftime("%Y-%m-%d")
⋮----
data = fetch_bars(self.symbols, start, end)
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
target = set(self.compute_signal())
⋮----
current = self.get_current_positions()
⋮----
# Sell dropped holdings
⋮----
# Fetch recent prices for target and currently held universe symbols.
# Used for share sizing and optional capital-cap accounting.
strategy_held = {symbol for symbol in current if symbol in self.symbols}
symbols_for_prices = sorted(target | strategy_held)
⋮----
start = (datetime.today() - timedelta(days=5)).strftime("%Y-%m-%d")
price_data = fetch_bars(symbols_for_prices, start, end) if symbols_for_prices else {}
⋮----
# Estimate available capital
account = self.client.get_account()
available_cash = float(getattr(account, "cash", 0.0) or 0.0)
⋮----
deployable_cash = available_cash
⋮----
current_value = 0.0
⋮----
px = float(price_data[symbol]["close"].iloc[-1])
⋮----
remaining_budget = max(self.max_capital - current_value, 0.0)
deployable_cash = min(available_cash, remaining_budget)
⋮----
allocation = deployable_cash / len(target) if target else 0.0
⋮----
# Buy new entries
⋮----
price = float(price_data[symbol]["close"].iloc[-1])
qty = math.floor(allocation / price)
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
````

## File: config.py
````python
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
# Alpaca credentials
APCA_API_KEY_ID = os.environ.get("APCA_API_KEY_ID")
APCA_API_SECRET_KEY = os.environ.get("APCA_API_SECRET_KEY")
⋮----
# PEAD strategy parameters (Post-Earnings Announcements Drift)
PEAD_SYMBOL = "GOOGL"
PEAD_START_DATE = "2016-01-01"
PEAD_END_DATE = "2025-12-31"
PEAD_POSITION_SIZE = 0.10        # 10% of capital per trade
PEAD_PTC = 0.001                 # 0.1% proportional transaction cost per leg
PEAD_MIN_TRAIN = 20              # Minimum events for training seed
PEAD_ENTRY_OFFSET_DAYS = 3       # Enter at T-3 close
PEAD_EXIT_MODE = "t_plus_1_open"  # Options: t_plus_1_open, t_plus_1_close
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

## File: openspec/specs/live-trader/spec.md
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

### Requirement: Log all order submissions
The live trader SHALL log each order submission (symbol, side, quantity, order ID) to stdout.

#### Scenario: Order logged on submission
- **WHEN** any order is submitted
- **THEN** a line is printed: `[YYYY-MM-DD HH:MM] BUY/SELL <qty> <symbol> → order_id=<id>`
````

## File: environment.yml
````yaml
name: base
channels:
  - defaults
  - conda-forge
  - https://repo.anaconda.com/pkgs/main
  - https://repo.anaconda.com/pkgs/r
dependencies:
  - _libgcc_mutex=0.1
  - _openmp_mutex=5.1
  - aiodns=3.6.1
  - aiohappyeyeballs=2.6.1
  - aiohttp=3.13.3
  - aiosignal=1.4.0
  - anaconda-anon-usage=0.7.5
  - annotated-types=0.6.0
  - anyio=4.12.1
  - archspec=0.2.5
  - arrow-cpp=23.0.1
  - asttokens=3.0.1
  - attrs=25.4.0
  - aws-c-auth=0.9.4
  - aws-c-cal=0.9.13
  - aws-c-common=0.12.6
  - aws-c-compression=0.3.1
  - aws-c-event-stream=0.5.9
  - aws-c-http=0.10.7
  - aws-c-io=0.23.3
  - aws-c-mqtt=0.13.3
  - aws-c-s3=0.11.3
  - aws-c-sdkutils=0.2.4
  - aws-checksums=0.2.8
  - aws-crt-cpp=0.35.4
  - aws-sdk-cpp=1.11.720
  - beautifulsoup4=4.14.3
  - blas=1.0
  - boltons=25.0.0
  - boto3=1.42.34
  - botocore=1.42.34
  - brotlicffi=1.2.0.0
  - bs4=4.14.3
  - bzip2=1.0.8
  - c-ares=1.34.6
  - ca-certificates=2025.12.2
  - certifi=2026.01.04
  - cffi=2.0.0
  - charset-normalizer=3.4.4
  - click=8.2.1
  - comm=0.2.3
  - conda=26.1.1
  - conda-anaconda-telemetry=0.3.0
  - conda-anaconda-tos=0.2.2
  - conda-content-trust=0.2.0
  - conda-libmamba-solver=26.3.0
  - conda-package-handling=2.4.0
  - conda-package-streaming=0.12.0
  - cpp-expected=1.1.0
  - cryptography=46.0.5
  - debugpy=1.8.16
  - decorator=5.2.1
  - distro=1.9.0
  - executing=2.2.1
  - expat=2.7.4
  - filelock=3.20.3
  - fmt=11.2.0
  - frozendict=2.4.6
  - frozenlist=1.8.0
  - fsspec=2026.1.0
  - gettext=0.25.1
  - gettext-tools=0.25.1
  - gflags=2.2.2
  - glog=0.5.0
  - greenlet=3.2.4
  - h11=0.16.0
  - hf-xet=1.2.0
  - httpcore=1.0.9
  - httpx=0.28.1
  - huggingface_hub=1.3.3
  - icu=73.1
  - idna=3.11
  - intel-openmp=2025.0.0
  - ipykernel=7.2.0
  - ipython=9.10.0
  - ipython_pygments_lexers=1.1.1
  - jansson=2.14
  - jedi=0.19.2
  - jiter=0.12.0
  - jmespath=1.1.0
  - joblib=1.5.3
  - jsonpatch=1.33
  - jsonpointer=3.0.0
  - jupyter_client=8.8.0
  - jupyter_core=5.9.1
  - langsmith=0.6.0
  - ld_impl_linux-64=2.44
  - libabseil=20260107.0
  - libarchive=3.8.2
  - libasprintf=0.25.1
  - libasprintf-devel=0.25.1
  - libbrotlicommon=1.2.0
  - libbrotlidec=1.2.0
  - libbrotlienc=1.2.0
  - libcurl=8.18.0
  - libev=4.33
  - libevent=2.1.12
  - libexpat=2.7.4
  - libffi=3.4.4
  - libgcc=15.2.0
  - libgcc-ng=15.2.0
  - libgettextpo=0.25.1
  - libgettextpo-devel=0.25.1
  - libgomp=15.2.0
  - libgrpc=1.78.0
  - libhwloc=2.12.1
  - libiconv=1.18
  - libidn2=2.3.8
  - libkrb5=1.22.1
  - libmamba=2.3.2
  - libmambapy=2.3.2
  - libnghttp2=1.67.1
  - libnsl=2.0.0
  - libprotobuf=6.33.5
  - libre2-11=2025.11.05
  - libsodium=1.0.20
  - libsolv=0.7.30
  - libssh2=1.11.1
  - libstdcxx=15.2.0
  - libstdcxx-ng=15.2.0
  - libthrift=0.22.0
  - libunistring=1.3
  - libuuid=1.41.5
  - libuv=1.52.0
  - libxcb=1.17.0
  - libxml2=2.13.9
  - libzlib=1.3.1
  - lmdb=0.9.31
  - lxml=4.9.3
  - lz4-c=1.9.4
  - markdown-it-py=4.0.0
  - matplotlib-inline=0.2.1
  - mdurl=0.1.2
  - menuinst=2.4.2
  - mkl=2025.0.0
  - mkl-service=2.5.2
  - mkl_fft=2.1.1
  - mkl_random=1.3.0
  - msgpack-python=1.1.1
  - multidict=6.7.1
  - ncurses=6.5
  - nest-asyncio=1.6.0
  - nlohmann_json=3.11.2
  - numpy=2.4.2
  - numpy-base=2.4.2
  - openssl=3.5.5
  - orc=2.2.0
  - orjson=3.11.7
  - outcome=1.3.0
  - packaging=25.0
  - pandas=3.0.1
  - parso=0.8.5
  - pcre2=10.46
  - pexpect=4.9.0
  - pip=26.0.1
  - platformdirs=4.5.0
  - pluggy=1.5.0
  - prompt-toolkit=3.0.52
  - prompt_toolkit=3.0.52
  - propcache=0.4.1
  - psutil=7.0.0
  - pthread-stubs=0.3
  - ptyprocess=0.7.0
  - pure_eval=0.2.3
  - pyarrow=23.0.1
  - pybind11-abi=5
  - pycares=4.10.0
  - pycosat=0.6.6
  - pycparser=2.23
  - pydantic=2.12.5
  - pydantic-core=2.41.5
  - pygments=2.19.2
  - pysocks=1.7.1
  - python=3.12.12
  - python-dateutil=2.9.0post0
  - pyyaml=6.0.3
  - pyzmq=27.1.0
  - re2=2025.11.05
  - readline=8.3
  - regex=2026.2.28
  - reproc=14.2.4
  - reproc-cpp=14.2.4
  - requests=2.32.5
  - requests-toolbelt=1.0.0
  - rich=14.2.0
  - ruamel.yaml=0.18.16
  - ruamel.yaml.clib=0.2.14
  - s2n=1.6.2
  - s3transfer=0.16.0
  - sacremoses=0.1.1
  - selenium=4.38.0
  - setuptools=80.10.2
  - shellingham=1.5.4
  - simdjson=3.10.1
  - six=1.17.0
  - snappy=1.2.2
  - sniffio=1.3.1
  - sortedcontainers=2.4.0
  - soupsieve=2.5
  - sqlalchemy=2.0.45
  - sqlite=3.51.2
  - stack_data=0.6.3
  - tbb=2022.3.0
  - tbb-devel=2022.3.0
  - tenacity=9.1.2
  - tk=8.6.15
  - tornado=6.5.4
  - tqdm=4.67.3
  - traitlets=5.14.3
  - transformers=2.1.1
  - trio=0.32.0
  - trio-websocket=0.12.2
  - truststore=0.10.1
  - typer-slim=0.20.0
  - typing-extensions=4.15.0
  - typing-inspection=0.4.2
  - typing_extensions=4.15.0
  - tzdata=2026a
  - urllib3=2.6.3
  - utf8proc=2.6.1
  - uuid-utils=0.12.0
  - uvloop=0.22.1
  - wcwidth=0.2.14
  - websocket-client=1.8.0
  - wheel=0.46.3
  - wsproto=1.3.1
  - xorg-libx11=1.8.12
  - xorg-libxau=1.0.12
  - xorg-libxdmcp=1.1.5
  - xorg-xorgproto=2024.1
  - xz=5.8.2
  - yaml=0.2.5
  - yaml-cpp=0.8.0
  - yarl=1.22.0
  - zeromq=4.3.5
  - zlib=1.3.1
  - zstandard=0.24.0
  - zstd=1.5.7
  - pip:
      - accelerate==1.5.2
      - dataclasses-json==0.6.7
      - finlight-client==0.2.0
      - httpx-sse==0.4.0
      - jinja2==3.1.6
      - langchain==0.3.22
      - langchain-community==0.3.20
      - langchain-core==0.3.49
      - langchain-openai==0.3.11
      - langchain-postgres==0.0.13
      - langchain-text-splitters==0.3.7
      - langgraph==0.3.21
      - langgraph-checkpoint==2.0.23
      - langgraph-prebuilt==0.1.7
      - langgraph-sdk==0.1.60
      - markupsafe==3.0.2
      - marshmallow==3.26.1
      - mpmath==1.3.0
      - multitasking==0.0.11
      - mypy-extensions==1.0.0
      - networkx==3.4.2
      - nvidia-cublas-cu12==12.4.5.8
      - nvidia-cuda-cupti-cu12==12.4.127
      - nvidia-cuda-nvrtc-cu12==12.4.127
      - nvidia-cuda-runtime-cu12==12.4.127
      - nvidia-cudnn-cu12==9.1.0.70
      - nvidia-cufft-cu12==11.2.1.3
      - nvidia-curand-cu12==10.3.5.147
      - nvidia-cusolver-cu12==11.6.1.9
      - nvidia-cusparse-cu12==12.3.1.170
      - nvidia-cusparselt-cu12==0.6.2
      - nvidia-nccl-cu12==2.21.5
      - nvidia-nvjitlink-cu12==12.4.127
      - nvidia-nvtx-cu12==12.4.127
      - openai==1.69.0
      - ormsgpack==1.9.1
      - peewee==3.17.9
      - pgvector==0.3.6
      - pip-review==1.3.0
      - psycopg==3.2.6
      - psycopg-pool==3.2.6
      - pydantic-settings==2.8.1
      - pyperclip==1.9.0
      - python-dotenv==1.0.1
      - style==1.1.0
      - sympy==1.13.1
      - tiktoken==0.9.0
      - torch==2.6.0
      - triton==3.2.0
      - typing-inspect==0.9.0
      - undetected-chromedriver==3.5.5
      - update==0.0.1
      - websockets==15.0.1
      - yfinance==0.2.55
prefix: /home/chenyang/miniconda3
````

## File: run.py
````python
"""
run.py — Entry point for M7 Cross-Sectional Momentum.

Usage:
    conda activate strategy-lab
    python run.py --mode backtest
    python run.py --mode live
    python run.py --mode live --capital-cap 30000
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
"""Run PEAD ML backtest pipeline: earnings → features → walk-forward → backtest."""
log = _setup_pead_logging()
⋮----
# Step 1: Fetch earnings calendar
⋮----
events = fetch_earnings_events(
⋮----
timing="AMC",  # After-market-close only
⋮----
# Step 2: Fetch daily bars (GOOGL + QQQ)
⋮----
bars = fetch_bars(
⋮----
# Step 3: Build features
⋮----
features = build_features(
⋮----
# Step 4: Walk-forward prediction
⋮----
predictions = walk_forward_predict(
⋮----
# Step 5: Backtest
⋮----
backtest = PEADBacktest(
⋮----
# Summary report
⋮----
report = evaluate(predictions)
⋮----
date_label = str(date)[:10]
⋮----
def main() -> None
⋮----
parser = argparse.ArgumentParser(description="Run momentum backtest, live paper rebalance, or PEAD ML backtest.")
⋮----
args = parser.parse_args()
⋮----
log = _setup_live_logging()
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
    """
⋮----
def __init__(self, paper: bool = True) -> None
⋮----
api_key = os.environ.get("APCA_API_KEY_ID")
secret_key = os.environ.get("APCA_API_SECRET_KEY")
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
3. Build pre-earnings features
4. Run walk-forward classification
5. Backtest event-driven entries/exits

Logs are written to `output/pead_backtest_*.log`.

### PEAD Strategy Findings: Multi-Stock Analysis

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

- **Entry**: T-3 close (3 days before earnings announcement)
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

Example crontab entry (every Monday pre-close, 19:45 UTC / 2:45 PM ET — 5-min buffer before Alpaca MOC cutoff):

```cron
45 19 * * 1 cd /home/chenyang/Git/alpaca-lab && /home/chenyang/miniconda3/envs/strategy-lab/bin/python scripts/weekly_live_rebalance.py --capital-cap 30000 >> output/live_rebalance.log 2>&1
```

This timing submits Market-on-Close (MOC) orders, aligning live execution with the closing price the backtest assumes. 19:45 UTC is DST-safe and provides a 5-minute buffer before the NYSE MOC cutoff (19:50 UTC).
````
