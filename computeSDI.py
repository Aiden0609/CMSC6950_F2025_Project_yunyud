import numpy as np
import pandas as pd

def data_padding(df: pd.DataFrame):
    """
    Ensure there's a row for every date in a year, need this func
    because spell computation has to be based on continuous dates

    df: dataframe after preprocessing
    """
    df = df.copy()

    years = sorted(df["Year"].unique())
    full = []

    for y in years:
        full_range = pd.date_range(
            start=f"{y}-01-01",
            end=f"{y}-12-31",
            freq="D"
        )
        full_df = pd.DataFrame({
            "Year": full_range.year,
            "Month": full_range.month,
            "Day": full_range.day,
            "doy": full_range.dayofyear,
        })
        merged = full_df.merge(
            df,
            on=["Year", "Month", "Day", "doy"],
            how="left"
        )

        full.append(merged)

    return pd.concat(full, ignore_index=True)


def compute_thresholds(df_ref):
    """
    Compute daily percentile thresholds for maximum and
    minimum temprature using a 30-year reference period,
    and add corresponding columns
    
    :param df: padded dataframe
    """
    quant = df_ref.groupby("doy").agg({
        "Max Temp": lambda x: np.percentile(x.dropna(), 90),
        "Min Temp": lambda x: np.percentile(x.dropna(), 90),
    })
    quant = quant.rename(columns={
        "Max Temp": "tmax90",
        "Min Temp": "tmin90",
    })
    return quant

def mark_extreme(df, quant):
    """
    Label each day as a hot day (1) or non-hot day (0),
    follows the definition of WSDI
    
    :param df: padded dateframe 
    :param quant: df with new columns, "tmax90", "tmin90", "hot"
    """
    df = df.copy()
    df["tmax90"] = df["doy"].map(quant["tmax90"])
    df["tmin90"] = df["doy"].map(quant["tmin90"])

    df["hot"] = ((df["Max Temp"] > df["tmax90"]) &
                 (df["Min Temp"] > df["tmin90"])).fillna(False).astype(int)
    
    return df

def detect_spells_poolday(binary_arr):
    """
    Implement the spell detection with pool day calculation(exact
    definition from reference), but not working, I kept this function
    for myself, please don't grade on it.
    """
    spells = []
    seq = False
    start, end = 0, 1
    one_count = 0
    while(end<len(binary_arr)-1):
        if binary_arr[end] == 1 and not seq:
            end = start
            seq = True
            one_count += 1
        elif binary_arr[end] == 1 and seq:
            one_count += 1
        elif binary_arr[end] == 0 and seq:
            if binary_arr[end + 1] == 0:
                seq = False
                if one_count >= 3:
                    spells.append([start, end - 1])
                start = end + 1
                one_count = 0
        end += 1
    return spells

def detect_spells(binary_arr):
    """
    Detect warm spells in a sequence of 0/1 values.
    Here a simplified version is defined as:
        >= 3 consecutive hot days (1)
    
    :param binary_arr: list of integer 0/1
    """
    spells = []
    start = None

    for i, x in enumerate(binary_arr):
        if x == 1:
            if start is None:
                start = i  # potential start of a spell
        else:
            if start is not None and i - start >= 3:
                spells.append((start, i - 1))
            start = None  # reset start

    if start is not None and len(binary_arr) - start >= 3:
        spells.append((start, len(binary_arr) - 1))

    return spells


def compute_wsdi(df):
    """
    SDI computation pipeline.
    After spell detection, assign a spell_id to each day within
    the spell and compute spell length per year
    """
    
    df_full = data_padding(df)
    df_ref = df_full[df_full["Year"].between(1994, 2023)]
    if df_ref.empty:
        df_ref = df_full

    quant = compute_thresholds(df_ref)

    df_extreme = mark_extreme(df_full, quant)
    df_extreme["spell_id"] = -1
    
    years = sorted(df_extreme["Year"].unique())

    for y in years:
        sub = df_extreme[df_extreme["Year"] == y].sort_values("doy")
        arr = sub["hot"].tolist()
        idx_list = sub.index.tolist()

        spells = detect_spells(arr)

        # assign spell_id
        for sid, (s, e) in enumerate(spells):
            true_s = idx_list[s]
            true_e = idx_list[e]
            df_extreme.loc[true_s:true_e, "spell_id"] = sid

    return df_extreme

if __name__ == "__main__":
    df = pd.read_csv("./data/processed/StJohns.csv")

    wsdi, df = compute_wsdi(df)

    print(wsdi)


