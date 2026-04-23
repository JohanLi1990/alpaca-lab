## ADDED Requirements

### Requirement: Event-driven backtest simulating overnight entry at T-1 close
The PEAD backtest SHALL simulate entering a long position at T-1 close and exiting at T open for each event where `pred_label == 1`. Each trade is independent; no portfolio is held between events.

#### Scenario: Trade entered at T-1 close
- **WHEN** `pred_label == 1` for an event
- **THEN** a long entry is recorded at `close(T-1)` with configured position size as a fraction of capital

#### Scenario: Trade exited at T open
- **WHEN** a trade is open and T open bar is available
- **THEN** the position is closed at `open(T)` and PnL is recorded as `(open(T) / close(T-1) - 1) * position_value`

#### Scenario: No trade on predicted-negative event
- **WHEN** `pred_label == 0` for an event
- **THEN** no entry or exit is simulated and capital is unchanged

### Requirement: Configurable position sizing as fixed fraction of capital
The backtest SHALL support a `position_size` parameter (float, fraction of current capital, e.g. 0.05 for 5%) applied to each trade independently. Capital starts at `initial_amount`.

#### Scenario: Position size applied to current capital
- **WHEN** capital is $10,000 and `position_size=0.05`
- **THEN** each trade risks $500 of capital

### Requirement: Transaction cost applied to each leg
The backtest SHALL apply a configurable proportional transaction cost (`ptc`) to both the entry and exit leg of each trade.

#### Scenario: Transaction costs reduce PnL
- **WHEN** `ptc=0.001` (0.1%)
- **THEN** net trade return equals `(open(T) / close(T-1) - 1) - 2 * ptc`

### Requirement: Equity curve and per-trade record
The backtest SHALL produce:
- An equity curve: capital value after each event (trade or no trade), indexed by `earnings_date`.
- A per-trade record DataFrame with columns: `earnings_date`, `entry_price`, `exit_price`, `gross_return`, `net_return`, `pred_prob`, `y`.

#### Scenario: Equity curve length equals number of evaluated events
- **WHEN** backtest runs over N events
- **THEN** the equity curve has exactly N+1 entries (initial value plus one per event)

#### Scenario: Per-trade record only contains traded events
- **WHEN** backtest completes
- **THEN** the per-trade DataFrame contains only rows where `pred_label == 1`

### Requirement: Risk summary consistent with existing risk.metrics module
The backtest SHALL call `risk.print_summary(equity_curve)` after completion to produce Sharpe ratio, max drawdown, Calmar ratio, and total return using the existing module.

#### Scenario: Risk summary printed after backtest
- **WHEN** `PEADBacktest.run()` completes
- **THEN** `risk.print_summary` is called with the equity curve and prints all metrics

### Requirement: Invocable via `python run.py --mode pead-backtest`
The main entry point SHALL support `--mode pead-backtest` as a new run mode that executes the full pipeline: fetch earnings events → fetch bars → build features → walk-forward predict → backtest → print summary.

#### Scenario: pead-backtest mode runs end to end
- **WHEN** `python run.py --mode pead-backtest` is invoked
- **THEN** the full pipeline completes without error and prints a risk summary

#### Scenario: Existing modes unaffected
- **WHEN** `python run.py --mode backtest` or `--mode live` is invoked
- **THEN** behavior is identical to before this change
