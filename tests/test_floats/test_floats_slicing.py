import numpy as np
import pandas as pd
import pytest

from staircase import Stairs


def s1(closed="left"):
    int_seq1 = Stairs(initial_value=0, closed=closed)
    int_seq1.layer(1, 10, 2)
    int_seq1.layer(-4, 5, -1.75)
    int_seq1.layer(3, 5, 2.5)
    int_seq1.layer(6, 7, -2.5)
    int_seq1.layer(7, 10, -2.5)
    return int_seq1


def s2():
    int_seq2 = Stairs(initial_value=0)
    int_seq2.layer(1, 7, -2.5)
    int_seq2.layer(8, 10, 5)
    int_seq2.layer(2, 5, 4.5)
    int_seq2.layer(2.5, 4, -2.5)
    int_seq2.layer(-2, 1, -1.75)
    return int_seq2


def s3():  # boolean
    int_seq = Stairs(initial_value=0)
    int_seq.layer(-10, 10, 1)
    int_seq.layer(-8, -7, -1)
    int_seq.layer(-5, -2, -1)
    int_seq.layer(0.5, 1, -1)
    int_seq.layer(3, 3.5, -1)
    int_seq.layer(7, 9.5, -1)
    return int_seq


def s4():  # boolean
    int_seq = Stairs(initial_value=0)
    int_seq.layer(-11, 9, 1)
    int_seq.layer(-9.5, -8, -1)
    int_seq.layer(-7.5, -7, -1)
    int_seq.layer(0, 3, -1)
    int_seq.layer(6, 6.5, -1)
    int_seq.layer(7, 8.5, -1)
    return int_seq


@pytest.fixture
def s1_fix():
    return s1()


@pytest.fixture
def s2_fix():
    return s2()


@pytest.fixture
def s3_fix():
    return s3()


@pytest.fixture
def s4_fix():
    return s4()


@pytest.mark.parametrize(
    "x, kwargs, expected_val",
    [
        (
            [-4, -2, 1, 3],
            {"aggfunc": "mean", "window": (-0.5, 0.5)},
            np.array([-0.875, -1.75, -0.75, 1.5]),
        ),
        (
            [-4, -2, 1, 3],
            {"aggfunc": "mean", "window": (-1, 0)},
            np.array([0.0, -1.75, -1.75, 0.25]),
        ),
        (
            [-4, -2, 1, 3],
            {"aggfunc": "mean", "window": (0, 1)},
            np.array([-1.75, -1.75, 0.25, 2.75]),
        ),
    ],
)
def test_s1_agg_mean(s1_fix, x, kwargs, expected_val):
    window = kwargs["window"]
    x = np.array(x)
    ii = pd.IntervalIndex.from_arrays(x + window[0], x + window[1])
    assert np.array_equal(s1_fix.slice(ii).mean().values, expected_val)


@pytest.mark.parametrize(
    "closed, x, kwargs, expected_val",
    [
        (
            "left",
            [0, 2, 7],
            {"aggfunc": "max", "window": (-1, 1)},
            np.array([-1.75, 0.25, -0.5]),
        ),
        (
            "right",
            [0, 2, 7],
            {"aggfunc": "max", "window": (-1, 1), "closed": "left"},
            np.array([-1.75, 0.25, 2.0]),
        ),
        (
            "left",
            [0, 2, 7],
            {"aggfunc": "max", "window": (-1, 1), "closed": "right"},
            np.array([0.25, 2.75, -0.5]),
        ),
        (
            "right",
            [0, 2, 7],
            {"aggfunc": "max", "window": (-1, 1), "closed": "right"},
            np.array([-1.75, 0.25, -0.5]),
        ),
    ],
)
def test_s1_agg_max(closed, x, kwargs, expected_val):
    window = kwargs["window"]
    x = np.array(x)
    ii = pd.IntervalIndex.from_arrays(
        x + window[0], x + window[1], closed=kwargs.get("closed", "left")
    )
    assert np.array_equal(s1(closed=closed).slice(ii).max().values, expected_val)


