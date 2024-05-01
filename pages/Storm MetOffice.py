
# import streamlit as st
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import pandas as pd
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
#         columns = row.find_elements(By.TAG_NAME, 'td')
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
#         url_previous = f'https://www.metoffice.gov.uk/weather/warnings-and-advice/uk-storm-season-{previous_season}'
#         table_xpath_previous = '//*[@id="content"]/div[3]/div[2]/div[1]/article/div/div[2]/div[1]/div/div[1]/div[1]/table/tbody' 
#         df_data_previous = get_storm_data(url_previous, table_xpath_previous)
#         st.subheader(f"{previous_season} Storm Season Data")
#         st.table(df_data_previous)
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
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import pandas as pd



# page_bg_img = """
# <style>
# [data-testid="stAppViewContainer"] {
# background-color: #4158D0;
# background-image: linear-gradient(315deg, #4f2991 3%, #7dc4ff 38%, #36cfcc 68%, #a92ed3 98%);
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
#         url_previous = f'https://www.metoffice.gov.uk/weather/warnings-and-advice/uk-storm-season-{previous_season}'
#         table_xpath_previous = '//*[@id="content"]/div[3]/div[2]/div[1]/article/div/div[2]/div[1]/div/div[1]/div[1]/table/tbody'
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
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
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
def get_storm_data(url, table_xpath):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    # Use webdriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.maximize_window()
    # Find the table element
    try:
        table_element = driver.find_element(By.XPATH, table_xpath)
    except:
        st.warning("No data found.")
        driver.quit()
        return pd.DataFrame()
    # Find rows within the table
    rows = table_element.find_elements(By.XPATH, './/tbody/tr')
    # Extract data from rows
    storm_result = []
    for row in rows:
        columns = row.find_elements(By.XPATH, 'td')
        temporary_data = {
            'Name': columns[0].text,
            'Date named': columns[1].text,
            'Date of impact': columns[2].text,
        }
        storm_result.append(temporary_data)
    df_data = pd.DataFrame(storm_result)
    driver.quit()  # Close the webdriver
    return df_data
def main():
    st.title("Met Office Storm Centre Data")
    # User input for storm season
    storm_season_latest = st.checkbox("Show Latest Storm Season", value=True)
    storm_season_previous = st.checkbox("Show Previous Storm Season", value=False)
    if not storm_season_latest and not storm_season_previous:
        st.warning("Please select at least one option.")
    if storm_season_latest:
        url_latest = 'https://www.metoffice.gov.uk/weather/warnings-and-advice/uk-storm-centre/index'
        table_xpath_latest = '//*[@id="content"]/div[3]/div[2]/div[1]/article/div/div[2]/div[1]/div/div[1]/div[2]/table'
        df_data_latest = get_storm_data(url_latest, table_xpath_latest)
        st.subheader("Latest Storm Season Data")
        st.table(df_data_latest)
    if storm_season_previous:
        previous_season = st.selectbox("Select Previous Storm Season", ['2022-23', '2021-22', '2020-21', '2019-20'])
        url_previous = f'https://www.metoffice.gov.uk/weather/warnings-and-advice/uk-storm-centre/uk-storm-season-{previous_season}'
        table_xpath_previous = '//*[@id="content"]/div[3]/div[2]/div[1]/article/div/div[2]/div[1]/div/div[1]/div[1]/table'
        df_data_previous = get_storm_data(url_previous, table_xpath_previous)
        if not df_data_previous.empty:
            st.subheader(f"{previous_season} Storm Season Data")
            st.table(df_data_previous)
        else:
            st.warning(f"No data found for the {previous_season} storm season.")
    # Option to download as CSV
    if st.button("Download CSV"):
        if not df_data_latest.empty:
            csv_export_latest = df_data_latest.to_csv(index=False)
            st.download_button("Download Latest Storm Season CSV", csv_export_latest, file_name="met_office_storm_data_latest.csv", key="csv_download_latest")
        if not df_data_previous.empty:
            csv_export_previous = df_data_previous.to_csv(index=False)
            st.download_button("Download Previous Storm Season CSV", csv_export_previous, file_name=f"met_office_storm_data_{previous_season}.csv", key="csv_download_previous")
if __name__ == "__main__":
    main()