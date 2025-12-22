import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # For weather icons
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

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"]
            wind = data["wind"]["speed"]
            weather_main = data["weather"][0]["main"]

            city_name_label.config(text=city.title())
            description.config(text=desc.capitalize())
            temperature.config(text=f"{temp}°C")
            extra_info.config(text=f"Humidity: {humidity}%\nWind: {wind} km/h")

            # Set dynamic weather icon
            if weather_main.lower() in ["clear"]:
                icon_label.config(image=sun_icon)
                weather_card.configure(bg="#facc15")  # sunny yellow background
            elif weather_main.lower() in ["clouds"]:
                icon_label.config(image=cloud_icon)
                weather_card.configure(bg="#64748b")  # grayish clouds
            elif weather_main.lower() in ["rain", "drizzle"]:
                icon_label.config(image=rain_icon)
                weather_card.configure(bg="#0ea5e9")  # blue rain
            elif weather_main.lower() in ["snow"]:
                icon_label.config(image=snow_icon)
                weather_card.configure(bg="#e0f2fe")  # light blue snow
            else:
                icon_label.config(image=default_icon)
                weather_card.configure(bg="#1e293b")

        else:
            description.config(text="City not found")
            temperature.config(text="--")
            extra_info.config(text="")
            icon_label.config(image=default_icon)
            weather_card.configure(bg="#1e293b")

    except Exception as e:
        description.config(text="Error fetching data")
        temperature.config(text="--")
        extra_info.config(text="")
        icon_label.config(image=default_icon)
        weather_card.configure(bg="#1e293b")

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
header_frame.pack(pady=20)

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
# Search Card
# =========================
search_card = tk.Frame(win, bg="#1e293b")
search_card.pack(pady=20, padx=30, fill="x")

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

# Weather Icon
# Load small icons from local or online
# Make sure to have PNGs in same folder: sun.png, cloud.png, rain.png, snow.png, default.png
sun_icon = ImageTk.PhotoImage(Image.open("sun.png").resize((100,100)))
cloud_icon = ImageTk.PhotoImage(Image.open("cloud.png").resize((100,100)))
rain_icon = ImageTk.PhotoImage(Image.open("rain.png").resize((100,100)))
snow_icon = ImageTk.PhotoImage(Image.open("snow.png").resize((100,100)))
default_icon = ImageTk.PhotoImage(Image.open("default.png").resize((100,100)))

icon_label = tk.Label(weather_card, bg="#1e293b")
icon_label.pack(pady=15)
icon_label.config(image=sun_icon)  # default icon

city_name_label = tk.Label(
    weather_card,
    text="Karachi",
    font=("Segoe UI", 22, "bold"),
    fg="#38bdf8",
    bg="#1e293b"
)
city_name_label.pack(pady=(5, 5))

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
temperature.pack(pady=10)

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
footer = tk.Label(
    win,
    text="Code by Imran • OpenWeather API",
    font=("Segoe UI", 10, "italic"),
    fg="#64748b",
    bg="#0f172a"
)
footer.pack(side="bottom", pady=10)

# =========================
# Auto-load default city on startup
# =========================
get_weather()

win.mainloop()
