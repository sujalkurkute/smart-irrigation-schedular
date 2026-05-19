from fastapi import APIRouter
from app.schemas.prediction_schema import IrrigationInput
from app.services.prediction_service import predict_irrigation

router = APIRouter()

@router.post("/predict")
def predict(data: IrrigationInput):
    return predict_irrigation(data)