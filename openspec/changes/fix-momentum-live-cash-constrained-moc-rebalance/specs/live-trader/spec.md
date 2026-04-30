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