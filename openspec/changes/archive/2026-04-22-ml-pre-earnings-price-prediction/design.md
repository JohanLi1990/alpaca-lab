## Context

The repo currently implements a weekly cross-sectional momentum strategy backed by a generic event-driven backtest engine (`core/backtest_base.py`) and an Alpaca daily-bar data layer (`data/alpaca_data.py`). Both are rule-based and calendar-driven (Monday/Friday rebalances). There is no event-conditioned or ML-driven logic anywhere.

This change introduces a new, orthogonal strategy family: a binary classifier trained on pre-earnings features (T-7 to T-1 daily bars) to predict whether the earnings reaction gap from T-1 close to T open will be positive. The initial scope is GOOGL, after-market-close events only, every-event evaluation first, with a confidence-threshold filter introduced in a second phase.

## Goals / Non-Goals

**Goals:**
- Build a reproducible, leak-proof ML pipeline: event table → features → walk-forward classifier → event-level backtest → risk summary.
- Keep the existing momentum strategy, backtest engine, and live trader completely untouched.
- Establish a science-grade evaluation protocol (walk-forward by event time, not random split) so results can be trusted for further iteration.
- Produce a `pead-backtest` run mode that can be invoked alongside existing modes without conflict.

**Non-Goals:**
- Live or paper trading of the PEAD signal (Phase 1 is research-only).
- Expanding beyond GOOGL or beyond after-close events in this change.
- Deep learning or LLM-based models.
- Intraday (minute-bar) feature engineering.
- Surprise factor or analyst estimate data.

## Decisions

### Decision: yfinance as earnings calendar source
**Choice**: Use `yfinance.Ticker("GOOGL").get_earnings_dates()` as the primary event calendar.

**Alternatives considered**:
- Alpaca's own calendar API — does not surface earnings timestamps.
- Google Investor Relations scraping — accurate but fragile, requires Selenium/BeautifulSoup; suitable only as a spot-check verification layer.
- Paid data vendors (e.g. Refinitiv, Bloomberg) — out of scope for this repo.

**Rationale**: `yfinance` is already in `environment.yml`, returns structured dates back several years, and is sufficient for a single-ticker research prototype. AMC/BMO classification is derived from the release time field. Events with ambiguous timestamps are excluded.

### Decision: Feature window is T-7 to T-1 daily bars only
**Choice**: Engineer all features exclusively from the 7 trading days preceding each earnings date using daily OHLCV bars fetched via the existing `fetch_bars` function.

**Alternatives considered**:
- Minute bars for intraday open/close pressure — materially more complex, adds latency on data fetch, not needed for phase 1 hypothesis test.
- Longer lookback (T-20, T-60) — adds context but also noise from non-earnings macro moves.

**Rationale**: The core hypothesis is specifically about pre-earnings informed flow, so the 7-day window is both theoretically motivated and small enough to avoid confounding with broader macro drift. Features include: cumulative return, daily return slope, downside-day concentration, relative volume vs 20-day baseline, ATR expansion, and stock-minus-QQQ relative return. All features are computed from information available at T-1 close with no forward-looking fields.

### Decision: Walk-forward event-level split — no random shuffle
**Choice**: Order all events chronologically. Train on events [0..N], test on event [N+1]. Expand window forward (expanding window walk-forward). Minimum training window: 20 events.

**Alternatives considered**:
- Random train/test split — standard for i.i.d. data but introduces look-ahead bias for financial time series.
- K-fold cross-validation — same bias problem plus events are not i.i.d.
- Fixed rolling window (train on last 20, test on next 1) — avoids stale data but reduces effective training size early on.

**Rationale**: Event-level walk-forward is the only protocol that matches production behavior (you never know future events when trading). Expanding window is preferred over rolling for this sample size (~40–60 GOOGL events since 2018) because rolling window training sets would be too small at the start.

### Decision: Logistic regression as Phase 1 baseline, XGBoost as Phase 2
**Choice**: Phase 1 uses `sklearn.linear_model.LogisticRegression` with standardized features. Phase 2 adds `xgboost.XGBClassifier` for non-linear interactions.

**Alternatives considered**:
- Random forest — good but less interpretable; reserve for Phase 2.
- Neural nets — no theoretical advantage over GBTs with this sample size (~40–60 rows).

**Rationale**: Logistic regression coefficients directly validate whether the feature story (downward pressure → positive gap, stretched run-up → negative gap) is reflected in the weights. If LR already has edge, that is a strong signal. XGBoost is added in Phase 2 to capture non-linear interactions (e.g. high drift AND high volume AND compressed price).

### Decision: Target label is binary sign of T-1 close to T open gap
**Choice**: `y = 1` if `open(T) / close(T-1) - 1 > 0.0`, else `y = 0`. Also compute continuous gap return for EV analysis.

**Alternatives considered**:
- Regression target (predict gap magnitude) — harder to calibrate for a threshold decision; binary classification better matches the go/no-go trading decision.
- Three-class (positive/flat/negative) — flat zone is ambiguous; start binary and extend if needed.

**Rationale**: The trading decision is binary: enter at T-1 close or not. The continuous gap return is computed alongside but only used for economic evaluation (average return per trade, not as training label).

### Decision: Entry at T-1 close, exit at T open
**Choice**: Simulate overnight position: buy at T-1 close, sell at T open. Transaction costs applied at both legs.

**Rationale**: This captures exactly the overnight gap the model predicts. T-close exit (hold through T trading session) is reserved for Phase 2 when continuation signal has been separately validated.

## Risks / Trade-offs

- **Small sample size (~40 GOOGL events from 2016–2025)** → Starting from 2016 gives approximately 40 events (10 years × 4 per year). With a 20-event minimum training window, ~20 events are available out-of-sample — roughly double what a 2018 start would yield (~12). Early walk-forward folds still have limited training points. Mitigate by reporting confidence intervals around hit rate. Accept that strong conclusions require a larger symbol universe (Phase 3).

- **yfinance AMC/BMO timestamps may be imprecise or missing** → Mitigate by excluding events with null or ambiguous time fields and spot-checking against GOOGL investor relations page. Log excluded event count.

- **Look-ahead bias in feature computation** → Mitigate by asserting that every feature references only `df.loc[:earnings_date - 1_trading_day]` slices. Add unit test that verifies feature vector date range does not touch or exceed T.

- **Overfitting to GOOGL-specific behaviour** → By design for Phase 1. Mitigation is not to scale up to production until out-of-sample walk-forward results are stable.

- **Gap-based exit ignores post-open continuation or reversal** → Phase 1 intentionally ignores intraday behaviour. If gap capture is positive, Phase 2 can test holding through T close.

## Open Questions

- What is the precise cutoff for classifying an event as AMC vs BMO? (e.g., release time after 16:00 ET = AMC). Needs to be codified in `earnings_calendar.py`.
- Should the T-open exit use the official Alpaca opening price or a 5-minute VWAP to reduce microstructure noise? Decision deferred to implementation.
- Is the 20-event minimum training window sufficient, or should it be pushed to 25? With ~40 events from 2016–2025, a 20-event seed leaves ~20 out-of-sample; pushing to 25 would reduce that to ~15. Revisit after confirming exact event count from yfinance.
