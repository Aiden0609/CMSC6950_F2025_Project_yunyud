import pytest
import pandas as pd
from utils import (
    compute_yearly_extremes,
    compute_monthly,
)

@pytest.mark.parametrize(
    "df_input,expected_max,expected_min",
    [
        (
            pd.DataFrame({
                "Year": [2020, 2020, 2021, 2021],
                "Max Temp": [5, 10, 7, 8],
                "Min Temp": [-3, -1, -5, -4],
            }),
            {2020: 10, 2021: 8},
            {2020: -3, 2021: -5}
        )
    ]
)
def test_compute_yearly_extremes(df_input, expected_max, expected_min):

    df_out = compute_yearly_extremes(df_input)

    for _, row in df_out.iterrows():
        y = row["Year"]
        assert row["Max Temp"] == expected_max[y]
        assert row["Min Temp"] == expected_min[y]


@pytest.mark.parametrize(
    "df_input,exp_max,exp_min,exp_precip",
    [
        (
            pd.DataFrame({
                "Month": [1, 1, 2, 2],
                "Max Temp": [10, 20, 5, 15],
                "Min Temp": [0, 5, -5, 0],
                "Total Precip": [3, 7, 10, 20],
            }),
            {1: 15, 2: 10},
            {1: 2.5, 2: -2.5},
            {1: 10, 2: 30},  # sum
        )
    ]
)
def test_compute_monthly(df_input, exp_max, exp_min, exp_precip):

    df_out = compute_monthly(df_input)

    for _, row in df_out.iterrows():
        m = row["Month"]
        assert row["Max Temp"] - exp_max[m] < 1e-10
        assert row["Min Temp"] - exp_min[m] < 1e-10
        assert row["Total Precip"] - exp_precip[m] < 1e-10
