## Context

This is a greenfield algorithmic trading project building on the event-driven backtest pattern from Hilpisch's *Python for Algorithmic Trading* (Chapter 6). The existing `BacktestBase` / `BacktestLongOnly` classes in `strategy-lab` provide proven mechanics (event loop, order simulation, P&L tracking) but are tightly coupled to a single symbol and a remote CSV data source. This project adapts that pattern for Alpaca's API, extends it to multi-symbol portfolios, and adds a live paper trading path.

The `strategy-lab` conda environment provides all required dependencies: `alpaca-py`, `pandas`, `numpy`, `python-dotenv`.

## Goals / Non-Goals

**Goals:**
- Layered architecture (`core/`, `data/`, `strategies/`) so future strategies share infrastructure without duplication
- Event-driven backtest with full portfolio simulation: multi-symbol, weekly rebalance, transaction cost simulation
- Risk analytics: annualized Sharpe ratio (√52), max drawdown, Calmar ratio, equity curve
- Paper trading live execution via `alpaca-py` using the same signal as the backtest
- Reproducible results with configurable parameters (lookback window, top-N holdings, backtest period)

**Non-Goals:**
- Intraday (sub-daily) bars — daily bars only for this change
- Long-short — long-only
- Live trading with real money — paper account only
- Optimization / parameter sweep — single parameter set, no grid search
- Portfolio margin / leverage calculations
- Notifications or alerting

## Decisions

### D1: Layered architecture over strategy-per-folder

**Decision**: Shared `core/`, `data/`, `risk/` modules; strategy implementations under `strategies/`.

**Rationale**: A folder-per-strategy pattern duplicates data fetching, order simulation, and risk calculation across every strategy. The layered approach mirrors standard OOP design — abstract base classes in `core/`, concrete implementations in `strategies/`. When `mean_reversion` is added later, it subclasses `BacktestBase` and reuses `data/` and `risk/` unchanged.

**Alternative considered**: Copy-paste from `strategy-lab` per strategy. Rejected — creates maintenance burden and diverging logic.

```
alpaca-lab/
├── core/
│   ├── backtest_base.py       ← AlpacaBacktestBase (abstract)
│   └── live_trader_base.py    ← AlpacaLiveTraderBase (abstract)
├── data/
│   └── alpaca_data.py         ← fetch_bars() via alpaca-py
├── risk/
│   └── metrics.py             ← Sharpe, drawdown, Calmar, plot
├── strategies/
│   └── momentum.py            ← CrossSectionalMomentum(BacktestBase)
├── config.py                  ← .env loading, M7 symbols, params
└── run.py                     ← CLI entry point
```

### D2: Weekly rebalance frequency

**Decision**: Rebalance every Friday (or last trading day of the week).

**Rationale**: Cross-sectional momentum signal has low turnover on daily bars — rankings rarely change day-to-day among M7. Weekly rebalancing reduces transaction costs while capturing meaningful rank shifts. Monthly is too slow for a 7-stock universe where one breakout (e.g., NVDA) can dominate. Daily introduces noise.

**Alternative considered**: Monthly. Rejected — with only 7 symbols, monthly is too coarse; a single outlier holds for too long.

### D3: Momentum signal = N-day simple return, no skip window

**Decision**: Signal = `(price[t] - price[t-N]) / price[t-N]`, no 1-month skip.

**Rationale**: The classic "12-1" skip window (skip most recent month to avoid reversal) is designed for large cross-sectional universes. With only 7 highly-correlated mega-caps, the reversal effect is less pronounced and the skip window reduces the already-small information set. Start without skip; revisit if backtest shows reversal drag.

**Alternative considered**: Log return rolling mean (Hilpisch style). Rejected in favor of simple price return — more interpretable and standard in momentum literature.

### D4: Data fetching via alpaca-py `StockHistoricalDataClient`

**Decision**: Fetch all M7 symbols in a single batched request, cache as a dict of DataFrames keyed by symbol.

**Rationale**: Alpaca's API supports multi-symbol requests natively. Fetching once at backtest start and caching avoids repeated API calls during the event loop. The backtest iterates over time index using `.iloc[bar]` slices per the Hilpisch pattern.

**Alternative considered**: Download to CSV and read locally. Acceptable for production but adds a data management step; fetch-and-cache is simpler for the first iteration.

### D5: Risk metrics in standalone `risk/metrics.py`

**Decision**: Risk calculations are pure functions operating on an equity curve (pandas Series), not methods on the backtest class.

**Rationale**: Pure functions are easier to test, reuse across strategies, and compose. The backtest `close_out()` produces the equity curve; `risk/metrics.py` consumes it. This decouples strategy logic from analytics.

### D6: Live trader uses polling loop, not WebSocket stream

**Decision**: Live paper trader runs as a scheduled weekly job — compute signal at market open Friday, submit orders, exit.

**Rationale**: Interday momentum does not require tick-level data. A simple script that runs once per week (cron or manual trigger) is far simpler than a persistent WebSocket connection. WebSocket is appropriate for intraday strategies (future work).

**Alternative considered**: `StockDataStream` WebSocket. Rejected for this change — adds complexity without benefit for weekly frequency.

## Risks / Trade-offs

- **[Lookahead bias]** → Ensure rebalance signal uses close price of day T, execute at open of day T+1 (next Friday open). The backtest must simulate this correctly.
- **[Survivorship bias]** → M7 is a backward-looking selection; all seven have survived and thrived. Backtest results will be optimistic vs. a live forward universe. Acknowledged limitation, acceptable for this learning project.
- **[Alpaca API rate limits]** → Fetching 6 years of daily bars for 7 symbols is well within free tier limits. Low risk.
- **[Paper trading order fills]** → Alpaca paper trading uses simulated fills at last trade price. May not perfectly reflect real slippage. Acceptable for paper.
- **[M7 composition drift]** → The "M7" label is recent; historical data for these tickers exists back to 2019 but their collective identity as a group did not. Backtest treats them as a static universe throughout — this is a known approximation.

## Open Questions

- **Lookback window default**: Start with 60 days (3 months)? Easy to make configurable.
- **Transaction cost simulation**: Use Alpaca's commission-free model (ptc=0, ftc=0) for paper, or simulate realistic costs (e.g., 0.1% ptc)?
- **Benchmark**: Compare equity curve against SPY buy-and-hold? Would strengthen the backtest analysis.
