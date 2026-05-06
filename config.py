import os
from dotenv import load_dotenv

load_dotenv()


def _validate_positive_int(name: str, value: int) -> int:
	if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
		raise ValueError(f"{name} must be a positive integer, got {value!r}")
	return value

# M7 universe
M7_SYMBOLS = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA"]

# Strategy parameters
LOOKBACK = 60       # N-day return lookback window
TOP_N = 3           # Number of symbols to hold long
INITIAL_AMOUNT = 10_000.0
FTC = 0.0           # Fixed transaction cost per trade
PTC = 0.0           # Proportional transaction cost per trade

# Backtest period
START_DATE = "2020-01-01"
END_DATE = "2025-12-31"

# Alpaca profile credentials
V1_APCA_API_KEY_ID = os.environ.get("V1_APCA_API_KEY_ID")
V1_APCA_API_SECRET_KEY = os.environ.get("V1_APCA_API_SECRET_KEY")
V2_APCA_API_KEY_ID = os.environ.get("V2_APCA_API_KEY_ID")
V2_APCA_API_SECRET_KEY = os.environ.get("V2_APCA_API_SECRET_KEY")

# PEAD strategy parameters (Post-Earnings Announcements Drift)
PEAD_SYMBOLS = ["NXPI", "AMD", "AVGO", "ANET", "GOOGL"]
PEAD_START_DATE = "2016-01-01"
PEAD_END_DATE = "2025-12-31"
PEAD_POSITION_SIZE = 0.10        # 10% of capital per trade
PEAD_PTC = 0.001                 # 0.1% proportional transaction cost per leg
PEAD_MIN_TRAIN = 20              # Minimum events for training seed
PEAD_ENTRY_OFFSET_DAYS = _validate_positive_int("PEAD_ENTRY_OFFSET_DAYS", 3)
PEAD_EXIT_MODE = "t_plus_1_open"  # Options: t_plus_1_open, t_plus_1_close


def get_pead_feature_anchor_offset_days() -> int:
	"""Return the trading-day offset for the last fully known feature bar."""
	return PEAD_ENTRY_OFFSET_DAYS + 1

# PEAD live trading parameters
PEAD_LIVE_SYMBOLS = list(PEAD_SYMBOLS)
PEAD_LIVE_POSITION_SIZE = 0.10   # 10% of account equity per trade
PEAD_LIVE_PTC = 0.001            # 0.1% proportional transaction cost per leg
PEAD_LIVE_STATE_FILE = "output/pead_live_state.json"
PEAD_LIVE_LOG_FILE = "output/pead_live_trades.csv"
PEAD_LIVE_STALE_DAYS = 30        # Auto-cleanup entries older than this many days
