## Why

The current PEAD research path enters at T-1 close and exits at T open, which may capture the earnings gap but miss earlier pre-announcement positioning and post-announcement follow-through. This change adds a new GOOGL PEAD timing variant that enters earlier at T-3 close, exits at T+1 open or T+1 close, and compares model-gated trades against an always-buy baseline on the same horizon.

## What Changes

- Shift PEAD feature computation to a 7-trading-day window ending at T-3 close so the new entry timing remains free of lookahead bias.
- Extend the PEAD backtest to support configurable entry at T-3 close and configurable exits at either T+1 open or T+1 close.
- Add PEAD-specific benchmark metrics that compare the model-gated strategy against an always-buy baseline over the same evaluated events and holding window.
- Update PEAD configuration and run-mode wiring so the timing variant can be executed and reported without changing the rest of the ML pipeline structure.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `pre-earnings-features`: Change the feature availability cutoff from T-1 to T-3 while preserving the 7-day feature horizon and no-lookahead guarantees.
- `pead-backtest`: Change PEAD execution timing to support T-3 entry with T+1 open or T+1 close exits, plus reporting for the configured timing variant.

## Impact

- Affected code: `data/pre_earnings_features.py`, `strategies/pead_backtest.py`, `run.py`, and `config.py`.
- Affected specs: `openspec/specs/pre-earnings-features/spec.md` and `openspec/specs/pead-backtest/spec.md`.
- No new external dependencies are expected.