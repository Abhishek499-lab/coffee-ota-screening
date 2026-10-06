"""
Combine sequence-evidence and environmental-evidence features into one
interpretable per-batch risk score.

Two layers, deliberately kept separate:
  1. combine_scores() — a simple, fully transparent weighted-sum model.
     This is what you pitch first: it's explainable to a non-technical
     QC stakeholder in one sentence, which matters for buy-in.
  2. train_demo_model() — an optional learned Logistic Regression, shown
     to demonstrate the pipeline CAN be upgraded to a trained model once
     real labeled outcomes (actual lab contamination results) exist.
     Currently trained on synthetic labels — do not present its output
     as a validated prediction.
"""

from typing import Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from src.config import (
    SEQUENCE_EVIDENCE_WEIGHT,
    ENVIRONMENT_EVIDENCE_WEIGHT,
    HIGH_RISK_THRESHOLD,
    RANDOM_SEED,
)


def combine_scores(seq_features: pd.DataFrame, env_features: pd.DataFrame) -> pd.DataFrame:
    """
    Weighted-sum combination of marker_match_score and env_risk_score
    into one final_risk_score per batch, plus a high_priority flag.
    """
    merged = seq_features.merge(env_features, on="batch_id", how="outer")

    # Batches with no sequence data yet still get scored on environment
    # alone (common case — sequencing is slower/costlier than logging
    # storage conditions).
    merged["marker_match_score"] = merged["marker_match_score"].fillna(0.0)
    merged["env_risk_score"] = merged["env_risk_score"].fillna(0.0)

    merged["final_risk_score"] = (
        merged["marker_match_score"] * SEQUENCE_EVIDENCE_WEIGHT
        + merged["env_risk_score"] * ENVIRONMENT_EVIDENCE_WEIGHT
    ).round(4)

    merged["high_priority_for_lab_testing"] = (
        merged["final_risk_score"] >= HIGH_RISK_THRESHOLD
    )

    return merged.sort_values("final_risk_score", ascending=False).reset_index(drop=True)


def train_demo_model(n_samples: int = 200) -> Tuple[LogisticRegression, float]:
    """
    DEMO ONLY. Trains Logistic Regression on synthetic data to show the
    pipeline's learned-model path works end-to-end. Replace the
    synthetic generator with real labeled (features, lab_confirmed_
    contaminated) data as soon as you have it — do not ship this
    trained-on-fake-data model as a real prediction tool.

    Returns the fitted model and its accuracy on a held-out synthetic
    test split (sanity check only, not a real accuracy claim).
    """
    rng = np.random.default_rng(RANDOM_SEED)

    marker_score = rng.uniform(0, 1, n_samples)
    env_score = rng.uniform(0, 1, n_samples)
    # Synthetic ground truth: higher combined signal -> more likely
    # "contaminated", with noise. FOR DEMO/PIPELINE-TESTING ONLY.
    true_prob = 0.6 * marker_score + 0.4 * env_score
    labels = (true_prob + rng.normal(0, 0.15, n_samples)) > 0.5

    X = np.column_stack([marker_score, env_score])
    y = labels.astype(int)

    split = int(n_samples * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = LogisticRegression(random_state=RANDOM_SEED)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    return model, accuracy
