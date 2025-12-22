import tkinter as tk
import requests
# from tkinter import combobox
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")  # use uppercase (best practice)
CITY_NAME = "Karachi"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather():
    params = {
        "q": CITY_NAME,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather_desc = data["weather"][0]["description"]

        weather_info = (
            f"City: {CITY_NAME}\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%\n"
            f"Description: {weather_desc.capitalize()}"
        )

        print(weather_info)

    else:
        print("City not found or API error")


win = tk.Tk()
win.geometry("500x780")
win.title("Weather App | Code by Imran")
win.configure(bg="#87ceeb")
main_title = tk.Label(win, text="Weather App", font=("Arial", 24, "bold"), bg="#87ceeb")
main_title.pack(pady=20)




win.mainloop()






















