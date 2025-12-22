import tkinter as tk
import requests
# from tkinter import combobox
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("api_key")
city_name = "karachi"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q="+city_name+"&appid="+API_KEY

def get_weather():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = main['temp']
        humidity = main['humidity']
        weather_desc = data['weather'][0]['description']
        weather_info = f"Temperature: {temperature}\nHumidity: {humidity}\nDescription: {weather_desc}"
        print(weather_info) 
    else:
        weather_info = "City Not Found"
        print(weather_info)



get_weather()
