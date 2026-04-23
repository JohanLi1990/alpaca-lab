"""
run.py — Entry point for Momentum Backtest, Live Trading, and PEAD Strategies.

Usage:
    conda activate strategy-lab
    python run.py --mode backtest                           # M7 momentum backtest
    python run.py --mode live                               # M7 live paper rebalance
    python run.py --mode live --capital-cap 30000           # M7 live with capital limit
    python run.py --mode pead-backtest                      # PEAD earnings prediction backtest
    python run.py --mode pead-live                          # PEAD daily live trading (cronjob)
"""

import argparse
import logging
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import config
from data.alpaca_data import fetch_bars
from data.earnings_calendar import fetch_earnings_events
from data.pre_earnings_features import build_features
from strategies.momentum import CrossSectionalMomentum, LiveMomentumTrader
from strategies.pead_classifier import (
    evaluate,
    fit_final_classifier,
    print_eval_report,
    save_trained_classifier,
    walk_forward_predict,
)
from strategies.pead_backtest import PEADBacktest
from strategies.pead_classifier_live import PEADClassifierLive


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
    fmt.converter = time.gmtime
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


def _setup_pead_logging() -> logging.Logger:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return _setup_logging(f"output/pead_backtest_{ts}.log")


def run_pead_backtest() -> None:
    """Run PEAD ML backtest pipeline for each configured PEAD symbol."""
    log = _setup_pead_logging()
    try:
        feature_anchor_offset_days = config.get_pead_feature_anchor_offset_days()
        log.info("=" * 70)
        log.info("  Post-Earnings Announcements Drift (PEAD) — ML Backtest")
        log.info("=" * 70)
        log.info("  Symbols      : %s", ', '.join(config.PEAD_SYMBOLS))
        log.info("  Period       : %s → %s", config.PEAD_START_DATE, config.PEAD_END_DATE)
        log.info("  Position Sz  : %.1f%%", config.PEAD_POSITION_SIZE * 100)
        log.info("  PTC per leg  : %.1f%%", config.PEAD_PTC * 100)
        log.info("  Min train    : %d events", config.PEAD_MIN_TRAIN)
        log.info("  Entry timing : T-%d open", config.PEAD_ENTRY_OFFSET_DAYS)
        log.info("  Feature stop : T-%d close", feature_anchor_offset_days)
        log.info("  Exit timing  : %s", config.PEAD_EXIT_MODE)
        log.info("=" * 70)

        for index, symbol in enumerate(config.PEAD_SYMBOLS, start=1):
            log.info("=" * 70)
            log.info("Symbol %d/%d: %s", index, len(config.PEAD_SYMBOLS), symbol)
            log.info("=" * 70)

            log.info("Step 1/6: Fetching earnings calendar from yfinance...")
            events = fetch_earnings_events(
                symbol=symbol,
                start=config.PEAD_START_DATE,
                end=config.PEAD_END_DATE,
                timing="AMC",
            )
            log.info("  Found %d AMC earnings events", len(events))

            log.info("Step 2/6: Fetching daily bars from Alpaca...")
            bars = fetch_bars(
                symbols=[symbol, "QQQ"],
                start=config.PEAD_START_DATE,
                end=config.PEAD_END_DATE,
            )
            log.info(
                "  Loaded %d bars for %s, %d bars for QQQ",
                len(bars[symbol]),
                symbol,
                len(bars["QQQ"]),
            )

            log.info("Step 3/6: Engineering pre-earnings features...")
            features = build_features(
                events_df=events,
                bars_dict=bars,
                symbol=symbol,
                entry_offset_days=config.PEAD_ENTRY_OFFSET_DAYS,
            )
            log.info("  Built features for %d events", len(features))
            log.info("  Baseline positive gap rate: %.1f%%", features["y"].mean() * 100)

            log.info("Step 4/6: Running walk-forward validation...")
            predictions = walk_forward_predict(
                features_df=features,
                min_train=config.PEAD_MIN_TRAIN,
                threshold=0.5,
                verbose=False,
            )
            log.info("  Generated %d predictions (%d skipped for training seed)", len(predictions), len(features) - len(predictions))

            log.info("Step 5/6: Running event-driven backtest...")
            backtest = PEADBacktest(
                predictions_df=predictions,
                bars_dict=bars,
                events_df=events,
                symbol=symbol,
                position_size=config.PEAD_POSITION_SIZE,
                ptc=config.PEAD_PTC,
                initial_amount=config.INITIAL_AMOUNT,
                entry_offset_days=config.PEAD_ENTRY_OFFSET_DAYS,
                exit_mode=config.PEAD_EXIT_MODE,
            )
            equity_curve, trades = backtest.run()

            log.info("Step 6/6: Fitting and saving final symbol model...")
            model, scaler = fit_final_classifier(features)
            model_path = PEADClassifierLive.get_model_path(symbol)
            save_trained_classifier(model, scaler, model_path)

            log.info("=" * 70)
            report = evaluate(predictions)
            print_eval_report(report)
            log.info("Saved symbol model for %s to %s", symbol, model_path)
            log.info("=" * 70)

            if len(trades) > 0:
                log.info("Per-trade records for %s (%d trades):", symbol, len(trades))
                for trade_idx, (date, trade) in enumerate(trades.iterrows()):
                    date_label = str(date)[:10]
                    log.info(
                        "  %d. %s | Entry=%.2f Exit=%.2f | Return=%+.2f%% | Pred=%d Actual=%d",
                        trade_idx + 1,
                        date_label,
                        trade["entry_price"],
                        trade["exit_price"],
                        trade["net_return"] * 100,
                        1 if trade["pred_prob"] >= 0.5 else 0,
                        int(trade["y"]),
                    )

        log.info("PEAD backtest completed successfully.")

    except Exception:  # noqa: BLE001
        log.error("PEAD BACKTEST FAILED — full traceback below:")
        log.error(traceback.format_exc())
        sys.exit(1)


