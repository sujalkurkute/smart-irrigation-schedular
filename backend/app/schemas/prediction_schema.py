from pydantic import BaseModel

class IrrigationInput(BaseModel):
    soil_ph: float
    soil_moisture: float
    temperature: float
    humidity: float
    rainfall: float
    sunlight_hours: float
    wind_speed: float
    field_area: float
    previous_irrigation: float