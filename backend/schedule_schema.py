from pydantic import BaseModel

class ScheduleInput(BaseModel):

    temperature: float
    humidity: float
    rainfall_forecast: float
    soil_moisture: float
    crop_type: str