
import streamlit as st 
import folium
import requests
from streamlit_folium import st_folium
import geopandas as gpd
from folium import plugins
import numpy as np


st.title("Zone Planner")
st.write("Navigating local zoning laws to get community projects done can be challenging, but AI can help.")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""---""")
    st.caption("STEP 1")
    st.write("Project Details")
with col2:
    st.markdown("""---""")
    st.caption("STEP 2")
    st.write("Site Selection")
with col3: 
    st.markdown("""---""")
    st.caption("STEP 3")
    st.write("Site Details")

with st.form("Site Selection"):
    st.subheader("Find your site")

    zoning_map = "https://data.sfgov.org/resource/yamn-gsa8.geojson?$limit=10000000"

    response_zoning = requests.get(zoning_map)
    zoningdata = gpd.read_file(response_zoning.text)

    zoningdata['Zoning'] = np.random.choice(['Zoned', 'Not Zoned'], size=len(zoningdata))

    # Create a Folium map centered on the mean of the geometry
    center = zoningdata.centroid.iloc[0].y, zoningdata.centroid.iloc[0].x
    m = folium.Map(location=center, zoom_start=14,tiles = 'CartoDB positron',attr="CARTODB")

    folium.GeoJson(
    data=zoningdata,
    name='My Layer',
    style_function=lambda x: {'fillColor': 'blue' if x['properties']['zoning_sim'] in ['RM-1','RM-2','RM-3'] else 'orange',
#                              'color': 'black',
                              'fill_opacity': 1,
                              'opacity': 0,
                              'weight': 1}
    ).add_to(m)

    # add a layer control to the map
    folium.LayerControl().add_to(m)

    # Add the drawing tool to the map
    #draw_options = {
    #    'polyline': False,
    #    'polygon': False,
    #    'marker': True,
    #    'circlemarker': False,
    #    'circle': False
    #}
    #draw_tool = plugins.Draw(export=True, draw_options)
    #draw_tool.add_to(m)

    st_folium(m)

    st.form_submit_button("Get Site Details")
