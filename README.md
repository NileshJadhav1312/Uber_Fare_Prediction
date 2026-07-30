# UberFare AI — Ride Fare Prediction

Predict Uber-style trip fares with a trained **XGBoost** regressor. The project includes data analysis notebooks, model comparison, a Flask + glassmorphic web UI, and an optional Streamlit app.

---

## About the project

Urban ride fares depend on many interacting factors: distance, duration, vehicle category, traffic, weather, pickup/drop area types, time of day, and special events. This project:

1. Cleans and explores a processed ride dataset (`data/processed_data.csv`)
2. Trains and compares several regression models on the same train/test split
3. Selects **XGBoost** as the only production model
4. Serves predictions through a web UI (Flask) or Streamlit

**Held-out test metrics (XGBoost):** R² ≈ **0.9897** · MAE ≈ **₹128** · RMSE ≈ **₹171**

---

## Models tested

| Model | Test R² | MAE (₹) | RMSE (₹) | Notes |
|-------|---------|---------|----------|--------|
| **XGBoost** (selected) | **0.9897** | **128.20** | **171.11** | Production model |
| Ridge Regression | 0.9092 | 349.50 | 506.97 | Comparison only |
| Linear Regression | 0.9092 | 349.80 | 506.98 | Comparison only |
| Multiple Regression (OLS) | 0.9092 | 349.80 | 506.98 | Same fit as Linear |
| Lasso Regression | 0.9083 | 349.79 | 509.62 | Comparison only |

Training and comparison live in `notebooks/02_model_training.ipynb`.  
**Only XGBoost is saved** (`models/xgboost_model.pkl` + `models/feature_columns.pkl`).

### Why XGBoost was selected

- Highest accuracy and lowest error by a wide margin (~9 R² points over linear models)
- Captures non-linear interactions among the 49 encoded features
- Produces valid positive fares on sample trips (linear models can predict negative Bike fares)
- Stable 5-fold cross-validation R²

---

## Project structure

```
fare_prediction/
├── data/
│   ├── input_dataset.csv          # Raw / source data
│   └── processed_data.csv         # Model-ready features + Fare (Target)
├── notebooks/
│   ├── 01_data_analysis.ipynb     # EDA
│   └── 02_model_training.ipynb    # Train, compare, save XGBoost only
├── models/
│   ├── xgboost_model.pkl          # Production model
│   └── feature_columns.pkl        # Feature schema (49 columns)
├── frontend/                      # Glassmorphic UI (served by Flask)
│   ├── index.html
│   ├── app.js
│   └── style.css
├── src/
│   ├── app.py                     # Flask API + static frontend
│   ├── predict.py                 # Load model + predict_fare()
│   └── evaluate.py                # Score model on full CSV
├── streamlit_app.py               # Optional Streamlit UI
├── requirements.txt
└── README.md
```

---

## Execution flow

```
data/processed_data.csv
        │
        ▼
notebooks/01_data_analysis.ipynb     → explore & validate data
        │
        ▼
notebooks/02_model_training.ipynb    → train Linear / Ridge / Lasso / OLS / XGBoost
        │                              → compare metrics
        │                              → save ONLY to models/xgboost_model.pkl + feature_columns.pkl
        ▼
src/predict.py                       → load XGBoost, build feature row, predict
        │
        ├──► src/app.py + frontend/  → Flask web app (default)
        ├──► streamlit_app.py        → Streamlit UI
        └──► src/evaluate.py         → offline metrics on full dataset
```

---

## Setup

```bash
# From project root
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
pip install flask flask-cors streamlit
```

> `flask`, `flask-cors`, and `streamlit` are required for the apps; install them if they are not already in your environment.

Ensure the trained artifacts exist:

- `models/xgboost_model.pkl`
- `models/feature_columns.pkl`

If missing, open `notebooks/02_model_training.ipynb`, run all cells (including **§14 Save Production Model**).

---

## Run — Flask + frontend (main app)

```bash
python src/app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Web UI |
| `/api/predict` | POST | JSON fare prediction |
| `/api/health` | GET | Health + model metrics |
| `/api/reload` | POST | Reload model after retrain |

Example predict body:

```json
{
  "distance_km": 15,
  "duration_min": 25,
  "vehicle_type": "UberX",
  "traffic_level": 1,
  "road_type": "City Road",
  "pickup_area_type": "Residential",
  "drop_area_type": "Commercial",
  "time_slot": "Morning Rush",
  "weather_condition": 0,
  "rainfall_intensity": 0,
  "temperature_level": 2,
  "busy_day": "Normal",
  "day_type": 0,
  "holiday": 0,
  "number_of_stops": 0
}
```

---

## Deploy / run on Streamlit

### Local

```bash
streamlit run streamlit_app.py
```

Browser opens at [http://localhost:8501](http://localhost:8501).

### Streamlit Community Cloud

1. Push this repo to GitHub (include `models/*.pkl` or train in CI).
2. Go to [https://share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select the repo, branch, and set **Main file path** to `streamlit_app.py`.
4. Add Python packages in Cloud settings / `requirements.txt` (include `streamlit`, `xgboost`, `scikit-learn`, `pandas`, `joblib`, `numpy`).
5. Deploy. The app imports `src.predict`, which loads `models/xgboost_model.pkl`.

### Optional Streamlit config

Create `.streamlit/config.toml` if you want a fixed port/theme:

```toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

---

## Evaluate the saved model

```bash
python src/evaluate.py
```

---

## Retrain workflow

1. Run `notebooks/02_model_training.ipynb` end-to-end.
2. Confirm §14 saved files under project-root `models/` (`xgboost_model.pkl` + `feature_columns.pkl` only).
3. Flask: click **Reload Model** in the UI, or `POST /api/reload`.
4. Streamlit: restart the app (or rerun) to pick up the new file.

---

## License / notes

Educational ML project. Model metrics are from the notebook’s 80/20 train-test split (`random_state=42`). Currency in the UI is treated as INR (₹).
