import tkinter as tk
from tkinter import ttk
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# =========================
# Weather Function
# =========================
def get_weather():
    city = city_var.get()

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        city_name_label.config(text=city.title())
        description.config(text=desc.capitalize())
        temperature.config(text=f"{temp}°C")
        extra_info.config(text=f"Humidity: {humidity}%\nWind: {wind} km/h")

    else:
        description.config(text="City not found")
        temperature.config(text="--")
        extra_info.config(text="")

# =========================
# Main Window
# =========================
win = tk.Tk()
win.geometry("500x780")
win.title("Weather App | Code by Imran")
win.configure(bg="#0f172a")

# =========================
# Header
# =========================
header_frame = tk.Frame(win, bg="#0f172a")
header_frame.pack(pady=30)

tk.Label(
    header_frame,
    text="Weather App",
    font=("Segoe UI", 28, "bold"),
    fg="#38bdf8",
    bg="#0f172a"
).pack()

tk.Label(
    header_frame,
    text="Live Weather Updates",
    font=("Segoe UI", 12),
    fg="#94a3b8",
    bg="#0f172a"
).pack(pady=5)

# =========================
# Search Card with Dropdown
# =========================
search_card = tk.Frame(win, bg="#1e293b")
search_card.pack(pady=25, padx=30, fill="x")

tk.Label(
    search_card,
    text="Select City",
    font=("Segoe UI", 12),
    fg="#e2e8f0",
    bg="#1e293b"
).pack(anchor="w", padx=20, pady=(20, 5))

# City dropdown
cities = ["Karachi", "Lahore", "Islamabad", "Delhi", "London", "New York"]
city_var = tk.StringVar(value="Karachi")

city_dropdown = ttk.Combobox(
    search_card,
    textvariable=city_var,
    values=cities,
    state="readonly",
    font=("Segoe UI", 13)
)
city_dropdown.pack(padx=20, pady=10, fill="x", ipady=6)

# Search Button
tk.Button(
    search_card,
    text="Get Weather",
    font=("Segoe UI", 14, "bold"),
    bg="#38bdf8",
    fg="#0f172a",
    bd=0,
    activebackground="#0ea5e9",
    cursor="hand2",
    command=get_weather
).pack(pady=20, padx=20, fill="x", ipady=10)

# =========================
# Weather Card
# =========================
weather_card = tk.Frame(win, bg="#1e293b")
weather_card.pack(pady=20, padx=30, fill="both", expand=True)

city_name_label = tk.Label(
    weather_card,
    text="Karachi",
    font=("Segoe UI", 22, "bold"),
    fg="#38bdf8",
    bg="#1e293b"
)
city_name_label.pack(pady=(25, 5))

description = tk.Label(
    weather_card,
    text="Clear Sky",
    font=("Segoe UI", 14),
    fg="#e2e8f0",
    bg="#1e293b"
)
description.pack(pady=5)

temperature = tk.Label(
    weather_card,
    text="32°C",
    font=("Segoe UI", 46, "bold"),
    fg="#ffffff",
    bg="#1e293b"
)
temperature.pack(pady=20)

extra_info = tk.Label(
    weather_card,
    text="Humidity: 68%\nWind: 5 km/h",
    font=("Segoe UI", 12),
    fg="#94a3b8",
    bg="#1e293b",
    justify="center"
)
extra_info.pack(pady=10)

# =========================
# Footer
# =========================
tk.Label(
    win,
    text="Code by Imran • OpenWeather API",
    font=("Segoe UI", 10),
    fg="#64748b",
    bg="#0f172a"
).pack(pady=15)

# =========================
# Auto-load default city on startup
# =========================
get_weather()

win.mainloop()
