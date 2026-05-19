from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.weather_routes import router as weather_router
from app.routes.prediction_routes import router as prediction_router
from app.routes.schedule_routes import router as schedule_router

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
app.include_router(weather_router)
app.include_router(prediction_router)
app.include_router(schedule_router)

@app.get("/")
def home():
    return {"message": "GrowSmart AI Backend Running"}