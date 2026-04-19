from __future__ import annotations

import logging
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

log = logging.getLogger(__name__)


def _to_series(equity_curve: list[tuple] | pd.Series) -> pd.Series:
    """Normalise equity_curve to a pandas Series indexed by date."""
    if isinstance(equity_curve, pd.Series):
        return equity_curve
    dates, values = zip(*equity_curve)
    return pd.Series(values, index=pd.to_datetime(dates))


def sharpe_ratio(
    equity_curve: list[tuple] | pd.Series,
    periods_per_year: int = 52,
) -> float:
    """Annualised Sharpe ratio (risk-free rate = 0).

    Parameters
    ----------
    equity_curve : list of (date, value) tuples or pd.Series
    periods_per_year : int
        52 for weekly, 252 for daily.

    Returns
    -------
    float
        Annualised Sharpe ratio.  Returns 0.0 if volatility is zero.
    """
    s = _to_series(equity_curve)
    returns = s.pct_change().dropna()
    std = returns.std()
    if std == 0 or math.isnan(std):
        return 0.0
    return float(returns.mean() / std * math.sqrt(periods_per_year))


def max_drawdown(equity_curve: list[tuple] | pd.Series) -> float:
    """Maximum peak-to-trough drawdown as a percentage (negative value).

    Returns
    -------
    float
        e.g. -25.4 means the worst drawdown was -25.4%.
        Returns 0.0 if the curve is monotonically increasing.
    """
    s = _to_series(equity_curve)
    rolling_max = s.cummax()
    drawdown = (s - rolling_max) / rolling_max * 100
    return float(drawdown.min())


def calmar_ratio(
    equity_curve: list[tuple] | pd.Series,
    periods_per_year: int = 52,
) -> float:
    """Calmar ratio: annualised return / abs(max drawdown).

    Returns
    -------
    float
        Calmar ratio.  Returns 0.0 if max drawdown is zero.
    """
    s = _to_series(equity_curve)
    n = len(s)
    if n < 2:
        return 0.0
    total_return = s.iloc[-1] / s.iloc[0]
    ann_return = total_return ** (periods_per_year / n) - 1
    mdd = max_drawdown(equity_curve)
    if mdd == 0:
        return 0.0
    return float(ann_return / abs(mdd / 100))


def print_summary(
    equity_curve: list[tuple] | pd.Series,
    periods_per_year: int = 52,
) -> None:
    """Print a formatted risk summary to stdout."""
    s = _to_series(equity_curve)
    total_ret = (s.iloc[-1] / s.iloc[0] - 1) * 100
    sr = sharpe_ratio(equity_curve, periods_per_year)
    mdd = max_drawdown(equity_curve)
    cr = calmar_ratio(equity_curve, periods_per_year)
    n = len(s)

    log.info("=" * 45)
    log.info("  Risk Summary")
    log.info("=" * 45)
    log.info("  Periods              : %d", n)
    log.info("  Total Return    [%%]  : %10.2f", total_ret)
    log.info("  Sharpe Ratio         : %10.2f", sr)
    log.info("  Max Drawdown    [%%]  : %10.2f", mdd)
    log.info("  Calmar Ratio         : %10.2f", cr)
    log.info("=" * 45)


def plot_equity_curve(
    equity_curve: list[tuple] | pd.Series,
    title: str = "Equity Curve",
    save_path: str | None = None,
) -> None:
    """Plot the equity curve using matplotlib."""
    s = _to_series(equity_curve)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(s.index, s.values, linewidth=1.5, color="steelblue")
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value ($)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    else:
        plt.show()
    plt.close(fig)
