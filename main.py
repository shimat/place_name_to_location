import folium
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from typing import Any
from data_loader import retrieve_local_search_result, to_dataframe


def area_marker(df: pd.DataFrame, map: folium.Map):

    folium.ColorLine(
        positions=((43.063786, 141.3013249), (43.0636449, 141.309629)),
        colors=(1, 1)
    ).add_to(map)

    for index, r in df.iterrows(): 
        folium.Marker(
            location=(r.lat, r.lon),
            popup=index,
        ).add_to(map)

st.set_page_config(layout="wide")
st.title("Hoge")
st.write("""
<style>
iframe { width: 1000px; height: 800px; }
</style>
""", unsafe_allow_html=True)

search_result = retrieve_local_search_result("宮の森")
df = to_dataframe(search_result)
st.dataframe(df, use_container_width=True)


sales_office = pd.DataFrame(
    data=[[43.057035277778,141.292136944444,],
          [43.048927777778,141.291418055556]],
    index=["本社","A営業所",],
    columns=("lat", "lon")
)
st.dataframe(sales_office)
map = folium.Map(location=(43.0626055, 141.3033632), zoom_start=15, crs="EPSG3857")
area_marker(sales_office, map)


# 地図の基準として兵庫県明石市を設定
japan_location = [35, 135]
map2 = folium.Map(location=japan_location, zoom_start=5)
# geojson読み込み
map2.choropleth(geo_data='japan.geojson')

folium_static(map2)