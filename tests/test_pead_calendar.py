import unittest
from datetime import datetime, timezone

from data.pead_calendar import (
    calculate_offset_trading_date,
    get_current_market_date,
    get_entry_trading_date,
    get_feature_anchor_trading_date,
    get_trading_dates,
)


class PEADCalendarTests(unittest.TestCase):
    def test_get_trading_dates_excludes_good_friday(self):
        trading_dates = get_trading_dates("2025-04-14", "2025-04-22")
        date_labels = set(trading_dates.strftime("%Y-%m-%d"))
        self.assertNotIn("2025-04-18", date_labels)

    def test_offset_helpers_skip_good_friday(self):
        earnings_date = "2025-04-22"
        self.assertEqual(str(calculate_offset_trading_date(earnings_date, -1).date()), "2025-04-21")
        self.assertEqual(str(get_entry_trading_date(earnings_date, 3).date()), "2025-04-16")
        self.assertEqual(str(get_feature_anchor_trading_date(earnings_date, 3).date()), "2025-04-15")

    def test_current_market_date_uses_new_york_timezone(self):
        now_utc = datetime(2026, 4, 24, 1, 50, tzinfo=timezone.utc)
        self.assertEqual(str(get_current_market_date(now_utc)), "2026-04-23")


if __name__ == "__main__":
    unittest.main()