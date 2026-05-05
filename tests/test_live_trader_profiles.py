import unittest
from unittest.mock import patch

from core.live_trader_base import AlpacaLiveTraderBase
from strategies.momentum import LiveMomentumTrader
from strategies.pead_live_trader import PEADLiveTrader


class LiveTraderProfileTests(unittest.TestCase):
    @patch("core.live_trader_base.TradingClient")
    @patch("core.live_trader_base.resolve_alpaca_credentials", return_value=("api", "secret"))
    def test_live_trader_base_uses_requested_profile(self, mock_resolve, mock_client):
        AlpacaLiveTraderBase(paper=True, profile="v2")

        mock_resolve.assert_called_once_with("v2")
        mock_client.assert_called_once_with("api", "secret", paper=True)

    @patch("core.live_trader_base.resolve_alpaca_credentials", side_effect=EnvironmentError("missing creds"))
    def test_live_trader_base_fails_fast_on_missing_profile_credentials(self, mock_resolve):
        with self.assertRaisesRegex(EnvironmentError, "missing creds"):
            AlpacaLiveTraderBase(paper=True, profile="v2")

        mock_resolve.assert_called_once_with("v2")

    @patch("core.live_trader_base.AlpacaLiveTraderBase.__init__", return_value=None)
    def test_live_momentum_trader_defaults_to_v1_profile(self, mock_base_init):
        LiveMomentumTrader(symbols=["AAPL"])

        mock_base_init.assert_called_once_with(paper=True, profile="v1")

    @patch("strategies.pead_live_trader.AlpacaLiveTraderBase.__init__", return_value=None)
    def test_pead_live_trader_defaults_to_v2_profile(self, mock_base_init):
        PEADLiveTrader(paper=True, position_size_pct=0.10)

        mock_base_init.assert_called_once_with(paper=True, profile="v2")


if __name__ == "__main__":
    unittest.main()
