## 1. Configuration and Run-Mode Wiring

- [x] 1.1 Add PEAD timing-variant config values for T-3 entry and configurable exit mode (`t_plus_1_open` or `t_plus_1_close`)
- [x] 1.2 Update `run_pead_backtest()` to log the configured entry/exit timing variant and keep the rest of the PEAD pipeline wiring intact

## 2. Feature Timing Shift

- [x] 2.1 Update `build_features()` to compute the 7-trading-day feature window ending at T-3 instead of T-1
- [x] 2.2 Update baseline-volume and baseline-range windows so they remain non-overlapping relative to the shifted T-3 feature window
- [x] 2.3 Update feature-window validation and warnings to enforce no-lookahead relative to the T-3 decision time

## 3. PEAD Backtest Timing Variant

- [x] 3.1 Extend the PEAD backtest to derive T-3 and T+1 dates from the symbol's daily bar index for each evaluated event
- [x] 3.2 Implement configurable exits at T+1 open and T+1 close using the configured PEAD exit mode
- [x] 3.3 Keep transaction-cost handling and per-trade records consistent with the new entry/exit prices
- [x] 3.4 Skip events with missing T-3 or T+1 bars and log warnings without breaking the run

## 4. Benchmark Reporting

- [x] 4.1 Compute always-buy benchmark metrics on the same evaluated event subset as the model-gated PEAD strategy
- [x] 4.2 Report always-buy hit rate, average gross return, average net return, and model-versus-benchmark uplift for the configured horizon

## 5. Validation

- [x] 5.1 Run `python run.py --mode pead-backtest` for the T-3 to T+1 open variant and confirm the pipeline completes end to end
- [x] 5.2 Run the PEAD timing variant with the T+1 close exit and confirm both exit modes produce valid trade records and benchmark metrics
- [x] 5.3 Verify the shifted feature window uses only bars available by T-3 for at least one sampled earnings event