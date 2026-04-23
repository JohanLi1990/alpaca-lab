## Why

Post-Earnings Announcements Drift (PEAD) backtests show strong alpha in semiconductors (NXPI, AMD, AVGO with 70-92% hit rates). The current system only backtests—we need live paper trading execution to validate signals in real market conditions and build operational confidence before deploying real capital.

## What Changes

- **Daily cronjob system** for PEAD multi-symbol live execution (NXPI, AMD, AVGO)
- **Entry logic** triggers at T-3 (3 days before earnings, using frozen pre-trained classifier)
- **Exit logic** triggers at T+1 or later (if cronjob missed), exits immediately at market price
- **State tracking** prevents double-trades for the same symbol/earnings-event combination
- **Trade logging** captures entry/exit details and PnL for audit trail
- **Clean-slate design** — after each event closes, position state is reset for next earnings
- **Robustness** — handles dropped cronjobs gracefully with `today >= T+1` exit condition

## Capabilities

### New Capabilities
- `pead-live-trader`: Daily cronjob-driven live execution engine; fetches earnings dates, checks T-3/T+1 triggers, places Alpaca market orders, coordinates symbol state
- `pead-state-manager`: JSON-based state file tracking current positions per symbol (earnings_date, entry_price, entry_qty); prevents double-trades; auto-cleanup after 30 days
- `pead-trade-logger`: Append-only CSV journal (symbol, earnings_date, entry_date, exit_date, entry_price, exit_price, qty, pnl, pnl_pct, timestamp)

### Modified Capabilities
- `pead-classifier`: Freeze trained model for live predictions (no retraining during live cycle; separate weekly batch job handles retraining after T+1 closes)

## Impact

- **New files**: `core/pead_live_trader.py`, `scripts/pead_daily_cronjob.py`
- **Modified files**: `run.py` (add `--mode pead-live` entry point), `config.py` (add PEAD live parameters)
- **Output artifacts**: `output/pead_live_state.json`, `output/pead_live_trades.csv`
- **Alpaca integration**: Uses existing `AlpacaLiveTraderBase` for order submission
- **Dependencies**: None new (uses existing alpaca, pandas, yfinance)
- **Breaking changes**: None; backtest system unchanged
