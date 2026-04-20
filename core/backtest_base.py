from __future__ import annotations

import logging

import pandas as pd

log = logging.getLogger(__name__)


class AlpacaBacktestBase:
    """Event-driven backtesting base class for multi-symbol portfolios.

    Subclasses must implement ``on_bar(bar)`` with the strategy signal logic.
    The event loop calls ``on_bar`` at each bar and detects Friday rebalances.

    Parameters
    ----------
    data : dict[str, pd.DataFrame]
        Mapping of symbol → OHLCV+return DataFrame (aligned on a common date index).
    initial_amount : float
        Starting capital in USD.
    ftc : float
        Fixed transaction cost per trade (USD).
    ptc : float
        Proportional transaction cost per trade (fraction, e.g. 0.001 = 0.1%).
    verbose : bool
        If True, print each order to stdout.
    """

    def __init__(
        self,
        data: dict[str, pd.DataFrame],
        initial_amount: float = 10_000.0,
        ftc: float = 0.0,
        ptc: float = 0.0,
        verbose: bool = True,
    ) -> None:
        self.data = data
        self.initial_amount = initial_amount
        self.ftc = ftc
        self.ptc = ptc
        self.verbose = verbose

        # Build a shared date index (intersection of all symbols)
        dates = None
        for df in data.values():
            dates = df.index if dates is None else dates.intersection(df.index)
        self.dates: pd.DatetimeIndex = dates.sort_values()

        # Portfolio state
        self.cash: float = initial_amount
        self.units_held: dict[str, float] = {}   # symbol → float shares
        self.trades: int = 0
        self.equity_curve: list[tuple] = []      # [(date, value), ...]

    # ------------------------------------------------------------------
    # Price helpers
    # ------------------------------------------------------------------

    def _price(self, symbol: str, bar: int) -> float:
        """Return closing price of symbol at bar index."""
        date = self.dates[bar]
        return float(self.data[symbol].loc[date, "close"])

    def _date(self, bar: int) -> pd.Timestamp:
        return self.dates[bar]

    # ------------------------------------------------------------------
    # Order simulation
    # ------------------------------------------------------------------

    def place_buy_order(self, symbol: str, bar: int, amount: float) -> None:
        """Buy as many whole shares of symbol as possible with given amount."""
        price = self._price(symbol, bar)
        units = int(amount / price)
        if units <= 0:
            return
        cost = units * price * (1 + self.ptc) + self.ftc
        self.cash -= cost
        self.units_held[symbol] = self.units_held.get(symbol, 0.0) + units
        self.trades += 1
        if self.verbose:
            log.info(
                "%s | BUY  %6d %-6s @ %10.2f | cash=%12.2f",
                self._date(bar).date(), units, symbol, price, self.cash,
            )

    def place_sell_order(self, symbol: str, bar: int, units: float) -> None:
        """Sell a given number of units of symbol."""
        if units <= 0:
            return
        price = self._price(symbol, bar)
        proceeds = units * price * (1 - self.ptc) - self.ftc
        self.cash += proceeds
        self.units_held[symbol] = self.units_held.get(symbol, 0.0) - units
        if self.units_held[symbol] <= 0:
            del self.units_held[symbol]
        self.trades += 1
        if self.verbose:
            log.info(
                "%s | SELL %6.0f %-6s @ %10.2f | cash=%12.2f",
                self._date(bar).date(), units, symbol, price, self.cash,
            )

    # ------------------------------------------------------------------
    # Portfolio valuation
    # ------------------------------------------------------------------

    def get_portfolio_value(self, bar: int) -> float:
        """Total portfolio value: cash + mark-to-market holdings."""
        mtm = sum(
            units * self._price(symbol, bar)
            for symbol, units in self.units_held.items()
        )
        return self.cash + mtm

    # ------------------------------------------------------------------
    # Close-out
    # ------------------------------------------------------------------

    def close_out(self, bar: int) -> None:
        """Liquidate all positions at the final bar and record last equity value."""
        for symbol, units in list(self.units_held.items()):
            self.place_sell_order(symbol, bar, units)
        final_value = self.get_portfolio_value(bar)
        self.equity_curve.append((self._date(bar), final_value))
        perf = (self.cash - self.initial_amount) / self.initial_amount * 100
        log.info("=" * 55)
        log.info("Final balance        [$] %12.2f", self.cash)
        log.info("Net performance       [%%] %12.2f", perf)
        log.info("Trades executed       [#] %12d", self.trades)
        log.info("=" * 55)

    # ------------------------------------------------------------------
    # Event loop
    # ------------------------------------------------------------------

    def on_bar(self, bar: int) -> None:  # pragma: no cover
        """Override in subclass: called on each bar (Monday only for rebalance)."""
        raise NotImplementedError

    def run_backtest(self) -> pd.Series | None:
        """Main event loop. Iterates over all bars, calls on_bar on Mondays."""
        self.cash = self.initial_amount
        self.units_held = {}
        self.trades = 0
        self.equity_curve = []

        # Record starting value
        self.equity_curve.append((self.dates[0], self.initial_amount))

        for bar in range(len(self.dates)):
            date = self.dates[bar]
            if date.weekday() == 0:  # Monday (Mon=0 … Fri=4)
                self.on_bar(bar)
                value = self.get_portfolio_value(bar)
                self.equity_curve.append((date, value))

        self.close_out(len(self.dates) - 1)
