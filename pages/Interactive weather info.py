import streamlit as st
import pandas as pd
import requests
import json
import folium
from streamlit_folium import folium_static
import pyowm
# UI components
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
st.title("Weather Forecast with Interactive Map")
# OpenWeatherMap API
owm = pyowm.OWM("569c216171a436cd3f04d77e39f100be")
mgr = owm.weather_manager()
# Select location
file = "pages/worldcities.csv"  # Adjust path as necessary
data = pd.read_csv(file, dtype=object)
country_set = set(data["country"])
country = st.selectbox('Select a country', options=country_set)
country_data = data[data["country"] == country]
city_set = country_data["city_ascii"]
city = st.selectbox('Select a city', options=city_set)
lat = float(country_data[country_data["city_ascii"] == city]["lat"])
lng = float(country_data[country_data["city_ascii"] == city]["lng"])
# Get current weather
obs = mgr.weather_at_coords(lat, lng)
weather = obs.weather
temp = weather.temperature('celsius')['temp']
cloud_cov = weather.clouds
wind_speed = weather.wind()['speed']
rain = weather.rain
rain = rain.get('1h', 0) if rain else 0
weather_desc = weather.detailed_status
# Determine weather condition and select cartoon image
def get_weather_image():
    if "rain" in weather_desc.lower():
        return "rain.png"
    elif "cloud" in weather_desc.lower():
        return "cloud.png"
    else:
        return "sun.png"
weather_image = get_weather_image()
# Display current weather information
st.subheader("Current weather")
st.write(f"Temperature: {temp} °C")
st.write(f"Cloud Coverage: {cloud_cov} %")
st.write(f"Wind Speed: {wind_speed} m/s")
st.write(f"Rainfall: {rain} mm/h")
st.image(weather_image, caption=weather_desc, width=100)
# Create interactive map
m = folium.Map(location=[lat, lng], zoom_start=10)
folium.Marker([lat, lng], popup=f"{city}, {country}", tooltip=f"{city}, {country} - {temp} °C").add_to(m)
# Display map
st.subheader("Selected location Map")
st_data = folium_static(m)
# Display additional weather information
st.subheader("Additional Weather Information")
st.write(f"Weather Description: {weather_desc}")
# Display forecast for the week ahead (if available)
if st.button("Show Forecast"):
    forecast = mgr.forecast_at_coords(lat, lng, '3h').forecast
    for weather in forecast:
        st.write(weather.reference_time('iso'), weather.temperature('celsius')["temp"], "°C")
import os
import pytz
import pyowm
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from PIL import Image
from dateutil.relativedelta import relativedelta # to add days or years


# API_KEY = os.environ['API_KEY']
owm = pyowm.OWM("569c216171a436cd3f04d77e39f100be")
mgr=owm.weather_manager()

degree_sign= u'\N{DEGREE SIGN}'

st.title("Updated Weather Forecast")


# st.write("### Type City name and select the Temperature Unit and Graph Type from the sidebar")

place=st.text_input("CITY:", "")


if place == None:
    st.write("Input a CITY!")


unit=st.selectbox("SELECT TEMPERATURE UNIT 🌡", options=["Celsius","Fahrenheit"])

g_type=st.selectbox("Select Graph Type",("Line Graph","Bar Graph"))

# if unit=="Celsius":
#     temp_unit=" °C"
# else:
#     temp_unit=" °F"
# if speed=="Kilometre/hour":
#     wind_unit=" km/h"
# else:
#     wind_unit=" m/s"
if unit == 'Celsius':
    unit_c = 'celsius'
else:
    unit_c = 'fahrenheit'


def get_temperature():
    days = []
    dates = []
    temp_min = []
    temp_max = []
    forecaster = mgr.forecast_at_place(place, '3h')
    forecast=forecaster.forecast
    for weather in forecast:
        day=datetime.utcfromtimestamp(weather.reference_time())
        #day = gmt_to_eastern(weather.reference_time())
        date = day.date()
        if date not in dates:
            dates.append(date)
            temp_min.append(None)
            temp_max.append(None)
            days.append(date)
        temperature = weather.temperature(unit_c)['temp']
        if not temp_min[-1] or temperature < temp_min[-1]:
            temp_min[-1] = temperature
        if not temp_max[-1] or temperature > temp_max[-1]:
            temp_max[-1] = temperature
    return(days, temp_min, temp_max)

