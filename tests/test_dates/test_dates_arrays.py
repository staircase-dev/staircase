import numpy as np
import pandas as pd
import pytest
import pytz

import staircase as sc
from staircase import Stairs


def pytest_generate_tests(metafunc):
    if "date_func" in metafunc.fixturenames:
        metafunc.parametrize(
            "date_func",
            ["pandas", "pydatetime", "numpy", "pandas_tz", "pydatetime_tz"],
            indirect=True,
        )


@pytest.fixture
def date_func(request):
    # returns a func which takes a pandas timestamp
    if request.param == "pandas":
        return lambda x: x
    elif request.param == "pydatetime":
        return pd.Timestamp.to_pydatetime
    elif request.param == "numpy":
        return pd.Timestamp.to_datetime64
    elif request.param == "pandas_tz":
        return lambda ts: pd.Timestamp.tz_localize(
            ts, pytz.timezone("Australia/Sydney")
        )
    elif request.param == "pydatetime_tz":
        return lambda ts: (
            pd.Timestamp.tz_localize(
                ts, pytz.timezone("Australia/Sydney")
            ).to_pydatetime()
        )
    else:
        assert False, "should not happen"


def timestamp(*args, date_func, **kwargs):
    ts = pd.Timestamp(*args, **kwargs)
    return date_func(ts)


# -4 27th
# -3 28th
# -2 29th
# -1 30th
# 0 31st dec
# 1  1st jan


def s1(date_func):
    int_seq1 = Stairs(initial_value=0)
    int_seq1.layer(
        timestamp(2020, 1, 1, date_func=date_func),
        timestamp(2020, 1, 10, date_func=date_func),
        2,
    ).layer(
        timestamp(2019, 12, 27, date_func=date_func),
        timestamp(2020, 1, 5, date_func=date_func),
        -1.75,
    )
    int_seq1.layer(
        timestamp(2020, 1, 3, date_func=date_func),
        timestamp(2020, 1, 5, date_func=date_func),
        2.5,
    )
    int_seq1.layer(
        timestamp(2020, 1, 6, date_func=date_func),
        timestamp(2020, 1, 7, date_func=date_func),
        -2.5,
    )
    int_seq1.layer(
        timestamp(2020, 1, 7, date_func=date_func),
        timestamp(2020, 1, 10, date_func=date_func),
        -2.5,
    )
    return int_seq1


def s2(date_func):
    int_seq2 = Stairs(initial_value=0)
    int_seq2.layer(
        timestamp(2020, 1, 1, date_func=date_func),
        timestamp(2020, 1, 7, date_func=date_func),
        -2.5,
    )
    int_seq2.layer(
        timestamp(2020, 1, 8, date_func=date_func),
        timestamp(2020, 1, 10, date_func=date_func),
        5,
    )
    int_seq2.layer(
        timestamp(2020, 1, 2, date_func=date_func),
        timestamp(2020, 1, 5, date_func=date_func),
        4.5,
    )
    int_seq2.layer(
        timestamp(2020, 1, 2, 12, date_func=date_func),
        timestamp(2020, 1, 4, date_func=date_func),
        -2.5,
    ).layer(
        timestamp(2019, 12, 29, date_func=date_func),
        timestamp(2020, 1, 1, date_func=date_func),
        -1.75,
    )
    return int_seq2


