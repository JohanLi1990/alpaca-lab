"""PEAD live trader for Alpaca paper trading execution.

Handles order placement (entry/exit), position sizing, and market price queries.
Extends AlpacaLiveTraderBase for paper trading via Alpaca API.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from alpaca.trading.enums import OrderSide
from alpaca.trading.requests import MarketOrderRequest

from core.live_trader_base import AlpacaLiveTraderBase

log = logging.getLogger(__name__)


class PEADLiveTrader(AlpacaLiveTraderBase):
    """Alpaca-based live trader for PEAD strategy."""

    def __init__(self, paper: bool = True, position_size_pct: float = 0.10):
        """Initialize PEAD live trader.
        
        Parameters
        ----------
        paper : bool
            Must be True (paper trading only)
        position_size_pct : float
            Position size as fraction of account equity (default: 0.10 = 10%)
        """
        super().__init__(paper=paper)
        self.position_size_pct = position_size_pct
        self.ptc = 0.001  # 0.1% proportional transaction cost per leg

    def calculate_position_size(self, entry_price: float) -> int:
        """Calculate number of shares to buy.
        
        Parameters
        ----------
        entry_price : float
            Entry order fill price
            
        Returns
        -------
        int
            Number of shares to buy (rounded down)
        """
        try:
            # Get account equity
            account = self.client.get_account()
            account_equity = float(account.equity)
            
            # Calculate position value
            position_value = account_equity * self.position_size_pct
            
            # Calculate shares
            qty = int(position_value / entry_price)
            
            log.info(
                "Position size: equity=%.2f position_pct=%.2f target_value=%.2f entry_price=%.2f qty=%d",
                account_equity, self.position_size_pct, position_value, entry_price, qty,
            )
            
            return qty
        except Exception as e:
            log.error("Failed to calculate position size: %s", e)
            raise

    def place_entry_order(self, symbol: str) -> tuple[str, float, int] | None:
        """Place a market BUY order for entry.
        
        Parameters
        ----------
        symbol : str
            Stock symbol
            
        Returns
        -------
        tuple[str, float, int] or None
            (order_id, fill_price, qty) if successful, else None
        """
        try:
            # Get current price to calculate position size
            entry_price = self.get_current_price(symbol)
            if entry_price is None:
                log.error("Failed to get current price for %s", symbol)
                return None
            
            # Calculate position size
            qty = self.calculate_position_size(entry_price)
            if qty <= 0:
                log.warning("Position size is 0 or negative for %s at price %.2f", symbol, entry_price)
                return None
            
            # Place market order
            request = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY,
                time_in_force="day",
            )
            
            order = self.client.submit_order(request)
            
            log.info(
                "Placed entry BUY order: %s %d @ market | order_id=%s",
                symbol, qty, order.id,
            )
            
            # Capture fill details
            fill_price = float(order.filled_avg_price) if order.filled_avg_price else entry_price
            filled_qty = int(order.filled_qty) if order.filled_qty else qty
            
            return order.id, fill_price, filled_qty
            
        except Exception as e:
            log.error("Failed to place entry order for %s: %s", symbol, e)
            return None

    def place_exit_order(self, symbol: str, qty: int) -> tuple[str, float] | None:
        """Place a market SELL order for exit.
        
        Parameters
        ----------
        symbol : str
            Stock symbol
        qty : int
            Shares to sell
            
        Returns
        -------
        tuple[str, float] or None
            (order_id, fill_price) if successful, else None
        """
        try:
            if qty <= 0:
                log.warning("Cannot place exit order for %s: qty=%d", symbol, qty)
                return None
            
            # Get current price
            exit_price = self.get_current_price(symbol)
            if exit_price is None:
                log.error("Failed to get current price for %s", symbol)
                return None
            
            # Place market order
            request = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force="day",
            )
            
            order = self.client.submit_order(request)
            
            log.info(
                "Placed exit SELL order: %s %d @ market | order_id=%s",
                symbol, qty, order.id,
            )
            
            # Capture fill details
            fill_price = float(order.filled_avg_price) if order.filled_avg_price else exit_price
            
            return order.id, fill_price
            
        except Exception as e:
            log.error("Failed to place exit order for %s: %s", symbol, e)
            return None

    def get_current_price(self, symbol: str) -> float | None:
        """Fetch current market price for a symbol.
        
        Parameters
        ----------
        symbol : str
            Stock symbol
            
        Returns
        -------
        float or None
            Current market price, or None if unavailable
        """
        try:
            # Use quotes endpoint to get latest price
            quote = self.client.get_latest_trade(symbol)
            if quote and quote.price:
                price = float(quote.price)
                log.debug("Current price for %s: %.2f", symbol, price)
                return price
            else:
                log.warning("No quote available for %s", symbol)
                return None
        except Exception as e:
            log.error("Failed to get current price for %s: %s", symbol, e)
            return None

    def get_order_details(self, order_id: str) -> dict | None:
        """Get details of a placed order.
        
        Parameters
        ----------
        order_id : str
            Order ID from Alpaca
            
        Returns
        -------
        dict or None
            Order details (status, filled_qty, filled_avg_price, etc.), or None on error
        """
        try:
            order = self.client.get_order_by_id(order_id)
            return {
                "order_id": order.id,
                "symbol": order.symbol,
                "qty": order.qty,
                "filled_qty": order.filled_qty,
                "filled_avg_price": order.filled_avg_price,
                "status": order.status,
                "created_at": order.created_at,
            }
        except Exception as e:
            log.error("Failed to get order details for %s: %s", order_id, e)
            return None
