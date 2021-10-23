import pandas as pd
import requests

from utils import get_lat_lon, get_lat_lon_extended


URL = "https://api.cian.ru/newbuilding-search/v1/get-newbuildings-for-serp/"
body = {
    "count": 25,
    "jsonQuery": {
        "region": {"type": "terms", "value": [1, 4593]},
        "status": {"type": "terms", "value": ["underConstruction"]},
    },
    "offset": 0,
    "subdomain": "www",
    "uri": "https://www.cian.ru/novostroyki-stroyashiesya/",
    "userCanUseHiddenBase": False,
}

# get count of new buildings
req = requests.post(URL, json=body)
count_zhks = req.json()["total"]

zhks = pd.DataFrame(
    columns=[
        "name",
        "displayName",
        "Sdacha",
        "location",
        "latitude",
        "longitude",
        "url",
    ]
)
for i in range(0, count_zhks, 25):
    body["offset"] = i
    req = requests.post(URL, json=body)

    for building in req.json()["newbuildings"]:
        id_ = building.get("id")

        zhks.loc[id_, "name"] = building.get("name")
        zhks.loc[id_, "displayName"] = building.get("displayName")
        zhks.loc[id_, "Sdacha"] = building.get("specialStatusDisplay")
        zhks.loc[id_, "location"] = building.get("addressLine", [{"title": None}])[0][
            "title"
        ]

        url = building.get("url")
        zhks.loc[id_, "url"] = url
        lat, lon = get_lat_lon(url)
        zhks.loc[id_, "latitude"] = lat
        zhks.loc[id_, "longitude"] = lon

# get skipped coords that we cannot parse easily from api
skipped_coords = [
    (id_, get_lat_lon_extended(url))
    for id_, url in zhks[zhks.isna().latitude].url.iteritems()
]

for id_, coords in skipped_coords:
    zhks.loc[id_, "latitude"] = coords[0]
    zhks.loc[id_, "longitude"] = coords[1]

zhks.index.name = "ID"
zhks.to_csv("zhks_cian.csv")