def init_plot():
     plt.figure('PyOWM Weather', figsize=(5,4))
     plt.xlabel('Day')
     plt.ylabel(f'Temperature ({degree_sign}F)')
     plt.title('Weekly Forecast')



def plot_temperatures(days, temp_min, temp_max):
    # days = dates.date2num(days)
    fig = go.Figure(
        data=[
            go.Bar(name='minimum temperatures', x=days, y=temp_min),
            go.Bar(name='maximum temperatures', x=days, y=temp_max)
        ]
    )
    fig.update_layout(barmode='group')
    return fig


def plot_temperatures_line(days, temp_min, temp_max):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=temp_min, name='minimum temperatures'))
    fig.add_trace(go.Scatter(x=days, y=temp_max, name='maximimum temperatures'))
    return fig

def label_xaxis(days):
    plt.xticks(days)
    axes = plt.gca()
    xaxis_format = dates.DateFormatter('%m/%d')
    axes.xaxis.set_major_formatter(xaxis_format)

def draw_bar_chart():
    days, temp_min, temp_max = get_temperature()
    fig = plot_temperatures(days, temp_min, temp_max)
    # write_temperatures_on_bar_chart(bar_min, bar_max)
    st.plotly_chart(fig)
    st.title("Minimum and Maximum Temperatures")
    for i in range (0,5):
        st.write("### ",temp_min[i],degree_sign,' --- ',temp_max[i],degree_sign)


def draw_line_chart():
    days, temp_min, temp_max = get_temperature()
    fig = plot_temperatures_line(days, temp_min, temp_max)
    st.plotly_chart(fig)
    st.title("Minimum and Maximum Temperatures")
    for i in range (0,5):
        st.write("### ",temp_min[i],degree_sign,' --- ',temp_max[i],degree_sign)

def other_weather_updates():
    forecaster = mgr.forecast_at_place(place, '3h')
    st.title("Impending Temperature Changes :")
    if forecaster.will_have_fog():
        st.write("### FOG Alert!")
    if forecaster.will_have_rain():
        st.write("### Rain Alert")
    if forecaster.will_have_storm():
        st.write("### Storm Alert!")
    if forecaster.will_have_snow():
        st.write("### Snow Alert!")
    if forecaster.will_have_tornado():
        st.write("### Tornado Alert!")
    if forecaster.will_have_hurricane():
        st.write("### Hurricane Alert!")
    if forecaster.will_have_clouds():
        st.write("### Cloudy Skies")    
    if forecaster.will_have_clear():
        st.write("### Clear Weather!")

# def lat_and_lon():
#     obs=mgr.weather_at_coords(place)
#     weather=obs.weather
#     latitude=weather.lat
#     longitude=weather.lon
#     st.write('### Longitude: ',place,longitude)
#     st.write('### Latitude: ',place,latitude)

# def lat_and_lon():
#     obs=mgr.weather_at_place(place)
#     weather=obs.weather
#     latitude=weather.latitude
#     longitude=weather.longitude
#     st.write('### Longitude: ',place,longitude)
#     st.write('### Latitude: ',place,latitude)
 
def get_info():
    obs=mgr.weather_at_place(place)
    info = obs.weather.detailed_status
    st.write('### Info: ',info ) 
     
def cloud_and_wind():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    cloud_cov=weather.clouds
    winds=weather.wind()['speed']
    st.title("Cloud coverage and wind speed")
    st.write('### The current cloud coverage for',place,'is',cloud_cov,'%')
    st.write('### The current wind speed for',place, 'is',winds,'mph')