def test_mean_1(date_func):
    pd.testing.assert_series_equal(
        sc.mean({1: s1(date_func), 2: s2(date_func)}).step_changes,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -0.875,
                timestamp(2019, 12, 29, date_func=date_func): -0.875,
                timestamp(2020, 1, 1, date_func=date_func): 0.625,
                timestamp(2020, 1, 2, date_func=date_func): 2.25,
                timestamp(2020, 1, 2, 12, date_func=date_func): -1.25,
                timestamp(2020, 1, 3, date_func=date_func): 1.25,
                timestamp(2020, 1, 4, date_func=date_func): 1.25,
                timestamp(2020, 1, 5, date_func=date_func): -2.625,
                timestamp(2020, 1, 6, date_func=date_func): -1.25,
                timestamp(2020, 1, 7, date_func=date_func): 1.25,
                timestamp(2020, 1, 8, date_func=date_func): 2.5,
                timestamp(2020, 1, 10, date_func=date_func): -2.25,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_2(date_func):
    pd.testing.assert_series_equal(
        sc.mean(pd.Series([s1(date_func), s2(date_func)])).step_changes,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -0.875,
                timestamp(2019, 12, 29, date_func=date_func): -0.875,
                timestamp(2020, 1, 1, date_func=date_func): 0.625,
                timestamp(2020, 1, 2, date_func=date_func): 2.25,
                timestamp(2020, 1, 2, 12, date_func=date_func): -1.25,
                timestamp(2020, 1, 3, date_func=date_func): 1.25,
                timestamp(2020, 1, 4, date_func=date_func): 1.25,
                timestamp(2020, 1, 5, date_func=date_func): -2.625,
                timestamp(2020, 1, 6, date_func=date_func): -1.25,
                timestamp(2020, 1, 7, date_func=date_func): 1.25,
                timestamp(2020, 1, 8, date_func=date_func): 2.5,
                timestamp(2020, 1, 10, date_func=date_func): -2.25,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_3(date_func):
    pd.testing.assert_series_equal(
        sc.mean(np.array([s1(date_func), s2(date_func)])).step_changes,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -0.875,
                timestamp(2019, 12, 29, date_func=date_func): -0.875,
                timestamp(2020, 1, 1, date_func=date_func): 0.625,
                timestamp(2020, 1, 2, date_func=date_func): 2.25,
                timestamp(2020, 1, 2, 12, date_func=date_func): -1.25,
                timestamp(2020, 1, 3, date_func=date_func): 1.25,
                timestamp(2020, 1, 4, date_func=date_func): 1.25,
                timestamp(2020, 1, 5, date_func=date_func): -2.625,
                timestamp(2020, 1, 6, date_func=date_func): -1.25,
                timestamp(2020, 1, 7, date_func=date_func): 1.25,
                timestamp(2020, 1, 8, date_func=date_func): 2.5,
                timestamp(2020, 1, 10, date_func=date_func): -2.25,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_4(date_func):
    pd.testing.assert_series_equal(
        sc.mean([s1(date_func), s2(date_func)]).step_changes,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -0.875,
                timestamp(2019, 12, 29, date_func=date_func): -0.875,
                timestamp(2020, 1, 1, date_func=date_func): 0.625,
                timestamp(2020, 1, 2, date_func=date_func): 2.25,
                timestamp(2020, 1, 2, 12, date_func=date_func): -1.25,
                timestamp(2020, 1, 3, date_func=date_func): 1.25,
                timestamp(2020, 1, 4, date_func=date_func): 1.25,
                timestamp(2020, 1, 5, date_func=date_func): -2.625,
                timestamp(2020, 1, 6, date_func=date_func): -1.25,
                timestamp(2020, 1, 7, date_func=date_func): 1.25,
                timestamp(2020, 1, 8, date_func=date_func): 2.5,
                timestamp(2020, 1, 10, date_func=date_func): -2.25,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_5(date_func):
    pd.testing.assert_series_equal(
        sc.mean((s1(date_func), s2(date_func))).step_changes,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -0.875,
                timestamp(2019, 12, 29, date_func=date_func): -0.875,
                timestamp(2020, 1, 1, date_func=date_func): 0.625,
                timestamp(2020, 1, 2, date_func=date_func): 2.25,
                timestamp(2020, 1, 2, 12, date_func=date_func): -1.25,
                timestamp(2020, 1, 3, date_func=date_func): 1.25,
                timestamp(2020, 1, 4, date_func=date_func): 1.25,
                timestamp(2020, 1, 5, date_func=date_func): -2.625,
                timestamp(2020, 1, 6, date_func=date_func): -1.25,
                timestamp(2020, 1, 7, date_func=date_func): 1.25,
                timestamp(2020, 1, 8, date_func=date_func): 2.5,
                timestamp(2020, 1, 10, date_func=date_func): -2.25,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_median_1(date_func):
    pd.testing.assert_series_equal(
        sc.median(
            [s1(date_func), s2(date_func), s1(date_func) + s2(date_func)]
        ).step_changes,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -1.75,
                timestamp(2020, 1, 1, date_func=date_func): -0.5,
                timestamp(2020, 1, 2, date_func=date_func): 4.25,
                timestamp(2020, 1, 2, 12, date_func=date_func): -2.25,
                timestamp(2020, 1, 3, date_func=date_func): 2.5,
                timestamp(2020, 1, 4, date_func=date_func): 0.5,
                timestamp(2020, 1, 5, date_func=date_func): -3.25,
                timestamp(2020, 1, 6, date_func=date_func): -2.0,
                timestamp(2020, 1, 7, date_func=date_func): 2.0,
                timestamp(2020, 1, 8, date_func=date_func): 5.0,
                timestamp(2020, 1, 10, date_func=date_func): -4.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_max_1(date_func):
    pd.testing.assert_series_equal(
        sc.max([s1(date_func), s2(date_func)]).step_changes,
        pd.Series(
            {
                timestamp(2019, 12, 29, date_func=date_func): -1.75,
                timestamp(2020, 1, 1, date_func=date_func): 2.0,
                timestamp(2020, 1, 2, date_func=date_func): 1.75,
                timestamp(2020, 1, 2, 12, date_func=date_func): -1.75,
                timestamp(2020, 1, 3, date_func=date_func): 2.5,
                timestamp(2020, 1, 5, date_func=date_func): -0.75,
                timestamp(2020, 1, 6, date_func=date_func): -2.5,
                timestamp(2020, 1, 7, date_func=date_func): 0.5,
                timestamp(2020, 1, 8, date_func=date_func): 5.0,
                timestamp(2020, 1, 10, date_func=date_func): -5.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_min_1(date_func):
    pd.testing.assert_series_equal(
        sc.min([s1(date_func), s2(date_func)]).step_changes,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -1.75,
                timestamp(2020, 1, 1, date_func=date_func): -0.75,
                timestamp(2020, 1, 2, date_func=date_func): 2.75,
                timestamp(2020, 1, 2, 12, date_func=date_func): -0.75,
                timestamp(2020, 1, 4, date_func=date_func): 2.5,
                timestamp(2020, 1, 5, date_func=date_func): -4.5,
                timestamp(2020, 1, 7, date_func=date_func): 2.0,
                timestamp(2020, 1, 10, date_func=date_func): 0.5,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_sum_1(date_func):
    pd.testing.assert_series_equal(
        sc.sum(
            [s1(date_func), s2(date_func), s1(date_func) + s2(date_func)]
        ).step_values,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -3.5,
                timestamp(2019, 12, 29, date_func=date_func): -7.0,
                timestamp(2020, 1, 1, date_func=date_func): -4.5,
                timestamp(2020, 1, 2, date_func=date_func): 4.5,
                timestamp(2020, 1, 2, 12, date_func=date_func): -0.5,
                timestamp(2020, 1, 3, date_func=date_func): 4.5,
                timestamp(2020, 1, 4, date_func=date_func): 9.5,
                timestamp(2020, 1, 5, date_func=date_func): -1.0,
                timestamp(2020, 1, 6, date_func=date_func): -6.0,
                timestamp(2020, 1, 7, date_func=date_func): -1.0,
                timestamp(2020, 1, 8, date_func=date_func): 9.0,
                timestamp(2020, 1, 10, date_func=date_func): 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_sample_1(date_func):
    sample = sc.sample(
        [s1(date_func), s2(date_func)], timestamp(2020, 1, 3, date_func=date_func)
    )
    expected = pd.DataFrame({timestamp(2020, 1, 3, date_func=date_func): [2.75, -0.5]})
    pd.testing.assert_frame_equal(
        sample,
        expected,
        check_names=False,
        check_index_type=False,
    )


def test_sample_2(date_func):
    ts3 = timestamp(2020, 1, 3, date_func=date_func)
    ts6 = timestamp(2020, 1, 6, date_func=date_func)
    ts8 = timestamp(2020, 1, 8, date_func=date_func)
    sample = sc.sample([s1(date_func), s2(date_func)], [ts3, ts6, ts8])
    expected = pd.DataFrame(
        {
            ts3: [2.75, -0.5],
            ts6: [-0.5, -2.5],
            ts8: [-0.5, 5.0],
        }
    )
    pd.testing.assert_frame_equal(
        sample,
        expected,
        check_names=False,
        check_index_type=False,
    )


def test_limit_1(date_func):
    ts3 = timestamp(2020, 1, 3, date_func=date_func)
    ts6 = timestamp(2020, 1, 6, date_func=date_func)
    ts8 = timestamp(2020, 1, 8, date_func=date_func)
    limits = sc.limit([s1(date_func), s2(date_func)], [ts3, ts6, ts8], side="left")
    expected = pd.DataFrame({ts3: [0.25, -0.5], ts6: [2.0, -2.5], ts8: [-0.5, 0.0]})
    pd.testing.assert_frame_equal(
        limits,
        expected,
        check_names=False,
        check_index_type=False,
    )


def test_limit_2(date_func):
    ts3 = timestamp(2020, 1, 3, date_func=date_func)
    ts6 = timestamp(2020, 1, 6, date_func=date_func)
    ts8 = timestamp(2020, 1, 8, date_func=date_func)
    limits = sc.limit([s1(date_func), s2(date_func)], [ts3, ts6, ts8], side="right")
    expected = pd.DataFrame({ts3: [2.75, -0.5], ts6: [-0.5, -2.5], ts8: [-0.5, 5.0]})
    pd.testing.assert_frame_equal(
        limits,
        expected,
        check_names=False,
        check_index_type=False,
    )


def _matrix_close_to_zeros(x):
    return all(map(lambda v: np.isclose(v, 0, atol=0.00001), x.flatten()))


# # np.cov(st1(np.linspace(-4,10,10000000)), st2(np.linspace(-4,10,10000000))) = array([[2.50159449, 0.28762709], [0.28762709, 6.02104508]])
def test_cov_matrix1(date_func):
    assert _matrix_close_to_zeros(
        sc.cov(
            [s1(date_func), s2(date_func)],
            where=(
                timestamp(2019, 12, 27, date_func=date_func),
                timestamp(2020, 1, 10, date_func=date_func),
            ),
        ).values
        - np.array([[2.50159449, 0.28762709], [0.28762709, 6.02104508]])
    )


# # np.cov(st1(np.linspace(0,12,10000000)), st2(np.linspace(0,12,10000000))) = array([[ 1.81727486, -0.25520783],[-0.25520783,  6.45312616]])
def test_cov_matrix2(date_func):
    assert _matrix_close_to_zeros(
        sc.cov(
            [s1(date_func), s2(date_func)],
            where=(
                timestamp(2019, 12, 31, date_func=date_func),
                timestamp(2020, 1, 12, date_func=date_func),
            ),
        ).values
        - np.array([[1.81727486, -0.25520783], [-0.25520783, 6.45312616]])
    )


# # np.corrcoef(st1(np.linspace(-4,10,10000000)), st2(np.linspace(-4,10,10000000))) = array([[1, 0.07411146], [0.07411146, 1]])
def test_corr_matrix1(date_func):
    assert _matrix_close_to_zeros(
        sc.corr(
            [s1(date_func), s2(date_func)],
            where=(
                timestamp(2019, 12, 27, date_func=date_func),
                timestamp(2020, 1, 10, date_func=date_func),
            ),
        ).values
        - np.array([[1, 0.07411146], [0.07411146, 1]])
    )


# # np.corrcoef(st1(np.linspace(0,12,10000000)), st2(np.linspace(0,12,10000000))) = array([[1, -0.07452442], [-0.07452442,  1]])
def test_corr_matrix2(date_func):
    assert _matrix_close_to_zeros(
        sc.corr(
            [s1(date_func), s2(date_func)],
            where=(
                timestamp(2019, 12, 31, date_func=date_func),
                timestamp(2020, 1, 12, date_func=date_func),
            ),
        ).values
        - np.array([[1, -0.07452442], [-0.07452442, 1]])
    )


@pytest.mark.parametrize(
    "func",
    [sc.sum, sc.max, sc.min, sc.median, sc.mean],
)
@pytest.mark.parametrize(
    "swap_order",
    [False, True],
)
def test_aggregation_with_constant_stairs(func, swap_order):
    # GH119 - no need to test result, just that it is passing
    s1 = sc.Stairs().layer(pd.Timestamp("2020"), pd.Timestamp("2021"))
    s2 = sc.Stairs()
    arr = [s2, s1] if swap_order else [s1, s2]
    func(arr)
