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
    "kwargs",
    [
        {"start": 1, "end": 10},
        {"start": 1},
        {"end": 10},
    ],
)
def test_layer_with_neginf_nan(kwargs):
    s = s1(np.nan)
    s.layer(**kwargs)
    assert (
        len(s.step_points) == 0
    ), "A stairs object with a value of np.nan everywhere should remain this way"


# %%
@pytest.mark.parametrize(
    "initial_value",
    [np.nan, 1],
)
def test_mask_neginf_to_posinf(initial_value):
    s = s1().mask(sc.Stairs(initial_value=initial_value))
    assert np.isnan(s.initial_value)
    assert len(s.step_points) == 0


@pytest.mark.parametrize(
    "end, expected_step_values",
    [
        (-5, s1().step_values.pipe(concat, {-5: 0.0})),
        (-4, s1().step_values),
        (-2, s1().step_values.drop(-4).pipe(concat, {-2.0: -1.75})),
        (1, s1().step_values.drop(-4)),
        (6, s1().step_values.drop([-4, 1, 3, 5])),
        (10, s1().step_values.drop([-4, 1, 3, 5, 6])),
        (11, pd.Series({11: 0.0})),
    ],
)
def test_mask_neginf(end, expected_step_values):
    s = s1().mask(sc.Stairs(end=end))
    pd.testing.assert_series_equal(
        s.step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )
    assert np.isnan(s.initial_value)


@pytest.mark.parametrize(
    "start, expected_step_values",
    [
        (-5, pd.Series({-5: np.nan})),
        (-4, pd.Series({-4: np.nan})),
        (-2, pd.Series({-4: -1.75, -2: np.nan})),
        (1, pd.Series({-4: -1.75, 1: np.nan})),
        (6, s1().step_values.drop([6, 10]).pipe(concat, {6: np.nan})),
        (10, s1().step_values.drop(10).pipe(concat, {10: np.nan})),
        (11, s1().step_values.pipe(concat, {11: np.nan})),
    ],
)
def test_mask_posinf(start, expected_step_values):
    s = s1().mask(sc.Stairs(start=start))
    pd.testing.assert_series_equal(
        s.step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )
    assert s.initial_value == 0


@pytest.mark.parametrize(
    "initial_value, tuple_mask",
    _add_tuple_mask_option(
        [
            (np.nan,),
            (1,),
        ],
    ),
)
def test_mask_neginf_to_posinf_with_nan_initial(initial_value, tuple_mask):
    mask_ = sc.Stairs(end=-4)
    nan_initial = s1().mask(mask_)
    mask_arg = (None, None) if tuple_mask else sc.Stairs(initial_value=initial_value)
    s = nan_initial.mask(mask_arg)
    assert np.isnan(s.initial_value)
    assert len(s.step_points) == 0


@pytest.mark.parametrize(
    "end, expected_step_values, tuple_mask",
    _add_tuple_mask_option(
        [
            (-5, s1().step_values),
            (-4, s1().step_values),
            (-2, s1().step_values.drop(-4).pipe(concat, {-2.0: -1.75})),
            (1, s1().step_values.drop(-4)),
            (6, s1().step_values.drop([-4, 1, 3, 5])),
            (10, s1().step_values.drop([-4, 1, 3, 5, 6])),
            (11, pd.Series({11: 0.0})),
        ],
    ),
)
def test_mask_neginf_with_nan_initial(end, expected_step_values, tuple_mask):
    mask_ = (None, -4) if tuple_mask else sc.Stairs(end=-4)
    nan_initial = s1().mask(mask_)
    mask_ = (None, end) if tuple_mask else sc.Stairs(end=end)
    s = nan_initial.mask(mask_)
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
            (-5, pd.Series([], dtype="float64")),
            (-4, pd.Series([], dtype="float64")),
            (-2, pd.Series({-4: -1.75, -2: np.nan})),
            (1, pd.Series({-4: -1.75, 1: np.nan})),
            (6, s1().step_values.drop([6, 10]).pipe(concat, {6: np.nan})),
            (10, s1().step_values.drop(10).pipe(concat, {10: np.nan})),
            (11, s1().step_values.pipe(concat, {11: np.nan})),
        ],
    ),
)
def test_mask_posinf_with_nan_initial(start, expected_step_values, tuple_mask):
    mask_ = (None, -4) if tuple_mask else sc.Stairs(end=-4)
    nan_initial = s1().mask(mask_)
    mask_ = (start, None) if tuple_mask else sc.Stairs(start=start)
    s = nan_initial.mask(mask_)
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
            (-6, -5, s1().step_values.pipe(concat, {-6: np.nan, -5: 0})),
            (-6, -4, s1().step_values.pipe(concat, {-6: np.nan})),
            (-6, -2, s1().step_values.drop(-4).pipe(concat, {-6: np.nan, -2: -1.75})),
            (2, 4, s1().step_values.drop(3).pipe(concat, {2: np.nan, 4: 2.75})),
            (7, 8, s1().step_values.pipe(concat, {7: np.nan, 8: -0.5})),
            (9, 11, s1().step_values.drop(10).pipe(concat, {9: np.nan, 11: 0})),
            (10, 11, s1().step_values.drop(10).pipe(concat, {10: np.nan, 11: 0})),
            (11, 12, s1().step_values.pipe(concat, {11: np.nan, 12: 0})),
            (-5, 12, pd.Series({-5: np.nan, 12: 0})),
        ]
    ),
)
def test_mask_single_step(start, end, expected_step_values, tuple_mask):
    mask_ = (start, end) if tuple_mask else sc.Stairs(start=start, end=end)
    s = s1().mask(mask_)
    pd.testing.assert_series_equal(
        s.step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )
    assert s.initial_value == 0


