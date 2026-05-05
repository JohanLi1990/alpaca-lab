import unittest
import os
from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd

from data.alpaca_data import fetch_bars


class FetchBarsTests(unittest.TestCase):
    def _make_bars_response(self) -> SimpleNamespace:
        index = pd.MultiIndex.from_tuples(
            [
                ("NXPI", pd.Timestamp("2026-04-22T00:00:00Z")),
                ("NXPI", pd.Timestamp("2026-04-23T00:00:00Z")),
            ],
            names=["symbol", "timestamp"],
        )
        df = pd.DataFrame(
            {
                "open": [200.0, 202.0],
                "high": [201.0, 203.0],
                "low": [199.0, 201.0],
                "close": [200.5, 202.5],
                "volume": [1000, 1100],
            },
            index=index,
        )
        return SimpleNamespace(df=df)

    @patch("data.alpaca_data._get_client")
    def test_fetch_bars_uses_inclusive_end_date_for_daily_requests(self, mock_get_client):
        mock_client = mock_get_client.return_value
        mock_client.get_stock_bars.return_value = self._make_bars_response()

        fetch_bars(["NXPI"], start="2026-04-14", end="2026-04-23")

        mock_get_client.assert_called_once_with(profile="v1")
        request = mock_client.get_stock_bars.call_args.args[0]
        self.assertEqual(str(request.start.date()), "2026-04-14")
        self.assertEqual(str(request.end.date()), "2026-04-24")

    @patch("data.alpaca_data._get_client")
    def test_fetch_bars_defaults_to_iex_feed(self, mock_get_client):
        mock_client = mock_get_client.return_value
        mock_client.get_stock_bars.return_value = self._make_bars_response()

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("APCA_STOCK_FEED", None)
            os.environ.pop("APCA_DATA_FEED", None)
            fetch_bars(["NXPI"], start="2026-04-14", end="2026-04-23")

        mock_get_client.assert_called_once_with(profile="v1")
        request = mock_client.get_stock_bars.call_args.args[0]
        self.assertEqual(request.feed, "iex")

    @patch("data.alpaca_data._get_client")
    def test_fetch_bars_honors_feed_override(self, mock_get_client):
        mock_client = mock_get_client.return_value
        mock_client.get_stock_bars.return_value = self._make_bars_response()

        with patch.dict(os.environ, {"APCA_STOCK_FEED": "SIP"}, clear=False):
            fetch_bars(["NXPI"], start="2026-04-14", end="2026-04-23")

        mock_get_client.assert_called_once_with(profile="v1")
        request = mock_client.get_stock_bars.call_args.args[0]
        self.assertEqual(request.feed, "sip")

    @patch("data.alpaca_data._get_client")
    def test_fetch_bars_preserves_first_requested_ohlcv_row(self, mock_get_client):
        mock_client = mock_get_client.return_value
        mock_client.get_stock_bars.return_value = self._make_bars_response()

        result = fetch_bars(["NXPI"], start="2026-04-14", end="2026-04-23")

        mock_get_client.assert_called_once_with(profile="v1")
        nxpi = result["NXPI"]
        self.assertEqual(len(nxpi), 2)
        self.assertTrue(pd.isna(nxpi.iloc[0]["return"]))
        self.assertEqual(nxpi.index[-1].strftime("%Y-%m-%d"), "2026-04-23")

    @patch("data.alpaca_data._get_client")
    def test_fetch_bars_supports_explicit_v2_profile(self, mock_get_client):
        mock_client = mock_get_client.return_value
        mock_client.get_stock_bars.return_value = self._make_bars_response()

        fetch_bars(["NXPI"], start="2026-04-14", end="2026-04-23", profile="v2")

        mock_get_client.assert_called_once_with(profile="v2")


if __name__ == "__main__":
    unittest.main()
