import unittest

import pandas as pd

from data.pre_earnings_features import build_features


class BuildFeaturesTimingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dates = pd.bdate_range("2026-01-05", periods=20)
        closes = [float(100 + idx) for idx in range(len(self.dates))]
        self.bars = pd.DataFrame(
            {
                "open": [value - 0.5 for value in closes],
                "high": [value + 1.0 for value in closes],
                "low": [value - 1.0 for value in closes],
                "close": closes,
                "volume": [1000 + (idx * 10) for idx in range(len(self.dates))],
            },
            index=self.dates,
        )
        self.qqq = self.bars.copy()
        self.events = pd.DataFrame(
            {
                "earnings_date": [self.dates[15]],
                "t_minus_1": [self.dates[14]],
                "symbol": ["GOOGL"],
            }
        )

    def test_build_features_uses_t4_anchor_for_t3_open_entry(self):
        features = build_features(
            events_df=self.events,
            bars_dict={"GOOGL": self.bars, "QQQ": self.qqq},
            symbol="GOOGL",
            entry_offset_days=3,
        )

        expected_window = self.bars.iloc[5:12]
        expected_drift = (
            expected_window["close"].iloc[-1] - expected_window["close"].iloc[0]
        ) / expected_window["close"].iloc[0]
        self.assertAlmostEqual(features.iloc[0]["drift_7d"], expected_drift)

    def test_build_features_supports_alternate_offsets_without_schema_changes(self):
        features_t4 = build_features(
            events_df=self.events,
            bars_dict={"GOOGL": self.bars, "QQQ": self.qqq},
            symbol="GOOGL",
            entry_offset_days=4,
        )
        features_t5 = build_features(
            events_df=self.events,
            bars_dict={"GOOGL": self.bars, "QQQ": self.qqq},
            symbol="GOOGL",
            entry_offset_days=5,
        )

        self.assertEqual(list(features_t4.columns), list(features_t5.columns))
        self.assertNotEqual(features_t4.iloc[0]["drift_7d"], features_t5.iloc[0]["drift_7d"])

    def test_build_features_inference_respects_explicit_feature_anchor(self):
        bars = self.bars.copy()
        bars.loc[self.dates[15], "close"] = 9999.0
        qqq = self.qqq.copy()
        qqq.loc[self.dates[15], "close"] = 9999.0
        events = pd.DataFrame(
            {
                "earnings_date": [self.dates[16]],
                "symbol": ["GOOGL"],
                "t_feature_anchor": [self.dates[11]],
            }
        )

        features = build_features(
            events_df=events,
            bars_dict={"GOOGL": bars, "QQQ": qqq},
            symbol="GOOGL",
            include_labels=False,
            entry_offset_days=3,
        )

        expected_window = bars.iloc[5:12]
        expected_drift = (
            expected_window["close"].iloc[-1] - expected_window["close"].iloc[0]
        ) / expected_window["close"].iloc[0]
        self.assertAlmostEqual(features.iloc[0]["drift_7d"], expected_drift)
        self.assertNotIn("y", features.columns)


if __name__ == "__main__":
    unittest.main()