"""PEAD live trading state manager.

Manages JSON-based state file tracking current open positions per symbol.
Handles idempotency, atomic writes, and automatic cleanup of stale entries.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


class PEADStateManager:
    """Manages persistent state for live PEAD trading positions.
    
    State file structure:
    {
      "NXPI": {
        "earnings_date": "2026-04-30",
        "entry_date": "2026-04-27",
        "entry_price": 125.50,
        "entry_qty": 80,
        "created_at": "2026-04-27T16:00:00Z"
      }
    }
    """

    def __init__(self, state_file: str = "output/pead_live_state.json"):
        """Initialize state manager.
        
        Parameters
        ----------
        state_file : str
            Path to JSON state file (default: output/pead_live_state.json)
        """
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state: dict[str, dict[str, Any]] = {}
        self.load_state()

    def load_state(self) -> None:
        """Load state from JSON file, creating empty state if file doesn't exist."""
        try:
            if self.state_file.exists():
                with open(self.state_file, "r") as f:
                    self._state = json.load(f)
                    log.info("Loaded state from %s, positions: %s", self.state_file, list(self._state.keys()))
            else:
                self._state = {}
                log.info("State file %s does not exist, initializing empty state", self.state_file)
        except json.JSONDecodeError as e:
            log.error("Failed to parse state file %s: %s", self.state_file, e)
            self._state = {}
        except Exception as e:
            log.error("Failed to load state file %s: %s", self.state_file, e)
            self._state = {}

    def save_state(self) -> None:
        """Save state to JSON file with atomic write (pretty-printed)."""
        try:
            # Write to temporary file first, then atomically rename
            temp_file = self.state_file.with_suffix('.tmp')
            with open(temp_file, "w") as f:
                json.dump(self._state, f, indent=2)
            temp_file.replace(self.state_file)
            log.debug("Saved state to %s", self.state_file)
        except Exception as e:
            log.error("Failed to save state file %s: %s", self.state_file, e)
            raise

    def add_position(
        self,
        symbol: str,
        earnings_date: str,
        entry_date: str,
        entry_price: float,
        entry_qty: int,
    ) -> None:
        """Record a new open position (entry executed).
        
        Parameters
        ----------
        symbol : str
            Stock symbol (e.g., "NXPI")
        earnings_date : str
            Earnings date in YYYY-MM-DD format
        entry_date : str
            Entry date in YYYY-MM-DD format
        entry_price : float
            Entry fill price
        entry_qty : int
            Entry fill quantity
        """
        self._state[symbol] = {
            "earnings_date": earnings_date,
            "entry_date": entry_date,
            "entry_price": float(entry_price),
            "entry_qty": int(entry_qty),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.save_state()
        log.info(
            "Added position: %s earnings=%s entry_date=%s price=%.2f qty=%d",
            symbol, earnings_date, entry_date, entry_price, entry_qty,
        )

    def remove_position(self, symbol: str) -> None:
        """Delete position after exit (clean slate for next earnings event).
        
        Parameters
        ----------
        symbol : str
            Stock symbol (e.g., "NXPI")
        """
        if symbol in self._state:
            del self._state[symbol]
            self.save_state()
            log.info("Removed position: %s", symbol)
        else:
            log.debug("Position %s not found in state, nothing to remove", symbol)

    def get_position(self, symbol: str) -> dict[str, Any] | None:
        """Check if symbol has an open position and return details.
        
        Parameters
        ----------
        symbol : str
            Stock symbol (e.g., "NXPI")
            
        Returns
        -------
        dict or None
            Position details if open, else None
        """
        return self._state.get(symbol)

    def already_traded(self, symbol: str, earnings_date: str) -> bool:
        """Check if we already traded this symbol for this earnings event (idempotency).
        
        Parameters
        ----------
        symbol : str
            Stock symbol (e.g., "NXPI")
        earnings_date : str
            Earnings date in YYYY-MM-DD format
            
        Returns
        -------
        bool
            True if position exists for this symbol and same earnings_date
        """
        if symbol not in self._state:
            return False
        return self._state[symbol].get("earnings_date") == earnings_date

    def cleanup_stale_entries(self, days: int = 30) -> None:
        """Remove entries older than specified days (handles missed exits).
        
        Parameters
        ----------
        days : int
            Entries older than this many days are removed (default: 30)
        """
        cutoff_time = datetime.now(timezone.utc) - timedelta(days=days)
        stale_symbols = []

        for symbol, position in self._state.items():
            created_at_str = position.get("created_at")
            if not created_at_str:
                continue
            try:
                created_at = datetime.fromisoformat(created_at_str)
                # Ensure timezone-aware comparison
                if created_at.tzinfo is None:
                    created_at = created_at.replace(tzinfo=timezone.utc)
                if created_at < cutoff_time:
                    stale_symbols.append(symbol)
            except ValueError as e:
                log.warning("Failed to parse created_at for %s: %s", symbol, e)

        for symbol in stale_symbols:
            log.warning(
                "Cleaned up stale position for %s (created %s, age > %d days)",
                symbol,
                self._state[symbol].get("created_at"),
                days,
            )
            del self._state[symbol]

        if stale_symbols:
            self.save_state()
