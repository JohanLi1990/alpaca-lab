## MODIFIED Requirements

### Requirement: Event-driven backtest simulating overnight entry at T-1 close
The PEAD backtest SHALL support a configurable timing variant that enters a long position at T-3 close and exits at either T+1 open or T+1 close for each event where `pred_label == 1`. Each trade is independent; no portfolio is held between events.

#### Scenario: Trade entered at T-3 close
- **WHEN** `pred_label == 1` for an event and the configured entry timing is T-3 close
- **THEN** a long entry is recorded at `close(T-3)` with configured position size as a fraction of capital

#### Scenario: Trade exited at T+1 open
- **WHEN** a trade is open and the configured exit mode is `t_plus_1_open`
- **THEN** the position is closed at `open(T+1)` and PnL is recorded from `close(T-3)` to `open(T+1)`

#### Scenario: Trade exited at T+1 close
- **WHEN** a trade is open and the configured exit mode is `t_plus_1_close`
- **THEN** the position is closed at `close(T+1)` and PnL is recorded from `close(T-3)` to `close(T+1)`

#### Scenario: No trade on predicted-negative event
- **WHEN** `pred_label == 0` for an event
- **THEN** no entry or exit is simulated and capital is unchanged

### Requirement: Transaction cost applied to each leg
The backtest SHALL apply a configurable proportional transaction cost (`ptc`) to both the entry and exit leg of each trade.

#### Scenario: Transaction costs reduce PnL
- **WHEN** `ptc=0.001` (0.1%)
- **THEN** net trade return equals `(exit_price / entry_price - 1) - 2 * ptc`

### Requirement: Invocable via `python run.py --mode pead-backtest`
The main entry point SHALL support `--mode pead-backtest` as the PEAD timing-variant runner that executes the full pipeline: fetch earnings events → fetch bars → build features using data available by T-3 → walk-forward predict → backtest the configured entry/exit horizon → print summary.

#### Scenario: pead-backtest mode runs end to end
- **WHEN** `python run.py --mode pead-backtest` is invoked
- **THEN** the full configured timing-variant pipeline completes without error and prints a PEAD risk summary

#### Scenario: Existing non-PEAD modes unaffected
- **WHEN** `python run.py --mode backtest` or `--mode live` is invoked
- **THEN** behavior is identical to before this change

## ADDED Requirements

### Requirement: Always-buy benchmark metrics for the configured PEAD horizon
The PEAD backtest flow SHALL compute and report benchmark metrics for an always-buy strategy that trades every evaluated PEAD event using the same entry date, exit date, and transaction cost assumptions as the model-gated strategy.

#### Scenario: Benchmark uses same evaluated events
- **WHEN** benchmark metrics are computed
- **THEN** the always-buy baseline uses the same evaluated event subset as the model-gated PEAD backtest

#### Scenario: Benchmark reports average return and hit rate
- **WHEN** the PEAD timing-variant run completes
- **THEN** the output includes always-buy hit rate, average gross return, average net return, and uplift versus the model-gated strategy for the configured horizon

#### Scenario: Benchmark uses same transaction cost assumptions
- **WHEN** `ptc` is configured for the PEAD timing-variant run
- **THEN** the always-buy benchmark applies the same per-leg transaction cost assumptions as the model-gated strategy