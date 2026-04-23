## Context

The current PEAD research path is built around a single GOOGL pipeline that classifies the sign of the T-1-close to T-open gap, computes features from the 7 trading days ending at T-1, and backtests an overnight trade that enters at T-1 close and exits at T open. The user wants to test a timing variant that enters earlier at T-3 close and exits later at either T+1 open or T+1 close, while otherwise keeping the ML workflow and feature set conceptually the same.

The main constraint is lookahead bias. A T-3 entry cannot legally use T-2 or T-1 data in feature computation. The design therefore needs to separate feature availability from execution timing while keeping the current PEAD pipeline recognizable and small enough to implement quickly.

## Goals / Non-Goals

**Goals:**
- Preserve the existing single-symbol GOOGL PEAD workflow and logistic-regression walk-forward structure.
- Shift the feature availability cutoff so the new T-3 entry remains free of lookahead bias.
- Support two configurable exits for the timing variant: T+1 open and T+1 close.
- Report benchmark metrics that compare model-gated trades against always-buy trades over the same evaluated events and holding window.

**Non-Goals:**
- Changing the earnings calendar source or event classification rules.
- Expanding to multi-symbol PEAD research in this change.
- Redefining the classifier target to the new T-3 to T+1 holding horizon.
- Adding a new model family or changing walk-forward training logic.

## Decisions

### Decision: Shift feature windows to end at T-3 close

**Choice:** Recompute the 7-day feature window as the 7 trading days ending at T-3 close, which effectively shifts the window from T-7..T-1 to T-9..T-3 while keeping the feature count and formulas intact.

**Alternatives considered:**
- Keep the current T-7..T-1 feature window. Rejected because T-2 and T-1 would be unavailable at a T-3 entry decision, creating lookahead bias.
- Shorten the window to T-7..T-3. Rejected because it changes the semantic meaning of the 7-day feature set and makes results harder to compare with the current strategy.

**Rationale:** This is the smallest safe change that preserves the existing feature definitions while moving the decision point earlier.

### Decision: Preserve the current classifier objective for this experiment

**Choice:** Keep the current classifier machinery and label structure intact for this change, and use the new execution timing as a PEAD strategy variant rather than redefining the learning target.

**Alternatives considered:**
- Redefine the label to predict T-3-close to T+1-open or T+1-close returns. Rejected for this change because the user selected the lower-scope path and the extra label redesign would broaden the experiment materially.

**Rationale:** The user explicitly chose the pragmatic variant first. This keeps scope small and makes it possible to test whether the current signal still adds value when traded over a longer window.

### Decision: Derive T-3 and T+1 from the bar index, not the earnings calendar schema

**Choice:** Continue using `earnings_date` and `t_minus_1` from the earnings event table, and derive T-3 and T+1 by walking the symbol's daily bar index inside feature engineering and backtest logic.

**Alternatives considered:**
- Extend the earnings calendar module to precompute `t_minus_3` and `t_plus_1`. Rejected because those values are only needed by this strategy variant and can be derived from already-fetched bars.

**Rationale:** This keeps the earnings calendar capability stable and localizes timing logic to the PEAD research path.

### Decision: Put always-buy benchmark reporting in the PEAD backtest layer

**Choice:** Compute and print always-buy benchmark metrics in the PEAD strategy/backtest/reporting flow using the same evaluated events, entry date, exit date, and transaction cost assumptions as the model-gated strategy.

**Alternatives considered:**
- Add the benchmark to the classifier evaluation helper. Rejected because the benchmark depends on the configured execution horizon, which is strategy-specific rather than classifier-generic.

**Rationale:** The comparison the user wants is about trade execution, not only label classification quality.

## Risks / Trade-offs

- **[Label/execution mismatch]** The classifier still predicts the original PEAD label while the executed trade holds a longer window. → Mitigation: document this explicitly in logs and specs as an exploratory timing variant, and keep the change scoped so a later proposal can realign the label if needed.
- **[More exposure to non-earnings market noise]** T-3 to T+1 holds the position across more non-event price movement than the original overnight trade. → Mitigation: compare against an always-buy baseline over the exact same horizon.
- **[Date derivation edge cases]** Holidays or missing bars can make T-3 or T+1 unavailable for specific events. → Mitigation: skip affected events with a warning and keep benchmark/model comparisons on the same evaluated subset.

## Migration Plan

1. Update PEAD configuration to expose entry and exit timing controls for this variant.
2. Shift feature window computation to the last 7 trading days ending at T-3.
3. Extend the PEAD backtest to derive T-3 and T+1 dates from bars and support both configured exit modes.
4. Add always-buy benchmark summary output to the PEAD run path.
5. Validate the variant on GOOGL and compare reported metrics for T+1 open versus T+1 close.

## Open Questions

- Which exit should be the default for `pead-backtest`: T+1 open, T+1 close, or a configurable switch with no default change?
- Should the logs report both exit horizons in one run, or should each run evaluate only one configured horizon?