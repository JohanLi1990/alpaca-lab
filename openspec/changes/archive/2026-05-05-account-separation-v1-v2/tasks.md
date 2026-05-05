## 1. Credential Profile Foundation

- [x] 1.1 Add a shared credential-resolution utility that maps profile `v1` and `v2` to profile-prefixed environment variables and raises clear errors on missing keys.
- [x] 1.2 Normalize environment handling to use `V2_APCA_API_KEY_ID` and `V2_APCA_API_SECRET_KEY` for V2.
- [x] 1.3 Add unit tests for profile resolution success and missing-variable failure paths.

## 2. Data Layer Profile Routing

- [x] 2.1 Update data client construction to accept a profile parameter and default to `v1` when omitted.
- [x] 2.2 Extend `fetch_bars()` and related internal helpers to pass profile through to authentication.
- [x] 2.3 Add tests verifying default `v1` data fetch behavior and explicit `v2` profile behavior.

## 3. Live Trader Profile Routing

- [x] 3.1 Update the live trader base class to accept a required profile for live strategy initialization and use profile-specific trading credentials.
- [x] 3.2 Update `LiveMomentumTrader` and momentum live entrypoints to pass profile `v1` explicitly.
- [x] 3.3 Update `PEADLiveTrader` and PEAD live entrypoints to pass profile `v2` explicitly.
- [x] 3.4 Add tests asserting momentum routes to v1 and PEAD routes to v2, including missing-credential fail-fast behavior.

## 4. Backtest Compatibility and Call-Site Audit

- [x] 4.1 Verify backtest and data-only call sites continue to use implicit default `v1` profile without behavior regression.
- [x] 4.2 Audit PEAD live data-fetch call sites and apply explicit `v2` only where intended, leaving non-live training/backtest flows on default `v1`.
- [x] 4.3 Confirm no remaining live path depends on legacy shared `APCA_API_KEY_ID` variables.

## 5. Documentation and Operational Readiness

- [x] 5.1 Update `.env` examples and README instructions to document V1/V2 profile variables and account ownership by strategy.
- [x] 5.2 Add a migration note for renaming V2 key variable from `V2_APCA_API_KEY` to `V2_APCA_API_KEY_ID`.
- [x] 5.3 Run targeted tests and one dry-run startup check for both live entrypoints to validate profile wiring before deployment.
