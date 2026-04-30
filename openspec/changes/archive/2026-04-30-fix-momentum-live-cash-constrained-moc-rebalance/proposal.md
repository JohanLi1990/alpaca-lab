## Why

The live momentum rebalance currently submits MOC sells and then sizes buys from the account cash snapshot taken before the close. This can skip legitimate replacement buys because same-day MOC sale proceeds are not available yet, while also obscuring the intended buy-priority and skip behavior.

## What Changes

- Clarify that the live momentum rebalance treats same-day MOC sale proceeds as unavailable for new buys.
- Preserve the existing behavior that dropped symbols are sold regardless of gain or loss.
- Define buy selection for new target entries using momentum rank order and only currently available cash.
- Require explicit logging when a target buy is skipped because cash is insufficient to purchase at least one share.
- Clarify that capital-cap calculations exclude positions already marked for sale and apply only to retained holdings plus new buys.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `momentum-strategy`: Change live rebalance behavior so new entries are funded only from currently available cash, prioritized by momentum rank, while dropped holdings are always sold.
- `live-trader`: Clarify how MOC order timing interacts with rebalance cash availability, buy skipping, and capital-cap accounting.

## Impact

- Affected code: `strategies/momentum.py`, and potentially shared live-order helper logic in `core/live_trader_base.py` if logging or position metadata access needs adjustment.
- Affected behavior: weekly live M7 rebalance order generation, skipped-buy logging, and capital-cap accounting.
- No new external dependencies or APIs.