def _setup_pead_live_logging() -> logging.Logger:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return _setup_logging(f"output/pead_live_{ts}.log")


def run_pead_live() -> None:
    """Run PEAD live paper trading daily cronjob."""
    log = _setup_pead_live_logging()
    try:
        feature_anchor_offset_days = config.get_pead_feature_anchor_offset_days()
        log.info("=" * 70)
        log.info("  PEAD Live Paper Trading — Daily Execution")
        log.info("=" * 70)
        log.info("  Symbols      : %s", ', '.join(config.PEAD_LIVE_SYMBOLS))
        log.info("  Position Pct : %.1f%%", config.PEAD_LIVE_POSITION_SIZE * 100)
        log.info("  Entry timing : T-%d open", config.PEAD_ENTRY_OFFSET_DAYS)
        log.info("  Feature stop : T-%d close", feature_anchor_offset_days)
        log.info("  Exit timing  : %s", config.PEAD_EXIT_MODE)
        log.info("  State File   : %s", config.PEAD_LIVE_STATE_FILE)
        log.info("  Trade Log    : %s", config.PEAD_LIVE_LOG_FILE)
        log.info("=" * 70)

        # Import and run cronjob
        from scripts.pead_live_cronjob import run_daily_execution
        run_daily_execution()
        
        log.info("PEAD live execution completed successfully.")

    except Exception:  # noqa: BLE001
        log.error("PEAD LIVE EXECUTION FAILED — full traceback below:")
        log.error(traceback.format_exc())
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run momentum backtest, live paper rebalance, PEAD ML backtest, or PEAD live trading.")
    parser.add_argument(
        "--mode",
        choices=["backtest", "live", "pead-backtest", "pead-live"],
        default="backtest",
        help="Execution mode: backtest (default), live paper rebalance, pead-backtest (ML earnings prediction), or pead-live (live PEAD trading).",
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
    elif args.mode == "pead-backtest":
        run_pead_backtest()
    elif args.mode == "pead-live":
        run_pead_live()
    else:
        run_backtest()


if __name__ == "__main__":
    main()
