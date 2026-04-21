## 1. Live Trader — MOC Order Execution

- [x] 1.1 In `core/live_trader_base.py`, change `time_in_force=TimeInForce.DAY` to `time_in_force=TimeInForce.CLS` in `submit_order`

## 2. Documentation — Crontab Timing

- [x] 2.1 In `scripts/weekly_live_rebalance.py`, update the crontab comment from `35 14 * * 1` (14:35 UTC) to `45 19 * * 1` (19:45 UTC) and update the timing rationale comment
- [x] 2.2 In `README.md`, update the crontab example from `35 14 * * 1` to `45 19 * * 1` and update the timing explanation

## 3. Verification

- [ ] 3.1 Update the crontab on the DigitalOcean droplet to `45 19 * * 1`
- [ ] 3.2 On next Monday, verify orders appear in Alpaca UI as MOC type and fill at the official closing price
