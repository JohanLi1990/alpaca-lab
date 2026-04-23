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