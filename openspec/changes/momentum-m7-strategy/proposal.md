## Why

This project needs a repeatable, well-tested algorithmic trading strategy that can be backtested rigorously and deployed to paper trading. Cross-sectional momentum on the Magnificent 7 (M7) provides a focused, high-signal universe to validate the full pipeline — from data ingestion through live execution — before expanding to broader universes or additional strategies.

## What Changes

- Introduce a layered project structure with shared `core/`, `data/`, and `strategies/` packages to support multiple strategies without code duplication
- Implement a cross-sectional momentum strategy targeting the M7 stocks (AAPL, MSFT, AMZN, NVDA, GOOGL, META, TSLA)
- Build an event-driven backtester modeled after the Hilpisch pattern, adapted to fetch data from Alpaca's historical bars API
- Add a risk analytics module computing Sharpe ratio, maximum drawdown, and Calmar ratio
- Implement a paper trading live trader using `alpaca-py` TradingClient with weekly rebalancing

## Capabilities

### New Capabilities

- `data-layer`: Fetch and cache daily OHLCV bars for a symbol universe via alpaca-py `StockHistoricalDataClient`
- `backtest-engine`: Event-driven backtesting base class supporting multi-symbol portfolios with transaction cost simulation
- `momentum-strategy`: Cross-sectional momentum signal: rank M7 by N-day return, go long top 3 equal-weight, rebalance weekly
- `risk-analytics`: Compute annualized Sharpe ratio (√52 for weekly), maximum drawdown (peak-to-trough), and Calmar ratio from an equity curve
- `live-trader`: Paper trading execution using `alpaca-py` TradingClient — weekly rebalance, same signal as backtest

### Modified Capabilities

## Impact

- **New packages**: `core/`, `data/`, `strategies/` under `alpaca-lab/`
- **Dependencies**: `alpaca-py`, `pandas`, `numpy`, `python-dotenv` (all present in `strategy-lab` conda env)
- **Config**: `.env` file with `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` (paper trading keys)
- **No existing code modified** — greenfield implementation
