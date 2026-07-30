"""
Uber Fare Prediction — Streamlit UI

Run:
    streamlit run streamlit_app.py
"""

import streamlit as st

from src.predict import predict_fare, load_xgboost_model

st.set_page_config(
    page_title="UberFare AI",
    page_icon="🚗",
    layout="centered",
)

st.title("UberFare AI")
st.caption("XGBoost fare predictor · R² ≈ 98.97%")

try:
    load_xgboost_model()
except Exception as exc:
    st.error(f"Could not load model: {exc}")
    st.stop()

with st.form("fare_form"):
    st.subheader("Trip details")

    c1, c2 = st.columns(2)
    with c1:
        distance_km = st.number_input("Distance (km)", min_value=0.1, value=15.0, step=0.5)
        vehicle_type = st.selectbox(
            "Vehicle type",
            ["UberX", "UberXL", "Black", "Comfort", "Go", "Mini", "Pool", "Premium", "SUV", "Bike", "Auto"],
        )
        traffic_level = st.selectbox(
            "Traffic level",
            options=[0, 1, 2, 3],
            index=1,
            format_func=lambda x: {0: "0 – Low", 1: "1 – Medium", 2: "2 – High", 3: "3 – Jam"}[x],
        )
        road_type = st.selectbox("Road type", ["City Road", "Highway", "Expressway", "Rural Road"])
        pickup_area = st.selectbox(
            "Pickup area",
            ["Residential", "Commercial", "IT Park", "Metro Station", "Railway Station",
             "Bus Stand", "Hospital", "College", "Mall", "Airport"],
        )
        weather_condition = st.selectbox(
            "Weather",
            options=[0, 1, 2, 3],
            index=0,
            format_func=lambda x: {0: "Clear", 1: "Cloudy", 2: "Rain", 3: "Storm"}[x],
        )
        rainfall = st.selectbox(
            "Rainfall",
            options=[0, 1, 2],
            index=0,
            format_func=lambda x: {0: "None", 1: "Light", 2: "Heavy"}[x],
        )
        holiday = st.selectbox("Holiday", options=[0, 1], format_func=lambda x: "Yes" if x else "No")

    with c2:
        duration_min = st.number_input("Duration (min)", min_value=1.0, value=25.0, step=1.0)
        stops = st.number_input("Stops added", min_value=0, max_value=5, value=0, step=1)
        drop_area = st.selectbox(
            "Drop-off area",
            ["Commercial", "Residential", "IT Park", "Metro Station", "Railway Station",
             "Bus Stand", "Hospital", "College", "Mall", "Airport"],
        )
        time_slot = st.selectbox(
            "Time slot",
            ["Morning Rush", "Evening Rush", "Evening", "Midday", "Morning", "Night", "Late Night"],
        )
        day_type = st.selectbox(
            "Day type",
            options=[0, 1],
            format_func=lambda x: "Weekend" if x else "Weekday",
        )
        temp_level = st.selectbox(
            "Temperature",
            options=[0, 1, 2, 3, 4],
            index=2,
            format_func=lambda x: {0: "Cold", 1: "Cool", 2: "Moderate", 3: "Warm", 4: "Hot"}[x],
        )
        busy_day = st.selectbox("Busy day", ["Normal", "Major Event", "Public Holiday", "Festival"])

    submitted = st.form_submit_button("Predict fare", use_container_width=True)

if submitted:
    try:
        fare = predict_fare(
            distance_km=distance_km,
            duration_min=duration_min,
            vehicle_type=vehicle_type,
            traffic_level=traffic_level,
            weather_condition=weather_condition,
            rainfall_intensity=rainfall,
            temperature_level=temp_level,
            holiday=holiday,
            day_type=day_type,
            number_of_stops=stops,
            road_type=road_type,
            pickup_area_type=pickup_area,
            drop_area_type=drop_area,
            time_slot=time_slot,
            busy_day=busy_day,
        )
        st.success(f"Predicted fare: ₹ {fare:,.2f}")
        st.caption(f"Expected range ≈ ₹ {fare * 0.90:,.0f} – ₹ {fare * 1.15:,.0f}")
    except Exception as exc:
        st.error(str(exc))
