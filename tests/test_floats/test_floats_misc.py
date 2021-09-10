import numpy as np
import pandas as pd
import pytest

import staircase.test_data as test_data
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


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_copy_and_equality(init_value):
    int_seq = Stairs(initial_value=init_value)
    int_seq_copy = int_seq.copy()
    assert int_seq.identical(int_seq_copy)
    assert int_seq_copy.identical(int_seq)


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_deepcopy(init_value):
    int_seq = Stairs(initial_value=init_value)
    int_seq_copy = int_seq.copy()
    int_seq_copy.layer(1, 2)
    assert not int_seq.identical(int_seq_copy)
    assert not int_seq_copy.identical(int_seq)


def test_to_dataframe(s1_fix):
    s1_fix.to_frame()


@pytest.mark.parametrize(
    "kwargs, expected_index, expected_vals",
    [
        (
            {"window": (-1, 1)},
            [-5, -3, 0, 2, 4, 5, 6, 7, 9, 11],
            [0.0, -1.75, -1.75, 0.25, 2.75, 2.375, 0.75, -0.5, -0.5, 0.0],
        ),
        (
            {"window": (-2, 0)},
            [-4, -2, 1, 3, 5, 6, 7, 8, 10, 12],
            [0.0, -1.75, -1.75, 0.25, 2.75, 2.375, 0.75, -0.5, -0.5, 0.0],
        ),
        (
            {"window": (-1, 1), "where": (0, 8)},
            [1, 2, 4, 5, 6, 7],
            [-0.75, 0.25, 2.75, 2.375, 0.75, -0.5],
        ),
    ],
)
def test_s1_rolling_mean(s1_fix, kwargs, expected_index, expected_vals):
    rm = s1_fix.rolling_mean(**kwargs)
    assert list(rm.values) == expected_vals
    assert list(rm.index) == expected_index


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"arrows": True, "style": "hlines"},
        {"arrows": False, "style": "hlines"},
        {"arrows": True, "style": "step"},
        {"arrows": False, "style": "step"},
    ],
)
def test_plot(s1_fix, kwargs):
    s1_fix.plot(**kwargs)


def test_plot_trivial_1():
    Stairs().plot()


def test_plot_trivial_2():
    Stairs(initial_value=np.nan).plot()


def test_plot_ecdf(s1_fix):
    s1_fix.plot.ecdf()


def test_plot_bad_backend(s1_fix):
    with pytest.raises(ValueError):
        s1_fix.plot(backend="")


def test_plot_ecdf_bad_backend(s1_fix):
    with pytest.raises(ValueError):
        s1_fix.plot.ecdf(backend="")


def test_diff(s1_fix):
    assert pd.Series.equals(
        s1_fix.diff(1).step_changes,
        pd.Series(
            {
                -4: -1.75,
                -3: 1.75,
                1: 2,
                2: -2,
                3: 2.5,
                4: -2.5,
                5: -0.75,
                6: -1.75,
                7: 2.5,
                10: 0.5,
                11: -0.5,
            }
        ),
    )


def test_str(s1_fix):
    assert str(s1_fix) is not None
    assert str(s1_fix) != ""


def test_repr(s1_fix):
    assert repr(s1_fix) is not None
    assert repr(s1_fix) != ""


def test_make_test_data():
    assert type(test_data.make_test_data()) == pd.DataFrame


def test_pipe(s1_fix):
    def is_stairs(s):
        return isinstance(s, Stairs)

    assert s1().pipe(is_stairs)


def test_step_changes(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.step_changes,
        pd.Series({-4: -1.75, 1: 2.0, 3: 2.5, 5: -0.75, 6: -2.5, 10: 0.5}),
        check_names=False,
        check_index_type=False,
    )


def test_step_values(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.step_values,
        pd.Series({-4: -1.75, 1: 0.25, 3: 2.75, 5: 2.0, 6: -0.5, 10: 0.0}),
        check_names=False,
        check_index_type=False,
    )


def test_step_points(s1_fix):
    assert list(s1_fix.step_points) == [-4, 1, 3, 5, 6, 10]


def test_step_changes_stepless():
    pd.testing.assert_series_equal(
        Stairs().step_changes,
        pd.Series([], dtype="float64"),
        check_names=False,
        check_index_type=False,
    )


def test_step_values_stepless():
    pd.testing.assert_series_equal(
        Stairs().step_values,
        pd.Series([], dtype="float64"),
        check_names=False,
        check_index_type=False,
    )


def test_step_points_stepless():
    assert list(Stairs().step_points) == []
