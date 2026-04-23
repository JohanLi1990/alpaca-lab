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
