import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

load_dotenv()


def _resolve_stock_feed() -> str:
    """Resolve stock data feed for Alpaca bars requests.

    Defaults to IEX so paper/free subscriptions can query recent data.
    Set APCA_STOCK_FEED or APCA_DATA_FEED to override (e.g., sip, delayed_sip).
    """
    return (
        os.environ.get("APCA_STOCK_FEED")
        or os.environ.get("APCA_DATA_FEED")
        or "iex"
    ).strip().lower()


def _get_client() -> StockHistoricalDataClient:
    """Build an authenticated StockHistoricalDataClient from environment variables."""
    api_key = os.environ.get("APCA_API_KEY_ID")
    secret_key = os.environ.get("APCA_API_SECRET_KEY")
    if not api_key or not secret_key:
        raise EnvironmentError(
            "Missing Alpaca credentials. "
            "Ensure APCA_API_KEY_ID and APCA_API_SECRET_KEY are set in your .env file."
        )
    return StockHistoricalDataClient(api_key, secret_key)


def fetch_bars(
    symbols: list[str],
    start: str,
    end: str,
    timeframe: TimeFrame = TimeFrame.Day,
) -> dict[str, pd.DataFrame]:
    """Fetch historical OHLCV bars for a list of symbols.

    Parameters
    ----------
    symbols : list[str]
        Ticker symbols to fetch.
    start : str
        Start date, e.g. '2019-01-01'.
    end : str
        End date, e.g. '2024-12-31'.
    timeframe : TimeFrame
        Bar timeframe (default: daily).

    Returns
    -------
    dict[str, pd.DataFrame]
        Mapping of symbol → DataFrame with columns [open, high, low, close, volume, return],
        indexed by date (UTC).

    Raises
    ------
    EnvironmentError
        If Alpaca credentials are not set.
    ValueError
        If any symbol has no data in the requested range.
    """
    client = _get_client()

    start_dt = datetime.strptime(start, "%Y-%m-%d")
    # Alpaca's `end` is exclusive for bar queries; add one day so caller's
    # YYYY-MM-DD end date remains inclusive at day granularity.
    end_dt = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)

    request = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=timeframe,
        start=start_dt,
        end=end_dt,
        feed=_resolve_stock_feed(),
    )

    bars = client.get_stock_bars(request)
    df_all = bars.df  # MultiIndex: (symbol, timestamp)

    result: dict[str, pd.DataFrame] = {}
    for symbol in symbols:
        if symbol not in df_all.index.get_level_values(0):
            raise ValueError(
                f"Symbol '{symbol}' returned no data for the range {start} to {end}."
            )

        df = df_all.loc[symbol].copy()
        df.index = pd.to_datetime(df.index).tz_localize(None)  # strip tz for simplicity

        # Keep only OHLCV columns
        df = df[["open", "high", "low", "close", "volume"]]

        # Compute log returns while preserving the first requested OHLCV bar.
        df["return"] = np.log(df["close"] / df["close"].shift(1))

        if df.empty:
            raise ValueError(
                f"Symbol '{symbol}' returned no OHLCV data for the range {start} to {end}."
            )

        result[symbol] = df

    return result
