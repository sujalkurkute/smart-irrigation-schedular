import joblib
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

ML_DIR = os.path.join(BASE_DIR, "ml")

# ── Load all 4 trained models ──
model_irrigate = joblib.load(os.path.join(ML_DIR, "schedule_irrigate_today_model.pkl"))
model_time     = joblib.load(os.path.join(ML_DIR, "schedule_recommended_time_model.pkl"))
model_next     = joblib.load(os.path.join(ML_DIR, "schedule_next_irrigation_day_model.pkl"))
model_water    = joblib.load(os.path.join(ML_DIR, "schedule_water_amount_mm_model.pkl"))

# ── Load label encoders ──
encoders = joblib.load(os.path.join(ML_DIR, "schedule_label_encoders.pkl"))

def soil_to_moisture(soil_condition: str) -> float:
    return {"dry": 18.0, "normal": 45.0, "wet": 72.0}.get(soil_condition, 35.0)

def generate_schedule(data: dict) -> dict:
    temperature    = float(data["temperature"])
    humidity       = float(data["humidity"])
    rainfall       = float(data["rainfall_forecast"])
    soil_moisture  = float(data["soil_moisture"])
    crop           = str(data["crop_type"])
    soil_condition = str(data.get("soil_condition", "normal"))

    # ── Encode crop ──
    try:
        crop_enc = int(encoders["crop"].transform([crop])[0])
    except Exception:
        # Unknown crop → use most common
        crop_enc = 0

    # ── Encode soil condition ──
    try:
        soil_enc = int(encoders["soil_condition"].transform([soil_condition])[0])
    except Exception:
        soil_enc = 1

    # ── Build feature row (must match training FEATURES order) ──
    features = pd.DataFrame([{
        "temperature":        temperature,
        "humidity":           humidity,
        "rainfall":           rainfall,
        "wind_speed":         10.0,
        "sunlight":           7.0,
        "soil_moisture":      soil_moisture,
        "crop_enc":           crop_enc,
        "soil_condition_enc": soil_enc
    }])

    # ── Run all 4 predictions ──
    irrigate_today_pred = int(model_irrigate.predict(features)[0])
    time_enc_pred       = int(model_time.predict(features)[0])
    next_enc_pred       = int(model_next.predict(features)[0])
    water_pred          = float(model_water.predict(features)[0])

    # ── Decode labels ──
    recommended_time    = str(encoders["time"].inverse_transform([time_enc_pred])[0])
    next_irrigation_day = str(encoders["next_day"].inverse_transform([next_enc_pred])[0])
    water_amount        = round(max(0.0, water_pred), 1)

    # ── Human-readable reason ──
    if rainfall > 30:
        reason = "Heavy rainfall expected — no irrigation needed today"
    elif soil_moisture < 30:
        reason = "Low soil moisture detected — irrigation is recommended"
    else:
        reason = "Moderate soil moisture — monitor and irrigate if needed"

    return {
        "today_irrigation":    bool(irrigate_today_pred),
        "recommended_time":    recommended_time,
        "water_amount_mm":     water_amount,
        "next_irrigation_day": next_irrigation_day,
        "reason":              reason,
        "model":               "ML"   # ← tells frontend this is ML-powered
    }