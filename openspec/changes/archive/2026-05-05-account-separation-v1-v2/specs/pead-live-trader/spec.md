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
