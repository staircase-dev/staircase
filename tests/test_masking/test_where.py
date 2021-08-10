# %%
import itertools

import numpy as np
import pandas as pd
import pytest

import staircase as sc


def _add_tuple_mask_option(list_of_args):
    return [(*args, x) for args, x in itertools.product(list_of_args, [True, False])]


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
    "initial_value",
    [np.nan, 0],
)
def test_where_neginf_to_posinf(initial_value):
    s = s1().where(sc.Stairs(initial_value=initial_value))
    assert np.isnan(s.initial_value)
    assert len(s.step_points) == 0


@pytest.mark.parametrize(
    "end, expected_step_values",
    [
        (-5, pd.Series({-5: np.nan})),
        (-4, pd.Series({-4: np.nan})),
        (-2, pd.Series({-4: -1.75, -2: np.nan})),
        (1, pd.Series({-4: -1.75, 1: np.nan})),
        (6, s1().step_values.drop([6, 10]).pipe(concat, {6: np.nan})),
        (10, s1().step_values.drop([10]).pipe(concat, {10: np.nan})),
        (11, s1().step_values.pipe(concat, {11: np.nan})),
    ],
)
def test_where_neginf(end, expected_step_values):
    s = s1().where(sc.Stairs(end=end))
    pd.testing.assert_series_equal(
        s.step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )
    assert s.initial_value == 0


@pytest.mark.parametrize(
    "start, expected_step_values",
    [
        (-5, s1().step_values.pipe(concat, {-5: 0})),
        (-4, s1().step_values),
        (-2, s1().step_values.drop([-4]).pipe(concat, {-2: -1.75})),
        (1, s1().step_values.drop([-4])),
        (6, pd.Series({6: -0.5, 10: 0})),
        (10, pd.Series({10: 0.0})),
        (11, pd.Series({11: 0.0})),
    ],
)
def test_where_posinf(start, expected_step_values):
    s = s1().where(sc.Stairs(start=start))
    pd.testing.assert_series_equal(
        s.step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )
    assert np.isnan(s.initial_value)


@pytest.mark.parametrize(
    "initial_value",
    [np.nan, 0],
)
def test_where_neginf_to_posinf_with_nan_initial(initial_value):
    mask_ = sc.Stairs(end=-4)
    nan_initial = s1().mask(mask_)
    s = nan_initial.where(sc.Stairs(initial_value=initial_value))
    assert np.isnan(s.initial_value)
    assert len(s.step_points) == 0


@pytest.mark.parametrize(
    "end, expected_step_values, tuple_mask",
    _add_tuple_mask_option(
        [
            (-5, pd.Series()),
            (-4, pd.Series()),
            (-2, pd.Series({-4.0: -1.75, -2: np.nan})),
            (1, pd.Series({-4.0: -1.75, 1: np.nan})),
            (6, s1().step_values.drop([6, 10]).pipe(concat, {6: np.nan})),
            (10, s1().step_values.drop([10]).pipe(concat, {10: np.nan})),
            (11, s1().step_values.pipe(concat, {11: np.nan})),
        ],
    ),
)
def test_where_neginf_with_nan_initial(end, expected_step_values, tuple_mask):
    mask_ = (None, -4) if tuple_mask else sc.Stairs(end=-4)
    nan_initial = s1().mask(mask_)
    mask_ = (None, end) if tuple_mask else sc.Stairs(end=end)
    s = nan_initial.where(mask_)
    pd.testing.assert_series_equal(
        s.step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )
    assert np.isnan(s.initial_value)


@pytest.mark.parametrize(
    "start, expected_step_values, tuple_mask",
    _add_tuple_mask_option(
        [
            (-5, s1().step_values),
            (-4, s1().step_values),
            (-2, s1().step_values.drop([-4]).pipe(concat, {-2: -1.75})),
            (1, s1().step_values.drop([-4])),
            (6, pd.Series({6: -0.5, 10: 0})),
            (10, pd.Series({10: 0.0})),
            (11, pd.Series({11: 0.0})),
        ],
    ),
)
def test_where_posinf_with_nan_initial(start, expected_step_values, tuple_mask):
    mask_ = (None, -4) if tuple_mask else sc.Stairs(end=-4)
    nan_initial = s1().mask(mask_)
    mask_ = (start, None) if tuple_mask else sc.Stairs(start=start)
    s = nan_initial.where(mask_)
    pd.testing.assert_series_equal(
        s.step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )
    assert np.isnan(s.initial_value)


@pytest.mark.parametrize(
    "start, end, expected_step_values, tuple_mask",
    _add_tuple_mask_option(
        [
            (-6, -5, pd.Series({-6: 0, -5: np.nan})),
            (-6, -4, pd.Series({-6: 0, -4: np.nan})),
            (-6, -2, pd.Series({-6: 0, -4: -1.75, -2: np.nan})),
            (2, 4, pd.Series({2: 0.25, 3: 2.75, 4: np.nan})),
            (7, 8, pd.Series({7: -0.5, 8: np.nan})),
            (9, 11, pd.Series({9: -0.5, 10: 0, 11: np.nan})),
            (10, 11, pd.Series({10: 0, 11: np.nan})),
            (11, 12, pd.Series({11: 0, 12: np.nan})),
            (-5, 12, s1().step_values.pipe(concat, {-5: 0, 12: np.nan})),
        ]
    ),
)
def test_where_single_step(start, end, expected_step_values, tuple_mask):
    mask_ = (start, end) if tuple_mask else sc.Stairs(start=start, end=end)
    s = s1().where(mask_)
    pd.testing.assert_series_equal(
        s.step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )
    assert np.isnan(s.initial_value)


@pytest.mark.parametrize(
    "start, end, expected_step_values, tuple_mask",
    _add_tuple_mask_option(
        [
            (-6, -5, pd.Series()),
            (-6, -4, pd.Series()),
            (-6, -2, pd.Series({-4: -1.75, -2: np.nan})),
            (2, 4, pd.Series({2: 0.25, 3: 2.75, 4: np.nan})),
            (7, 8, pd.Series({7: -0.5, 8: np.nan})),
            (9, 11, pd.Series({9: -0.5, 10: 0, 11: np.nan})),
            (10, 11, pd.Series({10: 0, 11: np.nan})),
            (11, 12, pd.Series({11: 0, 12: np.nan})),
            (-5, 12, s1().step_values.pipe(concat, {12: np.nan})),
        ],
    ),
)
def test_where_single_step_initial_nan(start, end, expected_step_values, tuple_mask):
    mask_ = (None, -4) if tuple_mask else sc.Stairs(end=-4)
    nan_initial = s1().mask(mask_)
    mask_ = (start, end) if tuple_mask else sc.Stairs(start=start, end=end)
    s = nan_initial.where(mask_)
    pd.testing.assert_series_equal(
        s.step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )
    assert np.isnan(s.initial_value)
