import numpy as np
import pandas as pd
import openrouteservice as ors

import time

client = ors.Client(key="5b3ce3597851110001cf6248533db39fd6ad470ca6e5197de9bd44de")


def loading_data() -> pd.DataFrame:
    df = pd.read_excel("information_about_schools.xlsx")
    return df


def preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    df = df[["name", "adress", "rayon", "X", "Y", "global_id"]]
    df["X"] = df["X"].str.replace(",", ".").astype(float)
    df["Y"] = df["Y"].str.replace(",", ".").astype(float)

    df.rename(columns={"X": "longitude", "Y": "latitude"}, inplace=True)

    return df


def get_osr_info(df: pd.DataFrame) -> list:
    polygons_list = []
    try:
        for i in range(0, len(df), 5):
            coordinates = df[["longitude", "latitude"]].values[i : i + 5].tolist()

            iso = client.isochrones(
                locations=coordinates,
                profile="foot-walking",
                range=[600],
                validate=False,
                attributes=["total_pop", "area", "reachfactor"],
            )
            time.sleep(5)

            polygons_list += iso["features"]
    except:
        print(
            f"parsing OSR caused error and stopped. {len(polygons_list)}/{len(df)} obects were received"
        )

    return polygons_list


df_school_location = loading_data()
df_school_location = preprocessing(df_school_location)

polygons_list = get_osr_info(df_school_location)

with open("polygons.npy", "wb") as f:
    np.save(f, polygons_list)