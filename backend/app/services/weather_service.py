import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = "60358d6892b953d1c87e7ba200338699"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str):

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    return response.json()