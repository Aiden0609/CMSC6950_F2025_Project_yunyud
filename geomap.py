# %%
import plotly.express as px
import pandas as pd
from utils import load_many

extreme_var = "Min Temp"
title_var = f"Yearly Extreme {extreme_var}"

dfs = load_many(all=True)

rows = []
for city, df in dfs.items():
    df = df[df["Year"] >= 2003].copy()
    rows.append(df[[
        "Year", "Latitude", "Longitude",
        "Min Temp", "Max Temp", "Date/Time", "doy"
    ]].assign(city=city))

df_all = pd.concat(rows).reset_index(drop=True)

ext_df = df_all.groupby(["city", "Year"]).agg({
    "Latitude": "first",
    "Longitude": "first",
    extreme_var: "min" if extreme_var == "Min Temp" else "max"
}).reset_index()

ext_df["value"] = -ext_df[extreme_var]

fig = px.scatter_geo(
    ext_df,
    lat="Latitude",
    lon="Longitude",
    size="value",
    hover_name="city",
    animation_frame="Year",
    projection="natural earth",
    title=f"{title_var}",
    color_continuous_scale="thermal"
)
fig.update_layout(
    height=600,
    geo=dict(
        showcountries=True,
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue",
        lonaxis=dict(range=[-140, -50]),
        lataxis=dict(range=[35, 75])
    )
)
fig.write_image("./output/geomap.pdf")
fig.show()


# %%
