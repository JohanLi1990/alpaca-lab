## Context

The live momentum trader submits Market-on-Close orders to match the backtest's close-execution assumption, but the current rebalance logic sizes buys from the account cash snapshot without distinguishing between already-available cash and proceeds from same-day MOC sells. As a result, replacement buys can be silently skipped or sized inconsistently, and buy priority across multiple new entries is undefined.

The change is confined to the weekly live momentum rebalance flow. It does not alter the signal definition, the MOC execution choice, or the rule that dropped symbols are sold regardless of unrealized gain or loss.

## Goals / Non-Goals

**Goals:**
- Keep MOC orders as the live execution model.
- Define a deterministic rebalance flow that always sells dropped symbols and funds new buys only from cash available before the close.
- Preserve momentum rank order when multiple new entries compete for limited cash.
- Make skipped buys and capital-cap behavior explicit in logs.

**Non-Goals:**
- Changing live execution from MOC to DAY orders.
- Reusing same-day MOC sale proceeds for new buys.
- Adding loss-aware sell filters or partial-position resizing.
- Changing the backtest strategy semantics.

## Decisions

### Decision: Treat same-day MOC sale proceeds as unavailable for buys

The rebalance will submit sells first for dropped symbols, but the buy budget will be computed strictly from currently available account cash. Same-day MOC sale proceeds are excluded because they are not available until the close.

Alternatives considered:
- Assume sell proceeds are reusable in the same rebalance run. Rejected because it conflicts with MOC timing.
- Switch to DAY orders so proceeds may become available sooner. Rejected because the change intent is to keep close-price execution.

### Decision: Buy only new entries and process them in signal rank order

The rebalance will preserve the ranked target list returned by the signal and iterate new entries in that order. This gives deterministic behavior when available cash can fund only a subset of replacements.

Alternatives considered:
- Convert targets to a set and lose ordering. Rejected because buy priority becomes arbitrary.
- Split cash equally across all targets, including symbols already held. Rejected because unchanged holdings are not resized in this live model.

### Decision: Allocate remaining cash progressively across remaining buy slots

For each new entry in rank order, the trader will compute a per-symbol budget from remaining buy cash divided by remaining unfunded entries. This preserves rank priority without overcommitting the first symbol.

Alternatives considered:
- Spend all remaining cash on the highest-ranked new entry. Rejected because it over-concentrates replacement buys.
- Precompute fixed equal allocations before filtering skipped names. Rejected because later entries would not benefit from cash released by earlier skips.

### Decision: Capital-cap accounting excludes positions already marked for sale

When `max_capital` is set, the trader will estimate currently retained exposure using only positions that remain in the target set. Positions already marked for sale will not count against the remaining budget.

Alternatives considered:
- Count all currently held strategy positions, including outgoing names. Rejected because it artificially suppresses buys during rotations.

### Decision: Log skipped buys explicitly

If remaining buy budget cannot fund at least one share of a target symbol, the trader will skip the order and write an explicit log entry with symbol, reference price, and remaining cash.

Alternatives considered:
- Silently skip zero-quantity buys. Rejected because it obscures whether skipped entries were intentional or a bug.

## Risks / Trade-offs

- Cash-constrained rotations may leave the portfolio temporarily underinvested -> This is accepted as the correct consequence of keeping MOC and refusing to rely on same-day sale proceeds.
- Using recent close prices for share sizing can differ slightly from the closing-auction fill -> Existing MOC design already accepts this approximation for order sizing.
- Rank-priority buys may still leave lower-ranked targets unfunded for a week -> Explicit logging will make these tradeoffs visible for later tuning.

## Migration Plan

1. Update live momentum rebalance logic to preserve ranked targets, compute retained exposure, and process new buys from available cash only.
2. Add or update focused tests covering sell-first behavior, rank-ordered buys, capital-cap accounting, and explicit skipped-buy logging.
3. Run the weekly rebalance test slice and any momentum-specific unit tests.
4. Deploy with no config migration; rollback is limited to restoring the prior rebalance method.

## Open Questions

None.