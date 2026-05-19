import joblib
import pandas as pd

# Load trained model
model = joblib.load("ml/irrigation_model.pkl")

# Load label encoder
label_encoder = joblib.load("ml/label_encoders.pkl")


def predict_irrigation(data):
    # Convert input data into dataframe
    input_data = pd.DataFrame([{
        "Soil_pH": data.soil_ph,
        "Soil_Moisture": data.soil_moisture,
        "Temperature_C": data.temperature,
        "Humidity": data.humidity,
        "Rainfall_mm": data.rainfall,
        "Sunlight_Hours": data.sunlight_hours,
        "Wind_Speed_kmh": data.wind_speed,
        "Field_Area_hectare": data.field_area,
        "Previous_Irrigation_mm": data.previous_irrigation
    }])

    # Predict
    prediction = model.predict(input_data)

    # Decode label
    result = label_encoder.inverse_transform(prediction)

    return {
        "prediction": result[0]
    }