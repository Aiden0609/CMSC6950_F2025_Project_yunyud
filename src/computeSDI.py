import numpy as np
import pandas as pd

def compute_thresholds(df, start, end):
    df_ref = df[df["Year"].between(start, end)]
    quant = df_ref.groupby("doy").agg({
        "Max Temp (°C)": lambda x: np.percentile(x, 90),
        "Min Temp (°C)": lambda x: np.percentile(x, 90),
    })
    quant = quant.rename(columns={
        "Max Temp (°C)": "tmax90",
        "Min Temp (°C)": "tmin90",
    })
    return quant

def mark_extreme(df, quant):
    df = df.copy()
    df["tmax90"] = df["doy"].map(quant["tmax90"])
    df["tmin90"] = df["doy"].map(quant["tmin90"])

    df["hot"] = ((df["Max Temp (°C)"] > df["tmax90"]) &
                 (df["Min Temp (°C)"] > df["tmin90"])).astype(int)
    df["cold"] = ((df["Max Temp (°C)"] < df["tmax90"]) &
                 (df["Min Temp (°C)"] < df["tmin90"])).astype(int)
    return df

def detect_spells(binary_arr):
    spells = []
    start = None
    for i, x in enumerate(binary_arr):
        if x == 1 and start is None:
            start = i
        elif x == 0 and start is not None:
            if i - start >= 3:
                spells.append((start, i - 1))
            start = None

    if start is not None and len(binary_arr) - start >= 3:
        spells.append((start, len(binary_arr) - 1))
    return spells

def compute_wsdi(df):
    years = df["Year"].unique()
    results = {}

    for y in years:
        sub = df[df["Year"] == y].sort_values("doy")
        arr = sub["hot"].tolist()
        spells = detect_spells(arr)
        lengths = [end - start + 1 for start, end in spells]
        results[y] = lengths
    return results


