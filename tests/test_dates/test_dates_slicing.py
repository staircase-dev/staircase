import pandas as pd
import pytest

import staircase as sc


# Not testing "W", it's a pain for period index
@pytest.mark.parametrize("freq_str", ["ns", "us", "ms", "s", "min", "h", "D", "M"])
def test_slice_month_period_range(freq_str):
    # GH108
    date_freq = "MS" if freq_str == "M" else freq_str
    pr = pd.period_range("2020", periods=100, freq=freq_str)
    dr = pd.date_range("2020", periods=100, freq=date_freq)
    slicer1 = sc.Stairs().slice(pr)
    slicer2 = sc.Stairs().slice(dr)
    slicer1._create_slices()
    slicer2._create_slices()
    assert all([s1.identical(s2) for s1, s2, in zip(slicer1._slices, slicer2._slices)])
