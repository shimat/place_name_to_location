import folium
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from typing import Any
from data_loader import retrieve_local_search_result
from constants import ContourData, CENTER_POSITIONS, CONTOURS, SEARCH_DISTANCE, ZOOM


def add_spot_markers(df: pd.DataFrame, map: folium.Map):
    for _, r in df.iterrows():
        folium.Marker(
            location=(r["lat"], r["lon"]),
            tooltip=f"{r['name']}<br/>{r['address']}",
            draggable=False
        ).add_to(map)


def add_contour_lines(contours: ContourData, map: folium.Map):
    colormap = ['r', "b", "g", "orange"]
    for contour in contours.coordinates_list:
        if not contour:
            continue
        folium.ColorLine(
            positions=contour,
            colors=tuple(0 for _ in contour),
            colormap=colormap,
            weight=7
        ).add_to(map)
        colormap.append(colormap.pop(0))


st.set_page_config(layout="wide")
st.title("Local search plot")
st.write("""
<style>
iframe { width: 100%; height: 800px; }
</style>
""", unsafe_allow_html=True)

area_names = (("宮の森", "円山", "琴似", "北大", "田園調布", "吉祥寺", "軽井沢"))
tabs = st.tabs(area_names)

for i, area_name in enumerate(area_names):
    with tabs[i]:
        df = retrieve_local_search_result(
            area_name,
            latlon=CENTER_POSITIONS[area_name],
            dist=SEARCH_DISTANCE[area_name])
        df = df.query("is_in == 0")

        map = folium.Map(location=CENTER_POSITIONS[area_name], zoom_start=ZOOM[area_name], crs="EPSG3857")
        contour_data = CONTOURS[area_name]
        add_spot_markers(df, map)
        add_contour_lines(contour_data, map)
        st.header(area_name)
        st.text(contour_data.description)
        folium_static(map)
        st.dataframe(df, use_container_width=True)
