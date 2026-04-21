## Why

Live orders execute mid-morning (~10:35 AM ET) using `TimeInForce.DAY`, while the backtest simulates execution at Monday's close price. This backtest/live misalignment means live results will diverge from backtested expectations. Switching to Market-on-Close (MOC) orders aligns live execution with the close price the backtest already assumes, eliminates DST sensitivity in the cron schedule, and reduces intraday slippage noise.

## What Changes

- `core/live_trader_base.py`: Change `TimeInForce.DAY` → `TimeInForce.CLS` in `submit_order`
- `core/live_trader_base.py`: Update `_warn_if_outside_hours` to also enforce a pre-close submission cutoff (must submit before 3:50 PM ET)
- `scripts/weekly_live_rebalance.py`: Update crontab comment to reflect new timing
- `README.md`: Update crontab example from `35 14 * * 1` (14:35 UTC) to `45 19 * * 1` (19:45 UTC, DST-safe)

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `live-trader`: Order submission now uses MOC (`TimeInForce.CLS`) instead of intraday market orders; `_warn_if_outside_hours` enforces a pre-close cutoff in addition to market-open check.

## Impact

- **`core/live_trader_base.py`**: `submit_order` and `_warn_if_outside_hours` change
- **`scripts/weekly_live_rebalance.py`**: Comment update only
- **`README.md`**: Crontab example update
- **`core/backtest_base.py`**: No changes required — already executes at close
- **`strategies/momentum.py`**: No changes required
- **Dependencies**: `alpaca-py` already exposes `TimeInForce.CLS`; no new packages needed
