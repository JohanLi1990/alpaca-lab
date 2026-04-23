## MODIFIED Requirements

### Requirement: Event-driven backtest simulating overnight entry at T-1 close
The PEAD backtest SHALL support a configurable entry offset `PEAD_ENTRY_OFFSET_DAYS` and SHALL enter a long position at `open(T-E)` for each event where `pred_label == 1`, where E is the configured entry offset. The backtest SHALL exit at either T+1 open or T+1 close according to configured exit mode. Each trade is independent; no portfolio is held between events.

#### Scenario: Trade entered at T-3 open
- **WHEN** `pred_label == 1` and `PEAD_ENTRY_OFFSET_DAYS=3`
- **THEN** a long entry is recorded at `open(T-3)` with configured position size as a fraction of capital

#### Scenario: Trade exited at T+1 open
- **WHEN** a trade is open and the configured exit mode is `t_plus_1_open`
- **THEN** the position is closed at `open(T+1)` and PnL is recorded from `open(T-E)` to `open(T+1)`

#### Scenario: Trade exited at T+1 close
- **WHEN** a trade is open and the configured exit mode is `t_plus_1_close`
- **THEN** the position is closed at `close(T+1)` and PnL is recorded from `open(T-E)` to `close(T+1)`

#### Scenario: No trade on predicted-negative event
- **WHEN** `pred_label == 0` for an event
- **THEN** no entry or exit is simulated and capital is unchanged

### Requirement: Invocable via `python run.py --mode pead-backtest`
The main entry point SHALL support `--mode pead-backtest` as the PEAD timing-variant runner that executes the full pipeline: fetch earnings events -> fetch bars -> build features using bars available by `T-(E+1)` where E is `PEAD_ENTRY_OFFSET_DAYS` -> walk-forward predict -> backtest the configured entry/exit horizon -> print summary.

#### Scenario: pead-backtest mode runs end to end
- **WHEN** `python run.py --mode pead-backtest` is invoked
- **THEN** the full configured timing-variant pipeline completes without error and prints a PEAD risk summary

#### Scenario: Existing non-PEAD modes unaffected
- **WHEN** `python run.py --mode backtest` or `--mode live` is invoked
- **THEN** behavior is identical to before this change
