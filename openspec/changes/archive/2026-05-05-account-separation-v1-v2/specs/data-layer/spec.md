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
