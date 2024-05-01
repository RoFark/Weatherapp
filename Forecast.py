import streamlit as st
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from streamlit_lottie import st_lottie
st.set_page_config(page_title="Weather PANDAS App :rain_cloud::barely_sunny::sunny:", page_icon=":panda_face:")
st.header("Weather :rain_cloud::barely_sunny::sunny:")
# Background image styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-color: #4158D0;
background-image: linear-gradient(315deg, #4F2991 3%, #7DC4FF 38%, #36CFCC 68%, #A92ED3 98%);
}
[data-testid="stHeader"] {
background: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
right: 2rem;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# create sidebars
city = st.text_input("ENTER City Name ")
unit_temperature = st.sidebar.selectbox("SELECT TEMPERATURE UNIT :thermometer:", options=["Celsius", "Fahrenheit"])
unit_wind_speed = st.sidebar.selectbox("SELECT WIND SPEED UNIT ", options=["Metre/sec", "Kilometre/hour"])
if city:  # Check if city is not empty
    api = "569c216171a436cd3f04d77e39f100be"
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == "200":
        # Display weather for next 5 days
        forecasts = data["list"]
        for forecast in forecasts:
            date = forecast["dt_txt"]
            weather_description = forecast["weather"][0]["description"]
            temperature_kelvin = forecast["main"]["temp"]
            wind_speed = forecast["wind"]["speed"]
            # Convert temperature to the selected unit
            if unit_temperature == "Celsius":
                temperature = temperature_kelvin - 273.15  # Kelvin to Celsius
                temperature_unit = "°C"
            else:
                temperature = (temperature_kelvin - 273.15) * 9/5 + 32  # Kelvin to Fahrenheit
                temperature_unit = "°F"
            # Convert wind speed to the selected unit
            if unit_wind_speed == "Metre/sec":
                wind_speed_unit = "m/s"
            else:
                wind_speed = wind_speed * 3.6  # m/s to km/h
                wind_speed_unit = "km/h"
            st.write(f"Date: {date}")
            st.write(f"Weather: {weather_description}")
            st.write(f"Temperature: {temperature:.2f}{temperature_unit}")
            st.write(f"Wind Speed: {wind_speed:.2f}{wind_speed_unit}")
            st.write("---")
    else:
        st.write("City not found, enter a valid city")
else:
    st.warning("Please enter a city name")
# Function to scrape the MetOffice website and parse the warnings
def scrape_warnings():
    url = "https://www.metoffice.gov.uk/weather/warnings-and-advice/accessible-uk-warnings"
    response = requests.get(url)
    time.sleep(2)
    return response.text
def parse_warnings(html):
    soup = BeautifulSoup(html, 'html.parser')
    red_warning = soup.find('div', class_='red')
    amber_warning = soup.find('div', class_='amber')
    yellow_warning = soup.find('div', class_='yellow')
    return red_warning, amber_warning, yellow_warning
def display_warnings(red_warning, amber_warning, yellow_warning):
    st.title("MetOffice Current :violet[Weather Warnings]:heavy_exclamation_mark:")
    if red_warning:
        st.markdown("<p style='color:red;'>Red Warning:</p>", unsafe_allow_html=True)
        st.write(red_warning.get_text(strip=True))
        st.markdown("---")
    if amber_warning:
        st.markdown("<p style='color:amber;'>Amber Warning:</p>", unsafe_allow_html=True)
        st.write(amber_warning.get_text(strip=True))
        st.markdown("---")
    if yellow_warning:
        st.markdown("<p style='color:yellow;'>Yellow Warning:</p>", unsafe_allow_html=True)
        st.write(yellow_warning.get_text(strip=True))
# Main function to display weather and warnings
def main():
    html_content = scrape_warnings()
    red_warning, amber_warning, yellow_warning = parse_warnings(html_content)
    display_warnings(red_warning, amber_warning, yellow_warning)
if __name__ == "__main__":
    main()



