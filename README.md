# 🌤️ Weather Forecast App

A modern, dark-themed weather forecast application built using **Streamlit**, **Plotly**, and the **OpenWeatherMap API**. This app provides real-time weather conditions, hourly updates, and a 5-day forecast in a clean and interactive UI.


## 📌 Key Features

- 🔍 **City-based Weather Search**
- 🌡 **Current Conditions**  
  - Temperature, Weather Description, Humidity, Wind Speed, Sunrise & Sunset  
- 📆 **5-Day Forecast**  
  - Each day presented in styled, consistent weather cards  
- 🕒 **Next 12-Hour Forecast**  
  - Hourly updates with icons and temperature  
- 📊 **Interactive Charts**  
  - Temperature trends using Plotly


## 🛠️ Built With

- [Streamlit](https://streamlit.io/) – Fast, interactive web apps in Python  
- [Plotly](https://plotly.com/python/) – Graphs and charts  
- [OpenWeatherMap API](https://openweathermap.org/api) – Weather data  
- Python Standard Libraries (`datetime`, `requests`)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone hhttps://github.com/princeparmar03/Real-Time-Weather-App.git
cd Real-Time-Weather-App
```

### 2. Install Dependencies

```bash
pip install streamlit requests matplotlib pandas
```

### 3. Add Your OpenWeatherMap API Key

```bash
API_KEY = "your_openweathermap_api_key"
```
You can get a free API key from: https://openweathermap.org/api

### ▶️ Run the App

```bash
streamlit run weather.py
or
python -m streamlit run weather.py
```

### 📁 Folder Structure

```bash
weather-forecast-streamlit/
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

```
