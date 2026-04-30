## ADDED Requirements

### Requirement: Rank symbols by N-day simple return
The strategy SHALL compute the N-day simple price return for each symbol at each rebalance bar and rank symbols from highest to lowest return.

#### Scenario: Returns computed at each rebalance
- **WHEN** the rebalance event fires at bar T
- **THEN** each symbol's score is `(close[T] - close[T-N]) / close[T-N]` where N is the configured lookback window

#### Scenario: Symbols ranked correctly
- **WHEN** NVDA has return=0.42, META=0.28, AAPL=0.05, others negative
- **THEN** ranking is NVDA(1), META(2), AAPL(3), ... in descending order

### Requirement: Go long top-N symbols equal-weight
The strategy SHALL enter long positions in the top `top_n` ranked symbols, allocating equal weight (1/top_n of available capital) to each. Symbols outside the top-N SHALL be sold if currently held.

#### Scenario: Equal-weight allocation
- **WHEN** top_n=3 and available capital is $9000
- **THEN** each of the 3 selected symbols receives $3000 of capital

#### Scenario: Dropped symbol is sold
- **WHEN** symbol S was in the top-N at the previous rebalance but is no longer in the top-N at the current rebalance
- **THEN** all units of S are sold at the current closing price

#### Scenario: New symbol enters top-N
- **WHEN** symbol S enters the top-N at the current rebalance and is not currently held
- **THEN** a buy order is placed for S using its equal-weight capital allocation

### Requirement: Rebalance only on weekly frequency
The strategy SHALL only execute rebalance logic on the last trading day of each calendar week (Friday, or Thursday if Friday is a holiday).

#### Scenario: Rebalance fires on Friday
- **WHEN** the current bar's date is a Friday
- **THEN** the full ranking and rebalance logic executes

#### Scenario: No trades on non-rebalance days
- **WHEN** the current bar's date is Monday through Thursday
- **THEN** no orders are placed and portfolio state is unchanged

### Requirement: Configurable parameters
The strategy SHALL accept `lookback` (int, days), `top_n` (int), `symbols` (list of str), `start` (str date), `end` (str date), `initial_amount` (float), `ftc` (float), and `ptc` (float) as constructor parameters.

#### Scenario: Default parameters produce valid backtest
- **WHEN** strategy is instantiated with symbols=M7, lookback=60, top_n=3, initial_amount=10000
- **THEN** backtest runs without error over the configured date range

### Requirement: Live rebalance preserves ranked replacement order
The live momentum rebalance SHALL preserve the momentum-ranked target order returned by the signal, SHALL submit sell orders for dropped strategy holdings regardless of unrealized gain or loss, and SHALL evaluate new replacement buys in that same rank order.

#### Scenario: Dropped symbol is sold even when losing
- **WHEN** symbol S is currently held by the live momentum strategy, is no longer in the target list, and has a negative unrealized PnL
- **THEN** the rebalance submits a sell order for S and does not retain it solely because it is at a loss

#### Scenario: New entries are evaluated in momentum rank order
- **WHEN** the live target ranking is `[AAPL, AMZN, NVDA]`, `AAPL` is already held, and `AMZN` and `NVDA` are new entries
- **THEN** the rebalance evaluates `AMZN` before `NVDA` when allocating limited buy cash

### Requirement: Live MOC buys use only pre-close available cash
The live momentum rebalance SHALL compute buy budget only from cash available before the close, SHALL NOT treat same-day MOC sale proceeds as available for new buys, and SHALL size buys only across new target entries.

#### Scenario: Same-day MOC sale proceeds are excluded from buy budget
- **WHEN** symbol `META` is scheduled for a same-day MOC sell and `AMZN` is a new target entry
- **THEN** the rebalance computes the `AMZN` buy budget without including expected proceeds from the `META` sell order

#### Scenario: Buy sizing uses only remaining new-entry slots
- **WHEN** there are two new target entries remaining and the live trader has `$1,000` of pre-close available cash
- **THEN** the next buy decision is sized from the remaining cash divided by the remaining unfunded new entries rather than by all target holdings

### Requirement: Insufficient-cash buys are skipped explicitly
The live momentum rebalance SHALL skip a target buy when remaining buy budget cannot fund at least one whole share and SHALL log the skipped symbol and reason explicitly.

#### Scenario: Buy skipped because one share cannot be funded
- **WHEN** `AMZN` is a new target entry, the remaining buy budget is below the reference price of one share, and no fractional shares are supported
- **THEN** no buy order is submitted for `AMZN` and logs record that the buy was skipped due to insufficient available cash before the close
