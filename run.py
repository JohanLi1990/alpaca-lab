"""
run.py — Entry point for M7 Cross-Sectional Momentum.

Usage:
    conda activate strategy-lab
    python run.py --mode backtest
    python run.py --mode live
    python run.py --mode live --capital-cap 30000
"""

import argparse
import logging
import os
import sys
import traceback
from pathlib import Path

import config
from data.alpaca_data import fetch_bars
from strategies.momentum import CrossSectionalMomentum, LiveMomentumTrader


def _setup_logging(log_path: str) -> logging.Logger:
    """Configure the root logger (stdout + file) so all module loggers propagate here."""
    Path("output").mkdir(exist_ok=True)
    root = logging.getLogger()
    # Guard: don't add duplicate handlers if called more than once in a session
    if root.handlers:
        root.handlers.clear()
    root.setLevel(logging.DEBUG)
    # Suppress noisy third-party debug logs
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    fmt = logging.Formatter("[%(asctime)s UTC] %(levelname)s %(name)s — %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(log_path)
    fh.setFormatter(fmt)
    root.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    root.addHandler(ch)
    return logging.getLogger("run")


def _setup_live_logging() -> logging.Logger:
    return _setup_logging("output/live_rebalance.log")


def _setup_backtest_logging() -> logging.Logger:
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return _setup_logging(f"output/backtest_{ts}.log")


def run_backtest() -> None:
    log = _setup_backtest_logging()
    try:
        log.info("=" * 55)
        log.info("  M7 Cross-Sectional Momentum — Backtest")
        log.info("=" * 55)
        log.info("  Symbols      : %s", ', '.join(config.M7_SYMBOLS))
        log.info("  Lookback     : %d days", config.LOOKBACK)
        log.info("  Top-N        : %d", config.TOP_N)
        log.info("  Period       : %s → %s", config.START_DATE, config.END_DATE)
        log.info("  Capital      : $%s", f"{config.INITIAL_AMOUNT:,.0f}")
        log.info("  FTC/PTC      : %s / %s", config.FTC, config.PTC)
        log.info("=" * 55)

        log.info("Fetching historical data from Alpaca...")
        data = fetch_bars(
            symbols=config.M7_SYMBOLS,
            start=config.START_DATE,
            end=config.END_DATE,
        )
        log.info("Data loaded. Bars per symbol: %d", next(iter(data.values())).shape[0])

        strategy = CrossSectionalMomentum(
            data=data,
            lookback=config.LOOKBACK,
            top_n=config.TOP_N,
            initial_amount=config.INITIAL_AMOUNT,
            ftc=config.FTC,
            ptc=config.PTC,
            verbose=True,
        )

        os.makedirs("output", exist_ok=True)
        strategy.run_backtest(save_path="output/equity_curve.png")
        log.info("Backtest complete. Equity curve saved to output/equity_curve.png")

    except Exception:  # noqa: BLE001
        log.error("BACKTEST FAILED — full traceback below:")
        log.error(traceback.format_exc())
        sys.exit(1)


def run_live_rebalance(capital_cap: float | None = None) -> None:
    print("=" * 55)
    print("  M7 Cross-Sectional Momentum — Live Paper Rebalance")
    print("=" * 55)
    print(f"  Symbols      : {', '.join(config.M7_SYMBOLS)}")
    print(f"  Lookback     : {config.LOOKBACK} days")
    print(f"  Top-N        : {config.TOP_N}")
    if capital_cap is not None:
        print(f"  Capital Cap  : ${capital_cap:,.0f}")
    print("=" * 55)
    print()

    trader = LiveMomentumTrader(
        symbols=config.M7_SYMBOLS,
        lookback=config.LOOKBACK,
        top_n=config.TOP_N,
        initial_amount=config.INITIAL_AMOUNT,
        max_capital=capital_cap,
    )
    trader.rebalance()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run momentum backtest or live paper rebalance.")
    parser.add_argument(
        "--mode",
        choices=["backtest", "live"],
        default="backtest",
        help="Execution mode: backtest (default) or one-shot live paper rebalance.",
    )
    parser.add_argument(
        "--capital-cap",
        type=float,
        default=None,
        help="Optional max USD to deploy for live mode (example: 30000).",
    )
    args = parser.parse_args()

    if args.mode == "live":
        log = _setup_live_logging()
        try:
            run_live_rebalance(capital_cap=args.capital_cap)
            log.info("Live rebalance completed successfully.")
        except Exception:  # noqa: BLE001
            log.error("LIVE REBALANCE FAILED — full traceback below:")
            log.error(traceback.format_exc())
            sys.exit(1)
    else:
        run_backtest()


if __name__ == "__main__":
    main()
