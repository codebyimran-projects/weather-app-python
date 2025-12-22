import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
from PIL import Image, ImageTk
import io
import os
from dotenv import load_dotenv
import threading

# =========================
# CONFIGURATION
# =========================
load_dotenv()
API_KEY = os.getenv("api_key")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Predefined cities
CITIES = [
    "Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad",
    "Multan", "Peshawar", "Quetta", "Sialkot", "Gujranwala",
    "London", "New York", "Tokyo", "Paris", "Dubai",
    "Sydney", "Mumbai", "Toronto", "Berlin", "Singapore"
]

# Weather icons mapping
WEATHER_ICONS = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "smoke": "💨",
    "haze": "😶‍🌫️",
    "dust": "💨",
    "fog": "🌁",
    "sand": "🌪️",
    "ash": "🌋",
    "squall": "💨",
    "tornado": "🌪️"
}

# Color themes for different weather conditions
COLOR_THEMES = {
    "clear": {"bg": "#FFD700", "fg": "#000000", "accent": "#FF8C00"},
    "clouds": {"bg": "#87CEEB", "fg": "#FFFFFF", "accent": "#4682B4"},
    "rain": {"bg": "#4169E1", "fg": "#FFFFFF", "accent": "#1E90FF"},
    "drizzle": {"bg": "#B0E0E6", "fg": "#2F4F4F", "accent": "#5F9EA0"},
    "thunderstorm": {"bg": "#483D8B", "fg": "#FFFFFF", "accent": "#8A2BE2"},
    "snow": {"bg": "#F0F8FF", "fg": "#000000", "accent": "#B0C4DE"},
    "default": {"bg": "#1E3A8A", "fg": "#FFFFFF", "accent": "#3B82F6"}
}

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App | Code by Imran")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#0F172A")
        
        # Center window
        self.center_window()
        
        # Current theme
        self.current_theme = COLOR_THEMES["default"]
        
        # Recent searches
        self.recent_searches = ["Karachi", "Lahore", "Islamabad"]
        
        # Setup UI
        self.setup_ui()
        
        # Load default city weather
        self.root.after(500, lambda: self.fetch_weather("Karachi"))

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Setup all UI components"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#0F172A")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Search Section
        self.create_search_section()
        
        # Weather Display
        self.create_weather_display()
        
        # Details Section
        self.create_details_section()
        
        # Footer
        self.create_footer()

    def create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self.main_frame, bg="#0F172A")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🌤️ Weather Master",
            font=("Arial", 24, "bold"),
            fg="#FFFFFF",
            bg="#0F172A"
        )
        title_label.pack(anchor="w")
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Real-time weather updates",
            font=("Arial", 10),
            fg="#94A3B8",
            bg="#0F172A"
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

    def create_search_section(self):
        """Create search section"""
        search_frame = tk.Frame(self.main_frame, bg="#1E293B", relief="flat", bd=1)
        search_frame.pack(fill="x", pady=(0, 20))
        
        # Search label
        tk.Label(
            search_frame,
            text="Search City",
            font=("Arial", 11, "bold"),
            fg="#E2E8F0",
            bg="#1E293B"
        ).pack(anchor="w", padx=15, pady=(12, 5))
        
        # Search input with dropdown
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(
            search_frame,
            textvariable=self.city_var,
            values=CITIES,
            font=("Arial", 12),
            state="normal",
            height=15
        )
        self.city_combo.pack(fill="x", padx=15, pady=5, ipady=8)
        self.city_combo.set("Karachi")
        self.city_combo.bind('<Return>', lambda e: self.on_search())
        
        # Button frame
        button_frame = tk.Frame(search_frame, bg="#1E293B")
        button_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Recent searches button
        recent_btn = tk.Button(
            button_frame,
            text="🕐 Recent",
            font=("Arial", 10),
            bg="#334155",
            fg="#E2E8F0",
            relief="flat",
            cursor="hand2",
            command=self.show_recent_menu
        )
        recent_btn.pack(side="left", padx=(0, 10))
        
        # Search button
        self.search_btn = tk.Button(
            button_frame,
            text="🔍 Search Weather",
            font=("Arial", 11, "bold"),
            bg="#3B82F6",
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.on_search
        )
        self.search_btn.pack(side="right", ipadx=20, ipady=6)
        
        # Bind hover effects
        recent_btn.bind("<Enter>", lambda e: recent_btn.config(bg="#475569"))
        recent_btn.bind("<Leave>", lambda e: recent_btn.config(bg="#334155"))
        self.search_btn.bind("<Enter>", lambda e: self.search_btn.config(bg="#2563EB"))
        self.search_btn.bind("<Leave>", lambda e: self.search_btn.config(bg="#3B82F6"))

    def create_weather_display(self):
        """Create weather display section"""
        self.weather_frame = tk.Frame(self.main_frame, bg=self.current_theme["bg"], relief="flat", bd=1)
        self.weather_frame.pack(fill="x", pady=(0, 20))
        
        # City name
        self.city_label = tk.Label(
            self.weather_frame,
            text="--",
            font=("Arial", 18, "bold"),
            fg=self.current_theme["fg"],
            bg=self.current_theme["bg"]
        )
        self.city_label.pack(pady=(20, 5))
        
        # Weather icon
        self.weather_icon = tk.Label(
            self.weather_frame,
            text="⏳",
            font=("Arial", 60),
            fg=self.current_theme["fg"],
            bg=self.current_theme["bg"]
        )
        self.weather_icon.pack(pady=10)
        
        # Temperature
        self.temp_label = tk.Label(
            self.weather_frame,
            text="--°C",
            font=("Arial", 48, "bold"),
            fg=self.current_theme["fg"],
            bg=self.current_theme["bg"]
        )
        self.temp_label.pack(pady=5)
        
        # Description
        self.desc_label = tk.Label(
            self.weather_frame,
            text="Fetching weather...",
            font=("Arial", 14),
            fg=self.current_theme["fg"],
            bg=self.current_theme["bg"]
        )
        self.desc_label.pack(pady=(5, 20))

    def create_details_section(self):
        """Create weather details section"""
        details_frame = tk.Frame(self.main_frame, bg="#1E293B", relief="flat", bd=1)
        details_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        tk.Label(
            details_frame,
            text="📊 Weather Details",
            font=("Arial", 12, "bold"),
            fg="#E2E8F0",
            bg="#1E293B"
        ).pack(anchor="w", padx=15, pady=(12, 10))
        
        # Details grid
        grid_frame = tk.Frame(details_frame, bg="#1E293B")
        grid_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Row 1
        row1 = tk.Frame(grid_frame, bg="#1E293B")
        row1.pack(fill="x", pady=5)
        
        self.feels_like_label = self.create_detail_item(row1, "🌡️ Feels Like", "--°C")
        self.humidity_label = self.create_detail_item(row1, "💧 Humidity", "--%")
        
        # Row 2
        row2 = tk.Frame(grid_frame, bg="#1E293B")
        row2.pack(fill="x", pady=5)
        
        self.wind_label = self.create_detail_item(row2, "💨 Wind", "-- km/h")
        self.pressure_label = self.create_detail_item(row2, "📊 Pressure", "-- hPa")
        
        # Row 3
        row3 = tk.Frame(grid_frame, bg="#1E293B")
        row3.pack(fill="x", pady=5)
        
        self.visibility_label = self.create_detail_item(row3, "👁️ Visibility", "-- km")
        self.clouds_label = self.create_detail_item(row3, "☁️ Clouds", "--%")

    def create_detail_item(self, parent, title, value):
        """Create a detail item with title and value"""
        item_frame = tk.Frame(parent, bg="#1E293B")
        item_frame.pack(side="left", expand=True, fill="x")
        
        # Title
        tk.Label(
            item_frame,
            text=title,
            font=("Arial", 9),
            fg="#94A3B8",
            bg="#1E293B"
        ).pack(anchor="w")
        
        # Value
        value_label = tk.Label(
            item_frame,
            text=value,
            font=("Arial", 11, "bold"),
            fg="#FFFFFF",
            bg="#1E293B"
        )
        value_label.pack(anchor="w", pady=(2, 0))
        
        return value_label

    def create_footer(self):
        """Create footer section"""
        footer_frame = tk.Frame(self.main_frame, bg="#0F172A")
        footer_frame.pack(fill="x", pady=(10, 0))
        
        # Status
        self.status_label = tk.Label(
            footer_frame,
            text="🟢 Ready",
            font=("Arial", 9),
            fg="#94A3B8",
            bg="#0F172A"
        )
        self.status_label.pack(side="left")
        
        # Copyright
        tk.Label(
            footer_frame,
            text="Made with ❤️ by Imran",
            font=("Arial", 9),
            fg="#64748B",
            bg="#0F172A"
        ).pack(side="right")

    def on_search(self):
        """Handle search button click"""
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name.")
            return
        
        # Start search in thread
        threading.Thread(target=self.fetch_weather, args=(city,), daemon=True).start()
        
        # Update UI
        self.search_btn.config(state="disabled", text="Searching...")
        self.status_label.config(text="🟡 Fetching weather data...")

    def fetch_weather(self, city):
        """Fetch weather data from API"""
        try:
            # API request
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }
            
            response = requests.get(BASE_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.root.after(0, lambda: self.update_ui(data))
                
                # Add to recent searches
                if city not in self.recent_searches:
                    self.recent_searches.insert(0, city)
                    if len(self.recent_searches) > 5:
                        self.recent_searches.pop()
            else:
                error_msg = "City not found" if response.status_code == 404 else "API Error"
                self.root.after(0, lambda: self.show_error(error_msg))
                
        except requests.exceptions.ConnectionError:
            self.root.after(0, lambda: self.show_error("No internet connection"))
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: self.show_error("Request timeout"))
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Error: {str(e)}"))
        finally:
            self.root.after(0, self.reset_search_button)

    def update_ui(self, data):
        """Update UI with weather data"""
        try:
            # Extract data
            city = data.get("name", "Unknown")
            country = data.get("sys", {}).get("country", "")
            temp = data.get("main", {}).get("temp", 0)
            feels_like = data.get("main", {}).get("feels_like", 0)
            humidity = data.get("main", {}).get("humidity", 0)
            pressure = data.get("main", {}).get("pressure", 0)
            wind_speed = data.get("wind", {}).get("speed", 0)
            visibility = data.get("visibility", 0)
            clouds = data.get("clouds", {}).get("all", 0)
            weather_desc = data.get("weather", [{}])[0].get("description", "").title()
            weather_main = data.get("weather", [{}])[0].get("main", "").lower()
            
            # Update theme based on weather
            self.update_theme(weather_main)
            
            # Update city label
            self.city_label.config(text=f"{city}, {country}" if country else city)
            
            # Update weather icon
            icon = WEATHER_ICONS.get(weather_main, "🌈")
            self.weather_icon.config(text=icon)
            
            # Update temperature
            self.temp_label.config(text=f"{temp:.1f}°C")
            
            # Update description
            self.desc_label.config(text=weather_desc)
            
            # Update details
            self.feels_like_label.config(text=f"{feels_like:.1f}°C")
            self.humidity_label.config(text=f"{humidity}%")
            self.wind_label.config(text=f"{wind_speed} km/h")
            self.pressure_label.config(text=f"{pressure} hPa")
            self.visibility_label.config(text=f"{visibility/1000:.1f} km" if visibility else "-- km")
            self.clouds_label.config(text=f"{clouds}%")
            
            # Update status
            self.status_label.config(text=f"🟢 Updated: {datetime.now().strftime('%H:%M:%S')}")
            
            # Update weather frame background
            self.weather_frame.config(bg=self.current_theme["bg"])
            
            # Update all widgets in weather frame
            for widget in self.weather_frame.winfo_children():
                widget.config(bg=self.current_theme["bg"], fg=self.current_theme["fg"])
            
        except Exception as e:
            self.show_error(f"Error updating UI: {str(e)}")

    def update_theme(self, weather_main):
        """Update color theme based on weather"""
        # Find matching theme
        for key in COLOR_THEMES:
            if key in weather_main:
                self.current_theme = COLOR_THEMES[key]
                return
        
        # Use default if no match
        self.current_theme = COLOR_THEMES["default"]

    def show_recent_menu(self):
        """Show recent searches menu"""
        if not self.recent_searches:
            messagebox.showinfo("Recent Searches", "No recent searches found.")
            return
        
        # Create menu
        menu = tk.Menu(self.root, tearoff=0)
        for city in self.recent_searches:
            menu.add_command(
                label=city,
                command=lambda c=city: self.select_recent_city(c)
            )
        
        # Show menu
        try:
            menu.tk_popup(
                self.search_btn.winfo_rootx(),
                self.search_btn.winfo_rooty() + self.search_btn.winfo_height()
            )
        finally:
            menu.grab_release()

    def select_recent_city(self, city):
        """Select city from recent searches"""
        self.city_var.set(city)
        self.fetch_weather(city)

    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
        
        # Reset UI to default
        self.city_label.config(text="--")
        self.weather_icon.config(text="❓")
        self.temp_label.config(text="--°C")
        self.desc_label.config(text="Error loading data")
        
        # Reset details
        self.feels_like_label.config(text="--°C")
        self.humidity_label.config(text="--%")
        self.wind_label.config(text="-- km/h")
        self.pressure_label.config(text="-- hPa")
        self.visibility_label.config(text="-- km")
        self.clouds_label.config(text="--%")
        
        self.status_label.config(text="🔴 Error occurred")

    def reset_search_button(self):
        """Reset search button state"""
        self.search_btn.config(state="normal", text="🔍 Search Weather")

def main():
    """Main function"""
    # Check API key
    if API_KEY == "your_api_key_here":
        response = messagebox.askyesno(
            "API Key Required",
            "You need an OpenWeather API key.\n\n"
            "1. Sign up at https://home.openweathermap.org/users/sign_up\n"
            "2. Get your API key\n"
            "3. Create a .env file with: OPENWEATHER_API_KEY=your_key\n\n"
            "Do you want to continue anyway?"
        )
        
        if not response:
            return
    
    # Create and run app
    root = tk.Tk()
    app = WeatherApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApp closed by user")

if __name__ == "__main__":
    main()