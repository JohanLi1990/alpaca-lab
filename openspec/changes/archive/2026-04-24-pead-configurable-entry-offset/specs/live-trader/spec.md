## MODIFIED Requirements

### Requirement: Weekly rebalance trigger
The PEAD live execution flow SHALL evaluate entry for each symbol using configurable entry offset `PEAD_ENTRY_OFFSET_DAYS`, where entry date is `T-E` and required feature bars are available by `T-(E+1)` close. The system SHALL NOT attempt entry prediction when the required anchor bar is not yet available, and SHALL log an explicit skip reason.

#### Scenario: Entry evaluated with available anchor bars
- **WHEN** live execution runs for symbol S and all bars through `T-(E+1)` are available
- **THEN** prediction is computed and entry order logic is evaluated for date `T-E`

#### Scenario: Entry skipped when anchor bar unavailable
- **WHEN** live execution runs before the required anchor bar has finalized for symbol S
- **THEN** no prediction or order is attempted for that symbol and logs record `missing feature-anchor bar`

#### Scenario: Existing order safety behavior preserved
- **WHEN** live execution runs outside supported order timing or data preconditions
- **THEN** no new entry order is submitted
