"""Load the trained XGBoost model and predict Uber fares."""

import os

import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "feature_columns.pkl")

_model = None
_feature_columns = None

VEHICLE_MAP = {
    "UberX": "Vehicle Type_Sedan",
    "Sedan": "Vehicle Type_Sedan",
    "UberXL": "Vehicle Type_XL",
    "XL": "Vehicle Type_XL",
    "Black": "Vehicle Type_Black",
    "Uber Black": "Vehicle Type_Black",
    "Pool": "Vehicle Type_Pool",
    "Uber Pool": "Vehicle Type_Pool",
    "Comfort": "Vehicle Type_Comfort",
    "Go": "Vehicle Type_Go",
    "Mini": "Vehicle Type_Mini",
    "Premium": "Vehicle Type_Premium",
    "SUV": "Vehicle Type_SUV",
    "Bike": "Vehicle Type_Bike",
    "Green": "Vehicle Type_Comfort",
    "Auto": None,
    "Auto Rickshaw": None,
    "Rickshaw": None,
}

MIN_FARE = 30.0


def load_xgboost_model():
    """Lazy-load model and feature column list from disk."""
    global _model, _feature_columns
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"XGBoost model not found: {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
    if _feature_columns is None:
        if not os.path.exists(FEATURES_PATH):
            raise FileNotFoundError(f"Feature columns not found: {FEATURES_PATH}")
        _feature_columns = joblib.load(FEATURES_PATH)
    return _model, _feature_columns


def reload_xgboost_model():
    """Force-reload model artifacts (call after retraining)."""
    global _model, _feature_columns
    _model = None
    _feature_columns = None
    return load_xgboost_model()


def prepare_features(
    distance_km,
    duration_min,
    vehicle_type="UberX",
    traffic_level=1,
    weather_condition=0,
    rainfall_intensity=0,
    temperature_level=2,
    holiday=0,
    day_type=0,
    number_of_stops=0,
    road_type="Highway",
    pickup_area_type="Commercial",
    drop_area_type="Residential",
    time_slot="Evening Rush",
    busy_day="Normal",
):
    """Build a single-row DataFrame matching the trained feature schema."""
    _, feature_columns = load_xgboost_model()
    row = {col: 0 for col in feature_columns}

    row["Distance (km)"] = float(distance_km)
    row["Estimated Duration (min)"] = float(duration_min)
    row["Weather Condition"] = int(weather_condition)
    row["Rainfall Intensity"] = int(rainfall_intensity)
    row["Traffic Level"] = int(traffic_level)
    row["Temperature Level"] = int(temperature_level)
    row["Holiday"] = int(holiday)
    row["Day Type"] = int(day_type)
    row["Number of Stops Added"] = float(number_of_stops)

    veh_col = VEHICLE_MAP.get(vehicle_type, "Vehicle Type_Sedan")
    if veh_col and veh_col in row:
        row[veh_col] = 1

    for prefix, value in (
        ("Road Type_", road_type),
        ("Pickup Area Type_", pickup_area_type),
        ("Drop Area Type_", drop_area_type),
        ("Time Slot_", time_slot),
        ("Busy Day_", busy_day),
    ):
        col = f"{prefix}{value}"
        if col in row:
            row[col] = 1

    return pd.DataFrame([row], columns=feature_columns)


def predict_fare(
    distance_km,
    duration_min,
    vehicle_type="UberX",
    traffic_level=1,
    weather_condition=0,
    rainfall_intensity=0,
    temperature_level=2,
    holiday=0,
    day_type=0,
    number_of_stops=0,
    road_type="Highway",
    pickup_area_type="Commercial",
    drop_area_type="Residential",
    time_slot="Evening Rush",
    busy_day="Normal",
):
    """Predict ride fare (INR) using the trained XGBoost model."""
    model, _ = load_xgboost_model()
    features = prepare_features(
        distance_km=distance_km,
        duration_min=duration_min,
        vehicle_type=vehicle_type,
        traffic_level=traffic_level,
        weather_condition=weather_condition,
        rainfall_intensity=rainfall_intensity,
        temperature_level=temperature_level,
        holiday=holiday,
        day_type=day_type,
        number_of_stops=number_of_stops,
        road_type=road_type,
        pickup_area_type=pickup_area_type,
        drop_area_type=drop_area_type,
        time_slot=time_slot,
        busy_day=busy_day,
    )
    return max(MIN_FARE, float(model.predict(features)[0]))


if __name__ == "__main__":
    fare = predict_fare(distance_km=15.0, duration_min=25.0, vehicle_type="UberX")
    print(f"Predicted fare (15 km / 25 min, UberX): ₹{fare:.2f}")