def sunrise_and_sunset():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    st.title("Sunrise and Sunset Times :")
    india = pytz.timezone("Asia/Kolkata")
    ss=weather.sunset_time(timeformat='iso')
    sr=weather.sunrise_time(timeformat='iso')  
    st.write("### Sunrise time in",place,"is",sr)
    st.write("### Sunset time in",place,"is",ss)

def updates():
    other_weather_updates()
    get_info()
    cloud_and_wind()
    sunrise_and_sunset()


if __name__ == '__main__':
    
    if st.button("SUBMIT"):
        if g_type == 'Line Graph':
            draw_line_chart()    
        else:
            draw_bar_chart()
        updates()


# import streamlit as st
# import pandas as pd
# import requests
# import json
# import folium
# from streamlit_folium import folium_static
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots  # Add this import
# page_bg_img = """
# <style>
# [data-testid="stAppViewContainer"] {
# background-color: #4158D0;
# background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
# }
# [data-testid="stHeader"] {
# background: rgba(0,0,0,0);
# }
# [data-testid="stToolbar"] {
# right: 2rem;
# }
# </style>
# """
# st.markdown(page_bg_img, unsafe_allow_html=True)
# # Title and description for your app
# st.title("How's the weather? :sun_behind_rain_cloud:")
# st.subheader("Choose location")
# file = "/Users/rosie.farkash/Desktop/Streamlit FE/pages/worldcities.csv"
# data = pd.read_csv(file, dtype=object)
# # Select Country
# country_set = set(data.loc[:, "country"])
# country = st.selectbox('Select a country', options=country_set)
# country_data = data.loc[data.loc[:, "country"] == country, :]
# city_set = country_data.loc[:, "city_ascii"]
# city = st.selectbox('Select a city', options=city_set)
# lat = float(country_data.loc[data.loc[:, "city_ascii"] == city, "lat"])
# lng = float(country_data.loc[data.loc[:, "city_ascii"] == city, "lng"])
# response_current = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current_weather=true')
# st.subheader("Current weather")
# result_current = json.loads(response_current._content)
# current = result_current["current_weather"]
# temp = current["temperature"]
# speed = current["windspeed"]
# direction = current["winddirection"]
# # Increment added or subtracted from degree values for wind direction
# ddeg = 11.25
# # Determine wind direction based on received degrees
# if direction >= (360 - ddeg) or direction < (0 + ddeg):
#     common_dir = "N"
# elif direction >= (337.5 - ddeg) and direction < (337.5 + ddeg):
#     common_dir = "N/NW"
# elif direction >= (315 - ddeg) and direction < (315 + ddeg):
#     common_dir = "NW"
# elif direction >= (292.5 - ddeg) and direction < (292.5 + ddeg):
#     common_dir = "W/NW"
# elif direction >= (270 - ddeg) and direction < (270 + ddeg):
#     common_dir = "W"
# elif direction >= (247.5 - ddeg) and direction < (247.5 + ddeg):
#     common_dir = "W/SW"
# elif direction >= (225 - ddeg) and direction < (225 + ddeg):
#     common_dir = "SW"
# elif direction >= (202.5 - ddeg) and direction < (202.5 + ddeg):
#     common_dir = "S/SW"
# elif direction >= (180 - ddeg) and direction < (180 + ddeg):
#     common_dir = "S"
# elif direction >= (157.5 - ddeg) and direction < (157.5 + ddeg):
#     common_dir = "S/SE"
# elif direction >= (135 - ddeg) and direction < (135 + ddeg):
#     common_dir = "SE"
# elif direction >= (112.5 - ddeg) and direction < (112.5 + ddeg):
#     common_dir = "E/SE"
# elif direction >= (90 - ddeg) and direction < (90 + ddeg):
#     common_dir = "E"
# elif direction >= (67.5 - ddeg) and direction < (67.5 + ddeg):
#     common_dir = "E/NE"
# elif direction >= (45 - ddeg) and direction < (45 + ddeg):
#     common_dir = "NE"
# elif direction >= (22.5 - ddeg) and direction < (22.5 + ddeg):
#     common_dir = "N/NE"
# st.info(f"Current temperature: {temp} °C. \n\n Wind speed {speed} m/s, coming from {common_dir}. \n\n Longitude- {lng} & Latitude- {lat}.")
# st.subheader("Week ahead")
# st.write('Temperature and rain forecast one week ahead & city location on the map', unsafe_allow_html=True)
# with st.spinner('Loading...'):
#     response_hourly = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&hourly=temperature_2m,precipitation')
#     result_hourly = json.loads(response_hourly._content)
#     hourly = result_hourly["hourly"]
#     hourly_df = pd.DataFrame.from_dict(hourly)
#     hourly_df.rename(columns={'time': 'Week ahead'}, inplace=True)
#     hourly_df









    
        
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import pandas as pd
# page_bg_img = """
# <style>
# [data-testid="stAppViewContainer"] {
# background-color: #4158D0;
# background-image: linear-gradient(315deg, #4F2991 3%, #7DC4FF 38%, #36CFCC 68%, #A92ED3 98%);
# }
# [data-testid="stHeader"] {
# background: rgba(0,0,0,0);
# }
# [data-testid="stToolbar"] {
# right: 2rem;
# }
# </style>
# """
# st.markdown(page_bg_img, unsafe_allow_html=True)
# def get_storm_data(url, table_xpath):
#     # Set up Chrome options
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Run Chrome in headless mode
#     # Use webdriver
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get(url)
#     driver.maximize_window()
#     # Find the table element
#     try:
#         table_element = driver.find_element(By.XPATH, table_xpath)
#     except:
#         st.warning("No data found.")
#         driver.quit()
#         return pd.DataFrame()
#     # Find rows within the table
#     rows = table_element.find_elements(By.XPATH, './/tbody/tr')
#     # Extract data from rows
#     storm_result = []
#     for row in rows:
#         columns = row.find_elements(By.XPATH, 'td')
#         temporary_data = {
#             'Name': columns[0].text,
#             'Date named': columns[1].text,
#             'Date of impact': columns[2].text,
#         }
#         storm_result.append(temporary_data)
#     df_data = pd.DataFrame(storm_result)
#     driver.quit()  # Close the webdriver
#     return df_data
# def main():
#     st.title("Met Office Storm Centre Data")
#     # User input for storm season
#     storm_season_latest = st.checkbox("Show Latest Storm Season", value=True)
#     storm_season_previous = st.checkbox("Show Previous Storm Season", value=False)
#     if not storm_season_latest and not storm_season_previous:
#         st.warning("Please select at least one option.")
#     if storm_season_latest:
#         url_latest = 'https://www.metoffice.gov.uk/weather/warnings-and-advice/uk-storm-centre/index'
#         table_xpath_latest = '//*[@id="content"]/div[3]/div[2]/div[1]/article/div/div[2]/div[1]/div/div[1]/div[2]/table'
#         df_data_latest = get_storm_data(url_latest, table_xpath_latest)
#         st.subheader("Latest Storm Season Data")
#         st.table(df_data_latest)
#     if storm_season_previous:
#         previous_season = st.selectbox("Select Previous Storm Season", ['2022-23', '2021-22', '2020-21', '2019-20'])
#         url_previous = f'https://www.metoffice.gov.uk/weather/warnings-and-advice/uk-storm-centre/uk-storm-season-{previous_season}'
#         table_xpath_previous = '/html/body/main/div[3]/div[2]/div[1]/article/div/div[2]/div[1]/div/div[1]/div[1]/table' 
#         df_data_previous = get_storm_data(url_previous, table_xpath_previous)
#         if not df_data_previous.empty:
#             st.subheader(f"{previous_season} Storm Season Data")
#             st.table(df_data_previous)
#         else:
#             st.warning(f"No data found for the {previous_season} storm season.")
#     # Option to download as CSV
#     if st.button("Download CSV"):
#         if not df_data_latest.empty:
#             csv_export_latest = df_data_latest.to_csv(index=False)
#             st.download_button("Download Latest Storm Season CSV", csv_export_latest, file_name="met_office_storm_data_latest.csv", key="csv_download_latest")
#         if not df_data_previous.empty:
#             csv_export_previous = df_data_previous.to_csv(index=False)
#             st.download_button("Download Previous Storm Season CSV", csv_export_previous, file_name=f"met_office_storm_data_{previous_season}.csv", key="csv_download_previous")
# if __name__ == "__main__":
#     main()




# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import time
# import pandas as pd
# page_bg_img = """
# <style>
# [data-testid="stAppViewContainer"] {
# background-color: #4158D0;
# background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
# }
# [data-testid="stHeader"] {
# background: rgba(0,0,0,0);
# }
# [data-testid="stToolbar"] {
# right: 2rem;
# }
# </style>
# """
# st.markdown(page_bg_img, unsafe_allow_html=True)
# url = "https://www.metoffice.gov.uk/weather/warnings-and-advice/accessible-uk-warnings"
# def scrape_website(url):
#     response = requests.get(url)
#     time.sleep(2)
#     return response.text
# def parse_html(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     sections = soup.find_all('div', class_='description')
#     warning_content_matrix = soup.find('div', class_='warning-content-matrix')
#     warning_description = soup.find('div', class_='warning-description')
#     warning_headlines = soup.find('div', class_='warning-headlines')
#     warning_detail_holder = soup.find('div', class_='warning-detail-holder')
#     if sections:
#         result = []
#         for section in sections:
#             level = section.find_previous('div', class_='level')
#             date = section.find_previous('div', class_='date')
#             regions = section.find_previous('div', class_='regions')
#             level_text = level.get_text(strip=True) if level else None
#             date_text = date.get_text(strip=True) if date else None
#             regions_text = regions.get_text(strip=True) if regions else None
#             description_text = section.get_text(strip=True)
#             result.append({
#                 "Level": level_text,
#                 "Date": date_text,
#                 "Regions": regions_text,
#                 "Description": description_text
#             })
#         return result, warning_content_matrix, warning_description, warning_headlines, warning_detail_holder
#     return [], None, None, None, None
# def display_data(data, warning_content_matrix, warning_description, warning_headlines, warning_detail_holder):
#     st.title("MetOffice Current Weather Warnings")
#     if data:
#         for info in data:
#             st.write(f"**Level: {info['Level']}**")
#             st.markdown(f"**Date:** {info['Date']}")
#             st.markdown(f"**Regions:** {info['Regions']}")
#             st.markdown(f"**Description:** {info['Description']}")
#             st.markdown("---")
#         # Create a DataFrame from the data
#         df = pd.DataFrame(data)
#         # Allow user to download the data as a CSV file
#         st.subheader("Download Data:")
#         csv_download = st.button("Download CSV")
#         if csv_download:
#             csv_data = df.to_csv(index=False)
#             st.download_button("Download CSV", csv_data, "metoffice_warnings.csv", "text/csv")
#     st.markdown("---")
#     if warning_content_matrix:
#         p_tag = warning_content_matrix.find('p')
#         if p_tag:
#             st.markdown(f"**Warning Impact Matrix:** {p_tag.get_text(strip=True)}")
#     if warning_description:
#         st.markdown(f"**Warning Description:** {warning_description.get_text(strip=True)}")
#     if warning_detail_holder:
#         h4_tag = warning_detail_holder.find('h4')
#         p_tag = warning_detail_holder.find('p')
#         if h4_tag:
#             st.markdown(f"**{h4_tag.get_text(strip=True)}:**")
#         if p_tag:
#             st.markdown(f"{p_tag.get_text(strip=True)}")
# def main():
#     html_content = scrape_website(url)
#     data, warning_content_matrix, warning_description, warning_headlines, warning_detail_holder = parse_html(html_content)
#     display_data(data, warning_content_matrix, warning_description, warning_headlines, warning_detail_holder)
# if __name__ == "__main__":
#     main()





