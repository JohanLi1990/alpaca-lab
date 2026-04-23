## Context

Currently, PEAD backtest is offline—run manually, analyze results after-the-fact. The classifier has been trained and validated on 2016–2025 historical data showing strong alpha in semiconductors (NXPI 92% hit rate, AMD 75%, AVGO 70%). Live execution faces two operational challenges:

1. **Timing precision**: Entry must trigger at T-3 close, exit at T+1 open (or later if cronjob fails). Multiple symbols have non-overlapping earnings dates, so cronjob must check readiness for each symbol daily.
2. **Idempotency**: Without state tracking, a retry or double-run could place duplicate orders. We need lightweight tracking to answer "did we already trade this event?"

Existing infrastructure available:
- `AlpacaLiveTraderBase` for Alpaca order submission (paper trading)
- `fetch_earnings_events()` to get earnings dates from yfinance
- `fetch_bars()` to get OHLCV data
- Trained classifier model for predictions

## Goals / Non-Goals

**Goals:**
- Daily cronjob that checks all three symbols and triggers entry/exit as calendar dates arrive
- Prevents double-trades for the same symbol/earnings-event pair
- Market orders for entry (T-3) and exit (T+1+), using current market price for PnL
- Full audit trail of all trades (entry price, exit price, PnL, timestamp)
- Clean state after each event (no carryover between earnings events)
- Graceful handling of missed cronjobs (execute exit on next available T+1+)
- No manual intervention needed after initial setup

**Non-Goals:**
- Model retraining during live cycle (separate weekly batch job, out of scope)
- Real (non-paper) trading
- Dynamic position sizing based on market conditions
- Sophisticated exit strategies (profit targets, stop losses)
- Cross-symbol correlation handling
- Integration with other strategies

## Decisions

### Decision 1: State Storage → JSON File (not database)
**Choice**: Single JSON file per symbol (`output/pead_live_state.json`), structured as `{symbol: {earnings_date, entry_date, entry_price, entry_qty, ...}}`.

**Rationale**: 
- Simple, human-readable, easy to inspect/debug
- No extra dependencies (sqlite, redis)
- Small data volume (3 symbols × 1 position each)
- File-based state survives cronjob restarts naturally

**Alternatives considered**:
- CSV file: More awkward to merge/update (would need read-modify-write)
- SQLite: Overkill for 3 symbols + 1 position each
- Redis: Adds operational complexity (another service)

### Decision 2: State Lifecycle → Delete After Exit
**Choice**: After exiting a position (T+1 or later), delete the state entry. Next earnings event gets a clean state.

**Rationale**:
- Simplifies idempotency check: "if symbol in state, position is open"
- No need to track closed positions in state file (that's what trades log does)
- Clean slate semantics match trading intent

### Decision 3: Trade Logging → Append-Only CSV
**Choice**: Single `output/pead_live_trades.csv` with columns: `symbol, earnings_date, entry_date, exit_date, entry_price, exit_price, qty, pnl, pnl_pct, timestamp`.

**Rationale**:
- Audit trail is immutable and queryable
- Easy to import into analysis tools (pandas, Excel)
- Append-only prevents accidental overwrites
- Decoupled from state (state is ephemeral, log is permanent)

### Decision 4: Order Type → Market Orders for Both Entry/Exit
**Choice**: Use market orders (vs limit orders) for both T-3 entry and T+1 exit.

**Rationale**:
- Simplicity: no need to guess fill prices
- Backtest assumes T-3 close/T+1 open prices (market order aligns with that)
- Given semicon volatility, slippage on market orders is acceptable cost
- Live execution will reveal if slippage kills alpha (if so, can switch to limit orders in future)

**Trade-off**: May experience slippage vs theoretical backtest prices. Mitigation: log actual fill prices; compare to backtest assumptions in weekly reviews.

### Decision 5: Exit Timing → `if today >= T+1`
**Choice**: Exit triggers when `today >= T+1 AND position is open AND earnings_date matches`. Handles missed cronjobs gracefully.

**Rationale**:
- If droplet was down on T+1, position still exits on next cronjob run
- Avoids lingering positions past intended exit date
- Simple to implement (just one inequality check)

### Decision 6: Entry Decision → Frozen Classifier, No Retraining
**Choice**: Use pre-trained classifier for live predictions. Retraining happens in separate weekly batch job after T+1 closes.

**Rationale**:
- Live cycle should be stable (no model churn day-to-day)
- Retraining needs full event data (only available after T+1 close)
- Weekly cadence (5 earnings events/year × 3 symbols = ~15 events/year) doesn't warrant daily updates
- Backtest already validated walk-forward performance; retrain weekly to stay current

## Risks / Trade-offs

**[Risk] Alpaca API rate limits or outages** → Mitigation: Catch exceptions, log errors, rely on next cronjob run. No exponential backoff needed for daily cron (single attempt).

**[Risk] Earnings date fetch fails (yfinance down)** → Mitigation: Cache earnings dates in state file; skip day if fetch fails but use last known dates.

**[Risk] State file corruption** → Mitigation: Always back up before write; validate JSON before loading; human-inspectable format aids recovery.

**[Risk] Slippage on market orders reduces alpha** → Mitigation: Log actual fill prices; weekly review will show if live returns match backtest. If not, switch to limit orders.

**[Risk] Model degradation over time** → Mitigation: Weekly retraining job updates model. If performance drops >10%, manual intervention to investigate.

**[Risk] Simultaneous cronjob runs (e.g., manual + scheduled)** → Mitigation: Load/check/write state atomically; OS file locking provides basic protection. For higher safety, add timestamp-based conflict detection.

## Migration Plan

1. **Develop locally** with paper trading on test symbols
2. **Deploy to DigitalOcean droplet** as new cron job entry
3. **Monitor first week** of live execution (observe fills, PnL, log quality)
4. **Verify backtest assumptions**: Compare actual T-3/T+1 fills to historical bar data; check if slippage is acceptable
5. **Scale to production** once confidence is built

Rollback: Simply disable cron job entry. Existing state file can be inspected/manually cleaned up if needed.

## Open Questions

1. How often does yfinance earnings data refresh? Should we cache and validate?
2. Should we add Slack/email alerts on entry/exit (for visibility)?
3. Weekly retraining job: separate script or integrated into cronjob logic?