def test_slicing_mean(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.slice(range(-4, 11, 2)).mean(),
        pd.Series(
            {
                pd.Interval(-4, -2, closed="left"): -1.75,
                pd.Interval(-2, 0, closed="left"): -1.75,
                pd.Interval(0, 2, closed="left"): -0.75,
                pd.Interval(2, 4, closed="left"): 1.5,
                pd.Interval(4, 6, closed="left"): 2.375,
                pd.Interval(6, 8, closed="left"): -0.5,
                pd.Interval(8, 10, closed="left"): -0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_slicing_max(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.slice(range(-4, 11, 2)).max(),
        pd.Series(
            {
                pd.Interval(-4, -2, closed="left"): -1.75,
                pd.Interval(-2, 0, closed="left"): -1.75,
                pd.Interval(0, 2, closed="left"): 0.25,
                pd.Interval(2, 4, closed="left"): 2.75,
                pd.Interval(4, 6, closed="left"): 2.75,
                pd.Interval(6, 8, closed="left"): -0.5,
                pd.Interval(8, 10, closed="left"): -0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_slicing_min(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.slice(range(-4, 11, 2)).min(),
        pd.Series(
            {
                pd.Interval(-4, -2, closed="left"): -1.75,
                pd.Interval(-2, 0, closed="left"): -1.75,
                pd.Interval(0, 2, closed="left"): -1.75,
                pd.Interval(2, 4, closed="left"): 0.25,
                pd.Interval(4, 6, closed="left"): 2.0,
                pd.Interval(6, 8, closed="left"): -0.5,
                pd.Interval(8, 10, closed="left"): -0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_slicing_mode(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.slice(range(-4, 11, 2)).mode(),
        pd.Series(
            {
                pd.Interval(-4, -2, closed="left"): -1.75,
                pd.Interval(-2, 0, closed="left"): -1.75,
                pd.Interval(0, 2, closed="left"): -1.75,
                pd.Interval(2, 4, closed="left"): 0.25,
                pd.Interval(4, 6, closed="left"): 2.0,
                pd.Interval(6, 8, closed="left"): -0.5,
                pd.Interval(8, 10, closed="left"): -0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_slicing_median(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.slice(range(-4, 11, 2)).median(),
        pd.Series(
            {
                pd.Interval(-4, -2, closed="left"): -1.75,
                pd.Interval(-2, 0, closed="left"): -1.75,
                pd.Interval(0, 2, closed="left"): -0.75,
                pd.Interval(2, 4, closed="left"): 1.5,
                pd.Interval(4, 6, closed="left"): 2.375,
                pd.Interval(6, 8, closed="left"): -0.5,
                pd.Interval(8, 10, closed="left"): -0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_slicing_agg_min(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.slice(range(-4, 11, 2)).agg("min")["min"],
        pd.Series(
            {
                pd.Interval(-4, -2, closed="left"): -1.75,
                pd.Interval(-2, 0, closed="left"): -1.75,
                pd.Interval(0, 2, closed="left"): -1.75,
                pd.Interval(2, 4, closed="left"): 0.25,
                pd.Interval(4, 6, closed="left"): 2.0,
                pd.Interval(6, 8, closed="left"): -0.5,
                pd.Interval(8, 10, closed="left"): -0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_slicing_apply_min(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.slice(range(-4, 11, 2)).apply(Stairs.min),
        pd.Series(
            {
                pd.Interval(-4, -2, closed="left"): -1.75,
                pd.Interval(-2, 0, closed="left"): -1.75,
                pd.Interval(0, 2, closed="left"): -1.75,
                pd.Interval(2, 4, closed="left"): 0.25,
                pd.Interval(4, 6, closed="left"): 2.0,
                pd.Interval(6, 8, closed="left"): -0.5,
                pd.Interval(8, 10, closed="left"): -0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_slicing_agg_min_max(s1_fix):
    result = s1_fix.slice(range(-4, 11, 2)).agg(["min", "max"])
    pd.testing.assert_series_equal(
        result["min"],
        pd.Series(
            {
                pd.Interval(-4, -2, closed="left"): -1.75,
                pd.Interval(-2, 0, closed="left"): -1.75,
                pd.Interval(0, 2, closed="left"): -1.75,
                pd.Interval(2, 4, closed="left"): 0.25,
                pd.Interval(4, 6, closed="left"): 2.0,
                pd.Interval(6, 8, closed="left"): -0.5,
                pd.Interval(8, 10, closed="left"): -0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )
    pd.testing.assert_series_equal(
        result["max"],
        pd.Series(
            {
                pd.Interval(-4, -2, closed="left"): -1.75,
                pd.Interval(-2, 0, closed="left"): -1.75,
                pd.Interval(0, 2, closed="left"): 0.25,
                pd.Interval(2, 4, closed="left"): 2.75,
                pd.Interval(4, 6, closed="left"): 2.75,
                pd.Interval(6, 8, closed="left"): -0.5,
                pd.Interval(8, 10, closed="left"): -0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_slicing_resample_mean(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.slice(range(0, 7, 2)).resample("mean").step_values,
        pd.Series({-4: -1.75, 0: -0.75, 2: 1.5, 4: 2.375, 6: -0.5, 10: 0.0}),
        check_names=False,
        check_index_type=False,
    )
