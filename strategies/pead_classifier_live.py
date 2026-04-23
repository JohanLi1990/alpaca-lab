"""PEAD live classifier wrapper.

Uses a frozen trained model for live entry predictions.
Falls back to training on historical data if no saved model exists.
"""

from __future__ import annotations

import logging
import pickle
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

import config
from data.alpaca_data import fetch_bars
from data.earnings_calendar import fetch_earnings_events
from data.pre_earnings_features import build_features
from strategies.pead_classifier import FEATURE_COLS

log = logging.getLogger(__name__)


class PEADClassifierLive:
    """Live PEAD classifier using frozen trained model."""
    FEATURE_COLS = FEATURE_COLS

    def __init__(self, symbol: str, model_path: str | None = None):
        """Initialize classifier.
        
        Parameters
        ----------
        symbol : str
            Symbol whose classifier should be loaded.
        model_path : str | None
            Optional explicit model path override.
        """
        self.symbol = symbol
        self.model_path = Path(model_path or self.get_model_path(symbol))
        self.model: LogisticRegression | None = None
        self.scaler: StandardScaler | None = None
        self.load_classifier()

    @staticmethod
    def get_model_path(symbol: str) -> str:
        """Return the on-disk model path for a symbol-specific classifier."""
        return f"output/pead_classifier_{symbol}.pkl"

    def load_classifier(self) -> None:
        """Load pre-trained classifier from pickle file."""
        try:
            if self.model_path.exists():
                with open(self.model_path, "rb") as f:
                    saved_data = pickle.load(f)
                    self.model = saved_data.get("model")
                    self.scaler = saved_data.get("scaler")
                if self.model and self.scaler:
                    log.info("Loaded pre-trained classifier from %s", self.model_path)
                else:
                    log.warning("Saved model file missing model or scaler, will train on demand")
                    self.model = None
                    self.scaler = None
            else:
                log.warning(
                    "Classifier model not found at %s, will train on demand during first live execution",
                    self.model_path,
                )
                self.model = None
                self.scaler = None
        except Exception as e:
            log.error("Failed to load classifier: %s", e)
            self.model = None
            self.scaler = None

    def train_on_historical_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        min_train: int = 20,
    ) -> None:
        """Train classifier on historical data (on-demand fallback).
        
        Parameters
        ----------
        symbol : str
            Stock symbol
        start_date : str
            Training period start (YYYY-MM-DD)
        end_date : str
            Training period end (YYYY-MM-DD)
        min_train : int
            Minimum training events
        """
        try:
            log.info("Training classifier on historical data for %s...", symbol)
            
            # Fetch earnings events
            events_df = fetch_earnings_events(
                symbol=symbol,
                start=start_date,
                end=end_date,
                timing="AMC",
            )
            log.info("Fetched %d AMC earnings events", len(events_df))
            
            # Fetch bars
            bars_dict = fetch_bars(
                symbols=[symbol, "QQQ"],
                start=start_date,
                end=end_date,
            )
            log.info("Fetched bars for %s and QQQ", symbol)
            
            # Build features
            features_df = build_features(
                events_df=events_df,
                bars_dict=bars_dict,
                symbol=symbol,
                entry_offset_days=config.PEAD_ENTRY_OFFSET_DAYS,
            )
            log.info("Built features for %d events", len(features_df))
            
            if len(features_df) < min_train:
                log.warning(
                    "Insufficient training data: %d events < min_train %d",
                    len(features_df), min_train,
                )
                return
            
            # Train on all historical data
            X = features_df[self.FEATURE_COLS].values
            y = features_df["y"].values
            
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            self.model = LogisticRegression(random_state=42, max_iter=1000)
            self.model.fit(X_scaled, y)
            
            log.info("Trained classifier on %d events", len(features_df))
            
            # Save model
            self.save_classifier()
            
        except Exception as e:
            log.error("Failed to train classifier: %s", e)
            raise

    def save_classifier(self) -> None:
        """Save trained model to pickle file."""
        try:
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.model_path, "wb") as f:
                pickle.dump(
                    {"model": self.model, "scaler": self.scaler},
                    f,
                )
            log.info("Saved classifier to %s", self.model_path)
        except Exception as e:
            log.error("Failed to save classifier: %s", e)
            raise

    def predict_entry(self, features: dict[str, float]) -> tuple[int, float]:
        """Generate entry prediction (pred_label, prob_positive).
        
        Parameters
        ----------
        features : dict[str, float]
            Feature dict with keys matching FEATURE_COLS
            
        Returns
        -------
        tuple[int, float]
            (pred_label: 0 or 1, prob_positive: probability)
            
        Raises
        ------
        ValueError
            If model is not trained
        """
        if self.model is None or self.scaler is None:
            raise ValueError("Classifier not trained. Call train_on_historical_data() first.")
        
        # Extract features in correct order
        X = np.array([[features.get(col, 0.0) for col in self.FEATURE_COLS]])
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Predict
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X_scaled)
            prob_positive = probs[0, 1]
        else:
            prob_positive = float(self.model.predict(X_scaled)[0])
        
        pred_label = 1 if prob_positive >= 0.5 else 0
        
        return pred_label, prob_positive

    def ensure_trained(self) -> None:
        """Train and save the symbol model if it is missing on disk."""
        if self.model is not None and self.scaler is not None:
            return

        self.train_on_historical_data(
            symbol=self.symbol,
            start_date=config.PEAD_START_DATE,
            end_date=config.PEAD_END_DATE,
            min_train=config.PEAD_MIN_TRAIN,
        )

        if self.model is None or self.scaler is None:
            raise ValueError(
                f"Classifier for {self.symbol} could not be trained. Check training data availability."
            )
