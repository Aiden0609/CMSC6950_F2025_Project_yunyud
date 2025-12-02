import pandas as pd

CITY_CSV = {
    "StJohns": "./data/processed/StJohns.csv",
    "Montreal": "./data/processed/Montreal.csv",
    "Calgary": "./data/processed/Calgary.csv",
    "Vancouver": "./data/processed/Vancouver.csv",
    "Toronto": "./data/processed/TorontoCity.csv",
}


def load_single(city: str) -> pd.DataFrame:
    """Load preprocessed climate data of one single city."""
    if city not in CITY_CSV:
        raise ValueError(f"Unknown city: {city}, please use one of the 5"
                         f"city names: {CITY_CSV.keys()}")

    df = pd.read_csv(CITY_CSV[city])
    df["Date"] = pd.to_datetime(df["Date/Time"])
    df["doy"] = df["Date"].dt.dayofyear
    return df


def load_many(cities: list = None, all=False) -> dict:
    """Load csv files of each city in the list and encapsulate into one dict"""
    if all:
        return {city: load_single(city) for city in CITY_CSV}
    elif len(cities) < 1:
        raise ValueError("Must contain valid city names.")
    cities_data = {}
    for city in cities:
        cities_data[city] = load_single(city)
    return cities_data


def compute_yearly_extremes(df: pd.DataFrame) -> pd.DataFrame:
    """Return a df containing yearly max/min."""
    return df.groupby("Year").agg({
        "Max Temp": "max",
        "Min Temp": "min",
    }).reset_index()


def compute_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute monthly temp and precip for climate data of a single city:
    """
    df = df.copy()

    monthly = df.groupby("Month").agg({
        "Max Temp": "mean",
        "Min Temp": "mean",
        "Total Precip": "sum"
    }).reset_index()

    return monthly
