from __future__ import annotations

import logging


log = logging.getLogger(__name__)

from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from core.alpaca_credentials import resolve_alpaca_credentials

load_dotenv()


class AlpacaLiveTraderBase:
    """Base class for Alpaca paper trading execution.

    Parameters
    ----------
    paper : bool
        Must be True.  Raises ``ValueError`` if False.
    profile : str
        Credential profile to use for Alpaca authentication.
    """

    def __init__(self, paper: bool = True, profile: str = "v1") -> None:
        if not paper:
            raise ValueError(
                "Live (non-paper) trading is not permitted. "
                "Instantiate with paper=True."
            )
        api_key, secret_key = resolve_alpaca_credentials(profile)
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
            time_in_force=TimeInForce.CLS,
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
        clock = self.client.get_clock()
        if not getattr(clock, "is_open", False):
            next_open = getattr(clock, "next_open", None)
            next_open_msg = str(next_open) if next_open is not None else "unknown"
            raise RuntimeError(
                "Refusing to submit orders outside regular market hours. "
                f"Alpaca clock reports market closed; next open: {next_open_msg}."
            )
