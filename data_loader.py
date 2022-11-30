import numpy as np
import pandas as pd
import requests
import streamlit as st
from time import sleep
from typing import Any

YAHOO_APPLICATION_ID = st.secrets.yahoo_credentials.application_id
YAHOO_API_URL = "https://map.yahooapis.jp/search/local/V1/localSearch" 


@st.experimental_memo
def retrieve_local_search_result(query: str) -> dict[Any]:
    params = {
        "appid": YAHOO_APPLICATION_ID,
        "output": "json",
        "query": query,
        "lat": 43.0632374,
        "lon": 141.2989056,
        "dist": 4,
        "detail": "standard",
        "results": 100,
        "start": 1}
    print("requesting 1...")
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
    return j


def to_dataframe(search_result: dict[Any]) -> pd.DataFrame:
    data = []
    for f in search_result["Feature"]:
        address = f['Property']['Address']
        data.append([f['Name'], address, 1 if "宮の森" in address else 0])
    return pd.DataFrame(
        data=np.array(data),
        columns=("name", "address", "is_in")
    )
