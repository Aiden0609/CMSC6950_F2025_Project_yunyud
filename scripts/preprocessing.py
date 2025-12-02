#%%
import glob
import os
import re
from typing import List

import pandas as pd

def clean_units(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove units like (°C), (mm), (kPa) from column names.
    Example: "Max Temp (°C)" -> "Max Temp"
    """
    new_cols = {}
    pattern = r"\s*\(.*?\)"    # "(...)" including spaces

    for col in df.columns:
        clean = re.sub(pattern, "", col).strip()
        new_cols[col] = clean

    return df.rename(columns=new_cols)

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
    df = clean_units(df)

    numeric_cols = [
        "Max Temp",
        "Min Temp",
        "Mean Temp",
        "Total Precip",
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
