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

    #get parcels 
    url_parcel = "https://data.sfgov.org/resource/9grn-xjpx.geojson?$limit=1000000"
    response_parcel_neighborhood = requests.get(url_parcel)
    parcel_neighborhood = gpd.read_file(response_parcel_neighborhood.text)
    parcel_neighborhood['Centroid'] = parcel_neighborhood.centroid
    parcel_neighborhood = parcel_neighborhood.drop('geometry', axis=1)

    #zoning
    zoning_map = "https://data.sfgov.org/resource/yamn-gsa8.geojson?$limit=10000000"
    response_zoning = requests.get(zoning_map)
    zoningdata = gpd.read_file(response_zoning.text)

    #merge the datasets together
    parcel_neighborhood = parcel_neighborhood.set_geometry('Centroid')
    merged = gpd.sjoin(parcel_neighborhood, zoningdata, how='inner', op='intersects')

    # create a Folium map centered on the data
    m = folium.Map(location=[merged.geometry.y.mean(), merged.geometry.x.mean()], zoom_start=16, tiles = 'CartoDB positron',attr="CARTODB")

    # create a GeoJSON layer for the data
    #geojson = folium.GeoJson(parcel_neighborhood_filt)

    for index, row in merged.iterrows():
        color = 'blue' if row['zoning_sim'] == 'RM-4' else 'orange'
        folium.CircleMarker(location=[row.Centroid.y, row.Centroid.x], radius=1, fill_color=color, color=color).add_to(m)

    st_folium(m)

    st.form_submit_button("Get Site Details")
