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
