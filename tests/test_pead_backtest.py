import unittest

import pandas as pd

from strategies.pead_backtest import PEADBacktest


class PEADBacktestTimingTests(unittest.TestCase):
    def setUp(self) -> None:
        dates = pd.bdate_range("2026-01-05", periods=10)
        self.bars = pd.DataFrame(
            {
                "open": [100.0 + idx for idx in range(len(dates))],
                "high": [101.0 + idx for idx in range(len(dates))],
                "low": [99.0 + idx for idx in range(len(dates))],
                "close": [100.5 + idx for idx in range(len(dates))],
                "volume": [1000 + idx for idx in range(len(dates))],
            },
            index=dates,
        )
        self.predictions = pd.DataFrame(
            {
                "earnings_date": [dates[6]],
                "pred_label": [1],
                "prob_positive": [0.8],
                "y": [1],
                "gap_return": [0.01],
            }
        ).set_index("earnings_date")
        self.events = pd.DataFrame(
            {
                "earnings_date": [dates[6]],
                "t_minus_1": [dates[5]],
            }
        )

    def test_backtest_uses_open_price_for_offset_entry(self):
        backtest = PEADBacktest(
            predictions_df=self.predictions,
            bars_dict={"GOOGL": self.bars},
            events_df=self.events,
            entry_offset_days=3,
            ptc=0.0,
        )

        equity_curve, trades = backtest.run()

        self.assertEqual(len(equity_curve), 2)
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades.iloc[0]["entry_price"], self.bars.iloc[3]["open"])

    def test_backtest_skips_when_feature_anchor_bar_missing(self):
        bars = self.bars.drop(self.bars.index[2])
        backtest = PEADBacktest(
            predictions_df=self.predictions,
            bars_dict={"GOOGL": bars},
            events_df=self.events,
            entry_offset_days=3,
            ptc=0.0,
        )

        equity_curve, trades = backtest.run()

        self.assertEqual(len(trades), 0)
        self.assertEqual(len(equity_curve), 1)


if __name__ == "__main__":
    unittest.main()