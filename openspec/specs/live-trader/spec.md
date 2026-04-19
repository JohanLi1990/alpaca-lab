## ADDED Requirements

### Requirement: Connect to Alpaca paper trading account
The live trader SHALL connect to Alpaca's paper trading endpoint using `TradingClient(api_key, secret_key, paper=True)` and MUST NOT connect to the live trading endpoint.

#### Scenario: Paper trading connection established
- **WHEN** `LiveTrader` is instantiated
- **THEN** it creates a `TradingClient` with `paper=True` and verifies the account is accessible

#### Scenario: Live endpoint connection refused
- **WHEN** `paper=False` is passed to `TradingClient`
- **THEN** the `LiveTrader` constructor raises a `ValueError` refusing to proceed

### Requirement: Compute momentum signal using latest market data
The live trader SHALL fetch the most recent N+1 daily bars for all M7 symbols using `StockHistoricalDataClient`, compute N-day returns, and rank symbols — identical logic to the backtest signal.

#### Scenario: Signal computed from latest data
- **WHEN** `compute_signal()` is called
- **THEN** it returns a ranked list of symbols using the same lookback window as the configured backtest

### Requirement: Submit market orders for target portfolio
The live trader SHALL submit `MarketOrderRequest` buy orders for new holdings and sell orders for dropped holdings at market price.

#### Scenario: Buy order submitted for new holding
- **WHEN** symbol S enters the top-N but is not currently held
- **THEN** a market buy order for `floor(allocation / current_price)` shares of S is submitted

#### Scenario: Sell order submitted for dropped holding
- **WHEN** symbol S was held but no longer in top-N
- **THEN** a market sell order for all held shares of S is submitted

#### Scenario: No order for unchanged holdings
- **WHEN** symbol S is in top-N and already held with approximately correct weight
- **THEN** no order is submitted for S

### Requirement: Weekly rebalance trigger
The live trader SHALL expose a `rebalance()` method that executes the full signal → order cycle. It is the caller's responsibility to invoke this weekly (via cron, scheduler, or manual execution).

#### Scenario: Rebalance completes without error
- **WHEN** `rebalance()` is called on a Friday during market hours or pre-market
- **THEN** all necessary orders are submitted and a summary is printed to stdout

#### Scenario: Market closed handling
- **WHEN** `rebalance()` is called outside market hours
- **THEN** orders are submitted as market orders and will fill at next open; a warning is logged

### Requirement: Log all order submissions
The live trader SHALL log each order submission (symbol, side, quantity, order ID) to stdout.

#### Scenario: Order logged on submission
- **WHEN** any order is submitted
- **THEN** a line is printed: `[YYYY-MM-DD HH:MM] BUY/SELL <qty> <symbol> → order_id=<id>`
