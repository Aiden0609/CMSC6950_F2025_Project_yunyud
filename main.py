#%%
from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


DATA_DIR = Path("data/processed")


def load_processed_dfs(data_dir=DATA_DIR) -> Dict[str, pd.DataFrame]:
    """
    Load every CSV inside ``data/processed`` into pandas DataFrames.
    """
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    csv_files = sorted(data_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files discovered in: {data_dir}")

    dfs: Dict[str, pd.DataFrame] = {}
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, parse_dates=["Date/Time"])
        dfs[csv_file.stem] = df
    return dfs


def basic_summary(city: str, df: pd.DataFrame) -> None:
    """Display a small summary for the provided DataFrame."""
    total_rows = len(df)
    numeric_cols = [col for col in df.select_dtypes("number").columns]
    min_date = df["Date/Time"].min() if "Date/Time" in df else None
    max_date = df["Date/Time"].max() if "Date/Time" in df else None

    print(f"\n=== {city} ===")
    print(f"Rows: {total_rows}")
    if min_date is not None and max_date is not None:
        print(f"Date coverage: {min_date.date()} → {max_date.date()}")


def main() -> None:
    dfs = load_processed_dfs(DATA_DIR)
    for city, df in dfs.items():
        basic_summary(city, df)


if __name__ == "__main__":
    main()
# %%
