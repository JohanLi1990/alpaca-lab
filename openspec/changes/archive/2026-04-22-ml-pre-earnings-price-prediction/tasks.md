## 1. Earnings Calendar

- [x] 1.1 Create `data/earnings_calendar.py` with `fetch_earnings_events(symbol, start, timing)` using `yfinance`
- [x] 1.2 Implement AMC/BMO classification: release time after 16:00 ET → AMC, before 09:30 ET → BMO, otherwise exclude and warn
- [x] 1.3 Compute `t_minus_1` column using NYSE trading calendar (pandas_market_calendars or exchange_calendars)
- [x] 1.4 Implement `timing` filter parameter to return AMC-only, BMO-only, or all classified events
- [x] 1.5 Raise `ValueError` on empty result after filtering; log count of excluded events

## 2. Pre-Earnings Feature Engineering

- [x] 2.1 Create `data/pre_earnings_features.py` with `build_features(events_df, bars_dict)` function
- [x] 2.2 Implement price drift features: `drift_7d`, `drift_slope` (OLS), `up_day_count`, `down_day_count`
- [x] 2.3 Implement volume pressure features: `rel_volume_mean` (vs T-8 to T-28 baseline), `down_volume_ratio`
- [x] 2.4 Implement volatility regime features: `atr_ratio` (window vs baseline), `gap_count`
- [x] 2.5 Implement relative-to-market feature: `rel_drift_vs_qqq` using QQQ bars from `bars_dict`
- [x] 2.6 Compute target label `y` (binary) and `gap_return` (continuous) from T open vs T-1 close
- [x] 2.7 Drop and log events with fewer than 7 valid bars in feature window or missing T open bar
- [x] 2.8 Add assertion that no feature computation window references any bar at or after earnings date T

## 3. ML Classifier

- [x] 3.1 Create `strategies/pead_classifier.py` with `walk_forward_predict(features_df, min_train, threshold)` function
- [x] 3.2 Implement expanding-window walk-forward loop: train on events 0..N-1, predict event N
- [x] 3.3 Fit `StandardScaler` on training fold only; apply (not re-fit) to test fold
- [x] 3.4 Use `LogisticRegression` as Phase 1 model; expose `model_cls` parameter for Phase 2 swap-in
- [x] 3.5 Return `prob_positive` and `pred_label` (thresholded at configurable `threshold`, default 0.5)
- [x] 3.6 Implement `evaluate(predictions_df)` that computes and returns `hit_rate`, `baseline_rate`, `avg_gap_return`, `avg_gap_return_negative`, `n_trades`, `n_total`
- [x] 3.7 Implement `print_eval_report(report)` that logs all evaluation metrics to stdout
- [x] 3.8 Log sorted feature coefficients by absolute magnitude after each fold fit when `verbose=True`

## 4. PEAD Backtest

- [x] 4.1 Create `strategies/pead_backtest.py` with `PEADBacktest` class accepting predictions, bars, `position_size`, `ptc`, `initial_amount`
- [x] 4.2 Implement `run()` method: iterate events in chronological order, simulate overnight entry at T-1 close and exit at T open for `pred_label == 1` events
- [x] 4.3 Apply `ptc` to both entry and exit legs
- [x] 4.4 Build equity curve Series indexed by `earnings_date` (N+1 entries including initial value)
- [x] 4.5 Build per-trade record DataFrame with columns: `earnings_date`, `entry_price`, `exit_price`, `gross_return`, `net_return`, `pred_prob`, `y`
- [x] 4.6 Call `risk.print_summary(equity_curve)` at end of `run()`

## 5. Data Layer Extension

- [x] 5.1 Verify `fetch_bars(["QQQ"], start, end)` works as a single-symbol call (no code change expected; add integration test or manual verification note)
- [x] 5.2 Update docstring to reflect single-symbol use case is supported

## 6. Run Mode Integration

- [x] 6.1 Add PEAD config constants to `config.py`: `PEAD_SYMBOL` ("GOOGL"), `PEAD_START_DATE` ("2016-01-01"), `PEAD_END_DATE` ("2025-12-31"), `PEAD_POSITION_SIZE`, `PEAD_PTC`, `PEAD_MIN_TRAIN` (20)
- [x] 6.2 Add `run_pead_backtest()` function in `run.py` that wires the full pipeline: earnings calendar → bars fetch → feature build → walk-forward predict → backtest → summary
- [x] 6.3 Add `--mode pead-backtest` to the argparse block in `run.py`; verify existing `backtest` and `live` modes are unaffected

## 7. Validation

- [x] 7.1 Manual smoke test: run `python run.py --mode pead-backtest` and confirm it produces evaluation report and equity curve without error
- [x] 7.2 Verify walk-forward produces predictions only from position `min_train` onward with no earlier events
- [x] 7.3 Spot-check 2–3 GOOGL earnings events against investor relations page to confirm AMC classification and T-1 date are correct
- [x] 7.4 Verify equity curve and per-trade records agree on PnL arithmetic for at least 2 events
