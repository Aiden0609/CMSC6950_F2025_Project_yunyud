#%%
import glob
import os
from typing import List

import pandas as pd


def aggregateCSV(path) -> pd.DataFrame:
    '''Aggregate raw csv files of a city
    Raw csv files can be found in ../data/raw/${Name of city}$
    Return one concatenated file of a city
    '''
    
    files: List[str] = sorted(glob.glob(path))
    if not files:
        raise FileNotFoundError(f"No matching files found in: {path}")

    dfs = [pd.read_csv(file) for file in files]
    all_df = pd.concat(dfs, ignore_index=True).drop_duplicates()

    return all_df


def preprocessing(city, base="../data/raw") -> pd.DataFrame:

    path = os.path.join(base, f"{city}/{city}*.csv")
    df = aggregateCSV(path)
    
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
    CITIES = ["StJohns", "Montreal", "Calgary", "TorontoCity", "Vancouver"]
    for city in CITIES:
        df = preprocessing(city, base="../data/raw")
        output_path = f"../data/processed/{city}.csv"
        df.to_csv(output_path, index=False)
        print(f"File saved as {output_path}")

# %%