# %%
@pytest.mark.parametrize(
    "start, end, expected_step_values, tuple_mask",
    _add_tuple_mask_option(
        [
            (-6, -5, s1().step_values),
            (-6, -4, s1().step_values),
            (-6, -2, s1().step_values.drop(-4).pipe(concat, {-2: -1.75})),
            (2, 4, s1().step_values.drop(3).pipe(concat, {2: np.nan, 4: 2.75})),
            (7, 8, s1().step_values.pipe(concat, {7: np.nan, 8: -0.5})),
            (9, 11, s1().step_values.drop(10).pipe(concat, {9: np.nan, 11: 0})),
            (10, 11, s1().step_values.drop(10).pipe(concat, {10: np.nan, 11: 0})),
            (11, 12, s1().step_values.pipe(concat, {11: np.nan, 12: 0})),
            (-5, 12, pd.Series({12: 0.0})),
        ],
    ),
)
def test_mask_single_step_initial_nan(start, end, expected_step_values, tuple_mask):
    mask_ = (None, -4) if tuple_mask else sc.Stairs(end=-4)
    nan_initial = s1().mask(mask_)
    mask_ = (start, end) if tuple_mask else sc.Stairs(start=start, end=end)
    s = nan_initial.mask(mask_)
    pd.testing.assert_series_equal(
        s.step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )
    assert np.isnan(s.initial_value)


def test_mask_on_stepless():
    pd.testing.assert_series_equal(
        sc.Stairs().mask((0, 2)).step_changes,
        pd.Series({0: np.nan, 2: 0.0}),
        check_names=False,
        check_index_type=False,
    )


def test_identical_nan_initial():
    assert sc.Stairs(initial_value=np.nan).identical(np.nan)


def test_value_sums_group_false(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.mask((-2, 0)).mask((6, 8)).value_sums(group=False),
        pd.Series(
            [2, 2, 1, 2, 2, 1, 2, 2],
            index=[-1.75, np.nan, -1.75, 0.25, 2.75, 2.0, np.nan, -0.5],
        ),
        check_names=False,
        check_index_type=False,
    )


def test_value_sums_dropna_false(s1_fix):
    pd.testing.assert_series_equal(
        s1_fix.mask((-2, 0)).mask((6, 8)).value_sums(dropna=False),
        pd.Series(
            [3, 2, 2, 1, 2, 4],
            index=[-1.75, -0.5, 0.25, 2.0, 2.75, np.nan],
        ),
        check_names=False,
        check_index_type=False,
    )


def test_isna(s1_fix):
    s = s1_fix.clip(None, 10).mask((-2, 0)).mask((4, 7)).isna()
    pd.testing.assert_series_equal(
        s.step_values,
        pd.Series(
            [1, 0, 1, 0, 1],
            index=[-2, 0, 4, 7, 10],
        ),
        check_names=False,
        check_index_type=False,
        check_dtype=False,
    )
    assert s.initial_value == 0


def test_notna(s1_fix):
    s = s1_fix.clip(None, 10).mask((-2, 0)).mask((4, 7)).notna()
    pd.testing.assert_series_equal(
        s.step_values,
        pd.Series(
            [0, 1, 0, 1, 0],
            index=[-2, 0, 4, 7, 10],
        ),
        check_names=False,
        check_index_type=False,
        check_dtype=False,
    )
    assert s.initial_value == 1
