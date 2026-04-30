## ADDED Requirements

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