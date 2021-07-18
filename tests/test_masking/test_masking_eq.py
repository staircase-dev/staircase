# %%
import numpy as np
import pandas as pd
import pytest

import staircase as sc


# def _expand_interval_definition(start, end=None, value=1):
#     return start, end, value
def concat(series, dict_):
    return pd.concat([series, pd.Series(dict_)]).sort_index()


def s1(initial_value=0):
    int_seq1 = sc.Stairs(initial_value=initial_value)
    int_seq1.layer(1, 10, 2)
    int_seq1.layer(-4, 5, -1.75)
    int_seq1.layer(3, 5, 2.5)
    int_seq1.layer(6, 7, -2.5)
    int_seq1.layer(7, 10, -2.5)
    return int_seq1


def s2(initial_value=0):
    int_seq2 = sc.Stairs(initial_value=initial_value)
    int_seq2.layer(1, 7, -2.5)
    int_seq2.layer(8, 10, 5)
    int_seq2.layer(2, 5, 4.5)
    int_seq2.layer(2.5, 4, -2.5)
    int_seq2.layer(-2, 1, -1.75)
    return int_seq2


@pytest.fixture
def s1_fix():
    return s1(0)


# %%


@pytest.mark.parametrize(
    "stairs1, stairs2",
    [
        (s1().mask(sc.Stairs(start=1, end=3)), s2()),
        (s1(), s2().mask(sc.Stairs(start=1, end=3))),
        (s1().mask(sc.Stairs(start=1, end=3)), s2().mask(sc.Stairs(start=1, end=3))),
    ],
)
def test_non_unique_mask_eq(stairs1, stairs2):
    result = stairs1 == stairs2
    expected = pd.Series({-4.0: 0.0, -2.0: 1.0, 1.0: np.nan, 3.0: 0.0, 10.0: 1.0})
    pd.testing.assert_series_equal(
        result.step_values, expected, check_names=False, check_index_type=False,
    )
    assert result.initial_value == 1


@pytest.mark.parametrize(
    "stairs1, stairs2",
    [
        (s1().mask(sc.Stairs(end=3)), s2()),
        (s1(), s2().mask(sc.Stairs(end=3))),
        (s1().mask(sc.Stairs(end=3)), s2().mask(sc.Stairs(end=3))),
    ],
)
def test_non_unique_nan_initial_mask_eq(stairs1, stairs2):
    result = stairs1 == stairs2
    expected = pd.Series({3.0: 0.0, 10.0: 1.0})
    pd.testing.assert_series_equal(
        result.step_values, expected, check_names=False, check_index_type=False,
    )
    assert np.isnan(result.initial_value)


@pytest.mark.parametrize(
    "stairs1, stairs2",
    [
        (s1().mask(sc.Stairs(start=1, end=3)).mask(sc.Stairs(start=5, end=9)), s2()),
        (s1().mask(sc.Stairs(start=5, end=9)).mask(sc.Stairs(start=1, end=3)), s2()),
        (s1(), s2().mask(sc.Stairs(start=1, end=3)).mask(sc.Stairs(start=5, end=9))),
        (s1(), s2().mask(sc.Stairs(start=5, end=9)).mask(sc.Stairs(start=1, end=3))),
        (s1().mask(sc.Stairs(start=1, end=3)), s2().mask(sc.Stairs(start=5, end=9))),
        (s1().mask(sc.Stairs(start=5, end=9)), s2().mask(sc.Stairs(start=1, end=3))),
    ],
)
def test_unique_non_overlapping_mask_eq(stairs1, stairs2):
    result = stairs1 == stairs2
    expected = pd.Series(
        {-4.0: 0.0, -2.0: 1.0, 1.0: np.nan, 3.0: 0.0, 5.0: np.nan, 9.0: 0.0, 10.0: 1.0}
    )
    pd.testing.assert_series_equal(
        result.step_values, expected, check_names=False, check_index_type=False,
    )
    assert result.initial_value == 1


@pytest.mark.parametrize(
    "stairs1, stairs2",
    [
        (s1().mask(sc.Stairs(end=3)).mask(sc.Stairs(start=5, end=9)), s2()),
        (s1().mask(sc.Stairs(start=5, end=9)).mask(sc.Stairs(end=3)), s2()),
        (s1(), s2().mask(sc.Stairs(end=3)).mask(sc.Stairs(start=5, end=9))),
        (s1(), s2().mask(sc.Stairs(start=5, end=9)).mask(sc.Stairs(end=3))),
        (s1().mask(sc.Stairs(end=3)), s2().mask(sc.Stairs(start=5, end=9))),
        (s1().mask(sc.Stairs(start=5, end=9)), s2().mask(sc.Stairs(end=3))),
    ],
)
def test_unique_non_overlapping_nan_initial_mask_eq(stairs1, stairs2):
    result = stairs1 == stairs2
    expected = pd.Series({3.0: 0.0, 5.0: np.nan, 9.0: 0.0, 10.0: 1.0})
    pd.testing.assert_series_equal(
        result.step_values, expected, check_names=False, check_index_type=False,
    )
    assert np.isnan(result.initial_value)


