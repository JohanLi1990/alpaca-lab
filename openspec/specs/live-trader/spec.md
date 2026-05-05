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
