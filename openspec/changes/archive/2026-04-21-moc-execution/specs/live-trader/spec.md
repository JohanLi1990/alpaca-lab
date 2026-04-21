## MODIFIED Requirements

### Requirement: Submit market orders for target portfolio
The live trader SHALL submit `MarketOrderRequest` buy and sell orders using `TimeInForce.CLS` (Market-on-Close) so that live execution price matches the closing price assumed by the backtest engine. Orders MUST be submitted while the market is open and before the exchange MOC cutoff (3:50 PM ET / 19:50 UTC).

#### Scenario: Buy order submitted as MOC for new holding
- **WHEN** symbol S enters the top-N but is not currently held
- **THEN** a MOC buy order (`time_in_force=TimeInForce.CLS`) for `floor(allocation / current_price)` shares of S is submitted

#### Scenario: Sell order submitted as MOC for dropped holding
- **WHEN** symbol S was held but no longer in top-N
- **THEN** a MOC sell order (`time_in_force=TimeInForce.CLS`) for all held shares of S is submitted

#### Scenario: No order for unchanged holdings
- **WHEN** symbol S is in top-N and already held with approximately correct weight
- **THEN** no order is submitted for S

### Requirement: Weekly rebalance trigger
The live trader SHALL expose a `rebalance()` method that executes the full signal → order cycle. The caller SHALL invoke this weekly via cron at `45 19 * * 1` (19:45 UTC, 2:45 PM ET) to ensure MOC orders are submitted before the 19:50 UTC exchange cutoff.

#### Scenario: Rebalance completes with MOC orders
- **WHEN** `rebalance()` is called on a Monday between market open and 19:50 UTC
- **THEN** all necessary MOC orders are submitted and confirmed via log output

#### Scenario: Market closed handling
- **WHEN** `rebalance()` is called outside market hours
- **THEN** a `RuntimeError` is raised and no orders are submitted
