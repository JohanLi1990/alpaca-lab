"""ML classifier for earnings gap predictions using walk-forward cross-validation.

Implements event-level expanding-window walk-forward validation with logistic
regression (Phase 1) or configurable classifiers (Phase 2).
"""

from __future__ import annotations

import logging
import pickle
from pathlib import Path
from typing import Any, Type

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

log = logging.getLogger(__name__)


FEATURE_COLS = [
    "drift_7d",
    "drift_slope",
    "up_day_count",
    "down_day_count",
    "rel_volume_mean",
    "down_volume_ratio",
    "atr_ratio",
    "gap_count",
    "rel_drift_vs_qqq",
]


def walk_forward_predict(
    features_df: pd.DataFrame,
    min_train: int = 20,
    threshold: float = 0.5,
    model_cls: Type[Any] | None = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """Run expanding-window walk-forward prediction.

    Parameters
    ----------
    features_df : pd.DataFrame
        Features DataFrame indexed by earnings_date with columns:
        drift_7d, drift_slope, up_day_count, down_day_count, rel_volume_mean,
        down_volume_ratio, atr_ratio, gap_count, rel_drift_vs_qqq, y, gap_return.
    min_train : int
        Minimum number of training events before making first prediction.
    threshold : float
        Probability threshold for binary prediction (default 0.5).
    model_cls : type or None
        Classifier class (e.g., LogisticRegression). Default: LogisticRegression.
    verbose : bool
        If True, log feature coefficients after each fold fit.

    Returns
    -------
    pd.DataFrame
        Predictions DataFrame with columns:
        - earnings_date: event date (index)
        - prob_positive: predicted probability of positive gap
        - pred_label: thresholded prediction (0 or 1)
        - y: actual target label
        - gap_return: actual gap return

    Notes
    -----
    - Predictions only available from position min_train onward.
    - Earlier events are in-sample training only.
    """
    features_df = features_df.sort_index().copy()

    if model_cls is None:
        model_cls = LogisticRegression

    X = features_df[FEATURE_COLS].values
    y = features_df["y"].values
    gap_returns = features_df["gap_return"].values
    dates = features_df.index

    predictions = []

    # Walk-forward loop
    for test_idx in range(min_train, len(features_df)):
        train_idx = test_idx - 1  # Expanding window: 0..test_idx-1 for training
        train_size = train_idx + 1

        # Ensure we have at least min_train events for training
        if train_size < min_train:
            continue

        # Split data
        X_train, y_train = X[:train_idx + 1], y[:train_idx + 1]
        X_test = X[test_idx : test_idx + 1]

        # Fit scaler on training data only
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train model
        model = model_cls(random_state=42, max_iter=1000)
        model.fit(X_train_scaled, y_train)

        # Log coefficients if verbose
        if verbose and hasattr(model, "coef_"):
            coefs = model.coef_[0]
            abs_coefs = np.abs(coefs)
            sorted_idx = np.argsort(-abs_coefs)
            log.info(f"Fold {test_idx} ({train_size} train events) - Top feature coefficients:")
            for i, idx in enumerate(sorted_idx[:5]):
                log.info(
                    f"  {i + 1}. {FEATURE_COLS[idx]}: {coefs[idx]:.4f}"
                )

        # Predict
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_test_scaled)
            prob_positive = probs[0, 1]  # Probability of class 1
        else:
            # Fallback for models without predict_proba
            prob_positive = float(model.predict(X_test_scaled)[0])

        pred_label = 1 if prob_positive >= threshold else 0

        predictions.append({
            "earnings_date": dates[test_idx],
            "prob_positive": prob_positive,
            "pred_label": pred_label,
            "y": y[test_idx],
            "gap_return": gap_returns[test_idx],
        })

    if not predictions:
        raise ValueError(
            f"No predictions made; check min_train ({min_train}) vs feature_df length ({len(features_df)})"
        )

    result = pd.DataFrame(predictions)
    result.set_index("earnings_date", inplace=True)

    log.info(f"Generated {len(result)} walk-forward predictions")
    return result


def evaluate(predictions_df: pd.DataFrame) -> dict[str, Any]:
    """Evaluate classifier predictions.

    Parameters
    ----------
    predictions_df : pd.DataFrame
        Predictions DataFrame with columns: pred_label, y, gap_return.

    Returns
    -------
    dict
        Report with keys:
        - hit_rate: proportion of correct predictions among all events
        - baseline_rate: proportion of positive events in full data
        - n_trades: number of predicted-positive events
        - avg_gap_return: mean gap return for predicted-positive events
        - avg_gap_return_negative: mean gap return for predicted-negative events
        - n_total: total number of events
    """
    correct = (predictions_df["pred_label"] == predictions_df["y"]).sum()
    hit_rate = correct / len(predictions_df) if len(predictions_df) > 0 else 0.0
    baseline_rate = predictions_df["y"].mean()

    n_trades = (predictions_df["pred_label"] == 1).sum()
    n_total = len(predictions_df)

    if n_trades > 0:
        avg_gap_return = predictions_df[predictions_df["pred_label"] == 1]["gap_return"].mean()
    else:
        avg_gap_return = 0.0

    n_negative_pred = (predictions_df["pred_label"] == 0).sum()
    if n_negative_pred > 0:
        avg_gap_return_negative = predictions_df[predictions_df["pred_label"] == 0][
            "gap_return"
        ].mean()
    else:
        avg_gap_return_negative = 0.0

    return {
        "hit_rate": hit_rate,
        "baseline_rate": baseline_rate,
        "n_trades": n_trades,
        "avg_gap_return": avg_gap_return,
        "avg_gap_return_negative": avg_gap_return_negative,
        "n_total": n_total,
    }


def print_eval_report(report: dict[str, Any]) -> None:
    """Print evaluation report to stdout.

    Parameters
    ----------
    report : dict
        Dictionary returned by evaluate().
    """
    log.info("=" * 70)
    log.info("PEAD CLASSIFIER EVALUATION")
    log.info("=" * 70)
    log.info(f"Total events:                     {report['n_total']}")
    log.info(f"Predicted positive:               {report['n_trades']}")
    log.info(f"Predicted negative:               {report['n_total'] - report['n_trades']}")
    log.info(f"Baseline positive rate:           {report['baseline_rate']:.2%}")
    log.info(f"Hit rate (accuracy):              {report['hit_rate']:.2%}")
    log.info(f"Avg gap return (pred positive):   {report['avg_gap_return']:.2%}")
    log.info(f"Avg gap return (pred negative):   {report['avg_gap_return_negative']:.2%}")
    log.info(f"Expected value per trade:         {report['avg_gap_return'] - 0.001:.4f} (after ptc)")
    log.info("=" * 70)


def fit_final_classifier(
    features_df: pd.DataFrame,
    model_cls: Type[Any] | None = None,
) -> tuple[Any, StandardScaler]:
    """Fit a final classifier on the full feature set for later live inference."""
    features_df = features_df.sort_index().copy()

    if model_cls is None:
        model_cls = LogisticRegression

    X = features_df[FEATURE_COLS].values
    y = features_df["y"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = model_cls(random_state=42, max_iter=1000)
    model.fit(X_scaled, y)

    return model, scaler


def save_trained_classifier(model: Any, scaler: StandardScaler, model_path: str | Path) -> None:
    """Persist a trained classifier/scaler pair to disk."""
    path = Path(model_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump({"model": model, "scaler": scaler}, f)

    log.info("Saved trained classifier to %s", path)
