🌱 AI & Data-Driven Irrigation Scheduling System

An intelligent irrigation decision support platform that helps farmers make smart watering decisions using Artificial Intelligence, Real-Time Weather Data, and Machine Learning.

This system combines:

🌦️ Real-time weather forecasting
🤖 AI-powered irrigation prediction
📅 Smart irrigation scheduling
💧 Water requirement estimation
🌍 District-wise environmental modeling
🐳 Dockerized deployment
🌐 Farmer-friendly multilingual interface
🚀 Problem Statement

Traditional irrigation methods often rely on manual judgement, leading to:

Excessive water wastage
Poor irrigation scheduling
Reduced crop productivity
High dependency on expensive IoT systems

Most smart irrigation systems require:

costly sensors
IoT hardware
maintenance infrastructure

Small and medium-scale farmers often cannot afford these systems.

💡 Our Solution

This project provides a low-cost AI-powered irrigation recommendation system using:

Real-time weather APIs
NASA environmental datasets
Machine Learning models
Farmer-friendly inputs

without requiring expensive hardware or sensors.

✨ Key Features
🌦️ Real-Time Weather Integration

Fetches:

Temperature
Humidity
Rainfall
Wind Speed

using OpenWeather API.

🤖 AI Irrigation Advisor

Predicts:

Low irrigation need
Medium irrigation need
High irrigation need

using Random Forest ML model.

📅 AI Irrigation Schedule Planner

Predicts:

Whether irrigation is needed today
Best irrigation time
Next irrigation day
Water amount required

using advanced XGBoost models.

🌍 District-Wise Environmental Modeling

Uses:

NASA environmental datasets
Maharashtra district climate patterns

to generate realistic irrigation recommendations.

🌐 Multilingual Farmer-Friendly UI

Supports:

English
Marathi
Hindi

Designed specifically for farmer usability.

🐳 Dockerized Full-Stack Deployment

Includes:

FastAPI backend
PostgreSQL database
Docker containers
Swagger documentation
🏗️ System Architecture
Frontend (HTML/CSS/JS)
        ↓
FastAPI Backend
        ↓
Weather API + ML Models
        ↓
Feature Engineering
        ↓
Random Forest / XGBoost
        ↓
Schedule Generation
        ↓
Farmer Recommendations
        ↓
PostgreSQL Storage
🧠 Machine Learning Models
🔹 Model 1 — Irrigation Need Prediction
Algorithm
RandomForestClassifier
Purpose

Predict:

Low irrigation need
Medium irrigation need
High irrigation need
Features Used
Soil Type
Soil Moisture
Temperature
Humidity
Rainfall
Crop Type
Region
Soil pH
Wind Speed
Field Area
Accuracy
~88%–90%
🔹 Model 3 — AI Schedule Planner
Algorithm
XGBoost
Predicts
Irrigate today?
Recommended irrigation time
Next irrigation day
Water amount (mm)
Features Used
Temperature
Humidity
Rainfall
Wind Speed
Sunlight
Soil Moisture
Crop Type
Soil Condition
Final Results
Output	Performance
irrigate_today	93.84%
recommended_time	90.02%
next_irrigation_day	91.79%
water_amount_mm	RMSE: 1.69 mm
📊 Overfitting Reduction Techniques

The project initially faced overfitting due to deterministic patterns.

To improve generalization:

✅ Noise Injection
✅ Reduced Tree Depth
✅ Regularization
✅ Cross Validation
✅ Subsampling
✅ District-Wise Unseen Testing
🛰️ Dataset Information

The project uses:

NASA environmental datasets
Maharashtra district climate data
Agricultural heuristics
Weather-based environmental parameters

Features include:

temperature
humidity
rainfall
sunlight
wind speed
soil conditions
🛠️ Technologies Used
Technology	Purpose
HTML	Frontend structure
CSS	Styling/UI
JavaScript	Frontend logic
Python	Backend + ML
FastAPI	Backend framework
PostgreSQL	Database
Docker	Containerization
Scikit-learn	Random Forest
XGBoost	Advanced ML
Pandas	Data processing
NumPy	Numerical operations
Joblib	Model persistence
OpenWeather API	Weather data
Uvicorn	FastAPI server
📁 Project Structure
New_HAck/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │
│   ├── ml/
│   │   ├── train_model.py
│   │   ├── train_schedule_model.py
│   │   ├── *.pkl
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── frontend/
    └── index.html
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone <repository-url>
cd New_HAck
2️⃣ Start Docker

Make sure Docker Desktop is running.

3️⃣ Run Project
docker compose up --build
4️⃣ Open Backend Swagger Docs
http://127.0.0.1:8000/docs
5️⃣ Open Frontend

Open:

frontend/index.html
🌦️ API Endpoints
Weather API
GET /weather/{city}

Returns:

temperature
humidity
rainfall
wind speed
Generate Schedule
POST /generate-schedule

Returns:

irrigation recommendation
irrigation timing
next irrigation day
water amount
👨‍🌾 Farmer-Friendly Design

Farmers only need to provide:

Village/City
Crop Type
Soil Condition
Field Size

The system automatically:

fetches weather
estimates soil moisture
generates AI recommendations
🔍 AI vs Rule-Based Components
🤖 AI-Based
Irrigation prediction
Schedule prediction
Water amount estimation
Next irrigation prediction
📌 Rule-Based
Soil moisture estimation
Recommendation reasoning
Safety thresholds
Fallback irrigation logic
📈 Future Improvements
📡 IoT Sensor Integration
🛰️ Satellite Data Integration
🎙️ Voice Assistant
📱 Mobile Application
🧠 Explainable AI
🌐 Offline Weather Caching
🎯 Impact

This project aims to:

conserve water
support smart agriculture
improve irrigation efficiency
help small farmers
provide scalable AI-powered farming assistance
👨‍💻 Developed Using
Machine Learning
Full-Stack Development
Environmental Intelligence
Weather Analytics
Agricultural Decision Support Systems
🏁 Conclusion

This project is not just a machine learning model.

It is a complete:

AI-Powered Irrigation Decision Support Platform

designed to make intelligent irrigation:

affordable
scalable
accessible
practical for real farmers.