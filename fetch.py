import csv
import json
import os
import requests
from pathlib import Path
from typing import Any

YAHOO_APPLICATION_ID = os.environ["YAHOO_APPLICATION_ID"]
YAHOO_SECRET = os.environ["YAHOO_SECRET"]
YAHOO_API_URL = "https://map.yahooapis.jp/search/local/V1/localSearch" 


def request_all():
    params = {
        "appid": YAHOO_APPLICATION_ID,
        "output": "json",
        "query": '宮の森',
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
        params["start"] += 100
        print(f"requesting { params['start'] }...")
        r = requests.get(YAHOO_API_URL, params=params)
        r.raise_for_status()
        j["Feature"].extend(r.json()["Feature"])
    return j        

#print(response.json())

"""
data = request_all()
Path("data.json").write_text(
    json.dumps(data, indent=2, ensure_ascii=False), 
    encoding="UTF-8-sig")
"""
data: dict[Any] = json.loads(Path("data.json").read_text(encoding="UTF-8-sig"))

with open("address.csv", mode="w", encoding="UTF-8-sig", newline="") as io:
    writer = csv.writer(io, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC,)
    writer.writerow(("name", "address", "is_in"))
    for f in data["Feature"]:
        address = f['Property']['Address']
        writer.writerow((f['Name'], address, 1 if "宮の森" in address else 0))