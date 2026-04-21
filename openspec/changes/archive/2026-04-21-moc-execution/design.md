## Context

The live trader currently submits intraday market orders (`TimeInForce.DAY`) at ~10:35 AM ET every Monday. The backtest engine simulates execution at Monday's closing price. This gap means live returns will differ from backtested results even with the same signal.

Additionally, the cron is set to `35 14 * * 1` (14:35 UTC), which is only 5 minutes after open during winter (EST, UTC-5), placing execution in the noisiest window of the trading day.

## Goals / Non-Goals

**Goals:**
- Align live execution price with the backtest's close-price assumption
- Eliminate DST sensitivity in the cron timing by switching to a fixed UTC pre-close window
- Ensure `_warn_if_outside_hours` remains a useful guard under the new timing model

**Non-Goals:**
- Changing the signal computation (still based on prior close prices)
- Supporting fractional shares or notional orders
- Modifying the backtest engine (already correct)

## Decisions

### Decision: Use `TimeInForce.CLS` (MOC orders)

**Chosen**: Change `submit_order` to use `TimeInForce.CLS` in `MarketOrderRequest`.

**Alternatives considered:**
- `TimeInForce.DAY` at a later time (e.g., 15:30 UTC) — still intraday, still diverges from backtest close price
- Limit orders at last close price — complicates order management, risk of non-fill

**Rationale**: MOC is the simplest change that closes the backtest/live gap. The execution price *is* the close price, exactly what the backtest models. Alpaca paper trading supports MOC.

### Decision: Cron timing → 19:45 UTC Monday

**Chosen**: `45 19 * * 1` — 2:45 PM ET year-round (19:50 UTC is Alpaca's MOC cutoff; 5-min buffer).

**Rationale**: NYSE MOC cutoff is 3:50 PM ET = 19:50 UTC fixed (no DST shift since NYSE close is always 21:00 UTC). 19:45 UTC gives a 5-minute submission buffer while ensuring the script runs well within the window.

### Decision: Relax `_warn_if_outside_hours` to check only market-open, not time-of-day

**Chosen**: Keep the existing `is_open` check. MOC orders must be submitted while the market is open (after 9:30 AM, before 3:50 PM ET). Alpaca's clock `is_open` flag covers this window naturally — no additional time-of-day logic needed.

**Rationale**: Adding a hardcoded 19:50 UTC ceiling creates a new DST-like fragility. Alpaca's clock is the authoritative source.

## Risks / Trade-offs

- **MOC not accepted on halted stocks** → Alpaca will reject the order; the existing error logging in `submit_order` will capture this. No special handling needed for paper trading.
- **Script fires after 19:50 UTC** (e.g., cron delay, server lag) → MOC deadline missed, order rejected. Mitigation: 5-minute buffer in cron timing; operator should monitor `output/live_rebalance.log`.
- **Price slippage at close auction** → MOC fills at the official closing price; any large imbalance in the closing auction could affect fill. Negligible at these quantities vs. M7 daily volume.

## Migration Plan

1. Update `TimeInForce.DAY` → `TimeInForce.CLS` in `live_trader_base.py`
2. Update crontab on the DigitalOcean droplet: `35 14 * * 1` → `45 19 * * 1`
3. Update the crontab comment in `weekly_live_rebalance.py` and example in `README.md`
4. Next Monday: verify orders appear in Alpaca UI as MOC type, confirm fill at closing price

**Rollback**: Revert `TimeInForce.CLS` to `TimeInForce.DAY` and restore crontab. No data migration required.

## Open Questions

None — all decisions resolved in the explore session.
