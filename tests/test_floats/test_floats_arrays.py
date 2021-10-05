import numpy as np
import pandas as pd
import pytest

import staircase as sc
from staircase import Stairs


@pytest.fixture
def IS1():
    int_seq1 = Stairs(initial_value=0)
    int_seq1.layer(1, 10, 2)
    int_seq1.layer(-4, 5, -1.75)
    int_seq1.layer(3, 5, 2.5)
    int_seq1.layer(6, 7, -2.5)
    int_seq1.layer(7, 10, -2.5)
    return int_seq1


@pytest.fixture
def IS2():
    int_seq2 = Stairs(initial_value=0)
    int_seq2.layer(1, 7, -2.5)
    int_seq2.layer(8, 10, 5)
    int_seq2.layer(2, 5, 4.5)
    int_seq2.layer(2.5, 4, -2.5)
    int_seq2.layer(-2, 1, -1.75)
    return int_seq2


def test_mean_1(IS1, IS2):
    pd.testing.assert_series_equal(
        sc.mean({1: IS1, 2: IS2}).step_changes,
        pd.Series(
            {
                -4.0: -0.875,
                -2.0: -0.875,
                1.0: 0.625,
                2.0: 2.25,
                2.5: -1.25,
                3.0: 1.25,
                4.0: 1.25,
                5.0: -2.625,
                6.0: -1.25,
                7.0: 1.25,
                8.0: 2.5,
                10.0: -2.25,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_2(IS1, IS2):
    pd.testing.assert_series_equal(
        sc.mean(pd.Series([IS1, IS2])).step_changes,
        pd.Series(
            {
                -4.0: -0.875,
                -2.0: -0.875,
                1.0: 0.625,
                2.0: 2.25,
                2.5: -1.25,
                3.0: 1.25,
                4.0: 1.25,
                5.0: -2.625,
                6.0: -1.25,
                7.0: 1.25,
                8.0: 2.5,
                10.0: -2.25,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_3(IS1, IS2):
    pd.testing.assert_series_equal(
        sc.mean(np.array([IS1, IS2])).step_changes,
        pd.Series(
            {
                -4.0: -0.875,
                -2.0: -0.875,
                1.0: 0.625,
                2.0: 2.25,
                2.5: -1.25,
                3.0: 1.25,
                4.0: 1.25,
                5.0: -2.625,
                6.0: -1.25,
                7.0: 1.25,
                8.0: 2.5,
                10.0: -2.25,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_4(IS1, IS2):
    pd.testing.assert_series_equal(
        sc.mean([IS1, IS2]).step_changes,
        pd.Series(
            {
                -4.0: -0.875,
                -2.0: -0.875,
                1.0: 0.625,
                2.0: 2.25,
                2.5: -1.25,
                3.0: 1.25,
                4.0: 1.25,
                5.0: -2.625,
                6.0: -1.25,
                7.0: 1.25,
                8.0: 2.5,
                10.0: -2.25,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_5(IS1, IS2):
    pd.testing.assert_series_equal(
        sc.mean((IS1, IS2)).step_changes,
        pd.Series(
            {
                -4.0: -0.875,
                -2.0: -0.875,
                1.0: 0.625,
                2.0: 2.25,
                2.5: -1.25,
                3.0: 1.25,
                4.0: 1.25,
                5.0: -2.625,
                6.0: -1.25,
                7.0: 1.25,
                8.0: 2.5,
                10.0: -2.25,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_median_1(IS1, IS2):
    pd.testing.assert_series_equal(
        sc.median({1: IS1, 2: IS2, 3: IS1 + IS2}).step_changes,
        pd.Series(
            {
                -4.0: -1.75,
                1.0: -0.5,
                2.0: 4.25,
                2.5: -2.25,
                3.0: 2.5,
                4.0: 0.5,
                5.0: -3.25,
                6.0: -2.0,
                7.0: 2.0,
                8.0: 5.0,
                10.0: -4.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_max_1(IS1, IS2):
    pd.testing.assert_series_equal(
        sc.max({1: IS1, 2: IS2}).step_changes,
        pd.Series(
            {
                -2.0: -1.75,
                1.0: 2.0,
                2.0: 1.75,
                2.5: -1.75,
                3.0: 2.5,
                5.0: -0.75,
                6.0: -2.5,
                7.0: 0.5,
                8.0: 5.0,
                10.0: -5.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_min_1(IS1, IS2):
    pd.testing.assert_series_equal(
        sc.min({1: IS1, 2: IS2}).step_changes,
        pd.Series(
            {
                -4.0: -1.75,
                1.0: -0.75,
                2.0: 2.75,
                2.5: -0.75,
                4.0: 2.5,
                5.0: -4.5,
                7.0: 2.0,
                10.0: 0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_sum_1(IS1, IS2):
    pd.testing.assert_series_equal(
        sc.sum([IS1, IS2, IS1 + IS2]).step_values,
        pd.Series(
            {
                -4.0: -3.5,
                -2.0: -7.0,
                1.0: -4.5,
                2.0: 4.5,
                2.5: -0.5,
                3.0: 4.5,
                4.0: 9.5,
                5.0: -1.0,
                6.0: -6.0,
                7.0: -1.0,
                8.0: 9.0,
                10.0: 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_sample_1(IS1, IS2):
    sample = sc.sample([IS1, IS2], 3)
    assert sample.to_dict() == {3: {0: 2.75, 1: -0.5}}


def test_sample_2(IS1, IS2):
    sample = sc.sample(pd.Series([IS1, IS2]), [3, 6, 8])
    expected = {3: {0: 2.75, 1: -0.5}, 6: {0: -0.5, 1: -2.5}, 8: {0: -0.5, 1: 5.0}}
    assert sample.to_dict() == expected


def test_limit_1(IS1, IS2):
    limits = sc.limit(pd.Series([IS1, IS2]), [3, 6, 8], side="left")
    expected = {3: {0: 0.25, 1: -0.5}, 6: {0: 2.0, 1: -2.5}, 8: {0: -0.5, 1: 0.0}}
    assert limits.to_dict() == expected


def test_limit_2(IS1, IS2):
    limits = sc.limit(pd.Series([IS1, IS2]), [3, 6, 8], side="right")
    expected = {3: {0: 2.75, 1: -0.5}, 6: {0: -0.5, 1: -2.5}, 8: {0: -0.5, 1: 5.0}}
    assert limits.to_dict() == expected


def _matrix_close_to_zeros(x):
    return all(map(lambda v: np.isclose(v, 0, atol=0.00001), x.flatten()))


# np.cov(st1(np.linspace(-4,10,10000000)), st2(np.linspace(-4,10,10000000))) = array([[2.50159449, 0.28762709], [0.28762709, 6.02104508]])
def test_cov_matrix1(IS1, IS2):
    assert _matrix_close_to_zeros(
        sc.cov([IS1, IS2], where=(-4, 10)).values
        - np.array([[2.50159449, 0.28762709], [0.28762709, 6.02104508]])
    )


# np.cov(st1(np.linspace(0,12,10000000)), st2(np.linspace(0,12,10000000))) = array([[ 1.81727486, -0.25520783],[-0.25520783,  6.45312616]])
def test_cov_matrix2(IS1, IS2):
    assert _matrix_close_to_zeros(
        sc.cov([IS1, IS2], where=(0, 12)).values
        - np.array([[1.81727486, -0.25520783], [-0.25520783, 6.45312616]])
    )


# np.corrcoef(st1(np.linspace(-4,10,10000000)), st2(np.linspace(-4,10,10000000))) = array([[1, 0.07411146], [0.07411146, 1]])
def test_corr_matrix1(IS1, IS2):
    assert _matrix_close_to_zeros(
        sc.corr([IS1, IS2], where=(-4, 10)).values
        - np.array([[1, 0.07411146], [0.07411146, 1]])
    )


# np.corrcoef(st1(np.linspace(0,12,10000000)), st2(np.linspace(0,12,10000000))) = array([[1, -0.07452442], [-0.07452442,  1]])
def test_corr_matrix2(IS1, IS2):
    assert _matrix_close_to_zeros(
        sc.corr([IS1, IS2], where=(0, 12)).values
        - np.array([[1, -0.07452442], [-0.07452442, 1]])
    )


@pytest.mark.parametrize(
    "func",
    [sc.sum, sc.max, sc.min, sc.median, sc.mean],
)
def test_aggregation_with_closed_right(func):
    # GH117
    s = sc.Stairs(start=0, end=1, closed="right")
    assert func([s, s]).number_of_steps == 2
