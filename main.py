import folium
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from typing import Any
from data_loader import retrieve_local_search_result, to_dataframe
from constants import CENTER_POSITIONS, CONTOURS, SEARCH_DISTANCE, ZOOM

def add_spot_markers(df: pd.DataFrame, map: folium.Map):
    for _, r in df.iterrows():
        folium.Marker(
            location=(r["lat"], r["lon"]),
            tooltip=f"{r['name']}<br/>{r['address']}",
            draggable=False
        ).add_to(map)

def add_contour_lines(contour, map: folium.Map):
    folium.ColorLine(
        positions=contour,
        colors=tuple(0 for _ in contour),
        colormap=['r', "g", "b"],
        weight=4
    ).add_to(map)

st.set_page_config(layout="wide")
st.title("Local search plot")
st.write("""
<style>
iframe { width: 1000px; height: 800px; }
</style>
""", unsafe_allow_html=True)

area_names = (("宮の森", "円山"))
tabs = st.tabs(area_names)

for i, area_name in enumerate(area_names):
    with tabs[i]:
        search_result = retrieve_local_search_result(
            area_name,
            latlon=CENTER_POSITIONS[area_name],
            dist=SEARCH_DISTANCE[area_name])
        df = to_dataframe(search_result).query("is_in == 0")

        map = folium.Map(location=CENTER_POSITIONS[area_name], zoom_start=ZOOM[area_name], crs="EPSG3857")
        add_spot_markers(df, map)
        add_contour_lines(CONTOURS[area_name], map)
        folium_static(map)
        st.dataframe(df, use_container_width=True)
