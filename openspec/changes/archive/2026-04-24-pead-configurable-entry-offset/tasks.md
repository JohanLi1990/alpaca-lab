## 1. Configuration and Timing Contract

- [x] 1.1 Add `PEAD_ENTRY_OFFSET_DAYS` validation (positive integer) in `config.py`
- [x] 1.2 Add helper(s) in `data/pead_calendar.py` to derive entry day `T-E` and feature anchor day `T-(E+1)`
- [x] 1.3 Update run/startup logging to print effective timing config (`entry_offset_days`, anchor offset, exit mode)

## 2. Data-Layer Boundary Fixes

- [x] 2.1 Ensure `data.alpaca_data.fetch_bars()` treats daily end date as inclusive
- [x] 2.2 Preserve OHLCV rows when first-row `return` is NaN (no blanket drop on return NaN)
- [x] 2.3 Add/adjust tests for inclusive end-date behavior and row preservation

## 3. Feature Engineering Generalization

- [x] 3.1 Update `build_features()` to accept `entry_offset_days` and derive anchor date from it
- [x] 3.2 Shift default T-3-open semantics to feature window `T-10..T-4` when `entry_offset_days=3`
- [x] 3.3 Keep feature column schema unchanged while using offset-derived windows
- [x] 3.4 Update warnings/errors to report missing bars in terms of derived anchor dates
- [x] 3.5 Add unit tests for offset variants (T-3, T-4, T-5) and no-lookahead guarantees

## 4. Backtest Timing Migration

- [x] 4.1 Update PEAD backtest entry pricing to use `open(T-E)` instead of fixed `close(T-3)`
- [x] 4.2 Keep exit modes (`t_plus_1_open`, `t_plus_1_close`) and ensure PnL uses new entry price basis
- [x] 4.3 Update event filtering to skip when `T-E`, `T-(E+1)`, or exit bars are unavailable
- [x] 4.4 Update backtest reporting to include configured entry offset and derived timing window

## 5. Live Cronjob Timing Migration

- [x] 5.1 Replace hardcoded T-3 checks in `scripts/pead_live_cronjob.py` with `PEAD_ENTRY_OFFSET_DAYS`
- [x] 5.2 Only build prediction features when bars through `T-(E+1)` are available
- [x] 5.3 For `entry_offset_days=3`, ensure live logic reflects T-3-open semantics using `T-10..T-4` features
- [x] 5.4 Keep idempotency/state handling correct under configurable entry offset
- [x] 5.5 Improve skip logging to distinguish timing-unavailable vs. true data-missing cases

## 6. End-to-End Validation

- [x] 6.1 Run `python run.py --mode pead-backtest` with `PEAD_ENTRY_OFFSET_DAYS=3` and confirm end-to-end success
- [x] 6.2 Run backtest with at least one alternate offset (for example 4 or 5) and confirm logic remains valid
- [x] 6.3 Run `python run.py --mode pead-live` in paper mode and verify no impossible post-hoc prediction behavior
- [x] 6.4 Confirm live logs clearly show effective timing configuration and entry/skip reasons per symbol

## 7. Documentation

- [x] 7.1 Update README PEAD section with entry-offset configuration and timing semantics
- [x] 7.2 Document how to test alternate entry offsets (T-3, T-4, T-5) safely
- [x] 7.3 Document migration note that prior backtest results are not directly comparable after timing change
