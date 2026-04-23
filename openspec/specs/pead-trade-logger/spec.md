## ADDED Requirements

### Requirement: Trade log file structure and initialization

The trade log (`output/pead_live_trades.csv`) SHALL be an append-only CSV file with columns: symbol, earnings_date, entry_date, exit_date, entry_price, exit_price, qty, pnl, pnl_pct, timestamp. The file SHALL be initialized with a header row on first write if it does not exist.

#### Scenario: Initialize trade log with header
- **WHEN** trade log does not exist and first trade is recorded
- **THEN** system SHALL create the file with header row: `symbol,earnings_date,entry_date,exit_date,entry_price,exit_price,qty,pnl,pnl_pct,timestamp`

#### Scenario: Load existing trade log
- **WHEN** trade log already exists
- **THEN** system SHALL append new trades to the existing file, preserving all previous records

#### Scenario: Trade log structure for single trade
- **WHEN** one trade completes (entry + exit)
- **THEN** trade log SHALL contain one row with all fields populated: `NXPI,2026-04-30,2026-04-27,2026-04-28,125.50,128.60,80,240.00,0.0238,2026-04-28T16:00:00Z`

### Requirement: Record trade entry event

When an entry order executes, the system SHALL begin recording trade details (capture symbol, earnings_date, entry_date, entry_price, entry_qty).

#### Scenario: Capture entry details on order execution
- **WHEN** entry market order executes on T-3
- **THEN** system SHALL store: symbol, earnings_date, entry_date=today, entry_price=filled_price, qty=filled_qty, entry_timestamp

#### Scenario: Hold entry details until exit
- **WHEN** entry is recorded and position held through T+1
- **THEN** entry details SHALL be retained in memory or temporary state, waiting for exit to complete the trade record

### Requirement: Record trade exit and compute PnL

When an exit order executes on T+1+, the system SHALL complete the trade record by adding exit details and computed PnL, then append one row to the trade log CSV.

#### Scenario: Capture exit details on order execution
- **WHEN** exit market order executes on T+1
- **THEN** system SHALL capture: exit_date=today, exit_price=filled_price, exit_timestamp

#### Scenario: Compute net PnL with transaction costs
- **WHEN** exit order executes
- **THEN** system SHALL compute:
  - gross_pnl_pct = (exit_price - entry_price) / entry_price
  - net_pnl_pct = gross_pnl_pct - 0.002 (entry cost 0.1% + exit cost 0.1%)
  - pnl_dollars = net_pnl_pct * entry_price * qty

#### Scenario: Append completed trade to log
- **WHEN** all trade details and PnL are computed
- **THEN** system SHALL append one row to the CSV file: `symbol,earnings_date,entry_date,exit_date,entry_price,exit_price,qty,pnl,pnl_pct,timestamp`

#### Scenario: Trade log records multiple trades chronologically
- **WHEN** multiple trades complete over time
- **THEN** trade log SHALL contain multiple rows (one per trade), appended in chronological order of exit timestamp

### Requirement: Append-only semantics for trade log

The trade log SHALL never be modified or overwritten once written. All operations are append-only to maintain audit trail integrity.

#### Scenario: Append new trade without modifying existing records
- **WHEN** a new trade completes and is logged
- **THEN** system SHALL append a new row; no existing rows are modified or deleted

#### Scenario: Trade log grows monotonically
- **WHEN** multiple trades are recorded over weeks/months
- **THEN** trade log file size increases monotonically; no truncation or reordering

### Requirement: Human-readable trade log format

Trade log format SHALL be plain CSV, easily imported into analysis tools (pandas, Excel, R) for performance analysis and audit.

#### Scenario: Trade log is queryable via pandas
- **WHEN** analyst reads the trade log
- **THEN** they can load it in pandas: `pd.read_csv('output/pead_live_trades.csv')` and analyze by symbol, earnings_date, PnL, hit rate, etc.

#### Scenario: Trade log is readable in Excel
- **WHEN** trade log is opened in Excel or Google Sheets
- **THEN** columns are labeled clearly and values are formatted for easy interpretation

### Requirement: Timestamp precision for audit trail

Each trade record SHALL include a precise timestamp (ISO 8601 format with seconds precision, UTC) to enable accurate sequencing and audit of events.

#### Scenario: Timestamp on trade exit
- **WHEN** exit order executes and trade is logged
- **THEN** timestamp column SHALL contain the exact exit order execution time in ISO 8601 format (e.g., `2026-04-28T16:00:30Z`)

#### Scenario: Timestamp enables event sequencing
- **WHEN** multiple trades are logged on the same day
- **THEN** their timestamps enable precise ordering of events

### Requirement: Record skipped entry events (for analysis)

When an entry is skipped due to negative classifier prediction, the system MAY optionally log a "skipped" record for analysis purposes (to compute true false-negative rate).

#### Scenario: Optional logging of skipped entries
- **WHEN** classifier predicts negative (pred_label == 0) on T-3
- **THEN** system MAY append a record to the trade log with fields: symbol, earnings_date, entry_date, exit_date=NULL, entry_price=NULL, exit_price=NULL, qty=0, pnl=0, pnl_pct=0, timestamp=T-3_time, plus a note "skipped_pred=0"
