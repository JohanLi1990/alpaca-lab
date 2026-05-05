import os
import time
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import Timeout as RequestsTimeout

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from core.alpaca_credentials import resolve_alpaca_credentials

load_dotenv()
log = logging.getLogger(__name__)


def _get_retry_config() -> tuple[int, float]:
    """Return retry settings for transient Alpaca data fetch errors.

    Environment overrides:
    - APCA_DATA_RETRY_COUNT (default: 10, minimum: 0)
    - APCA_DATA_RETRY_DELAY_SEC (default: 60.0, minimum: 1.0)
    """
    retry_count = int(os.environ.get("APCA_DATA_RETRY_COUNT", "10"))
    retry_delay_sec = float(os.environ.get("APCA_DATA_RETRY_DELAY_SEC", "60.0"))
    return max(0, retry_count), max(1.0, retry_delay_sec)


def _get_stock_bars_with_retry(client: StockHistoricalDataClient, request: StockBarsRequest):
    """Fetch bars with retries for transient transport-level failures."""
    retry_count, retry_delay_sec = _get_retry_config()
    last_error: Exception | None = None

    # retry_count means retries after the first failed attempt.
    total_attempts = retry_count + 1
    for attempt in range(1, total_attempts + 1):
        try:
            return client.get_stock_bars(request)
        except (RequestsConnectionError, RequestsTimeout) as err:
            last_error = err
            retries_used = attempt - 1
            if retries_used >= retry_count:
                break
            log.warning(
                "Transient Alpaca data error (%s). Retry %d/%d in %.0fs.",
                type(err).__name__,
                retries_used + 1,
                retry_count,
                retry_delay_sec,
            )
            time.sleep(retry_delay_sec)

    assert last_error is not None
    raise last_error


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


def _get_client(profile: str = "v1") -> StockHistoricalDataClient:
    """Build an authenticated StockHistoricalDataClient for a named profile."""
    api_key, secret_key = resolve_alpaca_credentials(profile)
    return StockHistoricalDataClient(api_key, secret_key)


def fetch_bars(
    symbols: list[str],
    start: str,
    end: str,
    timeframe: TimeFrame = TimeFrame.Day,
    profile: str = "v1",
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
    profile : str
        Credential profile to use for Alpaca authentication (default: "v1").

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
    client = _get_client(profile=profile)

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

    bars = _get_stock_bars_with_retry(client, request)
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
