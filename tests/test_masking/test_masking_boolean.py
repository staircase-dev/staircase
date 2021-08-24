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
    "kwargs, expected_values, expected_initial",
    [
        ({"end": -4}, pd.Series({-4.0: 1.0, 10.0: 0.0}), np.nan),
        ({"start": -4, "end": 1}, pd.Series({-4.0: np.nan, 1.0: 1.0, 10.0: 0.0}), 0),
        ({"start": 5, "end": 11}, pd.Series({-4.0: 1.0, 5.0: np.nan, 11.0: 0.0}), 0),
        ({"start": -10, "end": 11}, pd.Series({-10.0: np.nan, 11.0: 0.0}), 0),
        ({"start": 5}, pd.Series({-4.0: 1.0, 5: np.nan}), 0),
        ({"start": -5}, pd.Series({-5: np.nan}), 0),
    ],
)
def test_mask_make_boolean_s1(kwargs, expected_values, expected_initial):
    result = s1().mask(sc.Stairs(**kwargs)).make_boolean()
    pd.testing.assert_series_equal(
        result.step_values,
        expected_values,
        check_names=False,
        check_index_type=False,
    )
    if np.isnan(expected_initial):
        assert np.isnan(result.initial_value)
    else:
        assert result.initial_value == expected_initial


@pytest.mark.parametrize(
    "kwargs, expected_values, expected_initial",
    [
        ({"end": -4}, pd.Series({-4.0: 0.0, 10.0: 1.0}), np.nan),
        ({"start": -4, "end": 1}, pd.Series({-4.0: np.nan, 1.0: 0.0, 10.0: 1.0}), 1),
        ({"start": 5, "end": 11}, pd.Series({-4.0: 0.0, 5.0: np.nan, 11.0: 1.0}), 1),
        ({"start": -10, "end": 11}, pd.Series({-10.0: np.nan, 11.0: 1.0}), 1),
        ({"start": 5}, pd.Series({-4.0: 0.0, 5: np.nan}), 1),
        ({"start": -5}, pd.Series({-5: np.nan}), 1),
    ],
)
def test_mask_invert_s1(kwargs, expected_values, expected_initial):
    result = s1().mask(sc.Stairs(**kwargs)).invert()
    pd.testing.assert_series_equal(
        result.step_values,
        expected_values,
        check_names=False,
        check_index_type=False,
    )
    if np.isnan(expected_initial):
        assert np.isnan(result.initial_value)
    else:
        assert result.initial_value == expected_initial
