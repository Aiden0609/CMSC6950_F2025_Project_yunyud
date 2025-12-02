import pytest
import pandas as pd
import numpy as np
from computeSDI import compute_thresholds


@pytest.mark.parametrize(
    "temps, expected_p90",
    [
        ([10, 20, 30, 40, 50], np.percentile([10, 20, 30, 40, 50], 90)),
        ([5, 5, 5, 5], 5),
        ([1, 100], np.percentile([1, 100], 90)),
        ([0, 0, 100, 100], np.percentile([0, 0, 100, 100], 90)),
    ]
)
def test_compute_thresholds(temps, expected_p90):

    df = pd.DataFrame({
        "Year": [2000] * len(temps),
        "doy": [1] * len(temps),
        "Max Temp": temps,
        "Min Temp": temps,
    })

    quant = compute_thresholds(df)

    assert np.isclose(quant.loc[1, "tmax90"], expected_p90)
    assert np.isclose(quant.loc[1, "tmin90"], expected_p90)
