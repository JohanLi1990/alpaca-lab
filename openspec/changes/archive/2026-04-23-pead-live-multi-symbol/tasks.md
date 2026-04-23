## 1. State Manager Implementation

- [x] 1.1 Create `core/pead_state_manager.py` with `PEADStateManager` class
- [x] 1.2 Implement `load_state()` method to read JSON state file with error handling
- [x] 1.3 Implement `save_state()` method with atomic writes (file locking)
- [x] 1.4 Implement `add_position(symbol, earnings_date, entry_date, entry_price, entry_qty)` to record new entry
- [x] 1.5 Implement `remove_position(symbol)` to delete position after exit (clean slate)
- [x] 1.6 Implement `get_position(symbol)` to check if symbol has open position
- [x] 1.7 Implement `cleanup_stale_entries(days=30)` to remove entries older than 30 days
- [x] 1.8 Implement `already_traded(symbol, earnings_date)` idempotency check
- [x] 1.9 Add comprehensive logging for all state operations

## 2. Trade Logger Implementation

- [x] 2.1 Create `core/pead_trade_logger.py` with `PEADTradeLogger` class
- [x] 2.2 Implement `initialize_log()` to create CSV header if file doesn't exist
- [x] 2.3 Implement `log_trade(symbol, earnings_date, entry_date, exit_date, entry_price, exit_price, qty, pnl, pnl_pct)` to append trade row
- [x] 2.4 Implement PnL computation with transaction cost deduction (0.1% per leg = 0.2% total)
- [x] 2.5 Implement CSV writing with proper escaping and timestamp formatting (ISO 8601 UTC)
- [x] 2.6 Implement optional `log_skipped_entry(symbol, earnings_date, entry_date, reason)` for analysis
- [x] 2.7 Add error handling for file I/O and disk space issues

## 3. Earnings Calendar and T-N Utilities

- [x] 3.1 Create `data/pead_calendar.py` utility module
- [x] 3.2 Implement `get_trading_dates(start, end)` using NYSE calendar (accounts for holidays/weekends)
- [x] 3.3 Implement `calculate_offset_trading_date(anchor_date, offset)` to compute T-3, T+1 offsets
- [x] 3.4 Implement `is_today_entry_date(symbol, earnings_dates_dict)` to check if today is T-3 for any symbol
- [x] 3.5 Implement `is_today_exit_date(symbol, earnings_dates_dict)` to check if today is T+1+ for any symbol
- [x] 3.6 Implement `fetch_nearest_earnings(symbol)` wrapper around `fetch_earnings_events()`
- [x] 3.7 Add caching for earnings dates to avoid repeated yfinance calls within same cronjob execution

## 4. Classifier Integration for Live Predictions

- [x] 4.1 Identify pre-trained classifier model location/format (from backtest)
- [x] 4.2 Create `strategies/pead_classifier_live.py` wrapper for frozen model
- [x] 4.3 Implement `load_classifier()` to deserialize trained model
- [x] 4.4 Implement `predict_entry(features)` to generate pred_label and prob_positive
- [x] 4.5 Implement feature extraction for 7-day pre-earnings window (reuse from backtest)
- [x] 4.6 Add logging of classifier predictions for audit trail
- [x] 4.7 Test that live predictions match backtest predictions on historical data (validation)

## 5. Alpaca Order Execution

- [x] 5.1 Create `strategies/pead_live_trader.py` with `PEADLiveTrader` class extending `AlpacaLiveTraderBase`
- [x] 5.2 Implement `calculate_position_size(account_equity, entry_price, position_size_pct=0.10)` for entry qty
- [x] 5.3 Implement `place_entry_order(symbol, qty)` to submit market BUY order via Alpaca
- [x] 5.4 Implement `place_exit_order(symbol, qty)` to submit market SELL order via Alpaca
- [x] 5.5 Implement `get_current_price(symbol)` to fetch real-time market price for PnL calculation
- [x] 5.6 Implement error handling for Alpaca API failures (rate limits, insufficient buying power, API down)
- [x] 5.7 Implement order result capture (order_id, fill_price, fill_timestamp) from Alpaca responses
- [x] 5.8 Add detailed logging of all order submissions and fills

