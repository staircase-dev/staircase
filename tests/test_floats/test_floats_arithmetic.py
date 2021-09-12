import numpy as np
import pandas as pd
import pytest

from staircase import Stairs
from staircase.core.ops.common import DifferentClosedValuesError


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


def test_add_1(s1_fix, s2_fix):
    assert pd.Series.equals(
        (s1_fix + s2_fix).step_changes,
        pd.Series(
            {
                -4: -1.75,
                -2: -1.75,
                1: 1.25,
                2: 4.5,
                2.5: -2.5,
                3: 2.5,
                4: 2.5,
                5: -5.25,
                6: -2.5,
                7: 2.5,
                8: 5,
                10: -4.5,
            }
        ),
    )


def test_add_2(s1_fix):
    s = s1_fix + 3
    assert s.initial_value == 3
    assert pd.Series.equals(
        s.step_changes,
        s1_fix.step_changes,
    )


def test_add_3(s1_fix):
    s = 3 + s1_fix
    assert s.initial_value == 3
    assert pd.Series.equals(
        s.step_changes,
        s1_fix.step_changes,
    )


def test_sub_1(s1_fix, s2_fix):
    assert pd.Series.equals(
        (s1_fix - s2_fix).step_values,
        pd.Series(
            {
                -4.0: -1.75,
                -2.0: 0.0,
                1.0: 2.75,
                2.0: -1.75,
                2.5: 0.75,
                3.0: 3.25,
                4.0: 0.75,
                5.0: 4.5,
                6.0: 2.0,
                7.0: -0.5,
                8.0: -5.5,
                10.0: 0.0,
            }
        ),
    )


def test_sub_2(s1_fix):
    s = s1_fix - 3
    assert s.initial_value == -3
    assert pd.Series.equals(
        s.step_changes,
        s1_fix.step_changes,
    )


def test_sub_3(s1_fix):
    s = 3 - s1_fix
    assert s.initial_value == 3
    assert pd.Series.equals(
        s.step_changes,
        -(s1_fix.step_changes),
    )


def test_divide(s1_fix, s2_fix):
    assert pd.Series.equals(
        (s1_fix / (s2_fix + 1)).step_changes,
        pd.Series(
            {
                -4: -1.75,
                -2: 4.083333333333334,
                1: -2.5,
                2: 0.25,
                2.5: 0.4166666666666667,
                3: 5.0,
                4: -4.583333333333333,
                5: -2.25,
                6: 1.6666666666666665,
                7: -0.8333333333333333,
                8: 0.4166666666666667,
                10: 0.08333333333333333,
            }
        ),
    )


def test_divide_scalar(s1_fix):
    assert pd.Series.equals(
        (s1_fix / 0.5).step_changes,
        pd.Series(
            {
                -4: -3.5,
                1: 4.0,
                3: 5.0,
                5: -1.5,
                6: -5.0,
                10: 1.0,
            }
        ),
    )


def test_scalar_divide():
    s = Stairs().layer([1, 2, 5], [3, 4, 7], [1, -1, 2])
    assert pd.Series.equals(
        (2 / s).step_values,
        pd.Series(
            {
                1: 2.0,
                2: np.nan,
                3: -2.0,
                4: np.nan,
                5: 1.0,
                7: np.nan,
            }
        ),
    )


def test_multiply(s1_fix, s2_fix):
    assert pd.Series.equals(
        (s1_fix * s2_fix).step_changes,
        pd.Series(
            {
                -2: 3.0625,
                1: -3.6875,
                2: 1.125,
                2.5: -0.625,
                3: -1.25,
                4: 6.875,
                5: -10.5,
                6: 6.25,
                7: -1.25,
                8: -2.5,
                10: 2.5,
            }
        ),
    )


def test_multiply_scalar(s1_fix):
    assert pd.Series.equals(
        (s1_fix * 3).step_changes,
        pd.Series(
            {
                -4: -5.25,
                1: 6.0,
                3: 7.5,
                5: -2.25,
                6: -7.5,
                10: 1.5,
            }
        ),
    )


def test_multiply_scalar_2(s1_fix):
    assert pd.Series.equals(
        (3 * s1_fix).step_changes,
        pd.Series(
            {
                -4: -5.25,
                1: 6.0,
                3: 7.5,
                5: -2.25,
                6: -7.5,
                10: 1.5,
            }
        ),
    )


def test_negate(s1_fix):
    pd.testing.assert_series_equal(
        (-s1_fix).step_values,
        pd.Series({-4: 1.75, 1: -0.25, 3: -2.75, 5: -2.0, 6: 0.5, 10: 0.0}),
        check_names=False,
        check_index_type=False,
    )


def test_add_with_closed_mismatch():
    stairs1 = s1(closed="left")
    stairs2 = s1(closed="right")
    with pytest.raises(DifferentClosedValuesError):
        stairs1 + stairs2
