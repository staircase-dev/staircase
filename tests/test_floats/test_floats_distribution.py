import itertools

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
    "stairs_instance, bounds, cuts",
    itertools.product(
        [s1(), s2(), s3(), s4()],
        [(3, 4), (0, 10), (-10, 30), (-5, -1)],
        ["unit", (0, 2.5, 4, 4.5, 7)],
    ),
)
def test_hist_left_closed(stairs_instance, bounds, cuts):
    def make_expected_result(interval_index, lower, upper):
        return pd.Series(
            [
                ((stairs_instance >= i.left) * (stairs_instance < i.right)).agg(
                    "mean", (lower, upper)
                )
                for i in interval_index
            ],
            index=interval_index,
            dtype="float64",
        )

    hist = stairs_instance.clip(*bounds).hist(bins=cuts, stat="probability")
    expected = make_expected_result(hist.index, *bounds)
    assert (hist.apply(round, args=(5,)) == expected.apply(round, args=(5,))).all(), f"{bounds}, {cuts}"


@pytest.mark.parametrize(
    "stairs_instance, bounds, cuts",
    itertools.product(
        [s1(), s2(), s3(), s4()],
        [(3, 4), (0, 10), (-10, 30), (-5, -1)],
        ["unit", (0, 2.5, 4, 4.5, 7)],
    ),
)
def test_hist_right_closed(stairs_instance, bounds, cuts):
    def make_expected_result(interval_index, lower, upper):
        return pd.Series(
            [
                ((stairs_instance > i.left) * (stairs_instance <= i.right)).agg(
                    "mean", (lower, upper)
                )
                for i in interval_index
            ],
            index=interval_index,
            dtype="float64",
        )

    hist = stairs_instance.clip(*bounds).hist(
        bins=cuts, closed="right", stat="probability"
    )
    expected = make_expected_result(hist.index, *bounds)
    assert (hist.apply(round, args=(5,)) == expected.apply(round, args=(5,))).all(), f"{bounds}, {cuts}"


@pytest.mark.parametrize(
    "stairs_instance, bounds, closed",
    itertools.product(
        [s1(), s2(), s3(), s4()],
        [(3, 4), (0, 10), (-10, 30), (-5, -1)],
        ["left", "right"],
    ),
)
def test_hist_default_bins(stairs_instance, bounds, closed):
    # really testing the default binning process here
    hist = stairs_instance.clip(*bounds).hist(closed=closed, stat="probability")
    assert abs(hist.sum() - 1) < 0.000001


def test_value_sums(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.value_sums(),
        pd.Series({-1.75: 5, -0.5: 4, 0.25: 2, 2.0: 1, 2.75: 2}),
        check_names=False,
        check_index_type=False,
    )


def test_hist_frequency(s1_fix):
    index = pd.IntervalIndex.from_breaks([-2, 0, 2, 3], closed="left")
    pd.testing.assert_series_equal(
        s1_fix.hist(bins=[-2, 0, 2, 3], stat="frequency"),
        pd.Series([4.5, 1, 3], index=index),
        check_names=False,
        check_index_type=False,
    )


def test_hist_density(s1_fix):
    index = pd.IntervalIndex.from_breaks([-2, 0, 2, 3], closed="left")
    pd.testing.assert_series_equal(
        s1_fix.hist(bins=[-2, 0, 2, 3], stat="density"),
        pd.Series([0.36, 0.08, 0.12], index=index),
        check_names=False,
        check_index_type=False,
    )


def test_hist_probability(s1_fix):
    index = pd.IntervalIndex.from_breaks([-2, 0, 2, 3], closed="left")
    pd.testing.assert_series_equal(
        s1_fix.hist(bins=[-2, 0, 2, 3], stat="probability"),
        pd.Series([0.642857, 0.142857, 0.214286], index=index),
        check_names=False,
        check_index_type=False,
    )


def test_quantiles(s1_fix):
    assert (s1_fix.quantiles(4) == np.array([-1.75, -0.5, 0.25])).all()


def test_fractile(s1_fix):
    assert list(map(s1().fractile, (0.25, 0.5, 0.75))) == [
        -1.75,
        -0.5,
        0.25,
    ]
