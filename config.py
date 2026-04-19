import os
from dotenv import load_dotenv

load_dotenv()

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

# Alpaca credentials
APCA_API_KEY_ID = os.environ.get("APCA_API_KEY_ID")
APCA_API_SECRET_KEY = os.environ.get("APCA_API_SECRET_KEY")
