"""Daily cronjob for PEAD live trading execution.

Runs daily to check entry and exit conditions for configured symbols.
Entry: T-E open if classifier predicts positive using bars through T-(E+1) close
Exit: T+1 or later if position is open

Usage:
    python scripts/pead_live_cronjob.py
"""

from __future__ import annotations

import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import config
from core.pead_state_manager import PEADStateManager
from core.pead_trade_logger import PEADTradeLogger
from data.alpaca_data import fetch_bars
from data.pead_calendar import (
    calculate_offset_trading_date,
    clear_earnings_cache,
    get_cached_earnings,
    get_current_market_date,
    get_pead_timing_dates,
    is_today_entry_date,
    is_today_exit_date,
)
from data.pre_earnings_features import build_features
from strategies.pead_classifier_live import PEADClassifierLive
from strategies.pead_live_trader import PEADLiveTrader

log = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure logging for cronjob."""
    log_path = Path("output") / f"pead_live_cronjob_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    root = logging.getLogger()
    if root.handlers:
        root.handlers.clear()
    root.setLevel(logging.DEBUG)
    
    fmt = logging.Formatter(
        "[%(asctime)s UTC] %(levelname)s %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fmt.converter = time.gmtime
    
    fh = logging.FileHandler(log_path)
    fh.setFormatter(fmt)
    root.addHandler(fh)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    root.addHandler(ch)
    
    log.info("=" * 70)
    log.info("PEAD LIVE CRONJOB STARTED")
    log.info("=" * 70)


def run_daily_execution() -> None:
    """Execute daily PEAD live trading logic."""
    setup_logging()
    feature_anchor_offset_days = config.get_pead_feature_anchor_offset_days()
    log.info(
        "Effective PEAD timing: entry_offset_days=%d feature_anchor_offset_days=%d exit_mode=%s",
        config.PEAD_ENTRY_OFFSET_DAYS,
        feature_anchor_offset_days,
        config.PEAD_EXIT_MODE,
    )
    
    state_manager = PEADStateManager(config.PEAD_LIVE_STATE_FILE)
    trade_logger = PEADTradeLogger(config.PEAD_LIVE_LOG_FILE)
    trader = PEADLiveTrader(paper=True, position_size_pct=config.PEAD_LIVE_POSITION_SIZE, profile="v2")
    summary = {
        "entries_fired": [],
        "entries_skipped": [],
        "exits_fired": [],
        "exits_held": [],
        "errors": [],
    }
    
    try:
        # Clean up stale entries
        state_manager.cleanup_stale_entries(days=config.PEAD_LIVE_STALE_DAYS)
        
        # Fetch earnings dates for all symbols
        log.info("Fetching earnings dates for symbols: %s", config.PEAD_LIVE_SYMBOLS)
        earnings_dates = {}
        for symbol in config.PEAD_LIVE_SYMBOLS:
            earnings_date = get_cached_earnings(symbol, use_cache=True)
            if earnings_date:
                earnings_dates[symbol] = earnings_date
                log.info("  %s: nearest earnings = %s", symbol, earnings_date)
            else:
                log.warning("  %s: no earnings date found", symbol)
        
        # Process each symbol
        for symbol in config.PEAD_LIVE_SYMBOLS:
            log.info("Processing symbol: %s", symbol)
            
            try:
                classifier = PEADClassifierLive(symbol=symbol)
                if symbol not in earnings_dates:
                    log.warning("No earnings date for %s, skipping", symbol)
                    continue
                
                earnings_date = earnings_dates[symbol]
                timing_dates = get_pead_timing_dates(
                    earnings_date,
                    config.PEAD_ENTRY_OFFSET_DAYS,
                )
                entry_date = timing_dates["entry_date"]
                feature_anchor_date = timing_dates["feature_anchor_date"]
                exit_date = timing_dates["exit_date"]
                today = get_current_market_date()

                log.info(
                    "  Derived dates for %s: entry=T-%d on %s | anchor=T-%d on %s | exit=T+1 on %s | today=%s",
                    symbol,
                    config.PEAD_ENTRY_OFFSET_DAYS,
                    entry_date.date() if entry_date is not None else "unavailable",
                    config.PEAD_ENTRY_OFFSET_DAYS + 1,
                    feature_anchor_date.date() if feature_anchor_date is not None else "unavailable",
                    exit_date.date() if exit_date is not None else "unavailable",
                    today,
                )
                
                # Check for ENTRY (if today is T-E)
                if is_today_entry_date(symbol, earnings_dates, entry_offset_days=config.PEAD_ENTRY_OFFSET_DAYS):
                    log.info(
                        "TODAY IS T-%d FOR %s (earnings %s)",
                        config.PEAD_ENTRY_OFFSET_DAYS,
                        symbol,
                        earnings_date,
                    )
                    
                    # Check if already traded this event (idempotency)
                    if state_manager.already_traded(symbol, earnings_date):
                        log.info("Already entered %s for earnings %s, skipping", symbol, earnings_date)
                        summary["entries_skipped"].append((symbol, "already_traded"))
                        continue
                    
                    if entry_date is None:
                        log.error("Could not calculate entry date T-%d for %s", config.PEAD_ENTRY_OFFSET_DAYS, symbol)
                        summary["errors"].append((symbol, "entry_date_calculation"))
                        continue
                    if feature_anchor_date is None:
                        log.warning(
                            "Skipping %s: missing feature-anchor T-%d bar for earnings %s",
                            symbol,
                            config.PEAD_ENTRY_OFFSET_DAYS + 1,
                            earnings_date,
                        )
                        summary["entries_skipped"].append((symbol, "missing_feature_anchor_bar"))
                        continue

                    # Fetch 7-day OHLCV ending at feature anchor (for T-3 open: T-10 to T-4)
                    feature_window_start = calculate_offset_trading_date(feature_anchor_date, -6)
                    if feature_window_start is None:
                        log.warning(
                            "Skipping %s: insufficient history to derive 7-day feature window ending %s",
                            symbol,
                            feature_anchor_date.date(),
                        )
                        summary["entries_skipped"].append((symbol, "insufficient_feature_history"))
                        continue
                    
                    try:
                        log.info(
                            "Fetching bars for %s from %s to %s (entry=T-%d on %s, anchor=T-%d on %s)",
                            symbol,
                            feature_window_start.date(),
                            feature_anchor_date.date(),
                            config.PEAD_ENTRY_OFFSET_DAYS,
                            entry_date.date(),
                            config.PEAD_ENTRY_OFFSET_DAYS + 1,
                            feature_anchor_date.date(),
                        )
                        bars_dict = fetch_bars(
                            symbols=[symbol, "QQQ"],
                            start=str(feature_window_start.date()),
                            end=str(feature_anchor_date.date()),
                            profile="v2",
                        )

                        symbol_index = bars_dict[symbol].index
                        symbol_trading_dates = set(pd.to_datetime(symbol_index).strftime("%Y-%m-%d"))
                        if str(feature_anchor_date.date()) not in symbol_trading_dates:
                            log.warning(
                                "Skipping %s: missing feature-anchor bar %s in fetched daily data",
                                symbol,
                                feature_anchor_date.date(),
                            )
                            summary["entries_skipped"].append((symbol, "missing_feature_anchor_bar"))
                            continue
                        
                        # Build features for this event
                        # Create minimal events DataFrame for this single event
                        event_df = pd.DataFrame({
                            "earnings_date": [earnings_date],
                            "symbol": [symbol],
                            "t_feature_anchor": [str(feature_anchor_date.date())],
                        })
                        
                        features = build_features(
                            events_df=event_df,
                            bars_dict=bars_dict,
                            symbol=symbol,
                            include_labels=False,
                            entry_offset_days=config.PEAD_ENTRY_OFFSET_DAYS,
                        )
                        
                        if features.empty:
                            log.warning("Could not build features for %s", symbol)
                            summary["entries_skipped"].append((symbol, "feature_build_failed"))
                            continue
                        
                        # Extract features for prediction
                        features_row = features.iloc[0]
                        features_dict = {
                            col: float(features_row[col])
                            for col in classifier.FEATURE_COLS
                        }
                        
                        # Classify
                        classifier.ensure_trained()
                        pred_label, prob_positive = classifier.predict_entry(features_dict)
                        log.info("Prediction for %s: label=%d prob=%.4f", symbol, pred_label, prob_positive)
                        
                        if pred_label != 1:
                            log.info("Classifier predicts negative (label=%d) for %s, skipping entry", pred_label, symbol)
                            trade_logger.log_skipped_entry(symbol, earnings_date, str(entry_date.date()), f"pred_label={pred_label}")
                            summary["entries_skipped"].append((symbol, f"pred_label={pred_label}"))
                            continue
                        
                        # Place entry order
                        entry_result = trader.place_entry_order(symbol)
                        if entry_result is None:
                            log.error("Failed to place entry order for %s", symbol)
                            summary["errors"].append((symbol, "entry_order_failed"))
                            continue
                        
                        order_id, entry_price, entry_qty = entry_result
                        
                        # Update state
                        state_manager.add_position(
                            symbol=symbol,
                            earnings_date=earnings_date,
                            entry_date=str(entry_date.date()),
                            entry_price=entry_price,
                            entry_qty=entry_qty,
                        )
                        
                        log.info("Entry successful: %s %d @ %.2f (order %s)", symbol, entry_qty, entry_price, order_id)
                        summary["entries_fired"].append((symbol, earnings_date, entry_price, entry_qty))
                        
                    except Exception as e:
                        log.error("Entry logic failed for %s: %s", symbol, e)
                        summary["errors"].append((symbol, f"entry_exception: {e}"))
                else:
                    if entry_date is not None:
                        log.info(
                            "No entry evaluation for %s today: configured entry date was %s",
                            symbol,
                            entry_date.date(),
                        )
                    else:
                        log.info("No entry evaluation for %s today: entry date unavailable", symbol)
                
                # Check for EXIT (if today is T+1 or later)
                if is_today_exit_date(symbol, earnings_dates):
                    position = state_manager.get_position(symbol)
                    
                    if position is None:
                        log.info("No open position for %s on T+1, skipping exit", symbol)
                        continue
                    
                    # Verify this is the same earnings event
                    if position.get("earnings_date") != earnings_date:
                        log.warning(
                            "Position earnings_date mismatch for %s: position=%s current=%s",
                            symbol, position.get("earnings_date"), earnings_date,
                        )
                        continue
                    
                    log.info("TODAY IS T+1+ FOR %s (earnings %s)", symbol, earnings_date)
                    
                    # Get current price for PnL
                    exit_price = trader.get_current_price(symbol)
                    if exit_price is None:
                        log.error("Could not get current price for %s", symbol)
                        summary["errors"].append((symbol, "exit_price_failed"))
                        continue
                    
                    entry_price = position["entry_price"]
                    entry_qty = position["entry_qty"]
                    
                    # Place exit order
                    exit_result = trader.place_exit_order(symbol, entry_qty)
                    if exit_result is None:
                        log.error("Failed to place exit order for %s", symbol)
                        summary["errors"].append((symbol, "exit_order_failed"))
                        continue
                    
                    order_id, fill_price = exit_result
                    
                    # Compute PnL (with transaction costs)
                    gross_pnl_pct = (fill_price - entry_price) / entry_price if entry_price > 0 else 0.0
                    net_pnl_pct = gross_pnl_pct - (2 * config.PEAD_LIVE_PTC)
                    pnl_dollars = net_pnl_pct * entry_price * entry_qty
                    
                    # Log trade
                    t_plus_1 = calculate_offset_trading_date(earnings_date, 1)
                    exit_date_str = str(t_plus_1.date()) if t_plus_1 else str(get_current_market_date())
                    
                    trade_logger.log_trade(
                        symbol=symbol,
                        earnings_date=earnings_date,
                        entry_date=position["entry_date"],
                        exit_date=exit_date_str,
                        entry_price=entry_price,
                        exit_price=fill_price,
                        qty=entry_qty,
                        pnl=pnl_dollars,
                        pnl_pct=net_pnl_pct,
                    )
                    
                    # Remove position from state (clean slate)
                    state_manager.remove_position(symbol)
                    
                    log.info(
                        "Exit successful: %s %d @ %.2f | PnL=%.2f (%.2f%%) | order=%s",
                        symbol, entry_qty, fill_price, pnl_dollars, net_pnl_pct * 100, order_id,
                    )
                    summary["exits_fired"].append((symbol, earnings_date, fill_price, pnl_dollars, net_pnl_pct))
                else:
                    if exit_date is not None:
                        log.info(
                            "No exit evaluation for %s today: exit date is %s",
                            symbol,
                            exit_date.date(),
                        )
                    else:
                        log.info("No exit evaluation for %s today: exit date unavailable", symbol)
                
            except Exception as e:
                log.error("Error processing symbol %s: %s", symbol, e, exc_info=True)
                summary["errors"].append((symbol, str(e)))
        
        # Summary report
        log.info("=" * 70)
        log.info("DAILY EXECUTION SUMMARY")
        log.info("=" * 70)
        log.info("  Entries fired:    %d", len(summary["entries_fired"]))
        for sym, earnings, price, qty in summary["entries_fired"]:
            log.info("    - %s earnings=%s price=%.2f qty=%d", sym, earnings, price, qty)
        
        log.info("  Entries skipped:  %d", len(summary["entries_skipped"]))
        for sym, reason in summary["entries_skipped"]:
            log.info("    - %s: %s", sym, reason)
        
        log.info("  Exits fired:      %d", len(summary["exits_fired"]))
        for sym, earnings, price, pnl, pnl_pct in summary["exits_fired"]:
            log.info("    - %s earnings=%s price=%.2f pnl=%.2f (%.2f%%)", sym, earnings, price, pnl, pnl_pct * 100)
        
        log.info("  Errors:           %d", len(summary["errors"]))
        for sym, error in summary["errors"]:
            log.info("    - %s: %s", sym, error)
        
        log.info("=" * 70)
        log.info("PEAD LIVE CRONJOB COMPLETED")
        log.info("=" * 70)
        
        # Clear cache for next execution
        clear_earnings_cache()
        
    except Exception as e:
        log.error("Cronjob failed with exception: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run_daily_execution()
