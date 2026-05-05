import os
import unittest
from unittest.mock import patch

from core.alpaca_credentials import resolve_alpaca_credentials


class ResolveAlpacaCredentialsTests(unittest.TestCase):
    def test_resolves_v1_credentials(self):
        with patch.dict(
            os.environ,
            {
                "V1_APCA_API_KEY_ID": "k1",
                "V1_APCA_API_SECRET_KEY": "s1",
            },
            clear=False,
        ):
            self.assertEqual(resolve_alpaca_credentials("v1"), ("k1", "s1"))

    def test_resolves_v2_credentials(self):
        with patch.dict(
            os.environ,
            {
                "V2_APCA_API_KEY_ID": "k2",
                "V2_APCA_API_SECRET_KEY": "s2",
            },
            clear=False,
        ):
            self.assertEqual(resolve_alpaca_credentials("v2"), ("k2", "s2"))

    def test_raises_for_unknown_profile(self):
        with self.assertRaisesRegex(ValueError, "Unsupported Alpaca profile"):
            resolve_alpaca_credentials("v9")

    def test_raises_when_required_variables_are_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(EnvironmentError, "Missing Alpaca credentials for profile 'v2'"):
                resolve_alpaca_credentials("v2")


if __name__ == "__main__":
    unittest.main()
