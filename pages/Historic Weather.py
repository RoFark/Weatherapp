import streamlit as st
import pandas as pd
from datetime import datetime
from io import StringIO
import requests
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
def read_met_office_data():
    url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/heathrowdata.txt"
    try:
        # Fetch data from the URL using requests
        response = requests.get(url)
        response.raise_for_status()
        # Use StringIO to convert the content to a file-like object
        content = StringIO(response.text)
        # Read the lines from the file-like object
        lines = content.readlines()
    except (requests.RequestException, pd.errors.EmptyDataError):
        st.warning("No data found in the provided URL.")
        return None
    # Filter data based on year and month
    filtered_lines = []
    for line in lines[8:]:  # Start from the 9th line
        fields = line.split()
        if len(fields) == 7:
            filtered_lines.append(fields[:7])
    if not filtered_lines:
        st.warning("No data found.")
        return None
    # Create DataFrame from the filtered lines
    df = pd.DataFrame(filtered_lines, columns=['yyyy', 'mm', 'tmax', 'tmin', 'af', 'rain', 'sun'])
    return df
def main():
    st.title("Met Office Data Viewer")
    # Read Met Office data
    met_office_data = read_met_office_data()
    # Display the data
    if met_office_data is not None:
        st.subheader("Met Office Data")
        # Create filters
        year_filter = st.sidebar.selectbox("Filter by Year", ["All"] + sorted(met_office_data['yyyy'].unique().tolist()))
        month_filter = st.sidebar.selectbox("Filter by Month", ["All"] + sorted(met_office_data['mm'].unique().tolist()))
        # Apply filters
        filtered_data = met_office_data.copy()
        if year_filter != "All":
            filtered_data = filtered_data[filtered_data['yyyy'] == year_filter]
        if month_filter != "All":
            filtered_data = filtered_data[filtered_data['mm'] == month_filter]
        # Display filtered data with larger table
        st.dataframe(filtered_data, height=800)
if __name__ == "__main__":
    main()