import streamlit as st
import requests
from datetime import datetime
import plotly.graph_objs as go

# OpenWeatherMap API
API_KEY = "YOUR_API_KEY"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Icon mapping
def weather_icon(code):
    icons = {
        "01": "☀️", "02": "🌤️", "03": "☁️", "04": "☁️",
        "09": "🌧️", "10": "🌦️", "11": "⛈️", "13": "❄️", "50": "🌫️"
    }
    return icons.get(code[:2], "🌡️")

# Fetch 5-day forecast data
def fetch_forecast(city, api_unit):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": api_unit
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return None

# Main app
def main():
    st.set_page_config(page_title="Weather App", page_icon="🌦")
    st.title("🌍 Weather Forecast App")

    city = st.text_input("City Name", "Ahmedabad")
    unit_display = st.radio("Temperature Unit", ["Celsius", "Fahrenheit"], horizontal=True)
    api_unit = "metric" if unit_display == "Celsius" else "imperial"
    unit_symbol = "°C" if api_unit == "metric" else "°F"

    if st.button("Get Weather") or city:
        data = fetch_forecast(city, api_unit)
        if not data or data.get("cod") != "200":
            st.error("⚠️ Unable to fetch weather data.")
            return

        forecast_list = data["list"]
        city_info = data["city"]

        # 🌤️ Current Weather
        location_name = f"{city_info['name']}, {city_info['country']}"
        current = forecast_list[0]
        temp = current["main"]["temp"]
        desc = current["weather"][0]["description"].title()
        icon = weather_icon(current["weather"][0]["icon"])
        humidity = current["main"]["humidity"]
        wind = current["wind"]["speed"]

        sunrise_ts = city_info.get("sunrise")
        sunset_ts = city_info.get("sunset")
        sunrise = datetime.fromtimestamp(sunrise_ts).strftime("%I:%M %p") if sunrise_ts else "N/A"
        sunset = datetime.fromtimestamp(sunset_ts).strftime("%I:%M %p") if sunset_ts else "N/A"

        st.markdown(f"### 📍 {location_name}")
        col1, col2, col3 = st.columns(3)

        common_card_style = """
        background: linear-gradient(135deg, #2e2e45, #1b1b2d);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.4);
        min-height: 220px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        """


        with col1:
            st.markdown(f"""
                <div style='{common_card_style}'>
                    <h4 style="margin-bottom: 8px;">🌡 Temperature</h4>
                    <div style='font-size: 36px; margin: 8px 0;'>{temp:.1f}{unit_symbol}</div>
                    <p style='font-size: 18px;'>{icon} {desc}</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style='{common_card_style}'>
                    <h4 style="margin-bottom: 8px;">💧 Humidity & Wind</h4>
                    <p style='font-size: 20px; margin: 6px 0;'>💧 <b>{humidity}%</b></p>
                    <p style='font-size: 20px;'>💨 <b>{wind} {"m/s" if api_unit == "metric" else "mph"}</b></p>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div style='{common_card_style}'>
                    <h4 style="margin-bottom: 8px;">🌅 Sunrise & Sunset</h4>
                    <p style='font-size: 18px; margin: 6px 0;'>🌄 <b>{sunrise}</b></p>
                    <p style='font-size: 18px;'>🌇 <b>{sunset}</b></p>
                </div>
            """, unsafe_allow_html=True)

        # 📅 5-Day Forecast
        st.markdown("### 🔮 5-Day Forecast")
        daily = forecast_list[::8][:5]
        cols = st.columns(len(daily))
        for i, entry in enumerate(daily):
            dt = datetime.fromtimestamp(entry["dt"]).strftime("%a, %d %b")
            temp = entry["main"]["temp"]
            desc = entry["weather"][0]["description"].title()
            icon = weather_icon(entry["weather"][0]["icon"])
            with cols[i]:
                st.markdown(f"""
                    <div style="width: 100%; height: 280px;
                                background: linear-gradient(135deg, #3a3a50, #1e1e2f);
                                padding: 16px; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                                text-align: center; color: white;">
                        <h4>{dt}</h4>
                        <div style="font-size: 38px;">{icon}</div>
                        <div style="font-weight: bold;">{desc}</div>
                        <p>🌡️ <b>{temp:.1f}{unit_symbol}</b></p>
                    </div>
                """, unsafe_allow_html=True)

        # 📈 Temp Trend Chart
        st.subheader("📈 Temperature Trend (Next 5 Days)")
        times = [datetime.fromtimestamp(x["dt"]) for x in forecast_list]
        temps = [x["main"]["temp"] for x in forecast_list]
        fig = go.Figure(go.Scatter(x=times, y=temps, mode="lines+markers"))
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title=f"Temp ({unit_symbol})",
            height=400
        )
        st.plotly_chart(fig)

        # 🕒 Hourly Forecast
        st.subheader("🕒 Hourly Forecast (Next 12 Hours)")
        next_hours = forecast_list[:4]
        hour_cols = st.columns(len(next_hours))

        for i, entry in enumerate(next_hours):
            hour = datetime.fromtimestamp(entry["dt"]).strftime("%I %p")
            temp = entry["main"]["temp"]
            icon = weather_icon(entry["weather"][0]["icon"])
            desc = entry["weather"][0]["main"]

            with hour_cols[i]:
                st.markdown(f"""
                    <div style="
                        width: 100%;
                        height: 200px;
                        background: linear-gradient(135deg, #2c2c40, #1a1a2a);
                        padding: 16px;
                        border-radius: 16px;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                        text-align: center;
                        color: white;
                        font-family: 'Segoe UI', sans-serif;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    ">
                        <h4 style="margin: 4px 0;">{hour}</h4>
                        <div style="font-size: 32px; margin: 6px 0;">{icon}</div>
                        <div style="font-size: 18px; margin: 4px 0;">{temp:.1f}°{unit_symbol}</div>
                        <small style="opacity: 0.8;">{desc}</small>
                    </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
