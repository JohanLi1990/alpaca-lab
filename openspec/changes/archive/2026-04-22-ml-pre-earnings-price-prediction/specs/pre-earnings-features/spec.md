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
