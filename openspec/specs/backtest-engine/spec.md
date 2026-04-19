## ADDED Requirements

### Requirement: Event-driven iteration over time bars
The backtest engine SHALL iterate over each time bar in chronological order, evaluating strategy signals and simulating order execution at each bar.

#### Scenario: Bar-by-bar event loop
- **WHEN** `run_backtest()` is called
- **THEN** the engine processes each bar from index `lookback` to `len(data)-1` in order, calling `on_bar(bar)` exactly once per bar

### Requirement: Simulated order execution with transaction costs
The engine SHALL simulate buy and sell orders using the closing price at the signal bar, applying configurable fixed transaction cost (`ftc`) and proportional transaction cost (`ptc`).

#### Scenario: Buy order reduces cash balance
- **WHEN** a buy order is placed for N units at price P with ptc=0.001 and ftc=0
- **THEN** cash decreases by `N * P * (1 + ptc) + ftc`

#### Scenario: Sell order increases cash balance
- **WHEN** a sell order is placed for N units at price P with ptc=0.001 and ftc=0
- **THEN** cash increases by `N * P * (1 - ptc) - ftc`

### Requirement: Multi-symbol portfolio state tracking
The engine SHALL maintain portfolio state across multiple symbols: cash balance, units held per symbol, and current position per symbol.

#### Scenario: Portfolio state initialized correctly
- **WHEN** a backtest is instantiated with `initial_amount=10000`
- **THEN** cash equals 10000, units_held is an empty dict, and all positions are neutral (0)

#### Scenario: Portfolio state updated after trade
- **WHEN** a buy order is executed for symbol S
- **THEN** `units_held[S]` reflects the purchased units and cash reflects the deducted amount

### Requirement: Equity curve recorded at each rebalance
The engine SHALL record total portfolio value (cash + mark-to-market holdings) at each rebalance event, producing an equity curve as a pandas Series indexed by date.

#### Scenario: Equity curve length matches rebalance count
- **WHEN** backtest runs over a period with W weekly rebalances
- **THEN** the equity curve has exactly W+1 entries (including initial value)

### Requirement: Final close-out and summary
The engine SHALL close all open positions at the last bar and print a summary: final balance, net performance (%), number of trades, and call `calculate_risk_metrics()`.

#### Scenario: Close-out at end of backtest
- **WHEN** the event loop reaches the final bar
- **THEN** all positions are liquidated at the last closing price and the final cash balance reflects all proceeds
