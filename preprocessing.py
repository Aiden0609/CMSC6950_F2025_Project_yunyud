import glob
import os
from typing import List

import pandas as pd


def aggregateCSV(path = "./data/csv", stationId = 6720):
    
    pattern = os.path.join(path, f"station_{stationId}_daily_*.csv")
    files: List[str] = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No matching files found for pattern: {pattern}")

    dfs = [pd.read_csv(file) for file in files]
    all_df = pd.concat(dfs, ignore_index=True).drop_duplicates()

    output_path = os.path.join(path, f"station_{stationId}_daily_combined.csv")
    all_df.to_csv(output_path, index=False)
    print(f"Output path: {output_path}")
    return all_df


def preprocessingDf(path = "./data/csv", stationId = 6720):
    
    combined_path = os.path.join(path, f"station_{stationId}_daily_combined.csv")
    if not os.path.exists(combined_path):
        df = aggregateCSV(path=path, stationId=stationId)
    else:
        df = pd.read_csv(combined_path)

    numeric_cols = [
        "Max Temp (°C)",
        "Min Temp (°C)",
        "Mean Temp (°C)",
        "Total Precip (mm)",
    ]
    temporal_cols = ["Year", "Month", "Day"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    df[temporal_cols] = df[temporal_cols].apply(pd.to_numeric)
    df["Date/Time"] = pd.to_datetime(df["Date/Time"])

    df = df.dropna(subset=numeric_cols + temporal_cols + ["Date/Time"]).copy()
    df[temporal_cols] = df[temporal_cols].astype(int)
    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":
    preprocessingDf()
