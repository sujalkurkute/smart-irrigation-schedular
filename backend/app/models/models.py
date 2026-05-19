from sqlalchemy import Column, Integer, String, Float, Boolean
from app.config.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    farm_name = Column(String)
    soil_type = Column(String)
    crop_type = Column(String)

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    irrigate = Column(Boolean)
    water_liters = Column(Float)
    confidence = Column(Float)