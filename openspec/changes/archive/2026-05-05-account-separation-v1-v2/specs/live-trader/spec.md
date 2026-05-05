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
