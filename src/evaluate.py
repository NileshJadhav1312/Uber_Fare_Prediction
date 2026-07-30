"""Evaluate the saved XGBoost model on processed_data.csv."""

import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

DATA_PATH = os.path.join(BASE_DIR, "data", "processed_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_model.pkl")


def evaluate_xgboost():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data not found: {DATA_PATH}")

    model = joblib.load(MODEL_PATH)
    data = pd.read_csv(DATA_PATH)
    X = data.drop(columns=["Fare (Target)"])
    y = data["Fare (Target)"]
    preds = model.predict(X)

    metrics = {
        "r2": r2_score(y, preds),
        "mae": mean_absolute_error(y, preds),
        "rmse": float(np.sqrt(mean_squared_error(y, preds))),
        "n": len(data),
    }

    print("=" * 56)
    print("XGBoost evaluation — Uber Fare Prediction")
    print("=" * 56)
    print(f"Samples : {metrics['n']}")
    print(f"R²      : {metrics['r2']:.4f} ({metrics['r2'] * 100:.2f}%)")
    print(f"MAE     : ₹{metrics['mae']:.2f}")
    print(f"RMSE    : ₹{metrics['rmse']:.2f}")
    print("=" * 56)
    return metrics


if __name__ == "__main__":
    evaluate_xgboost()
