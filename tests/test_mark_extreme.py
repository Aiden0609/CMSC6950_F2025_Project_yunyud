import pytest
import pandas as pd
from computeSDI import mark_extreme


@pytest.mark.parametrize(
    "max_temp, min_temp, tmax90, tmin90, expected_hot",
    [
        (35, 25, 30, 20, 1),
        (35, 15, 30, 20, 0),
        (25, 25, 30, 20, 0),
        (30, 20, 30, 20, 0),
        (40, 40, 39, 39, 1),
    ]
)
def test_mark_extreme(max_temp, min_temp, tmax90, tmin90, expected_hot):

    df = pd.DataFrame({
        "Year": [2000],
        "doy": [1],
        "Max Temp": [max_temp],
        "Min Temp": [min_temp],
    })

    quant = pd.DataFrame({
        "tmax90": [tmax90],
        "tmin90": [tmin90],
    }, index=[1])

    out = mark_extreme(df, quant)

    assert out.loc[0, "hot"] == expected_hot
