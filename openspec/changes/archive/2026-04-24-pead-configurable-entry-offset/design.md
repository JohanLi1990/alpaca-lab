## Context

The PEAD system currently mixes a fixed T-3 entry concept with daily-bar availability constraints. In live mode, when the job runs before a T-3 daily bar is finalized, feature generation can fail because the required anchor bar is absent. This surfaced as event drops for near-term earnings symbols.

The user wants two things:
1. A coherent timing model for T-3 open entry, which implies features must stop at T-4 close (window T-10..T-4).
2. Configurable entry offsets so strategy variants (T-4, T-5, etc.) can be tested without code rewrites.

This change introduces one timing contract used by both backtest and live: entry offset is configurable, and feature window is derived from offset deterministically.

## Goals / Non-Goals

**Goals:**
- Define a single timing model shared by backtest and live PEAD flows.
- Support configurable entry offsets through config, with offset-specific feature windows.
- Eliminate impossible decision timing (for example requiring a bar that does not exist yet at decision time).
- Preserve classifier pipeline compatibility by keeping feature names stable while changing date anchoring.
- Make runtime behavior explicit in logs and docs.

**Non-Goals:**
- Re-architecting the model family or introducing a new model type.
- Introducing intraday minute-bar feature engineering in this change.
- Implementing full hyperparameter/offset grid optimization tooling.

## Decisions

1. Decision: Introduce config-driven entry offset as the source of truth.
- Choice: Add PEAD entry offset config values and propagate through feature builder, backtest, and live execution.
- Why: Hardcoded timing creates fragile behavior and blocks strategy iteration.
- Alternative considered: Keep fixed T-3 and add ad-hoc exceptions in live mode.
- Why rejected: Preserves incoherent semantics and accumulates timing bugs.

2. Decision: Define feature window relative to entry offset, not fixed named dates.
- Choice: For entry offset E (positive integer days before earnings), feature window is 7 trading days ending at E+1 (for T-3 open, end at T-4; window T-10..T-4).
- Why: Guarantees every feature bar is known before entry execution.
- Alternative considered: Keep T-3 feature anchor and delay decisions until next day.
- Why rejected: Violates intended entry timing and produces post-hoc decisions.

3. Decision: Use open-entry semantics in backtest/live for offset-driven entry day.
- Choice: Entry execution uses entry-day open price, with exit mode remaining configurable (T+1 open/close).
- Why: Aligns with user intent for "decide at T-3 open" and avoids requiring same-day close data.
- Alternative considered: Entry-at-close semantics with post-close trigger.
- Why rejected: Contradicts requested timing variant and daytime cron usage.

4. Decision: Keep data-layer daily fetch inclusive and avoid dropping first bar in requested range.
- Choice: Maintain inclusive end-date fetch and preserve OHLCV rows even if return is NaN on first row.
- Why: Offset-derived windows require precise boundaries; dropping a boundary bar causes false "missing bar" failures.
- Alternative considered: Compute returns externally and keep current drop behavior.
- Why rejected: Unnecessary complexity and repeated edge-case handling downstream.

## Risks / Trade-offs

- [Risk] Timing model changes alter historical backtest performance and comparability with archived results.
  -> Mitigation: Log entry offset and derived window dates for each run; document baseline shift in README.

- [Risk] Offset generalization can introduce off-by-one errors around holidays.
  -> Mitigation: Centralize offset date derivation in `data/pead_calendar.py` and add unit tests for known holiday weeks.

- [Risk] Existing trained models may degrade if retrained under new timing semantics.
  -> Mitigation: Keep model artifact versioning and include a retrain step in tasks after timing migration.

- [Risk] Different data plans (IEX/SIP limits) can still cause missing-recent-bar errors.
  -> Mitigation: Keep descriptive logging and explicit skip reasons; document required market-data subscription behavior.
