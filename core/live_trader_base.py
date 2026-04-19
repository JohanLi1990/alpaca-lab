from __future__ import annotations

import logging
import os
from datetime import datetime, time, timezone

log = logging.getLogger(__name__)

from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

load_dotenv()

# NYSE core session (ET converted to UTC offset naively for checking)
_NYSE_OPEN = time(14, 30)   # 09:30 ET = 14:30 UTC
_NYSE_CLOSE = time(21, 0)   # 16:00 ET = 21:00 UTC


class AlpacaLiveTraderBase:
    """Base class for Alpaca paper trading execution.

    Parameters
    ----------
    paper : bool
        Must be True.  Raises ``ValueError`` if False.
    """

    def __init__(self, paper: bool = True) -> None:
        if not paper:
            raise ValueError(
                "Live (non-paper) trading is not permitted. "
                "Instantiate with paper=True."
            )
        api_key = os.environ.get("APCA_API_KEY_ID")
        secret_key = os.environ.get("APCA_API_SECRET_KEY")
        if not api_key or not secret_key:
            raise EnvironmentError(
                "Missing Alpaca credentials. "
                "Ensure APCA_API_KEY_ID and APCA_API_SECRET_KEY are set in your .env file."
            )
        self.client = TradingClient(api_key, secret_key, paper=True)

    # ------------------------------------------------------------------
    # Positions
    # ------------------------------------------------------------------

    def get_current_positions(self) -> dict[str, float]:
        """Return current open positions as {symbol: qty}."""
        positions = self.client.get_all_positions()
        return {p.symbol: float(p.qty) for p in positions}

    # ------------------------------------------------------------------
    # Order submission
    # ------------------------------------------------------------------

    def submit_order(self, symbol: str, side: OrderSide, qty: float) -> None:
        """Submit a market order and log the result.

        Parameters
        ----------
        symbol : str
        side : OrderSide
            ``OrderSide.BUY`` or ``OrderSide.SELL``.
        qty : float
            Number of whole shares.
        """
        qty = int(qty)
        if qty <= 0:
            return
        request = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=side,
            time_in_force=TimeInForce.DAY,
        )
        order = self.client.submit_order(request)
        log.info(
            "ORDER %s %d %s → order_id=%s",
            side.value.upper(), qty, symbol, order.id,
        )

    # ------------------------------------------------------------------
    # Market-hours check
    # ------------------------------------------------------------------

    def _warn_if_outside_hours(self) -> None:
        now_utc = datetime.now(timezone.utc)
        if now_utc.weekday() >= 5:  # Saturday=5, Sunday=6
            raise RuntimeError(
                f"Refusing to submit orders on a weekend "
                f"(UTC: {now_utc.strftime('%A %Y-%m-%d %H:%M')}). "
                "Alpaca DAY orders submitted on weekends are silently rejected."
            )
        now_time = now_utc.time()
        if not (_NYSE_OPEN <= now_time <= _NYSE_CLOSE):
            log.warning(
                "Current time %s UTC is outside NYSE core hours (14:30–21:00 UTC). "
                "Orders will be queued and fill at market open.",
                now_time.strftime("%H:%M"),
            )