## 6. Daily Cronjob Logic

- [x] 6.1 Create `scripts/pead_live_cronjob.py` as the main cronjob entry point
- [x] 6.2 Implement main loop: `for symbol in [NXPI, AMD, AVGO]:`
- [x] 6.3 For each symbol:
  - [x] 6.3.1 Fetch nearest earnings date
  - [x] 6.3.2 Calculate T-3 and T+1 trading dates
  - [x] 6.3.3 Check if today == T-3; if yes, execute entry logic
  - [x] 6.3.4 Check if today >= T+1; if yes, execute exit logic
- [x] 6.4 Implement entry logic: check prediction, place order, update state, log result
- [x] 6.5 Implement exit logic: get current price, calculate PnL, place order, update state, log trade
- [x] 6.6 Implement error handling: catch all exceptions, log, continue to next symbol
- [x] 6.7 Add summary logging at end of cronjob execution (e.g., "Entry fired for NXPI, exit skipped for AMD, error on AVGO")

## 7. Integration with Existing run.py

- [x] 7.1 Add `--mode pead-live` option to `run.py` argument parser
- [x] 7.2 Implement `run_pead_live()` function in `run.py`
- [x] 7.3 Set up logging configuration for pead-live mode (log to file + stdout)
- [x] 7.4 Call `PEADLiveTrader.run_daily_execution()` or equivalent main function
- [x] 7.5 Update README.md with usage instructions for `python run.py --mode pead-live`

## 8. Configuration and Parameters

- [x] 8.1 Add PEAD live parameters to `config.py`:
  - [x] 8.1.1 `PEAD_LIVE_SYMBOLS = ["NXPI", "AMD", "AVGO"]`
  - [x] 8.1.2 `PEAD_LIVE_POSITION_SIZE = 0.10` (10% of capital)
  - [x] 8.1.3 `PEAD_LIVE_PTC = 0.001` (0.1% per leg)
  - [x] 8.1.4 `PEAD_LIVE_STATE_FILE = "output/pead_live_state.json"`
  - [x] 8.1.5 `PEAD_LIVE_LOG_FILE = "output/pead_live_trades.csv"`
  - [x] 8.1.6 `PEAD_LIVE_STALE_DAYS = 30`
- [x] 8.2 Make configuration parameters easily modifiable

## 9. Testing and Validation

- [ ] 9.1 Unit test `PEADStateManager`: load/save, idempotency checks, cleanup
- [ ] 9.2 Unit test `PEADTradeLogger`: CSV format, PnL calculation, append semantics
- [ ] 9.3 Unit test `calculate_offset_trading_date()`: T-3, T+1 calculations, holiday handling
- [ ] 9.4 Unit test classifier prediction wrapper: loads model, returns pred_label/prob
- [ ] 9.5 Integration test: simulate one full entry/exit cycle (mock Alpaca API)
- [ ] 9.6 Manual test on paper trading: dry-run with real Alpaca API (no real execution, observe logs)
- [ ] 9.7 Validate that live predictions match historical backtest on same data

## 10. Documentation and Deployment

- [ ] 10.1 Update README.md with new `--mode pead-live` instructions
- [ ] 10.2 Document cronjob setup: example crontab entry for daily 8am ET execution
- [ ] 10.3 Document state file format and manual inspection procedures
- [ ] 10.4 Document trade log schema and how to analyze results
- [ ] 10.5 Create deployment checklist for DigitalOcean droplet
- [ ] 10.6 Add comments to all new modules explaining key design decisions
- [ ] 10.7 Write runbook for troubleshooting common issues (missed orders, state corruption, etc.)

## 11. Weekly Model Retraining (Separate Job, Lower Priority)

- [ ] 11.1 Design weekly retraining job (runs Sunday evening, retrain on all accumulated T+1 results)
- [ ] 11.2 Note: This is a separate cronjob entry; scope it for future implementation if needed
