import pandas as pd
import numpy as np
import random

# Load NASA weather data
df = pd.read_csv("maharashtra_weather.csv")

CROPS = [
    "Wheat", "Rice", "Maize", "Cotton", "Sugarcane",
    "Soybean", "Onion", "Tomato", "Sunflower", "Groundnut"
]

SOIL_CONDITIONS = ["dry", "normal", "wet"]

SOIL_MOISTURE_MAP = {
    "dry":    (10, 25),   # 10–25%
    "normal": (35, 55),   # 35–55%
    "wet":    (60, 80),   # 60–80%
}

# Rule engine (same logic as your current schedule_service.py)
def rule_engine(temperature, humidity, rainfall, soil_moisture, crop):
    if rainfall > 30:
        return {
            "irrigate_today":      0,
            "recommended_time":    "Not Needed",
            "water_amount_mm":     0,
            "next_irrigation_day": "After Rainfall",
            "reason":              "Heavy rainfall expected"
        }
    elif soil_moisture < 30:
        if temperature > 35:
            time = "5:30 AM"
            water = 15
        else:
            time = "6:30 AM"
            water = 10
        return {
            "irrigate_today":      1,
            "recommended_time":    time,
            "water_amount_mm":     water,
            "next_irrigation_day": "Tomorrow",
            "reason":              "Low soil moisture detected"
        }
    else:
        return {
            "irrigate_today":      0,
            "recommended_time":    "Monitor Soil",
            "water_amount_mm":     5,
            "next_irrigation_day": "2 Days Later",
            "reason":              "Moderate soil moisture"
        }

print("⏳ Generating training dataset...")

rows = []
for _, weather_row in df.iterrows():
    for crop in CROPS:
        for soil_condition in SOIL_CONDITIONS:
            # Random soil moisture within range for this condition
            moisture_min, moisture_max = SOIL_MOISTURE_MAP[soil_condition]
            soil_moisture = round(random.uniform(moisture_min, moisture_max), 1)

            # Get rule engine labels
            label = rule_engine(
                temperature  = weather_row["temperature"],
                humidity     = weather_row["humidity"],
                rainfall     = weather_row["rainfall"],
                soil_moisture= soil_moisture,
                crop         = crop
            )

            # In generate_dataset.py, replace the rows.append() section with this:

import numpy as np

for _, weather_row in df.iterrows():
    for crop in CROPS:
        for soil_condition in SOIL_CONDITIONS:
            moisture_min, moisture_max = SOIL_MOISTURE_MAP[soil_condition]
            soil_moisture = round(random.uniform(moisture_min, moisture_max), 1)

            # ── ADD REAL-WORLD NOISE ──
            temp_noisy     = weather_row["temperature"] + np.random.normal(0, 1.5)
            humidity_noisy = weather_row["humidity"]    + np.random.normal(0, 3.0)
            rainfall_noisy = max(0, weather_row["rainfall"] + np.random.normal(0, 2.0))
            moisture_noisy = max(0, min(100, soil_moisture  + np.random.normal(0, 4.0)))

            # ── BORDERLINE CASES (most important) ──
            # Cases near the decision boundary confuse the model
            # soil_moisture near 30 = uncertain
            # rainfall near 30 = uncertain
            if random.random() < 0.15:  # 15% borderline cases
                moisture_noisy = random.uniform(25, 35)  # near boundary of 30
            if random.random() < 0.10:  # 10% borderline rainfall
                rainfall_noisy = random.uniform(25, 35)  # near boundary of 30
            if random.random() < 0.10:  # 10% borderline temperature
                temp_noisy = random.uniform(33, 37)      # near boundary of 35

            label = rule_engine(
                temperature   = temp_noisy,
                humidity      = humidity_noisy,
                rainfall      = rainfall_noisy,
                soil_moisture = moisture_noisy,
                crop          = crop
            )

            rows.append({
                "district":       weather_row["district"],
                "temperature":    round(temp_noisy, 1),
                "humidity":       round(humidity_noisy, 1),
                "rainfall":       round(rainfall_noisy, 2),
                "wind_speed":     weather_row["wind_speed"],
                "sunlight":       weather_row["sunlight"],
                "soil_condition": soil_condition,
                "soil_moisture":  round(moisture_noisy, 1),
                "crop":           crop,
                "irrigate_today":       label["irrigate_today"],
                "recommended_time":     label["recommended_time"],
                "water_amount_mm":      label["water_amount_mm"],
                "next_irrigation_day":  label["next_irrigation_day"],
            })

dataset = pd.DataFrame(rows)
dataset.to_csv("schedule_training_data.csv", index=False)

print(f"✅ Dataset generated!")
print(f"📊 Total rows     : {len(dataset)}")
print(f"🌾 Crops          : {dataset['crop'].nunique()}")
print(f"🗺️  Districts      : {dataset['district'].nunique()}")
print(f"💧 Irrigate today : {dataset['irrigate_today'].value_counts().to_dict()}")
print(dataset.head(5))