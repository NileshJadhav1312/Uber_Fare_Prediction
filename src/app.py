"""Flask API for Uber fare prediction (serves frontend + /api/predict)."""

import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.predict import load_xgboost_model, predict_fare, reload_xgboost_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_model.pkl")

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

try:
    load_xgboost_model()
    print("[OK] XGBoost model loaded.")
except Exception as exc:
    print(f"[WARNING] Could not load XGBoost model: {exc}")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "model": "XGBoost Regressor",
        "metrics": {"r2_score": 0.9897, "mae": 128.20, "rmse": 171.11},
    })


@app.route("/api/reload", methods=["POST"])
def reload_model():
    """Hot-reload the XGBoost model from disk after retraining."""
    try:
        _, features = reload_xgboost_model()
        mtime = os.path.getmtime(MODEL_PATH)
        last_modified = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        return jsonify({
            "success": True,
            "message": "XGBoost model reloaded successfully",
            "model_last_modified": last_modified,
            "feature_count": len(features),
        })
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


def _traffic_level_from_payload(data):
    if "traffic_level" in data:
        return int(data["traffic_level"])

    delay_min = float(data.get("traffic_delay_sec", 0.0)) / 60.0
    if delay_min < 2.0:
        return 0
    if delay_min < 6.0:
        return 1
    if delay_min < 15.0:
        return 2
    return 3


def _default_time_slot():
    hour = datetime.datetime.now().hour
    if 7 <= hour < 10:
        return "Morning Rush"
    if 10 <= hour < 16:
        return "Midday"
    if 16 <= hour < 20:
        return "Evening Rush"
    if 20 <= hour < 23:
        return "Night"
    if hour >= 23 or hour < 5:
        return "Late Night"
    return "Morning"


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json() or {}
        weekday = datetime.datetime.now().weekday()

        predicted_fare = predict_fare(
            distance_km=float(data.get("distance_km", 10.0)),
            duration_min=float(data.get("duration_min", 20.0)),
            vehicle_type=str(data.get("vehicle_type", "UberX")),
            traffic_level=_traffic_level_from_payload(data),
            weather_condition=int(data.get("weather_condition", 0)),
            rainfall_intensity=int(data.get("rainfall_intensity", 0)),
            temperature_level=int(data.get("temperature_level", 2)),
            holiday=int(data.get("holiday", 0)),
            day_type=int(data.get("day_type", 1 if weekday >= 5 else 0)),
            number_of_stops=float(data.get("number_of_stops", 0)),
            road_type=data.get("road_type", "Highway"),
            pickup_area_type=data.get("pickup_area_type", "Commercial"),
            drop_area_type=data.get("drop_area_type", "Residential"),
            time_slot=data.get("time_slot") or _default_time_slot(),
            busy_day=data.get("busy_day", "Normal"),
        )

        return jsonify({
            "success": True,
            "predicted_fare": round(predicted_fare, 2),
            "currency": "INR",
            "model_used": "XGBoost Regressor",
            "r2_accuracy": "98.97%",
        })
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Uber Fare Prediction API on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
