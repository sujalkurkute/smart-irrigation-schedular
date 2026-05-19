from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

import time

for i in range(10):
    try:
        connection = engine.connect()
        print("Database connected successfully!")
        connection.close()
        break
    except Exception as e:
        print("Database not ready yet, retrying...")
        time.sleep(5)
        
# Session maker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base model
Base = declarative_base()