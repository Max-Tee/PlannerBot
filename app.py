import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point
import pydeck as pdk


# Initialize connection.
conn = st.experimental_connection('snowflake', type='sql')
df = conn.query("SELECT * FROM PUBLIC.PROPERTY_ATTRIBUTES_ASSESSMENT_USA_SAMPLE WHERE ZIPCODE = '94112' AND PROP_ZONING = 'RH1' limit 10;", ttl=600)



#get vacant count
vacant_count = df["vacant"].value_counts().get("Y", 0)
total_count = len(df)
vacant_percent = vacant_count/total_count*100
median_value = df['assed_landval'].median()


col1, col2 = st.columns(2)


with col1:
    st.metric("Total Count of Eligible Parcels", total_count)
    st.metric("Percent Vacant", vacant_percent)
    st.metric("Median Value", median_value)
with col2: 
    st.write("Test")    
    #st.bar(bar_chart of prop_lu_desc)
    #st.bar(bldg_yrbld)

st.table(df)


# create a Point geometry column from the latitude and longitude columns
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]

st.table(geometry)

# create a geopandas dataframe with the geometry and other columns
gdf = gpd.GeoDataFrame(df, geometry=geometry)


st.table(gdf)

# create a Folium map centered on the data
m = folium.Map(location=[gdf.geometry.y.mean(), gdf.geometry.x.mean()], zoom_start=16, tiles = 'CartoDB positron',attr="CARTODB")


for index, row in gdf.iterrows():
    color = 'blue' if row['prop_zoning'] == 'RH1' else 'orange'
    folium.CircleMarker(location=[row.geometry.lon, row.geometry.lat], radius=2, fill_color=color, color=color).add_to(m)


st.folium(m)

