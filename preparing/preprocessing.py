import pandas as pd
import geopandas as gpd

adm_data = pd.read_csv("admzone_msc_school_year.csv", index_col=0)

df_500 = pd.read_csv("fishnet2021.csv", index_col=0)

df_500 = df_500.set_index("cell_zid")

df_500_quantity = pd.read_csv("01_CLocation_July.csv", index_col=0)

df_500_quantity_coords = df_500_quantity.merge(
    df_500, how="left", left_index=True, right_index=True
)

df_500m_coords = df_500_quantity_coords[["customers_cnt_home", "coords"]]

adm_data = adm_data.dropna(subset=["coords"])
adm_data.to_csv("adm_data_child_share.csv")

## Second file
data = gpd.read_file("data/admzones2021/admzones2021.shp")

adm_data = pd.read_csv("adm_data_child_share.csv", index_col=0)

adm_data_school_year = adm_data.merge(
    data[["adm_name", "geometry"]], how="left", left_on="adm_name", right_on="adm_name"
).drop("coords", axis=1)

data = gpd.read_file("data/fishnet2021/fishnet2021.shp")

df_500m_coords.reset_index(level=0, inplace=True)

df_500_quantity = df_500m_coords.merge(
    data, how="left", left_on="zid", right_on="cell_zid"
).drop(["coords", "cell_zid"], axis=1)

dicti = pd.read_excel("Справочник.xlsx")

df_500_quantity_adm = df_500_quantity.merge(
    dicti[["cell_zid", "adm_zid"]], how="left", left_on="zid", right_on="cell_zid"
)

df_final = df_500_quantity_adm.merge(
    adm_data_school_year, how="left", left_on="adm_zid", right_on="adm_zid"
).drop("cell_zid", axis=1)

df_final.to_csv("500_with_adm.csv")
