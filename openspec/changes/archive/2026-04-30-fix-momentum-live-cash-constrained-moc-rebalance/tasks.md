## 1. Rebalance Logic

- [x] 1.1 Update `LiveMomentumTrader.rebalance()` to preserve ranked targets, identify dropped holdings, and submit sells for dropped symbols regardless of unrealized PnL.
- [x] 1.2 Change live buy-budget calculation to use only currently available cash, excluding same-day MOC sale proceeds and excluding positions marked for sale from capital-cap accounting.
- [x] 1.3 Implement rank-ordered new-entry buys using remaining cash divided across remaining buy slots, and log explicit insufficient-cash skips when fewer than one whole share can be purchased.

## 2. Focused Validation

- [x] 2.1 Add or update tests covering sell-first behavior, rank-ordered replacement buys, and insufficient-cash skip logging.
- [x] 2.2 Add or update tests covering capital-cap accounting that ignores positions already scheduled to exit.
- [x] 2.3 Run the relevant momentum and live-rebalance test slice and confirm the new behavior passes.