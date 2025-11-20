import numpy as np
import pandas as pd
from datetime import date


def dateparser(date_str):
    y, m, d = map(int, date_str.split('-'))
    return date(y, m, d).timetuple().tm_yday - 1

def generateRef(df: pd.DataFrame):
    w = [[] for _ in range(366)]
    c = [[] for _ in range(366)]
    df = df[(df["Year"] >= 1994) & (df["Year"] <= 2023)]
    for index, row in df.iterrows():
        i = dateparser(row["Date/Time"])
        w[i].append(row["Max Temp (°C)"])
        c[i].append(row["Min Temp (°C)"])
    return w, c

def getThreshold(data: list) -> float:
    w, c = [], []
    for i in range(len(data)):
        w.append(np.percentile(data[i], 90))
        c.append(np.percentile(data[i], 10))
    return w, c
