from fastapi import APIRouter
from app.schemas.schedule_schema import ScheduleInput
from app.services.schedule_service import generate_schedule

router = APIRouter()

@router.post("/generate-schedule")
def schedule(data: ScheduleInput):

    result = generate_schedule(data.dict())

    return result