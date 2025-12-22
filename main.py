import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import threading

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# =========================
# Weather Function with Error Handling
# =========================
def get_weather(event=None):
    city = city_var.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return
    
    # Show loading state
    loading_label.pack(pady=10)
    search_btn.config(state="disabled", text="Loading...")
    win.update()
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if response.status_code == 200:
            # Extract data
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]
            desc = data["weather"][0]["description"]
            wind = data["wind"]["speed"]
            weather_main = data["weather"][0]["main"].lower()
            
            # Get country and time
            country = data.get("sys", {}).get("country", "")
            sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%I:%M %p')
            sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%I:%M %p')
            
            # Update UI
            city_name_label.config(text=f"{city.title()}, {country}" if country else city.title())
            description.config(text=desc.capitalize())
            temperature.config(text=f"{temp:.1f}°C")
            feels_like_label.config(text=f"Feels like: {feels_like:.1f}°C")
            
            # Update detailed info
            details_text = f"""
            ⚡ Min/Max: {temp_min:.1f}°C / {temp_max:.1f}°C
            💧 Humidity: {humidity}%
            💨 Wind: {wind} km/h
            📊 Pressure: {pressure} hPa
            🌅 Sunrise: {sunrise}
            🌇 Sunset: {sunset}
            """
            extra_info.config(text=details_text.strip())
            
            # Update weather icon and colors
            update_weather_theme(weather_main)
            
            # Add to recent searches
            if city.title() not in recent_searches:
                recent_searches.insert(0, city.title())
                if len(recent_searches) > 5:
                    recent_searches.pop()
                recent_menu['menu'].delete(0, 'end')
                for search in recent_searches:
                    recent_menu['menu'].add_command(label=search, 
                                                   command=lambda s=search: set_city(s))
            
            # Save to history
            save_to_history(city, temp, desc)

        else:
            messagebox.showerror("Error", f"City not found: {city}")
            description.config(text="City not found")
            temperature.config(text="--")
            feels_like_label.config(text="")
            extra_info.config(text="")
            update_weather_theme("unknown")

    except requests.exceptions.Timeout:
        messagebox.showerror("Error", "Request timeout. Please try again.")
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "No internet connection.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        # Hide loading state
        loading_label.pack_forget()
        search_btn.config(state="normal", text="Get Weather")

def update_weather_theme(weather_main):
    """Update colors and emoji based on weather condition"""
    weather_icons = {
        "clear": ("☀️", "#FBBF24", "#F59E0B"),
        "cloud": ("☁️", "#94A3B8", "#64748B"),
        "rain": ("🌧️", "#60A5FA", "#3B82F6"),
        "drizzle": ("🌦️", "#38BDF8", "#0EA5E9"),
        "snow": ("❄️", "#BAE6FD", "#7DD3FC"),
        "storm": ("⛈️", "#F87171", "#DC2626"),
        "thunder": ("⚡", "#FBBF24", "#F59E0B"),
        "mist": ("🌫️", "#A5B4FC", "#818CF8"),
        "fog": ("🌁", "#CBD5E1", "#94A3B8"),
        "haze": ("😶‍🌫️", "#FDE68A", "#FCD34D")
    }
    
    # Find matching weather condition
    icon, color1, color2 = "🌈", "#8B5CF6", "#7C3AED"  # Default purple
    
    for key in weather_icons:
        if key in weather_main:
            icon, color1, color2 = weather_icons[key]
            break
    
    # Update UI elements
    emoji_label.config(text=icon)
    weather_card.config(bg=color1)
    
    # Update all child widgets
    for widget in weather_card.winfo_children():
        widget.config(bg=color1)
    
    # Special config for specific widgets
    city_name_label.config(bg=color1, fg="#1E293B")
    description.config(bg=color1, fg="#374151")
    temperature.config(bg=color1, fg="#111827")
    feels_like_label.config(bg=color1, fg="#4B5563")
    extra_info.config(bg=color1, fg="#374151")
    
    # Add gradient effect
    weather_card.config(highlightbackground=color2, highlightthickness=2)

def set_city(city):
    """Set city from recent searches"""
    city_var.set(city)
    get_weather()

