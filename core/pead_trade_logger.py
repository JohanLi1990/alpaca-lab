"""PEAD live trading trade logger.

Maintains append-only CSV log of all entry/exit trades for audit trail
and performance analysis.
"""

from __future__ import annotations

import csv
import logging
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)


class PEADTradeLogger:
    """Logs all PEAD live trades to append-only CSV file.
    
    CSV columns:
    symbol, earnings_date, entry_date, exit_date, entry_price, exit_price,
    qty, pnl, pnl_pct, timestamp
    """

    CSV_HEADER = [
        "symbol",
        "earnings_date",
        "entry_date",
        "exit_date",
        "entry_price",
        "exit_price",
        "qty",
        "pnl",
        "pnl_pct",
        "timestamp",
    ]

    def __init__(self, log_file: str = "output/pead_live_trades.csv"):
        """Initialize trade logger.
        
        Parameters
        ----------
        log_file : str
            Path to CSV trade log file (default: output/pead_live_trades.csv)
        """
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.initialize_log()

    def initialize_log(self) -> None:
        """Create CSV header if file doesn't exist."""
        try:
            if not self.log_file.exists():
                with open(self.log_file, "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=self.CSV_HEADER)
                    writer.writeheader()
                log.info("Initialized trade log at %s", self.log_file)
            else:
                log.debug("Trade log %s already exists", self.log_file)
        except Exception as e:
            log.error("Failed to initialize trade log %s: %s", self.log_file, e)
            raise

    def log_trade(
        self,
        symbol: str,
        earnings_date: str,
        entry_date: str,
        exit_date: str,
        entry_price: float,
        exit_price: float,
        qty: int,
        pnl: float,
        pnl_pct: float,
    ) -> None:
        """Log a completed trade (entry + exit).
        
        Parameters
        ----------
        symbol : str
            Stock symbol
        earnings_date : str
            Earnings date (YYYY-MM-DD)
        entry_date : str
            Entry date (YYYY-MM-DD)
        exit_date : str
            Exit date (YYYY-MM-DD)
        entry_price : float
            Entry fill price
        exit_price : float
            Exit fill price
        qty : int
            Shares traded
        pnl : float
            Profit/loss in dollars
        pnl_pct : float
            Profit/loss as percentage (0.05 = 5%)
        """
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            row = {
                "symbol": symbol,
                "earnings_date": earnings_date,
                "entry_date": entry_date,
                "exit_date": exit_date,
                "entry_price": f"{entry_price:.2f}",
                "exit_price": f"{exit_price:.2f}",
                "qty": qty,
                "pnl": f"{pnl:.2f}",
                "pnl_pct": f"{pnl_pct:.4f}",
                "timestamp": timestamp,
            }
            
            with open(self.log_file, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.CSV_HEADER)
                writer.writerow(row)
            
            log.info(
                "Logged trade: %s %s earnings_date=%s entry=%s exit=%s pnl=%.2f (%.2f%%)",
                symbol, entry_date, earnings_date, entry_price, exit_price, pnl, pnl_pct * 100,
            )
        except Exception as e:
            log.error("Failed to log trade for %s: %s", symbol, e)
            raise

    def log_skipped_entry(
        self,
        symbol: str,
        earnings_date: str,
        entry_date: str,
        reason: str = "pred_label=0",
    ) -> None:
        """Optionally log a skipped entry for analysis (pred_label=0 case).
        
        Parameters
        ----------
        symbol : str
            Stock symbol
        earnings_date : str
            Earnings date (YYYY-MM-DD)
        entry_date : str
            Entry date (YYYY-MM-DD)
        reason : str
            Reason for skip (default: "pred_label=0")
        """
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            row = {
                "symbol": symbol,
                "earnings_date": earnings_date,
                "entry_date": entry_date,
                "exit_date": "SKIPPED",
                "entry_price": "",
                "exit_price": "",
                "qty": 0,
                "pnl": 0.0,
                "pnl_pct": 0.0,
                "timestamp": timestamp,
            }
            
            with open(self.log_file, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.CSV_HEADER)
                writer.writerow(row)
            
            log.info(
                "Logged skipped entry: %s %s reason=%s",
                symbol, entry_date, reason,
            )
        except Exception as e:
            log.error("Failed to log skipped entry for %s: %s", symbol, e)
            raise
