import numpy as np
import pandas as pd

def compute_extreme(df):

    df_ref = df[df["Year"].between(1994, 2023)]

    tmax = [[] for _ in range(366)]
    tmin = [[] for _ in range(366)]

    for _, row in df_ref.iterrows():
        i = row["doy"]
        tmax[i].append(row["Max Temp (°C)"])
        tmin[i].append(row["Min Temp (°C)"])

    return tmax, tmin

def compute_thresholds(tmax, tmin):
    w = []
    c = []

    for d in range(366):
        # 5 day window indices
        win = [(d + i) % 366 for i in (-2, -1, 0, 1, 2)]

        tmax_window = []
        tmin_window = []

        for idx in win:
            tmax_window.extend(tmax[idx])
            tmin_window.extend(tmin[idx])

        w.append(np.percentile(tmax_window, 90) if tmax_window else np.nan)
        c.append(np.percentile(tmin_window, 10) if tmin_window else np.nan)

    return w, c

def compute_spell_index(condition):
    """
    condition: Boolean array, True where extreme event occurs.
    Returns total length of all spells ≥6 days.
    """
    count = 0
    current = 0

    for v in condition:
        if v:
            current += 1
        else:
            if current >= 6:
                count += current
            current = 0

    if current >= 6:
        count += current

    return count

def compute_SDI(df):
    df = df.copy()
    df["Date/Time"] = pd.to_datetime(df["Date/Time"])
    df["doy"] = df["Date/Time"].dt.dayofyear - 1

    tmax, tmin = compute_extreme(df)

    w, c = compute_thresholds(tmax, tmin)

    results = []

    for year, dfg in df.groupby("Year"):
        dfg = dfg.sort_values("doy")

        warm = dfg["Max Temp (°C)"].values > np.array([w[d] for d in dfg["doy"]])
        cold = dfg["Min Temp (°C)"].values < np.array([c[d] for d in dfg["doy"]])

        WSDI = compute_spell_index(warm)
        CSDI = compute_spell_index(cold)

        results.append({"Year": year, "WSDI": WSDI, "CSDI": CSDI})

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = pd.read_csv("./data/processed/StJohns.csv")

    results = compute_SDI(df)

    print(results)