def save_to_history(city, temp, desc):
    """Save weather data to history file"""
    try:
        history_file = "weather_history.json"
        history = []
        
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        
        history.append({
            "city": city,
            "temperature": temp,
            "description": desc,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Keep only last 50 entries
        history = history[-50:]
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception as e:
        print(f"Error saving history: {e}")

def on_enter(e):
    """Button hover effect"""
    e.widget.config(bg="#0EA5E9")

def on_leave(e):
    """Button leave effect"""
    e.widget.config(bg="#38BDF8")

# =========================
# Main Window
# =========================
win = tk.Tk()
win.geometry("500x850")
win.title("Weather App | Code by Imran")
win.configure(bg="#0F172A")
win.resizable(False, False)

# Make window center screen
win.update_idletasks()
width = win.winfo_width()
height = win.winfo_height()
x = (win.winfo_screenwidth() // 2) - (width // 2)
y = (win.winfo_screenheight() // 2) - (height // 2)
win.geometry(f'{width}x{height}+{x}+{y}')

# =========================
# Header with Gradient
# =========================
header_frame = tk.Frame(win, bg="#0F172A")
header_frame.pack(pady=(20, 10))

# Title with gradient effect
title_label = tk.Label(
    header_frame,
    text="🌤️ Weather Dashboard",
    font=("Segoe UI", 32, "bold"),
    fg="#38BDF8",
    bg="#0F172A"
)
title_label.pack()

subtitle_label = tk.Label(
    header_frame,
    text="Real-time weather updates • Powered by OpenWeather",
    font=("Segoe UI", 11),
    fg="#94A3B8",
    bg="#0F172A"
)
subtitle_label.pack(pady=(5, 15))

# =========================
# Search Card
# =========================
search_card = tk.Frame(win, bg="#1E293B", bd=2, relief="ridge")
search_card.pack(pady=15, padx=30, fill="x")

search_label = tk.Label(
    search_card,
    text="📍 Enter City Name",
    font=("Segoe UI", 12, "bold"),
    fg="#E2E8F0",
    bg="#1E293B"
)
search_label.pack(anchor="w", padx=20, pady=(20, 5))

# City input with dropdown
cities = ["Karachi", "Lahore", "Islamabad", "Delhi", "London", "New York", 
          "Tokyo", "Paris", "Dubai", "Sydney", "Mumbai", "Toronto"]
recent_searches = ["Karachi", "Lahore", "Islamabad"]

city_var = tk.StringVar(value="Karachi")

# Create input frame
input_frame = tk.Frame(search_card, bg="#1E293B")
input_frame.pack(padx=20, pady=10, fill="x")

city_entry = ttk.Combobox(
    input_frame,
    textvariable=city_var,
    values=cities,
    font=("Segoe UI", 13),
    state="normal",
    height=8
)
city_entry.pack(side="left", fill="x", expand=True, ipady=8)
city_entry.bind('<Return>', get_weather)

# Recent searches label
recent_label = tk.Label(
    search_card,
    text="Recent Searches:",
    font=("Segoe UI", 10),
    fg="#94A3B8",
    bg="#1E293B"
)
recent_label.pack(anchor="w", padx=20, pady=(5, 0))

# Recent searches menu
recent_menu = ttk.Menubutton(
    search_card,
    text="Select Recent",
    direction="below"
)
recent_menu.pack(anchor="w", padx=20, pady=5)

recent_menu.menu = tk.Menu(recent_menu, tearoff=0)
recent_menu["menu"] = recent_menu.menu

for city in recent_searches:
    recent_menu.menu.add_command(label=city, 
                                command=lambda s=city: set_city(s))

# Get Weather Button with hover effect
search_btn = tk.Button(
    search_card,
    text="Get Weather",
    font=("Segoe UI", 14, "bold"),
    bg="#38BDF8",
    fg="#0F172A",
    bd=0,
    padx=30,
    cursor="hand2",
    command=get_weather
)
search_btn.pack(pady=(10, 20), ipady=12)
search_btn.bind("<Enter>", on_enter)
search_btn.bind("<Leave>", on_leave)

# Loading indicator
loading_label = tk.Label(
    search_card,
    text="⏳ Loading weather data...",
    font=("Segoe UI", 10, "italic"),
    fg="#94A3B8",
    bg="#1E293B"
)

# =========================
# Weather Card
# =========================
weather_card = tk.Frame(
    win,
    bg="#1E293B",
    bd=2,
    relief="ridge",
    highlightthickness=2
)
weather_card.pack(pady=15, padx=30, fill="both", expand=True)

# Emoji/Icon
emoji_label = tk.Label(
    weather_card,
    text="☀️",
    font=("Segoe UI", 80),
    bg="#1E293B"
)
emoji_label.pack(pady=(25, 10))

# City name
city_name_label = tk.Label(
    weather_card,
    text="Karachi, PK",
    font=("Segoe UI", 24, "bold"),
    fg="#38BDF8",
    bg="#1E293B"
)
city_name_label.pack(pady=(5, 5))

# Weather description
description = tk.Label(
    weather_card,
    text="Clear Sky",
    font=("Segoe UI", 14),
    fg="#E2E8F0",
    bg="#1E293B"
)
description.pack(pady=5)

# Temperature
temperature = tk.Label(
    weather_card,
    text="32.0°C",
    font=("Segoe UI", 48, "bold"),
    fg="#FFFFFF",
    bg="#1E293B"
)
temperature.pack(pady=10)

# Feels like temperature
feels_like_label = tk.Label(
    weather_card,
    text="Feels like: 34.2°C",
    font=("Segoe UI", 11),
    fg="#94A3B8",
    bg="#1E293B"
)
feels_like_label.pack(pady=5)

# Separator
separator = tk.Frame(weather_card, height=2, bg="#334155")
separator.pack(fill="x", padx=40, pady=15)

# Extra information (detailed)
extra_info = tk.Label(
    weather_card,
    text="",
    font=("Segoe UI", 11),
    fg="#94A3B8",
    bg="#1E293B",
    justify="left"
)
extra_info.pack(pady=10, padx=20)

# =========================
# Footer with Status
# =========================
footer_frame = tk.Frame(win, bg="#0F172A")
footer_frame.pack(side="bottom", fill="x", pady=(10, 0))

# Status bar
status_bar = tk.Label(
    footer_frame,
    text="🟢 Ready • Last updated: --",
    font=("Segoe UI", 9),
    fg="#64748B",
    bg="#0F172A"
)
status_bar.pack(side="left", padx=20, pady=5)

# Copyright
copyright_label = tk.Label(
    footer_frame,
    text="Code by Imran • OpenWeather API",
    font=("Segoe UI", 10, "italic"),
    fg="#64748B",
    bg="#0F172A"
)
copyright_label.pack(side="right", padx=20, pady=5)

# =========================
# Auto-load on startup
# =========================
def initial_load():
    """Load initial weather data"""
    win.after(100, get_weather)

initial_load()

# =========================
# Run the application
# =========================
if __name__ == "__main__":
    try:
        win.mainloop()
    except KeyboardInterrupt:
        print("\nWeather app closed")