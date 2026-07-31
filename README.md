# 🚖 UberFare AI — Ride Fare Prediction

<div align="center">

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://fareprediction-tlzr.onrender.com)
[![App Status](https://img.shields.io/website?url=https%3A%2F%2Ffareprediction-tlzr.onrender.com&style=for-the-badge&label=App%20Status)](https://fareprediction-tlzr.onrender.com)

### 🌐 Live Demo
**https://fareprediction-tlzr.onrender.com**

*The live application is built with **Flask** and hosted on **Render's Free Tier**. The first request may take **30–60 seconds** if the service is waking up.*

</div>

---

# 📌 Overview

UberFare AI is a machine learning project that predicts **Uber-style ride fares** using an **XGBoost Regressor**. The prediction considers multiple ride-related factors including:

- 📍 Distance
- ⏱ Trip Duration
- 🚗 Vehicle Type
- 🚦 Traffic Conditions
- 🌦 Weather
- 🏙 Pickup & Drop Area Type
- 🕒 Time Slot
- 📅 Holidays
- 🛑 Number of Stops

The project includes:

- 📊 Exploratory Data Analysis (EDA)
- 🤖 Multiple Regression Model Comparison
- 🏆 Production-ready XGBoost Model
- 🌐 Flask Web Application
- 🎨 Glassmorphism UI
- 📈 Streamlit App (Local Use)

---

# 📊 Model Performance

## ✅ Production Model (XGBoost)

| Metric | Score |
|---------|-------|
| **R² Score** | **0.9897** |
| **MAE** | **₹128.20** |
| **RMSE** | **₹171.11** |

---

# 🤖 Models Compared

| Model | Test R² | MAE (₹) | RMSE (₹) | Status |
|------|------:|------:|------:|------|
| ✅ XGBoost | **0.9897** | **128.20** | **171.11** | Production |
| Ridge Regression | 0.9092 | 349.50 | 506.97 | Comparison |
| Linear Regression | 0.9092 | 349.80 | 506.98 | Comparison |
| Multiple Regression (OLS) | 0.9092 | 349.80 | 506.98 | Comparison |
| Lasso Regression | 0.9083 | 349.79 | 509.62 | Comparison |

---

# ⭐ Why XGBoost?

XGBoost was selected because it:

- Achieved the highest prediction accuracy
- Produced the lowest prediction error
- Captures complex nonlinear relationships
- Avoids negative fare predictions
- Delivered stable 5-fold Cross Validation performance
- Significantly outperformed linear models

---

# 📂 Project Structure

```text
fare_prediction/
│
├── data/
│   ├── input_dataset.csv
│   └── processed_data.csv
│
├── notebooks/
│   ├── 01_data_analysis.ipynb
│   └── 02_model_training.ipynb
│
├── models/
│   ├── xgboost_model.pkl
│   └── feature_columns.pkl
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
│
├── src/
│   ├── app.py
│   ├── predict.py
│   └── evaluate.py
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

# ⚙ Project Workflow

```text
Processed Dataset
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Train Multiple Models
        │
        ▼
Compare Performance
        │
        ▼
Save XGBoost Model
        │
        ▼
Prediction API
        │
 ┌──────┼───────────┐
 ▼      ▼           ▼
Flask  Streamlit  Evaluation
```

---

# 🛠 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/fare_prediction.git

cd fare_prediction
```

Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt

pip install flask flask-cors streamlit
```

---

# 📦 Required Model Files

Make sure these files exist:

```text
models/
├── xgboost_model.pkl
└── feature_columns.pkl
```

If they do not exist:

Open

```
notebooks/02_model_training.ipynb
```

Run every cell to generate the trained model.

---

# 🚀 Run Flask Application

```bash
python src/app.py
```

Open

```
http://127.0.0.1:5000
```

---

# 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web Interface |
| `/api/predict` | POST | Predict Fare |
| `/api/health` | GET | Model Health |
| `/api/reload` | POST | Reload Saved Model |

---

# 📥 Sample Prediction Request

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

# 🌍 Deploy on Render

The application is deployed using **Render**.

### Live URL

https://fareprediction-tlzr.onrender.com

### Deployment Steps

1. Push project to GitHub
2. Login to Render
3. Create New Web Service
4. Connect GitHub Repository

Build Command

```bash
pip install -r requirements.txt
```

Start Command

```bash
python src/app.py
```

For production you can also use

```bash
gunicorn src.app:app
```

---

# 💻 Streamlit (Optional)

Run locally

```bash
streamlit run streamlit_app.py
```

Open

```
http://localhost:8501
```

---

# ⚙ Optional Streamlit Configuration

Create

```
.streamlit/config.toml
```

```toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

---

# 📈 Evaluate Model

```bash
python src/evaluate.py
```

---

# 🔄 Retraining Workflow

1. Run

```
02_model_training.ipynb
```

2. Save

```
models/xgboost_model.pkl
models/feature_columns.pkl
```

3. Reload Flask model

```
POST /api/reload
```

or restart the application.

---

# 🛠 Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Flask
- Streamlit
- HTML
- CSS
- JavaScript
- Bootstrap
- Render

---

# 📷 Screenshots

Add screenshots here.

```
screenshots/
├── homepage.png
├── prediction.png
├── result.png
```

---

# 📄 License

This project is developed for educational and portfolio purposes.

The fare values shown are treated as **Indian Rupees (₹)**.

---

# 👨‍💻 Author

**Nilesh Jadhav**

- LinkedIn: https://linkedin.com/in/your-link
- GitHub: https://github.com/yourusername

---

<div align="center">

### ⭐ If you like this project, don't forget to Star the repository!

</div>