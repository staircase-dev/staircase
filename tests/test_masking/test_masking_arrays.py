import numpy as np
import pandas as pd
import pytest

import staircase as sc
from staircase import Stairs


def s1(closed="left"):
    return (
        sc.Stairs(initial_value=0, closed=closed)
        .layer(1, 10, 2)
        .layer(-4, 5, -1.75)
        .layer(3, 5, 2.5)
        .layer(6, 7, -2.5)
        .layer(7, 10, -2.5)
    )


def s2():
    return (
        sc.Stairs()
        .layer(start=-2, value=-1.75)
        .layer(start=1, value=-0.75)
        .layer(start=2, value=4.5)
        .layer(start=2.5, value=-2.5)
        .layer(start=7, value=2.5)
        .layer(start=8, value=-4.5)
        .layer(start=10, value=2.5)
        .layer(start=11, value=5)
        .layer(start=13, value=-5)
    )


def test_sum():
    s1mask = s1().mask((2, 4))
    s2mask = s2().mask((7, 9))
    pd.testing.assert_series_equal(
        sc.sum([s1mask, s2mask, s1mask + s2mask]).step_values(),
        pd.Series(
            {
                -4.0: -3.5,
                -2.0: -7.0,
                1.0: -4.5,
                2.0: np.nan,
                4.0: 4.5,
                5.0: 3.0,
                6.0: -2.0,
                7.0: np.nan,
                9.0: -6.0,
                10.0: 0.0,
                11.0: 10.0,
                13.0: 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_max():
    s1mask = s1().mask((2, 4))
    s2mask = s2().mask((7, 9))
    pd.testing.assert_series_equal(
        sc.max([s1mask, s2mask]).step_values(),
        pd.Series(
            {
                -2.0: -1.75,
                1.0: 0.25,
                2.0: np.nan,
                4.0: 2.75,
                5.0: 2.0,
                6.0: -0.5,
                7.0: np.nan,
                9.0: -0.5,
                10.0: 0.0,
                11.0: 5.0,
                13.0: 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_min():
    s1mask = s1().mask((2, 4))
    s2mask = s2().mask((7, 9))
    pd.testing.assert_series_equal(
        sc.min([s1mask, s2mask]).step_values(),
        pd.Series(
            {
                -4.0: -1.75,
                1.0: -2.5,
                2.0: np.nan,
                4.0: -0.5,
                7.0: np.nan,
                9.0: -2.5,
                10.0: 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_1():
    s1mask = s1().mask((2, 4))
    s2mask = s2().mask((7, 9))
    pd.testing.assert_series_equal(
        sc.mean([s1mask, s2mask]).step_values(),
        pd.Series(
            {
                -4.0: -0.875,
                -2.0: -1.75,
                1.0: -1.125,
                2.0: np.nan,
                4.0: 1.125,
                5.0: 0.75,
                6.0: -0.5,
                7.0: np.nan,
                9.0: -1.5,
                10.0: 0.0,
                11.0: 2.5,
                13.0: 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_2():
    s1mask = s1().mask((2, 4))
    s2mask = s2().mask((7, 9)).mask((None, 0))
    result = sc.mean([s1mask, s2mask])
    pd.testing.assert_series_equal(
        result.step_values(),
        pd.Series(
            {
                0.0: -1.75,
                1.0: -1.125,
                2.0: np.nan,
                4.0: 1.125,
                5.0: 0.75,
                6.0: -0.5,
                7.0: np.nan,
                9.0: -1.5,
                10.0: 0.0,
                11.0: 2.5,
                13.0: 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )
    assert np.isnan(result.initial_value)


def test_median():
    s1mask = s1().mask((2, 4))
    s2mask = s2().mask((7, 9))
    pd.testing.assert_series_equal(
        sc.median([s1mask, s2mask, s1mask + s2mask]).step_values(),
        pd.Series(
            {
                -4.0: -1.75,
                1.0: -2.25,
                2.0: np.nan,
                4.0: 2.25,
                5.0: 1.5,
                6.0: -0.5,
                7.0: np.nan,
                9.0: -2.5,
                10.0: 0.0,
                11.0: 5.0,
                13.0: 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_sample():
    s1mask = s1().mask((2, 4))
    s2mask = s2().mask((7, 9))
    expected = pd.DataFrame(
        {
            1: [0.25, -2.5, -2.25],
            3: [np.nan, -0.5, np.nan],
            5: [2.0, -0.5, 1.5],
            7: [-0.5, np.nan, np.nan],
            9: [-0.5, -2.5, -3.0],
        }
    )
    pd.testing.assert_frame_equal(
        sc.sample([s1mask, s2mask, s1mask + s2mask], [1, 3, 5, 7, 9]),
        expected,
        check_names=False,
        check_index_type=False,
    )
