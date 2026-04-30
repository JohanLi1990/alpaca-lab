import unittest
from types import SimpleNamespace
from unittest.mock import patch
import sys
import types

import pandas as pd

from alpaca.trading.enums import OrderSide

# risk.metrics imports matplotlib at module import time; stub it for unit tests.
sys.modules.setdefault("matplotlib", types.ModuleType("matplotlib"))
sys.modules.setdefault("matplotlib.pyplot", types.ModuleType("matplotlib.pyplot"))

from strategies.momentum import LiveMomentumTrader


def _price_df(price: float) -> pd.DataFrame:
    return pd.DataFrame({"close": [price]}, index=pd.to_datetime(["2026-04-29"]))


class LiveMomentumTraderRebalanceTests(unittest.TestCase):
    @patch("core.live_trader_base.AlpacaLiveTraderBase.__init__", return_value=None)
    @patch("strategies.momentum.fetch_bars")
    @patch("strategies.momentum.log")
    def test_rebalance_sells_first_rank_orders_buys_and_logs_skip(
        self,
        mock_log,
        mock_fetch_bars,
        _base_init,
    ):
        trader = LiveMomentumTrader(symbols=["AAPL", "AMZN", "META", "NVDA"], max_capital=None)
        trader.client = SimpleNamespace(get_account=lambda: SimpleNamespace(cash="1000"))

        with patch.object(trader, "_warn_if_outside_hours"), \
             patch.object(trader, "compute_signal", return_value=["AAPL", "AMZN", "NVDA"]), \
             patch.object(trader, "get_current_positions", return_value={"AAPL": 10.0, "META": 14.0}), \
             patch.object(trader, "submit_order") as mock_submit:
            mock_fetch_bars.return_value = {
                "AAPL": _price_df(200.0),
                "AMZN": _price_df(400.0),
                "META": _price_df(100.0),
                "NVDA": _price_df(300.0),
            }

            trader.rebalance()

        # Sell dropped holding first, then buy ranked replacement that can be funded.
        self.assertEqual(mock_submit.call_count, 2)
        self.assertEqual(mock_submit.call_args_list[0].args, ("META", OrderSide.SELL, 14))
        self.assertEqual(mock_submit.call_args_list[1].args, ("NVDA", OrderSide.BUY, 1))

        # AMZN should be explicitly skipped due to insufficient pre-close cash.
        self.assertTrue(any("SKIP BUY %s: insufficient available cash before close" in c.args[0] for c in mock_log.info.call_args_list))

    @patch("core.live_trader_base.AlpacaLiveTraderBase.__init__", return_value=None)
    @patch("strategies.momentum.fetch_bars")
    def test_capital_cap_ignores_positions_marked_for_sale(
        self,
        mock_fetch_bars,
        _base_init,
    ):
        trader = LiveMomentumTrader(symbols=["AAPL", "AMZN", "META"], max_capital=1000.0)
        trader.client = SimpleNamespace(get_account=lambda: SimpleNamespace(cash="5000"))

        with patch.object(trader, "_warn_if_outside_hours"), \
             patch.object(trader, "compute_signal", return_value=["AAPL", "AMZN"]), \
             patch.object(trader, "get_current_positions", return_value={"AAPL": 1.0, "META": 10.0}), \
             patch.object(trader, "submit_order") as mock_submit:
            mock_fetch_bars.return_value = {
                "AAPL": _price_df(100.0),
                "AMZN": _price_df(100.0),
                "META": _price_df(200.0),
            }

            trader.rebalance()

        # META is sold, and AMZN buy sizing uses cap minus retained (AAPL) value: (1000 - 100) / 100 = 9 shares.
        self.assertEqual(mock_submit.call_args_list[0].args, ("META", OrderSide.SELL, 10))
        self.assertEqual(mock_submit.call_args_list[1].args, ("AMZN", OrderSide.BUY, 9))

    @patch("core.live_trader_base.AlpacaLiveTraderBase.__init__", return_value=None)
    @patch("strategies.momentum.fetch_bars")
    def test_capital_cap_must_be_less_than_available_cash(
        self,
        mock_fetch_bars,
        _base_init,
    ):
        trader = LiveMomentumTrader(symbols=["AAPL"], max_capital=1000.0)
        trader.client = SimpleNamespace(get_account=lambda: SimpleNamespace(cash="1000"))

        with patch.object(trader, "_warn_if_outside_hours"), \
             patch.object(trader, "compute_signal", return_value=["AAPL"]), \
             patch.object(trader, "get_current_positions", return_value={}), \
             patch.object(trader, "submit_order"):
            mock_fetch_bars.return_value = {"AAPL": _price_df(100.0)}

            with self.assertRaisesRegex(ValueError, "max_capital must be less than current available cash"):
                trader.rebalance()


if __name__ == "__main__":
    unittest.main()