## Why

The current PEAD live path fails on entry day because the decision timing and available bar data are inconsistent: we trigger on T-3 while the model expects a fully available T-3 daily bar. This creates impossible behavior ("decide T-3" only after T-3 has passed) and causes dropped events in live runs.

We also need entry timing to be strategy-configurable instead of hardcoded so we can test and compare variants (for example T-3 open, T-4 open, T-5 open) without rewriting feature logic and backtest/live orchestration each time.

## What Changes

- Add configurable PEAD entry timing via config (`PEAD_ENTRY_OFFSET_DAYS`) and derive the feature window from that offset.
- Redefine default live/backtest semantics to support T-3 open entry by using only bars available by T-4 close (feature window T-10..T-4).
- Generalize feature engineering to compute windows from `entry_offset_days` (not fixed T-3 assumptions).
- Update backtest entry/exit pricing logic to use configurable entry anchor and keep configurable exit mode.
- Update live cronjob trigger logic to evaluate entry on entry-day open semantics and avoid impossible "predict after the fact" paths.
- Update logging and docs to print the configured entry/feature window so runtime behavior is explicit.

## Capabilities

### New Capabilities
- `pead-entry-timing-config`: Config-driven PEAD entry timing and derived feature window rules shared by backtest and live execution.

### Modified Capabilities
- `pre-earnings-features`: Requirement changes from fixed T-3 feature anchoring to offset-driven window generation.
- `pead-backtest`: Requirement changes from fixed T-3 close entry to configurable entry offset with open-entry semantics.
- `live-trader`: Requirement changes to ensure PEAD live entry decisions align with data actually available at decision time.
- `data-layer`: Requirement changes to enforce inclusive date windows for daily bars used in offset-derived feature windows.

## Impact

- Affected code:
  - `config.py`
  - `data/pre_earnings_features.py`
  - `data/pead_calendar.py`
  - `data/alpaca_data.py`
  - `strategies/pead_backtest.py`
  - `scripts/pead_live_cronjob.py`
  - `run.py`
- New/updated OpenSpec files under this change for one new capability and multiple modified capabilities.
- Backtest outputs will change because entry/feature timing changes.
- README and runbook sections for PEAD timing must be updated to describe configurable entry offsets.
