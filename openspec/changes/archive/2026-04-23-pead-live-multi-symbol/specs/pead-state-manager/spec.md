## ADDED Requirements

### Requirement: State file structure and initialization

The state file (`output/pead_live_state.json`) SHALL be a JSON document tracking current open positions per symbol. Structure: `{symbol: {earnings_date, entry_date, entry_price, entry_qty, created_at}}`. The state file SHALL be initialized as empty on first run or if no positions are open.

#### Scenario: Load state file on startup
- **WHEN** cronjob starts and state file exists
- **THEN** system SHALL read and parse the JSON file; if parsing fails, log error and treat as empty state

#### Scenario: Initialize state file if missing
- **WHEN** state file does not exist
- **THEN** system SHALL create an empty state file `{}`

#### Scenario: State structure for single open position
- **WHEN** one symbol has an open position for current earnings event
- **THEN** state file SHALL contain: `{"NXPI": {"earnings_date": "2026-04-30", "entry_date": "2026-04-27", "entry_price": 125.50, "entry_qty": 80, "created_at": "2026-04-27T16:00:00Z"}}`

#### Scenario: State structure for multiple open positions
- **WHEN** multiple symbols have open positions simultaneously
- **THEN** state file SHALL contain entries for each symbol independently: `{"NXPI": {...}, "AMD": {...}, "AVGO": {...}}`

### Requirement: Record new position state on entry

When an entry order executes, the system SHALL write a new state entry with entry details and timestamp.

#### Scenario: Write entry state after buy order
- **WHEN** entry market order executes on T-3
- **THEN** system SHALL append/update state entry: `state[symbol] = {earnings_date, entry_date: today, entry_price: filled_price, entry_qty: filled_qty, created_at: timestamp}`

#### Scenario: Entry state persists until exit
- **WHEN** entry state is recorded and position is held through T+1
- **THEN** state entry SHALL remain in the state file until exit order executes

### Requirement: Idempotency check before entry

Before placing an entry order, the system SHALL check if a position already exists for this symbol and earnings date, and skip if already present.

#### Scenario: Skip entry if already in state
- **WHEN** cronjob runs on T-3 AND symbol already exists in state file with the same earnings_date
- **THEN** system SHALL not place another BUY order; record as "skipped (already entered)"

#### Scenario: Allow entry if earnings event is different
- **WHEN** cronjob runs on T-3 for earnings event E2 AND symbol exists in state but for a previous earnings event E1
- **THEN** this would indicate a failed exit (shouldn't happen); log warning and do not enter (state cleanup required manually)

### Requirement: Delete state entry on position exit

After a position exits, the system SHALL delete the corresponding state entry, resetting to clean slate for the next earnings event.

#### Scenario: Delete entry on successful exit
- **WHEN** exit market order executes on T+1
- **THEN** system SHALL delete `state[symbol]`, leaving state file clean for next earnings event

#### Scenario: Clean state for future events
- **WHEN** position is exited and state entry is deleted
- **THEN** next earnings event for the same symbol can re-enter without interference

### Requirement: Auto-cleanup of stale state entries

The system SHALL automatically remove state entries older than 30 days, in case a position was never exited (e.g., due to manual intervention or error).

#### Scenario: Cleanup entries older than 30 days
- **WHEN** cronjob runs and detects a state entry with created_at timestamp > 30 days ago
- **THEN** system SHALL delete that entry, log warning: "Cleaned up stale NXPI position from 2026-03-25"

#### Scenario: Do not cleanup recent entries
- **WHEN** state entry has created_at < 30 days ago
- **THEN** entry SHALL remain in the state file

### Requirement: Atomic read-modify-write for state file

State file operations (read, check, update, write) SHALL be performed atomically to prevent corruption or lost updates if multiple cronjobs run simultaneously.

#### Scenario: Atomic entry write
- **WHEN** placing an entry order
- **THEN** system SHALL: load state file, check if symbol exists, add/update entry, write atomically (not partial writes)

#### Scenario: Atomic entry delete
- **WHEN** exiting a position
- **THEN** system SHALL: load state file, delete symbol entry, write atomically

#### Scenario: Handle concurrent writes
- **WHEN** two cronjob instances try to update state simultaneously
- **THEN** system SHALL use file locking or atomic operations to ensure one write completes before the other starts (no corruption)

### Requirement: Human-readable state file format

The state file format SHALL be plain JSON, suitable for manual inspection and debugging.

#### Scenario: State file is readable without special tools
- **WHEN** cronjob writes state file
- **THEN** a human can open the file in a text editor and understand the current position(s)

#### Scenario: Pretty-printed JSON for clarity
- **WHEN** state file is written
- **THEN** JSON SHALL be formatted with indentation (not minified) for readability
