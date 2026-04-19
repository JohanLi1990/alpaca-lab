## 1. Project Structure & Config

- [x] 1.1 Create directory layout: `core/`, `data/`, `risk/`, `strategies/` with `__init__.py` files
- [x] 1.2 Create `config.py` with M7 symbol list, default parameters (lookback=60, top_n=3, start/end dates), and `.env` loading via `python-dotenv`

## 2. Data Layer (`data/alpaca_data.py`)

- [x] 2.1 Implement `fetch_bars(symbols, start, end, timeframe=TimeFrame.Day)` using `StockHistoricalDataClient`
- [x] 2.2 Add credential loading from environment variables; raise `EnvironmentError` if missing
- [x] 2.3 Add log return column (`return = log(close / close.shift(1))`) and drop NaN rows for each symbol
- [x] 2.4 Raise `ValueError` with descriptive message if any requested symbol returns empty data

## 3. Backtest Engine (`core/backtest_base.py`)

- [x] 3.1 Implement `AlpacaBacktestBase.__init__` with portfolio state: `cash`, `units_held` (dict), `trades`, `equity_curve` (list)
- [x] 3.2 Implement `place_buy_order(symbol, bar, amount)` with `ftc`/`ptc` cost simulation
- [x] 3.3 Implement `place_sell_order(symbol, bar, units)` with `ftc`/`ptc` cost simulation
- [x] 3.4 Implement `get_portfolio_value(bar)` summing cash + mark-to-market value of all holdings
- [x] 3.5 Implement `close_out(bar)` to liquidate all positions and append final equity curve entry
- [x] 3.6 Implement `run_backtest()` event loop: iterate bars, detect Friday rebalance, call `on_bar(bar)`, record equity

## 4. Risk Analytics (`risk/metrics.py`)

- [x] 4.1 Implement `sharpe_ratio(equity_curve, periods_per_year=52)` — handle zero-volatility edge case
- [x] 4.2 Implement `max_drawdown(equity_curve)` — peak-to-trough percentage
- [x] 4.3 Implement `calmar_ratio(equity_curve, periods_per_year=52)`
- [x] 4.4 Implement `print_summary(equity_curve)` printing all metrics rounded to 2 decimal places
- [x] 4.5 Implement `plot_equity_curve(equity_curve, title, save_path=None)` using matplotlib

## 5. Momentum Strategy (`strategies/momentum.py`)

- [x] 5.1 Implement `CrossSectionalMomentum(AlpacaBacktestBase).__init__` accepting all configurable parameters
- [x] 5.2 Implement `compute_scores(bar)` — N-day simple return for each symbol, return ranked Series
- [x] 5.3 Implement `on_bar(bar)` — if Friday: call `compute_scores`, select top_n, sell dropped symbols, buy new symbols equal-weight
- [x] 5.4 Implement `run_backtest()` override calling parent event loop, then `risk.print_summary(self.equity_curve)` and `risk.plot_equity_curve()`
- [x] 5.5 Verify rebalance-only-on-Friday logic: non-Friday bars must produce no orders

## 6. Entry Point (`run.py`)

- [x] 6.1 Create `run.py` CLI that instantiates `CrossSectionalMomentum` with params from `config.py` and calls `run_backtest()`
- [x] 6.2 Print backtest configuration summary (symbols, lookback, top_n, date range, initial capital) before running

## 7. Live Trader (`core/live_trader_base.py` + `strategies/momentum.py`)

- [x] 7.1 Implement `AlpacaLiveTraderBase.__init__` with `TradingClient(paper=True)`; raise `ValueError` if `paper=False`
- [x] 7.2 Implement `get_current_positions()` using `TradingClient.get_all_positions()`
- [x] 7.3 Implement `submit_order(symbol, side, qty)` using `MarketOrderRequest`; log each submission
- [x] 7.4 Add `LiveMomentumTrader(AlpacaLiveTraderBase)` with `compute_signal()` using `StockHistoricalDataClient`
- [x] 7.5 Implement `rebalance()`: fetch latest data → compute signal → diff vs current positions → submit buy/sell orders
- [x] 7.6 Add market-hours warning when `rebalance()` is called outside NYSE hours

## 8. Validation

- [ ] 8.1 Run backtest over 2019-01-01 to 2024-12-31; confirm equity curve is generated and risk metrics print without error
- [ ] 8.2 Visually inspect equity curve plot for sanity (no flat lines, no NaN gaps)
- [ ] 8.3 Run `python run.py` and confirm output includes Sharpe ratio, max drawdown, Calmar ratio
- [ ] 8.4 Run `LiveMomentumTrader.rebalance()` once against paper account; confirm orders appear in Alpaca paper dashboard
