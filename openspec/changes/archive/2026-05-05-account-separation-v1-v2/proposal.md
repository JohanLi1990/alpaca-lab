## Why

The project now runs two distinct paper accounts: V1 for momentum and V2 for PEAD. Today, live trading and data clients still rely on one shared credential pair, which risks sending orders to the wrong account and makes strategy isolation fragile.

## What Changes

- Introduce profile-aware Alpaca credential resolution for both trading and data clients.
- Enforce strategy-to-profile mapping in live flows:
  - Momentum weekly live rebalance uses profile v1.
  - PEAD live cronjob uses profile v2.
- Normalize V2 environment variable naming to `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY`.
- Keep backtests and general data-only fetches on default profile v1 unless explicitly overridden.
- Add validation and error messages that clearly identify missing profile-specific credentials.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `data-layer`: Add profile-aware data client authentication with default v1 behavior for backtests and data-only fetches.
- `live-trader`: Add profile-aware trading client authentication and require momentum live flow to use v1 credentials.
- `pead-live-trader`: Require PEAD live flow to use v2 credentials and preserve existing PEAD execution behavior.

## Impact

- Affected code:
  - Credential loading and client creation in core live trading base and data layer.
  - Live entrypoints and strategy constructors for momentum and PEAD.
  - Environment configuration documentation and startup validation.
  - Tests covering credential resolution and live profile routing.
- External systems:
  - Alpaca paper accounts for V1 and V2.
- Operational impact:
  - Reduces cross-strategy account contamination risk and makes account ownership explicit by flow.