@pytest.mark.parametrize(
    "stairs1, stairs2",
    [
        (s1().mask(sc.Stairs(start=1, end=4)).mask(sc.Stairs(start=4, end=9)), s2()),
        (s1().mask(sc.Stairs(start=4, end=9)).mask(sc.Stairs(start=1, end=4)), s2()),
        (s1(), s2().mask(sc.Stairs(start=1, end=4)).mask(sc.Stairs(start=4, end=9))),
        (s1(), s2().mask(sc.Stairs(start=4, end=9)).mask(sc.Stairs(start=1, end=4))),
        (s1().mask(sc.Stairs(start=1, end=4)), s2().mask(sc.Stairs(start=4, end=9))),
        (s1().mask(sc.Stairs(start=4, end=9)), s2().mask(sc.Stairs(start=1, end=4))),
    ],
)
def test_unique_adjacent_mask_eq(stairs1, stairs2):
    result = stairs1 == stairs2
    expected = pd.Series({-4.0: 0.0, -2.0: 1.0, 1.0: np.nan, 9.0: 0.0, 10.0: 1.0})
    pd.testing.assert_series_equal(
        result.step_values, expected, check_names=False, check_index_type=False,
    )
    assert result.initial_value == 1


@pytest.mark.parametrize(
    "stairs1, stairs2",
    [
        (s1().mask(sc.Stairs(end=4)).mask(sc.Stairs(start=4, end=9)), s2()),
        (s1().mask(sc.Stairs(start=4, end=9)).mask(sc.Stairs(end=4)), s2()),
        (s1(), s2().mask(sc.Stairs(end=4)).mask(sc.Stairs(start=4, end=9))),
        (s1(), s2().mask(sc.Stairs(start=4, end=9)).mask(sc.Stairs(end=4))),
        (s1().mask(sc.Stairs(end=4)), s2().mask(sc.Stairs(start=4, end=9))),
        (s1().mask(sc.Stairs(start=4, end=9)), s2().mask(sc.Stairs(end=4))),
    ],
)
def test_unique_adjacent_nan_initial_mask_eq(stairs1, stairs2):
    result = stairs1 == stairs2
    expected = pd.Series({9.0: 0.0, 10.0: 1.0})
    pd.testing.assert_series_equal(
        result.step_values, expected, check_names=False, check_index_type=False,
    )
    assert np.isnan(result.initial_value)


@pytest.mark.parametrize(
    "stairs1, stairs2",
    [
        (s1().mask(sc.Stairs(start=1, end=6)).mask(sc.Stairs(start=4, end=9)), s2()),
        (s1().mask(sc.Stairs(start=4, end=9)).mask(sc.Stairs(start=1, end=6)), s2()),
        (s1(), s2().mask(sc.Stairs(start=1, end=6)).mask(sc.Stairs(start=4, end=9))),
        (s1(), s2().mask(sc.Stairs(start=4, end=9)).mask(sc.Stairs(start=1, end=6))),
        (s1().mask(sc.Stairs(start=1, end=6)), s2().mask(sc.Stairs(start=4, end=9))),
        (s1().mask(sc.Stairs(start=4, end=9)), s2().mask(sc.Stairs(start=1, end=6))),
    ],
)
def test_unique_overlapping_mask_eq(stairs1, stairs2):
    result = stairs1 == stairs2
    expected = pd.Series({-4.0: 0.0, -2.0: 1.0, 1.0: np.nan, 9.0: 0.0, 10.0: 1.0})
    pd.testing.assert_series_equal(
        result.step_values, expected, check_names=False, check_index_type=False,
    )
    assert result.initial_value == 1


@pytest.mark.parametrize(
    "stairs1, stairs2",
    [
        (s1().mask(sc.Stairs(end=6)).mask(sc.Stairs(start=4, end=9)), s2()),
        (s1().mask(sc.Stairs(start=4, end=9)).mask(sc.Stairs(end=6)), s2()),
        (s1(), s2().mask(sc.Stairs(end=6)).mask(sc.Stairs(start=4, end=9))),
        (s1(), s2().mask(sc.Stairs(start=4, end=9)).mask(sc.Stairs(end=6))),
        (s1().mask(sc.Stairs(end=6)), s2().mask(sc.Stairs(start=4, end=9))),
        (s1().mask(sc.Stairs(start=4, end=9)), s2().mask(sc.Stairs(end=6))),
    ],
)
def test_unique_overlapping_nan_initial_mask_eq(stairs1, stairs2):
    result = stairs1 == stairs2
    expected = pd.Series({9.0: 0.0, 10.0: 1.0})
    pd.testing.assert_series_equal(
        result.step_values, expected, check_names=False, check_index_type=False,
    )
    assert np.isnan(result.initial_value)
