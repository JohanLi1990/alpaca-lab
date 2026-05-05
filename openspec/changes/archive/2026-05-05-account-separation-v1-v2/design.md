## Context

The repository currently initializes Alpaca trading and market-data clients from one shared credential pair. This was sufficient when all strategies used one paper account, but the operating model now requires hard separation: momentum weekly live trading runs on V1, while PEAD live trading runs on V2.

The account split must be explicit in code to avoid accidental cross-account order placement. At the same time, existing backtests should remain simple and continue to use V1 credentials by default for data fetches.

## Goals / Non-Goals

**Goals:**
- Introduce a profile-aware credential model for Alpaca trading and data clients.
- Make live strategy account routing explicit and deterministic:
  - Momentum live -> v1
  - PEAD live -> v2
- Normalize V2 variable naming to `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY`.
- Preserve backward usability for backtests by defaulting data-only fetches to profile v1.
- Provide precise startup failures when required profile credentials are missing.

**Non-Goals:**
- No strategy logic changes for signal generation, ranking, or PEAD entry/exit rules.
- No migration to live-money trading accounts.
- No change to portfolio sizing formulas or transaction-cost assumptions.

## Decisions

### Decision: Introduce profile-based credential resolution
Use named profiles (`v1`, `v2`) rather than one global credential pair. Both trading and data client builders resolve keys by profile.

Rationale:
- Prevents accidental account mixing.
- Keeps flow ownership obvious and testable.
- Supports future profile expansion without redesign.

Alternatives considered:
- Process-level environment variable swapping before each script run. Rejected due to fragility and poor testability.
- Hardcoded strategy-specific keys. Rejected for security and maintainability reasons.

### Decision: Keep data-layer default profile as v1
Data fetching APIs default to profile `v1` unless caller explicitly sets another profile.

Rationale:
- Matches current backtest expectation and user preference.
- Minimizes call-site churn for non-live workflows.

Alternatives considered:
- Require explicit profile at every call site. Rejected due to unnecessary verbosity and migration burden.

### Decision: Enforce live routing at strategy entrypoints
Live momentum constructors/entrypoints pass profile `v1`; PEAD live constructors/entrypoints pass profile `v2`.

Rationale:
- Puts account selection where execution intent is defined.
- Prevents accidental fallback to wrong profile.

Alternatives considered:
- Select profile only in shared base classes by runtime mode. Rejected because mode alone cannot infer strategy ownership.

### Decision: Normalize V2 env names to API_KEY_ID format
Adopt `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY` for consistency with V1 naming and existing Alpaca naming style.

Rationale:
- Reduces confusion and avoids conditional naming logic.

Alternatives considered:
- Keep `V2_APCA_API_KEY` while introducing alias handling. Rejected to avoid long-term ambiguity.

## Risks / Trade-offs

- [Risk] Profile defaults could hide missing explicit routing in new live flows.
  Mitigation: Require explicit profile in live trader constructors and add tests asserting v1/v2 routing.

- [Risk] Environment migration mistakes (old V2 variable name still present).
  Mitigation: Add clear startup validation and error text naming the exact missing variables.

- [Risk] PEAD live and PEAD training/fallback data fetches may need different profiles over time.
  Mitigation: Keep data APIs profile-overridable so call sites can opt into v2 explicitly where needed.

## Migration Plan

1. Add profile-aware credential resolvers for trading and data clients.
2. Update live strategy constructors and script entrypoints to pass explicit profiles.
3. Update environment documentation and examples to use `V2_APCA_API_KEY_ID`.
4. Add/adjust tests for default-v1 data behavior and live routing behavior.
5. Deploy with both V1 and V2 credentials present and verify account-specific order placement in paper dashboards.

Rollback:
- Revert to prior shared-credential behavior by removing profile arguments and restoring single-variable resolution.
- Keep previous .env key names only if rollback requires temporary compatibility.

## Open Questions

- Should PEAD classifier fallback training in live mode continue to use default v1 data or explicitly use v2 for consistency with PEAD live execution?
- Should we keep temporary compatibility aliases for the legacy `V2_APCA_API_KEY` name during one transition release?
