#!/usr/bin/env python3
"""Run one weekly live paper rebalance with optional safety guards.

Examples:
    python scripts/weekly_live_rebalance.py
    python scripts/weekly_live_rebalance.py --capital-cap 30000
    python scripts/weekly_live_rebalance.py --force
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path


def _setup_logging(log_path: Path) -> logging.Logger:
    """Configure the root logger (stdout + file) so all module loggers propagate here."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    # Suppress noisy third-party debug logs
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    fmt = logging.Formatter("[%(asctime)s UTC] %(levelname)s %(name)s — %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
    # File handler — append so history is preserved
    fh = logging.FileHandler(log_path)
    fh.setFormatter(fmt)
    root.addHandler(fh)
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    root.addHandler(ch)
    return logging.getLogger("weekly")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Weekly live rebalance runner.")

    def _positive_float(value: str) -> float:
        parsed = float(value)
        if parsed <= 0:
            raise argparse.ArgumentTypeError("--capital-cap must be > 0")
        return parsed

    parser.add_argument(
        "--capital-cap",
        type=_positive_float,
        default=None,
        help="Optional max USD to deploy for strategy positions.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Run even if today is not Monday UTC.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    os.chdir(repo_root)
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    log = _setup_logging(repo_root / "output" / "live_rebalance.log")

    # Monday-only safety guard in UTC. Cron: 45 19 * * 1 (19:45 UTC / 2:45 PM ET)
    # — submits MOC orders with a 5-min buffer before the 19:50 UTC Alpaca MOC cutoff.
    now_utc = datetime.now(timezone.utc)
    if not args.force and now_utc.weekday() != 0:
        log.info(
            "Skip: today is %s UTC; runner executes on Mondays only.",
            now_utc.strftime("%A"),
        )
        return 0

    try:
        import config
        from data.alpaca_data import _get_retry_config
        from strategies.momentum import LiveMomentumTrader

        retry_count, retry_delay_sec = _get_retry_config()
        total_attempts = retry_count + 1
        worst_case_wait_min = (retry_count * retry_delay_sec) / 60.0

        log.info("=" * 55)
        log.info("  Weekly M7 Live Paper Rebalance")
        log.info("=" * 55)
        log.info("  Alpaca Data Retry Policy (bars fetch):")
        log.info(
            "    retries=%d | delay=%.0fs | total attempts=%d | worst-case added wait=%.1f min",
            retry_count,
            retry_delay_sec,
            total_attempts,
            worst_case_wait_min,
        )
        log.info("=" * 55)
        log.info("  Symbols    : %s", ", ".join(config.M7_SYMBOLS))
        log.info("  Lookback   : %d days", config.LOOKBACK)
        log.info("  Top-N      : %d", config.TOP_N)
        if args.capital_cap is not None:
            log.info("  Capital Cap: $%s", f"{args.capital_cap:,.0f}")
        else:
            log.info("  Capital Cap: auto (50%% of available cash)")
        log.info("=" * 55)

        trader = LiveMomentumTrader(
            symbols=config.M7_SYMBOLS,
            lookback=config.LOOKBACK,
            top_n=config.TOP_N,
            initial_amount=config.INITIAL_AMOUNT,
            max_capital=args.capital_cap,
            profile="v1",
        )
        trader.rebalance()
        log.info("Weekly rebalance completed successfully.")
        return 0

    except Exception:  # noqa: BLE001
        log.error("REBALANCE FAILED — full traceback below:")
        log.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
