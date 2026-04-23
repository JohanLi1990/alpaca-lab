## ADDED Requirements

### Requirement: Daily cronjob executes PEAD trading logic

The system SHALL run PEAD live execution as a daily cronjob. At each execution, the system SHALL:
1. Check each symbol (NXPI, AMD, AVGO) to determine if today is T-3 or T+1+ relative to the symbol's nearest upcoming earnings date
2. Execute entry orders for any symbol at T-3, provided a positive classifier prediction exists
3. Execute exit orders for any symbol at T+1 or later, if a position is currently open
4. Log all order execution results

#### Scenario: Entry trigger on T-3
- **WHEN** cronjob runs on a day that is T-3 for a symbol's nearest earnings event AND classifier predicts positive (pred_label == 1)
- **THEN** system SHALL fetch 7-day OHLCV data (T-9 through T-3), place a market BUY order, record entry state with entry_date/entry_price/entry_qty

#### Scenario: Entry skipped on negative prediction
- **WHEN** cronjob runs on T-3 for a symbol AND classifier predicts negative (pred_label == 0)
- **THEN** system SHALL not place an order; position entry is skipped for this event

#### Scenario: Exit trigger on T+1 or later
- **WHEN** cronjob runs on a day that is T+1 or later for a symbol's current open earnings event AND a position is currently open
- **THEN** system SHALL place a market SELL order at current market price (immediate execution), log exit price and PnL, clear state entry for that symbol

#### Scenario: Double-trade prevention
- **WHEN** cronjob runs on T-3 for a symbol AND state file already shows an open position for this symbol and the same earnings_date
- **THEN** system SHALL not place another BUY order; only one entry per symbol per earnings event

#### Scenario: Missed cronjob recovery
- **WHEN** cronjob does not run on T+1 (e.g., droplet downtime), but runs on T+2 or later AND a position is still open
- **THEN** system SHALL execute the exit order immediately on the first available execution, preventing positions from lingering past intended exit date

### Requirement: Classifier integration for entry prediction

The system SHALL use a pre-trained, frozen classifier to generate predictions for live trades. For each symbol on T-3:
1. Load the latest trained classifier (no retraining during live cycle)
2. Extract 7-day pre-earnings features (T-9 through T-3)
3. Generate pred_label (0 or 1) and prob_positive probability
4. Use pred_label to gate entry: only execute if pred_label == 1

#### Scenario: Load classifier
- **WHEN** daily cronjob initializes
- **THEN** system SHALL load the most recent trained classifier model

#### Scenario: Predict for T-3 features
- **WHEN** on T-3 execution and need to decide whether to enter
- **THEN** system SHALL extract 7-day momentum/volatility/QQQ correlation features, invoke classifier.predict(), receive pred_label and prob_positive

#### Scenario: Entry gated on positive prediction
- **WHEN** classifier returns pred_label == 1
- **THEN** entry order proceeds to execution

#### Scenario: Entry blocked on negative prediction
- **WHEN** classifier returns pred_label == 0
- **THEN** entry order is not placed; day is recorded as "skipped"

### Requirement: Market order execution with Alpaca API

The system SHALL submit market orders via Alpaca's trading API (paper trading account). For each order:
1. Calculate position size as `(account_equity * 0.10) / current_price` for entry orders
2. Submit market order (buy on entry, sell on exit) with time_in_force = Day
3. Capture order ID, fill price, and fill timestamp
4. Handle errors (insufficient buying power, API rate limits) by logging and deferring to next cronjob run

#### Scenario: Calculate entry position size
- **WHEN** entry order is ready to submit
- **THEN** system SHALL read account equity, multiply by 0.10 (10% position size), divide by T-3 close price to get share count, round down to integer

#### Scenario: Submit entry market order
- **WHEN** position size is calculated
- **THEN** system SHALL submit market BUY order via AlpacaLiveTraderBase, capturing order_id and requested fill price

#### Scenario: Submit exit market order
- **WHEN** T+1+ exit is triggered
- **THEN** system SHALL submit market SELL order via AlpacaLiveTraderBase for the full open position quantity, capturing order_id and fill price

#### Scenario: Handle Alpaca errors gracefully
- **WHEN** order submission fails (e.g., API down, insufficient buying power)
- **THEN** system SHALL log error, not crash, continue to next symbol, retry on next cronjob run

### Requirement: Earnings date fetching and T-N offset calculation

The system SHALL fetch the nearest upcoming earnings date for each symbol using yfinance, then calculate T-3 and T+1 offsets accounting for NYSE trading calendar (exclude weekends, US federal holidays).

#### Scenario: Fetch nearest earnings date
- **WHEN** cronjob runs
- **THEN** system SHALL call fetch_earnings_events(symbol) to retrieve the next upcoming earnings date for each symbol (NXPI, AMD, AVGO)

#### Scenario: Calculate T-3 from earnings date
- **WHEN** earnings_date is known
- **THEN** system SHALL find the trading day exactly 3 trading days before earnings_date (skip weekends and US holidays), call this T-3

#### Scenario: Calculate T+1 from earnings date
- **WHEN** earnings_date is known
- **THEN** system SHALL find the trading day exactly 1 trading day after earnings_date, call this T+1

#### Scenario: Handle holiday edge cases
- **WHEN** earnings_date or T-3/T+1 calculation crosses a US federal holiday or weekend
- **THEN** system SHALL skip non-trading days and use NYSE trading calendar to find the correct trading day offset

### Requirement: PnL calculation at exit

The system SHALL calculate and record the profit/loss for each trade at exit time using actual execution prices.

#### Scenario: Calculate net PnL in dollars
- **WHEN** exit order executes on T+1
- **THEN** system SHALL compute: pnl_dollars = (exit_price - entry_price) * qty_shares - (2 * 0.001 * position_value) [accounting for entry and exit transaction costs of 0.1% each]

#### Scenario: Calculate PnL percentage
- **WHEN** exit order executes
- **THEN** system SHALL compute: pnl_pct = pnl_dollars / (entry_price * qty_shares)

#### Scenario: Record PnL in trade log
- **WHEN** exit order executes with known entry_price, exit_price, and qty
- **THEN** system SHALL append pnl_dollars and pnl_pct to the trade log entry
