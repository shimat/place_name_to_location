import pandas as pd
import requests
import streamlit as st
from time import sleep
from typing import Any

YAHOO_APPLICATION_ID = st.secrets.yahoo_credentials.application_id
YAHOO_API_URL = "https://map.yahooapis.jp/search/local/V1/localSearch" 


@st.experimental_memo
def retrieve_local_search_result(area_name: str, latlon: tuple[int, int], dist: int) -> dict[Any]:
    json = _request_yahoo_local_search(area_name, latlon, dist)
    return _to_dataframe(json, area_name)


def _request_yahoo_local_search(query: str, latlon: tuple[int, int], dist: int) -> dict[Any]:
    params = {
        "appid": YAHOO_APPLICATION_ID,
        "output": "json",
        "query": query,
        "lat": latlon[0],
        "lon": latlon[1],
        "dist": dist,
        "detail": "standard",
        "results": 100,
        "start": 1}
    print(f"requesting start ({query})")
    r = requests.get(YAHOO_API_URL, params=params)
    r.raise_for_status()

    j: dict[Any] = r.json()
    total: int = min(j["ResultInfo"]["Total"], 3000)
    while len(j["Feature"]) < total:
        sleep(0.5)
        params["start"] += 100
        print(f"requesting { params['start'] }...")
        r = requests.get(YAHOO_API_URL, params=params)
        r.raise_for_status()
        j["Feature"].extend(r.json()["Feature"])
    print("request done")
    return j


def _to_dataframe(search_result: dict[Any], area_name: str) -> pd.DataFrame:
    rows = []
    for f in search_result["Feature"]:
        address = f["Property"]["Address"].removeprefix("北海道")
        is_in = 1 if area_name in address else 0
        lon, lat = f["Geometry"]["Coordinates"].split(",")
        rows.append({
            "name": f["Name"],
            "address": address,
            "lat": float(lat),
            "lon": float(lon),
            "is_in": is_in
        })
    return pd.DataFrame.from_dict(rows)
