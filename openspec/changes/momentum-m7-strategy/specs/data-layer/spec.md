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
