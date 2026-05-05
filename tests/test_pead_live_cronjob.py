import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

import config
from scripts.pead_live_cronjob import run_daily_execution


class PEADLiveCronjobTimingTests(unittest.TestCase):
    @patch("scripts.pead_live_cronjob.clear_earnings_cache")
    @patch("scripts.pead_live_cronjob.fetch_bars")
    @patch("scripts.pead_live_cronjob.build_features")
    @patch("scripts.pead_live_cronjob.get_pead_timing_dates")
    @patch("scripts.pead_live_cronjob.is_today_exit_date", return_value=False)
    @patch("scripts.pead_live_cronjob.is_today_entry_date", return_value=True)
    @patch("scripts.pead_live_cronjob.get_cached_earnings", return_value="2026-04-28")
    @patch("scripts.pead_live_cronjob.PEADClassifierLive")
    @patch("scripts.pead_live_cronjob.PEADLiveTrader")
    @patch("scripts.pead_live_cronjob.PEADTradeLogger")
    @patch("scripts.pead_live_cronjob.PEADStateManager")
    @patch("scripts.pead_live_cronjob.setup_logging")
    def test_live_cronjob_uses_offset_derived_feature_anchor(
        self,
        _setup_logging,
        mock_state_manager_cls,
        _trade_logger_cls,
        _trader_cls,
        mock_classifier_cls,
        _get_cached_earnings,
        _is_today_entry_date,
        _is_today_exit_date,
        mock_get_pead_timing_dates,
        mock_build_features,
        mock_fetch_bars,
        _clear_cache,
    ):
        mock_state_manager = mock_state_manager_cls.return_value
        mock_state_manager.already_traded.return_value = False

        mock_classifier = mock_classifier_cls.return_value
        mock_classifier.FEATURE_COLS = [
            "drift_7d",
            "drift_slope",
            "up_day_count",
            "down_day_count",
            "rel_volume_mean",
            "down_volume_ratio",
            "atr_ratio",
            "gap_count",
            "rel_drift_vs_qqq",
        ]
        mock_classifier.predict_entry.return_value = (0, 0.2)

        mock_get_pead_timing_dates.return_value = {
            "entry_date": pd.Timestamp("2026-04-23"),
            "feature_anchor_date": pd.Timestamp("2026-04-22"),
            "exit_date": pd.Timestamp("2026-04-29"),
        }
        mock_fetch_bars.return_value = {
            "NXPI": pd.DataFrame(
                {
                    "open": [1.0] * 7,
                    "high": [2.0] * 7,
                    "low": [0.5] * 7,
                    "close": [1.5] * 7,
                    "volume": [100] * 7,
                    "return": [None] * 7,
                },
                index=pd.bdate_range("2026-04-14", periods=7),
            ),
            "QQQ": pd.DataFrame(
                {
                    "open": [1.0] * 7,
                    "high": [2.0] * 7,
                    "low": [0.5] * 7,
                    "close": [1.5] * 7,
                    "volume": [100] * 7,
                    "return": [None] * 7,
                },
                index=pd.bdate_range("2026-04-14", periods=7),
            ),
        }
        mock_build_features.return_value = pd.DataFrame(
            [
                {
                    "drift_7d": 0.1,
                    "drift_slope": 0.1,
                    "up_day_count": 4.0,
                    "down_day_count": 2.0,
                    "rel_volume_mean": 1.2,
                    "down_volume_ratio": 0.3,
                    "atr_ratio": 1.1,
                    "gap_count": 1.0,
                    "rel_drift_vs_qqq": 0.05,
                }
            ],
            index=[pd.Timestamp("2026-04-28")],
        )

        with patch.object(config, "PEAD_LIVE_SYMBOLS", ["NXPI"]):
            run_daily_execution()

        _trader_cls.assert_called_once_with(
            paper=True,
            position_size_pct=config.PEAD_LIVE_POSITION_SIZE,
            profile="v2",
        )
        mock_classifier.ensure_trained.assert_called_once_with()

        mock_fetch_bars.assert_called_once_with(
            symbols=["NXPI", "QQQ"],
            start="2026-04-14",
            end="2026-04-22",
            profile="v2",
        )
        self.assertEqual(mock_build_features.call_args.kwargs["entry_offset_days"], config.PEAD_ENTRY_OFFSET_DAYS)
        event_df = mock_build_features.call_args.kwargs["events_df"]
        self.assertEqual(event_df.iloc[0]["t_feature_anchor"], "2026-04-22")


if __name__ == "__main__":
    unittest.main()