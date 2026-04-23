## Why

Informed order-flow in the 7 trading days before an earnings announcement leaves measurable footprints in price and volume behaviour. By training a machine learning classifier on those pre-event features we can predict whether the gap between T-1 close and T open will be positive, allowing a low-frequency, overnight entry at T-1 close that captures the earnings reaction before it fully prices in. The current repo contains only rule-based weekly momentum; this change adds the first ML-driven, event-conditioned strategy.

## What Changes

- New data module to fetch GOOGL earnings event dates and AMC/BMO timing via `yfinance`.
- New feature-engineering pipeline that constructs T-7 to T-1 pre-earnings features (price drift, volume behaviour, volatility regime, relative-to-index metrics) from Alpaca daily bars.
- New ML training and evaluation pipeline: walk-forward, event-level cross-validation using scikit-learn or XGBoost-family classifiers.
- New event-driven backtest that enters at T-1 close and exits at T open (Phase 1) or T close (Phase 2) based on classifier signal.
- New run mode `python run.py --mode pead-backtest` to execute the full pipeline end-to-end.
- New confidence-threshold filter applied on top of the base classifier to improve per-trade expectancy (Phase 2).

## Capabilities

### New Capabilities

- `earnings-calendar`: Fetch, validate, and cache earnings event dates with AMC/BMO timing for a given symbol using `yfinance`. Produces a structured event table as the source of truth for all downstream pipeline stages.
- `pre-earnings-features`: Engineer pre-event feature vectors from T-7 to T-1 daily OHLCV bars per earnings event. Features cover price drift shape, volume pressure, volatility regime, and relative-to-benchmark behaviour.
- `ml-classifier`: Train and evaluate a binary classifier (positive gap vs non-positive gap) using walk-forward, event-level splits. Supports baseline logistic regression and gradient-boosted tree models. Reports hit rate, expectancy, and calibration diagnostics.
- `pead-backtest`: Event-driven backtest that uses the classifier signal (and optional confidence threshold) to simulate overnight entries at T-1 close and exits at T open or T close. Produces an equity curve and risk summary consistent with existing `risk.metrics` standards.

### Modified Capabilities

- `data-layer`: Add support for fetching daily bars keyed by event date windows (T-N to T-1 slices) to serve the feature-engineering pipeline. No breaking changes to existing `fetch_bars` signature.

## Impact

- New dependencies already present in `environment.yml`: `yfinance`, `scikit-learn`-compatible libs, `xgboost` or similar (via existing pip installs).
- New files: `data/earnings_calendar.py`, `data/pre_earnings_features.py`, `strategies/pead_classifier.py`, `strategies/pead_backtest.py`.
- `run.py` gains a new `--mode pead-backtest` branch; existing `backtest` and `live` modes are unchanged.
- No changes to `core/backtest_base.py` or `core/live_trader_base.py` public interfaces.
- No changes to existing momentum strategy or its specs.
