
# Weather App | Python Tkinter

[Repository Link](https://github.com/codebyimran-projects/weather-app-python)

A modern, feature-rich **Weather App** built with **Python** and **Tkinter**, providing real-time weather updates for cities around the world using the **OpenWeather API**. The app uses **emojis** for weather icons and has a dynamic color theme based on the weather condition.

---

## Features

- Real-time weather updates for multiple cities  
- Dropdown to select city + search input  
- Recent searches menu  
- Dynamic emoji-based weather icons (sun, cloud, rain, snow, etc.)  
- Color themes based on weather conditions  
- Detailed weather information:  
  - Temperature & Feels Like  
  - Humidity  
  - Wind speed  
  - Pressure  
  - Visibility  
  - Cloud coverage  
- Responsive and modern UI using Tkinter frames  
- Error handling for invalid cities or API issues  

---

## Installation

1. **Clone the repository**  

```bash
git clone https://github.com/codebyimran-projects/weather-app-python.git
cd weather-app-python
````

2. **Create and activate a virtual environment (optional but recommended)**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** in the root directory and add your OpenWeather API key:

```
api_key=YOUR_OPENWEATHER_API_KEY
```

5. **Run the app**

```bash
python main.py
```

---

## Dependencies

* `tkinter` (built-in with Python)
* `requests` (for API calls)
* `python-dotenv` (to load API key from .env)
* `Pillow` (optional if you want images/icons instead of emojis)

Install missing packages with:

```bash
pip install requests python-dotenv pillow
```

---

## Usage

1. Open the app.
2. Select a city from the dropdown or type a city name.
3. Click **Search Weather** or press **Enter**.
4. View real-time weather details, including temperature, humidity, wind, pressure, visibility, and cloud coverage.
5. Access recent searches via the **🕐 Recent** button.

---

## License

This project is **open-source**. Feel free to use and modify it for personal projects.

---

## Author

**Muhammad Imran**
[GitHub](https://github.com/codebyimran-projects)

