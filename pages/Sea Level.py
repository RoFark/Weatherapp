# """
# This is a Streamlit web app for visualizing areas impacted by rising sea level.
# """

# import streamlit as st
# import geemap.foliumap as geemap
# import ee
# from streamlit_folium import folium_static
# """Contains functions for creating interactive plots of sea level rise data."""

# import plotly.graph_objs as go
# import pandas as pd


# def create_sea_level_interactive_plot():
#     """
#     Creates an interactive plot of sea level rise data using Plotly.

#     Parameters:
#     - data: A pandas DataFrame with columns 'year_fraction', 'GMSL', and 'GMSL_smoothed'.
#     """

#     data = pd.read_csv('/Users/rosie.farkash/Desktop/Streamlit FE/sea_level_data.csv')

#     # Create the scatter plot for GMSL Variation
#     gmsl_variation = go.Scatter(
#         x=data['year_fraction'],
#         y=data['GMSL'],
#         mode='lines',
#         name='GMSL Variation',
#         # fill='tozeroy',  # Fill to the x-axis
#         # Light blue fill with transparency
#         fillcolor='rgba(135, 206, 250, 0.1)',
#     )

#     # Create the scatter plot for Smoothed GMSL
#     smoothed_gmsl = go.Scatter(
#         x=data['year_fraction'],
#         y=data['GMSL_smoothed'],
#         mode='lines',
#         name='Smoothed GMSL',
#         line=dict(color='white', width=2)  # Black line with thickness of 2
#     )

#     # Highlight the last point with a red dot
#     last_point = data.iloc[-1]
#     red_dot = go.Scatter(
#         x=[last_point['year_fraction']],
#         y=[last_point['GMSL_smoothed']],
#         mode='markers',
#         marker=dict(color='red', size=10),  # Red dot with size 10
#         name='2023 Level',
#         showlegend=False
#     )

#     # Combine the plots
#     data_plots = [gmsl_variation, smoothed_gmsl, red_dot]

#     # Define the layout of the plot
#     layout = go.Layout(
#         template="plotly_dark",
#         title={'text': 'Sea Level Rise Over Time',
#                'x': 0.5, 'xanchor': 'center'},
#         xaxis=dict(title='Year'),
#         yaxis=dict(title='GMSL Variation (mm)'),
#         # Position the legend in the upper left corner
#         legend=dict(x=0.05, y=0.95),
#         margin=dict(l=50, r=50, t=50, b=50),  # Set plot margins
#         hovermode='closest',  # Show closest data point on hover
#     )

#     # Create the figure with data and layout
#     fig = go.Figure(data=data_plots, layout=layout)

#     return fig




# # st.set_page_config(page_title="Rising Sea Level", page_icon="🌏")

# st.write("# Rising Sea Level impact (2050) on lands in red")

# ee.Initialize(ee.ServiceAccountCredentials(
#     st.secrets.gee_service_account,
#     key_data=st.secrets.gee_service_account_credentials))

# rise = st.slider("sea level rise (m)", 0.2, 5., value=0.3)

# # create map centered on maldives capital with street level zoom
# m = geemap.Map(center=(22.30, 114.1694), zoom=14, basemap="HYBRID")
# dem = ee.Image("NASA/NASADEM_HGT/001")
# impacted_land = dem.expression(
#     f"(elevation < {rise}) && (swb == 0)",
#     {'elevation': dem.select('elevation'),
#      'swb': dem.select('swb')})
# viz_params = {'min': 0, 'max': 1, 'palette': ['000000', 'FF0000'],
#               'opacity': 0.4}

# m.addLayer(impacted_land, viz_params, 'impacted areas')
# m.addLayerControl()

# # render folium map
# folium_static(m)


# st.plotly_chart(create_sea_level_interactive_plot(), use_container_width=True)

# st.write(
#     "#### Sea level data retrieved from [Global mean sea level](https://sealevel.nasa.gov/understanding-sea-level/key-indicators/global-mean-sea-level)")
# st.write(
#     "#### For more accurate sea level rise projections, visit [NASA Sea Level Projection Tool](https://sealevel.nasa.gov/ipcc-ar6-sea-level-projection-tool)")