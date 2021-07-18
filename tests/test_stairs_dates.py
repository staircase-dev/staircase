import itertools
from datetime import datetime

import numpy as np
import pandas as pd
import pytest
import pytz

import staircase.test_data as test_data
from staircase import Stairs
from staircase.constants import inf


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


def assert_expected_type(stairs, date_func):
    if stairs._data is None:
        return
    example_type = timestamp(2020, 1, 1, date_func=date_func)
    example_type = pd.Timestamp(
        example_type
    )  # pandas natively converts datetimes to timestamps
    assert all(
        [type(example_type) == type(x) for x in stairs._data.index]
    ), "Unexpected type in step points"
    if isinstance(example_type, (pd.Timestamp, datetime)):
        assert all(
            [example_type.tzinfo == x.tzinfo for x in stairs._data.index]
        ), "Unexpected timezone in step points"


def _compare_iterables(it1, it2):
    it1 = [i for i in it1 if i is not None]
    it2 = [i for i in it2 if i is not None]
    for e1, e2 in zip(it1, it2):
        if e1 != e2:
            return False
    return True


def s1(date_func):
    int_seq1 = Stairs(initial_value=0)
    int_seq1.layer(
        timestamp(2020, 1, 1, date_func=date_func),
        timestamp(2020, 1, 10, date_func=date_func),
        2,
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
    )
    return int_seq2


def s3(date_func):  # boolean
    int_seq = Stairs(initial_value=0)
    int_seq.layer(
        timestamp(2020, 1, 10, date_func=date_func),
        timestamp(2020, 1, 30, date_func=date_func),
        1,
    )
    int_seq.layer(
        timestamp(2020, 1, 12, date_func=date_func),
        timestamp(2020, 1, 13, date_func=date_func),
        -1,
    )
    int_seq.layer(
        timestamp(2020, 1, 15, date_func=date_func),
        timestamp(2020, 1, 18, date_func=date_func),
        -1,
    )
    int_seq.layer(
        timestamp(2020, 1, 20, 12, date_func=date_func),
        timestamp(2020, 1, 21, date_func=date_func),
        -1,
    )
    int_seq.layer(
        timestamp(2020, 1, 23, date_func=date_func),
        timestamp(2020, 1, 23, 12, date_func=date_func),
        -1,
    )
    int_seq.layer(
        timestamp(2020, 1, 27, date_func=date_func),
        timestamp(2020, 1, 29, 12, date_func=date_func),
        -1,
    )
    return int_seq


def s4(date_func):  # boolean
    int_seq = Stairs(initial_value=0)
    int_seq.layer(
        timestamp(2020, 1, 9, date_func=date_func),
        timestamp(2020, 1, 29, date_func=date_func),
        1,
    )
    int_seq.layer(
        timestamp(2020, 1, 10, 12, date_func=date_func),
        timestamp(2020, 1, 12, date_func=date_func),
        -1,
    )
    int_seq.layer(
        timestamp(2020, 1, 12, 12, date_func=date_func),
        timestamp(2020, 1, 13, date_func=date_func),
        -1,
    )
    int_seq.layer(
        timestamp(2020, 1, 20, date_func=date_func),
        timestamp(2020, 1, 23, date_func=date_func),
        -1,
    )
    int_seq.layer(
        timestamp(2020, 1, 26, date_func=date_func),
        timestamp(2020, 1, 26, 12, date_func=date_func),
        -1,
    )
    int_seq.layer(
        timestamp(2020, 1, 27, date_func=date_func),
        timestamp(2020, 1, 28, 12, date_func=date_func),
        -1,
    )
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


def test_max_dates_1(date_func):
    assert s1(date_func).max() == 4.5, "Expected maximum to be 4.5"


def test_max_dates_2(date_func):
    assert (
        s1(date_func).max((None, timestamp(2020, 1, 2, date_func=date_func))) == 2
    ), "Expected maximum to be 2"


def test_max_dates_3(date_func):
    assert (
        s1(date_func).max((timestamp(2020, 1, 5, 12, date_func=date_func), None)) == 2
    ), "Expected maximum to be 2"


def test_max_dates_4(date_func):
    assert (
        s1(date_func).max(
            (
                timestamp(2020, 1, 8, date_func=date_func),
                timestamp(2020, 1, 9, date_func=date_func),
            )
        )
        == -0.5
    ), "Expected maximum to be -0.5"


def test_min_dates_1(date_func):
    assert s1(date_func).min() == -0.5, "Expected minimum to be -0.5"


def test_min_dates_2(date_func):
    assert (
        s1(date_func).min((None, timestamp(2020, 1, 4, date_func=date_func))) == 0
    ), "Expected minimum to be 0"


def test_min_dates_3(date_func):
    assert (
        s1(date_func).min((timestamp(2020, 1, 10, 12, date_func=date_func), None)) == 0
    ), "Expected minimum to be 0"


def test_min_dates_4(date_func):
    assert (
        s1(date_func).min(
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 4, 12, date_func=date_func),
            )
        )
        == 4.5
    ), "Expected minimum to be 4.5"


def test_mode_dates_1(date_func):
    assert s1(date_func).mode() == -0.5, "Expected mode to be -0.5"


def test_mode_dates_2(date_func):
    assert (
        s1(date_func).mode((None, timestamp(2020, 1, 4, date_func=date_func))) == 2
    ), "Expected mode to be 2"


def test_mode_dates_3(date_func):
    assert (
        s1(date_func).mode((timestamp(2019, 12, 27, date_func=date_func), None)) == 0
    ), "Expected mode to be 0"


def test_mode_dates_4(date_func):
    assert (
        s1(date_func).mode(
            (
                timestamp(2020, 1, 4, 12, date_func=date_func),
                timestamp(2020, 1, 6, 12, date_func=date_func),
            )
        )
        == 2
    ), "Expected mode to be 2"


def test_median_dates_1(date_func):
    assert s1(date_func).median() == 2, "Expected median to be 2"


def test_median_dates_2(date_func):
    assert (
        s1(date_func).median((None, timestamp(2020, 1, 17, date_func=date_func))) == 0
    ), "Expected median to be 0"


def test_median_dates_3(date_func):
    assert (
        s1(date_func).median((timestamp(2020, 1, 3, date_func=date_func), None)) == -0.5
    ), "Expected median to be -0.5"


def test_median_dates_4(date_func):
    assert (
        s1(date_func).median(
            (
                timestamp(2020, 1, 4, 12, date_func=date_func),
                timestamp(2020, 1, 6, 12, date_func=date_func),
            )
        )
        == 2
    ), "Expected median to be 2"


def test_mean_dates_1(date_func):
    assert abs(s1(date_func).mean() - 13 / 9) <= 0.00001, "Expected mean to be 13/9"


def test_mean_dates_2(date_func):
    assert (
        s1(date_func).mean((None, timestamp(2020, 1, 6, date_func=date_func))) == 3
    ), "Expected mean to be 3"


def test_mean_dates_3(date_func):
    assert (
        s1(date_func).mean((timestamp(2020, 1, 4, date_func=date_func), None)) == 0.75
    ), "Expected mean to be 0.75"


def test_mean_dates_4(date_func):
    assert (
        s1(date_func).mean(
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 8, date_func=date_func),
            )
        )
        == 1.375
    ), "Expected mean to be 1.375"


def test_integrate_dates_1(date_func):
    assert (
        s1(date_func).integrate() / pd.Timedelta("1 D") == 13
    ), "Expected integral to be 13 days"


def test_integrate_dates_2(date_func):
    assert (
        s1(date_func).integrate((None, timestamp(2020, 1, 6, date_func=date_func)))
        / pd.Timedelta("1 D")
        == 15
    ), "Expected integral to be 15 days"


def test_integrate_dates_3(date_func):
    assert (
        s1(date_func).integrate((timestamp(2020, 1, 4, date_func=date_func), None))
        / pd.Timedelta("1 H")
        == 108
    ), "Expected integral to be 108 hours"


def test_integrate_dates_4(date_func):
    assert (
        s1(date_func).integrate(
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 8, date_func=date_func),
            )
        )
        / pd.Timedelta("1 H")
        == 132
    ), "Expected integral to be 132 hours"


def test_integral_and_mean_dates_1(date_func):
    integral, mean = s1(date_func).get_integral_and_mean()
    assert abs(mean - 13 / 9) <= 0.00001, "Expected mean to be 13/9"
    assert integral / pd.Timedelta("1 H") == 312, "Expected integral to be 312 hours"


def test_integral_and_mean_dates_2(date_func):
    integral, mean = s1(date_func).get_integral_and_mean(
        (None, timestamp(2020, 1, 6, date_func=date_func))
    )
    assert mean == 3, "Expected mean to be 3"
    assert integral / pd.Timedelta("1 D") == 15, "Expected integral to be 15"


def test_integral_and_mean_3(date_func):
    integral, mean = s1(date_func).get_integral_and_mean(
        (timestamp(2020, 1, 4, date_func=date_func), None)
    )
    assert mean == 0.75, "Expected mean to be 0.75"
    assert integral / pd.Timedelta("1 H") == 108, "Expected integral to be 108 hours"


def test_integral_and_mean_dates_4(date_func):
    integral, mean = s1(date_func).get_integral_and_mean(
        (
            timestamp(2020, 1, 4, date_func=date_func),
            timestamp(2020, 1, 8, date_func=date_func),
        )
    )
    assert mean == 1.375, "Expected mean to be 1.375"
    assert integral / pd.Timedelta("1 H") == 132, "Expected integral to be 132 hours"


def test_percentile_dates_1(date_func):
    assert s1(date_func).percentile(20) == -0.5, "Expected 20th percentile to be -0.5"
    assert s1(date_func).percentile(40) == -0.5, "Expected 40th percentile to be -0.5"
    assert s1(date_func).percentile(60) == 2, "Expected 60th percentile to be 2"
    assert s1(date_func).percentile(80) == 4.5, "Expected 80th percentile to be 4.5"


def test_percentile_dates_2(date_func):
    assert (
        s1(date_func).percentile(
            20, where=(None, timestamp(2020, 1, 6, date_func=date_func))
        )
        == 2
    ), "Expected 20th percentile to be 2"
    assert (
        s1(date_func).percentile(
            40, where=(None, timestamp(2020, 1, 6, date_func=date_func))
        )
        == 2
    ), "Expected 40th percentile to be 2"
    assert (
        s1(date_func).percentile(
            60, where=(None, timestamp(2020, 1, 6, date_func=date_func))
        )
        == 3.25
    ), "Expected 60th percentile to be 3.25"
    assert (
        s1(date_func).percentile(
            80, where=(None, timestamp(2020, 1, 6, date_func=date_func))
        )
        == 4.5
    ), "Expected 80th percentile to be 4.5"


def test_percentile_dates_3(date_func):
    assert (
        s1(date_func).percentile(20, (timestamp(2020, 1, 4, date_func=date_func), None))
        == -0.5
    ), "Expected 20th percentile to be -0.5"
    assert (
        s1(date_func).percentile(40, (timestamp(2020, 1, 4, date_func=date_func), None))
        == -0.5
    ), "Expected 40th percentile to be -0.5"
    assert (
        s1(date_func).percentile(60, (timestamp(2020, 1, 4, date_func=date_func), None))
        == -0.5
    ), "Expected 60th percentile to be -0.5"
    assert (
        s1(date_func).percentile(80, (timestamp(2020, 1, 4, date_func=date_func), None))
        == 2
    ), "Expected 80th percentile to be 2"


def test_percentile_dates_4(date_func):
    assert (
        s1(date_func).percentile(
            20,
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 8, date_func=date_func),
            ),
        )
        == -0.5
    ), "Expected 20th percentile to be -0.5"
    assert (
        s1(date_func).percentile(
            40,
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 8, date_func=date_func),
            ),
        )
        == -0.5
    ), "Expected 40th percentile to be -0.5"
    assert (
        s1(date_func).percentile(
            60,
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 8, date_func=date_func),
            ),
        )
        == 2
    ), "Expected 60th percentile to be 2"
    assert (
        s1(date_func).percentile(
            80,
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 8, date_func=date_func),
            ),
        )
        == 4.5
    ), "Expected 80th percentile to be 4.5"


def test_get_percentiles_dates_1(date_func):
    expected_step_values = pd.Series(
        [-0.5, 2.0, 4.5, 4.5], index=[0, 44.444444, 77.77777778, 100]
    )
    pd.testing.assert_series_equal(
        s1(date_func).get_percentiles().step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )


def test_get_percentiles_dates_2(date_func):
    expected_step_values = pd.Series([2, 4.5, 4.5], index=[0, 60, 100])
    pd.testing.assert_series_equal(
        s1(date_func)
        .get_percentiles((None, timestamp(2020, 1, 6, date_func=date_func)))
        .step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )


def test_get_percentiles_dates_3(date_func):
    expected_step_values = pd.Series(
        [-0.5, 2.0, 4.5, 4.5], index=[0, 66.6666666667, 83.333333333, 100]
    )
    pd.testing.assert_series_equal(
        s1(date_func)
        .get_percentiles((timestamp(2020, 1, 4, date_func=date_func), None))
        .step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )


def test_get_percentiles_dates_4(date_func):
    expected_step_values = pd.Series([-0.5, 2.0, 4.5, 4.5], index=[0, 50, 75, 100])
    pd.testing.assert_series_equal(
        s1(date_func)
        .get_percentiles(
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 8, date_func=date_func),
            )
        )
        .step_values,
        expected_step_values,
        check_names=False,
        check_index_type=False,
    )


def test_plot(date_func):
    s1(date_func).plot()


# def test_resample_dates_1(date_func):
#     assert s1(date_func).resample(timestamp(2020, 1, 4)).step_changes == {
#         timestamp(2020, 1, 4).tz_localize(s1(date_func)._keys()[0].tz): 4.5
#     }


# def test_resample_dates_2(date_func):
#     assert s1(date_func).resample(timestamp(2020, 1, 6), how="right").step_changes == {
#         timestamp(2020, 1, 6).tz_localize(s1(date_func)._keys()[0].tz): -0.5
#     }


# def test_resample_dates_3(date_func):
#     assert s1(date_func).resample(timestamp(2020, 1, 6), how="left").step_changes == {
#         timestamp(2020, 1, 6).tz_localize(s1(date_func)._keys()[0].tz): 2
#     }


# def test_resample_dates_4(date_func):
#     assert s1(date_func).resample(
#         [timestamp(2020, 1, 4), timestamp(2020, 1, 6)]
#     ).step_changes == {
#         timestamp(2020, 1, 4).tz_localize(s1(date_func)._keys()[0].tz): 4.5,
#         timestamp(2020, 1, 6).tz_localize(s1(date_func)._keys()[0].tz): -5.0,
#     }


# def test_resample_dates_5(date_func):
#     assert s1(date_func).resample(
#         [timestamp(2020, 1, 4), timestamp(2020, 1, 6)], how="right"
#     ).step_changes == {
#         timestamp(2020, 1, 4).tz_localize(s1(date_func)._keys()[0].tz): 4.5,
#         timestamp(2020, 1, 6).tz_localize(s1(date_func)._keys()[0].tz): -5.0,
#     }


# def test_resample_dates_6(date_func):
#     assert s1(date_func).resample(
#         [timestamp(2020, 1, 4), timestamp(2020, 1, 6)], how="left"
#     ).step_changes == {
#         timestamp(2020, 1, 4).tz_localize(s1(date_func)._keys()[0].tz): 4.5,
#         timestamp(2020, 1, 6).tz_localize(s1(date_func)._keys()[0].tz): -2.5,
#     }


def test_sample_dates_1(date_func):
    assert s1(date_func).sample(timestamp(2020, 1, 6, date_func=date_func)) == -0.5


def test_limit_dates_1(date_func):
    assert (
        s1(date_func).limit(timestamp(2020, 1, 6, date_func=date_func), side="right")
        == -0.5
    )


def test_limit_dates_2(date_func):
    assert (
        s1(date_func).limit(timestamp(2020, 1, 6, date_func=date_func), side="left")
        == 2
    )


def test_sample_dates_4(date_func):
    assert _compare_iterables(
        s1(date_func).sample(
            [
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 6, date_func=date_func),
            ]
        ),
        [4.5, -0.5],
    )


def test_limit_dates_3(date_func):
    assert _compare_iterables(
        s1(date_func).limit(
            [
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 6, date_func=date_func),
            ],
            side="right",
        ),
        [4.5, -0.5],
    )


def test_limit_dates_4(date_func):
    assert _compare_iterables(
        s1(date_func).limit(
            [
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 6, date_func=date_func),
            ],
            side="left",
        ),
        [4.5, 2],
    )


def test_step_changes_dates(date_func):
    expected_step_changes = pd.Series(
        [2, 2.5, -2.5, -2.5, 0.5],
        index=[
            timestamp("2020-1-1", date_func=date_func),
            timestamp("2020-1-3", date_func=date_func),
            timestamp("2020-1-5", date_func=date_func),
            timestamp("2020-1-6", date_func=date_func),
            timestamp("2020-1-10", date_func=date_func),
        ],
    )
    pd.testing.assert_series_equal(
        s1(date_func).step_changes,
        expected_step_changes,
        check_names=False,
        check_index_type=False,
    )


def test_dataframe_dates(date_func):
    ans = pd.DataFrame(
        {
            "start": [
                -inf,
                timestamp("2020-01-01", date_func=date_func),
                timestamp("2020-01-03", date_func=date_func),
                timestamp("2020-01-05", date_func=date_func),
                timestamp("2020-01-06", date_func=date_func),
                timestamp("2020-01-10", date_func=date_func),
            ],
            "end": [
                timestamp("2020-01-01", date_func=date_func),
                timestamp("2020-01-03", date_func=date_func),
                timestamp("2020-01-05", date_func=date_func),
                timestamp("2020-01-06", date_func=date_func),
                timestamp("2020-01-10", date_func=date_func),
                inf,
            ],
            "value": [0, 2, 4.5, 2, -0.5, 0],
        }
    )
    pd.testing.assert_frame_equal(s1(date_func).to_frame(), ans)


def test_add_dates(date_func):
    expected_step_changes = pd.Series(
        {
            timestamp("2020-01-01 00:00:00", date_func=date_func): -0.5,
            timestamp("2020-01-02 00:00:00", date_func=date_func): 4.5,
            timestamp("2020-01-02 12:00:00", date_func=date_func): -2.5,
            timestamp("2020-01-03 00:00:00", date_func=date_func): 2.5,
            timestamp("2020-01-04 00:00:00", date_func=date_func): 2.5,
            timestamp("2020-01-05 00:00:00", date_func=date_func): -7.0,
            timestamp("2020-01-06 00:00:00", date_func=date_func): -2.5,
            timestamp("2020-01-07 00:00:00", date_func=date_func): 2.5,
            timestamp("2020-01-08 00:00:00", date_func=date_func): 5,
            timestamp("2020-01-10 00:00:00", date_func=date_func): -4.5,
        }
    )
    result = s1(date_func) + s2(date_func)
    pd.testing.assert_series_equal(
        result.step_changes,
        expected_step_changes,
        check_names=False,
        check_index_type=False,
    )
    assert_expected_type(result, date_func)


def test_subtract_dates(date_func):
    expected_step_changes = pd.Series(
        {
            timestamp("2020-01-01 00:00:00", date_func=date_func): 4.5,
            timestamp("2020-01-02 00:00:00", date_func=date_func): -4.5,
            timestamp("2020-01-02 12:00:00", date_func=date_func): 2.5,
            timestamp("2020-01-03 00:00:00", date_func=date_func): 2.5,
            timestamp("2020-01-04 00:00:00", date_func=date_func): -2.5,
            timestamp("2020-01-05 00:00:00", date_func=date_func): 2.0,
            timestamp("2020-01-06 00:00:00", date_func=date_func): -2.5,
            timestamp("2020-01-07 00:00:00", date_func=date_func): -2.5,
            timestamp("2020-01-08 00:00:00", date_func=date_func): -5,
            timestamp("2020-01-10 00:00:00", date_func=date_func): 5.5,
        }
    )
    result = s1(date_func) - s2(date_func)
    pd.testing.assert_series_equal(
        result.step_changes,
        expected_step_changes,
        check_names=False,
        check_index_type=False,
    )
    assert_expected_type(result, date_func)


def test_multiply_dates(date_func):
    expected_step_changes = pd.Series(
        {
            timestamp("2020-01-01 00:00:00", date_func=date_func): -5.0,
            timestamp("2020-01-02 00:00:00", date_func=date_func): 9.0,
            timestamp("2020-01-02 12:00:00", date_func=date_func): -5.0,
            timestamp("2020-01-03 00:00:00", date_func=date_func): -1.25,
            timestamp("2020-01-04 00:00:00", date_func=date_func): 11.25,
            timestamp("2020-01-05 00:00:00", date_func=date_func): -14.0,
            timestamp("2020-01-06 00:00:00", date_func=date_func): 6.25,
            timestamp("2020-01-07 00:00:00", date_func=date_func): -1.25,
            timestamp("2020-01-08 00:00:00", date_func=date_func): -2.5,
            timestamp("2020-01-10 00:00:00", date_func=date_func): 2.5,
        }
    )
    result = s1(date_func) * s2(date_func)
    pd.testing.assert_series_equal(
        result.step_changes,
        expected_step_changes,
        check_names=False,
        check_index_type=False,
    )
    assert_expected_type(result, date_func)


def test_multiply_dates_scalar(date_func):
    expected_step_changes = pd.Series(
        {
            timestamp("2020-01-01 00:00:00", date_func=date_func): 6.0,
            timestamp("2020-01-03 00:00:00", date_func=date_func): 7.5,
            timestamp("2020-01-05 00:00:00", date_func=date_func): -7.5,
            timestamp("2020-01-06 00:00:00", date_func=date_func): -7.5,
            timestamp("2020-01-10 00:00:00", date_func=date_func): 1.5,
        }
    )
    result = s1(date_func) * 3
    pd.testing.assert_series_equal(
        result.step_changes,
        expected_step_changes,
        check_names=False,
        check_index_type=False,
    )
    assert_expected_type(result, date_func)


def test_divide_dates(date_func):
    expected_step_changes = pd.Series(
        {
            timestamp("2020-01-01 00:00:00", date_func=date_func): -1.3333333333333333,
            timestamp("2020-01-02 00:00:00", date_func=date_func): 2.0,
            timestamp("2020-01-02 12:00:00", date_func=date_func): 3.3333333333333335,
            timestamp("2020-01-03 00:00:00", date_func=date_func): 5.0,
            timestamp("2020-01-04 00:00:00", date_func=date_func): -7.5,
            timestamp("2020-01-05 00:00:00", date_func=date_func): -2.833333333333333,
            timestamp("2020-01-06 00:00:00", date_func=date_func): 1.6666666666666665,
            timestamp("2020-01-07 00:00:00", date_func=date_func): -0.8333333333333333,
            timestamp("2020-01-08 00:00:00", date_func=date_func): 0.4166666666666667,
            timestamp("2020-01-10 00:00:00", date_func=date_func): 0.08333333333333333,
        }
    )
    result = s1(date_func) / (s2(date_func) + 1)
    pd.testing.assert_series_equal(
        result.step_changes,
        expected_step_changes,
        check_names=False,
        check_index_type=False,
    )
    assert_expected_type(result, date_func)


def test_divide_dates_scalar(date_func):
    expected_step_changes = pd.Series(
        {
            timestamp("2020-01-01 00:00:00", date_func=date_func): 4.0,
            timestamp("2020-01-03 00:00:00", date_func=date_func): 5.0,
            timestamp("2020-01-05 00:00:00", date_func=date_func): -5.0,
            timestamp("2020-01-06 00:00:00", date_func=date_func): -5.0,
            timestamp("2020-01-10 00:00:00", date_func=date_func): 1.0,
        }
    )
    result = s1(date_func) / 0.5
    pd.testing.assert_series_equal(
        result.step_changes,
        expected_step_changes,
        check_names=False,
        check_index_type=False,
    )
    assert_expected_type(result, date_func)


def test_to_frame(date_func):
    s1(date_func).to_frame()


@pytest.mark.parametrize(
    "stairs_func, bounds, cuts",
    itertools.product(
        [s1, s2, s3, s4],
        [
            ((2020, 1, 3), (2020, 1, 4)),
            ((2020, 1, 1), (2020, 1, 4)),
            ((2020, 1, 2), (2020, 2, 4)),
        ],
        ["unit", (-2, 0, 0.5, 4, 4.5, 7)],
    ),
)
def test_hist_default_bins_left_closed(date_func, stairs_func, bounds, cuts):
    stairs_instance = stairs_func(date_func)
    bounds = [timestamp(*args, date_func=date_func) for args in bounds]

    def make_expected_result(interval_index, lower, upper):
        return pd.Series(
            [
                ((stairs_instance >= i.left) * (stairs_instance < i.right)).mean(
                    (lower, upper)
                )
                for i in interval_index
            ],
            index=interval_index,
        )

    hist = stairs_instance.hist(x=cuts, where=bounds, normalize=True)
    expected = make_expected_result(hist.index, *bounds)
    pd.testing.assert_series_equal(
        hist, expected, check_names=False, check_index_type=False,
    )


@pytest.mark.parametrize(
    "stairs_func, bounds, cuts",
    itertools.product(
        [s1, s2, s3, s4],
        [
            ((2020, 1, 3), (2020, 1, 4)),
            ((2020, 1, 1), (2020, 1, 4)),
            ((2020, 1, 2), (2020, 2, 4)),
        ],
        ["unit", (-2, 0, 0.5, 4, 4.5, 7)],
    ),
)
def test_hist_default_bins_right_closed(date_func, stairs_func, bounds, cuts):
    stairs_instance = stairs_func(date_func)
    bounds = [timestamp(*args, date_func=date_func) for args in bounds]

    def make_expected_result(interval_index, lower, upper):
        return pd.Series(
            [
                ((stairs_instance > i.left) * (stairs_instance <= i.right)).mean(
                    (lower, upper)
                )
                for i in interval_index
            ],
            index=interval_index,
        )

    hist = stairs_instance.hist(x=cuts, where=bounds, closed="right", normalize=True)
    expected = make_expected_result(hist.index, *bounds)
    pd.testing.assert_series_equal(
        hist, expected, check_names=False, check_index_type=False,
    )


@pytest.mark.parametrize(
    "stairs_func, bounds, closed",
    itertools.product(
        [s1, s2, s3, s4],
        [
            ((2020, 1, 3), (2020, 1, 4)),
            ((2020, 1, 1), (2020, 1, 4)),
            ((2020, 1, 2), (2020, 2, 4)),
        ],
        ["left", "right"],
    ),
)
def test_hist_default_bins(date_func, stairs_func, bounds, closed):
    # really testing the default binning process here
    stairs_instance = stairs_func(date_func)
    bounds = [timestamp(*args, date_func=date_func) for args in bounds]
    hist = stairs_instance.hist(where=bounds, closed=closed, normalize=True)
    assert abs(hist.sum() - 1) < 0.000001


def test_shift(date_func):
    ans = Stairs(initial_value=0)
    ans.layer(
        timestamp(2020, 1, 2, date_func=date_func),
        timestamp(2020, 1, 11, date_func=date_func),
        2,
    )
    ans.layer(
        timestamp(2020, 1, 4, date_func=date_func),
        timestamp(2020, 1, 6, date_func=date_func),
        2.5,
    )
    ans.layer(
        timestamp(2020, 1, 7, date_func=date_func),
        timestamp(2020, 1, 8, date_func=date_func),
        -2.5,
    )
    ans.layer(
        timestamp(2020, 1, 8, date_func=date_func),
        timestamp(2020, 1, 11, date_func=date_func),
        -2.5,
    )
    result = s1(date_func).shift(pd.Timedelta(24, unit="H"))
    assert bool(result == ans)
    assert_expected_type(result, date_func)


# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,10, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st1(pts))
# = 3.8580225122881124

# low, high = timestamp(2019,12,30, date_func=date_func), timestamp(2020,1,8,16, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st1(pts))
# = 3.501189060642099

# low, high = timestamp(2020,1,2, date_func=date_func), timestamp(2020,1,11,3, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st1(pts))
# = 3.971476824920255


@pytest.mark.parametrize(
    "bounds, expected",
    [
        ((), 3.8580225122881124),
        (((2019, 12, 30), (2020, 1, 8, 16)), 3.501189060642099),
        (((2020, 1, 2), (2020, 1, 11, 3)), 3.971476824920255),
    ],
)
def test_s1_var(date_func, bounds, expected):
    bounds = [timestamp(*args, date_func=date_func) for args in bounds]
    if len(bounds) > 0:
        bounds = [bounds]
    assert np.isclose(s1(date_func).var(*bounds), expected, atol=0.00001)


# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,10, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st2(pts))
# = 8.068647476524724

# low, high = timestamp(2019,12,30, date_func=date_func), timestamp(2020,1,8,16, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st2(pts))
# = 4.283962544589773

# low, high = timestamp(2020,1,2, date_func=date_func), timestamp(2020,1,11,3, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.var(st2(pts))
# = 6.9166823043723


@pytest.mark.parametrize(
    "bounds, expected",
    [
        ((), 8.068647476524724),
        (((2019, 12, 30), (2020, 1, 8, 16)), 4.283962544589773),
        (((2020, 1, 2), (2020, 1, 11, 3)), 6.9166823043723),
    ],
)
def test_s2_var(date_func, bounds, expected):
    bounds = [timestamp(*args, date_func=date_func) for args in bounds]
    if len(bounds) > 0:
        bounds = [bounds]
    assert np.isclose(s2(date_func).var(*bounds), expected, atol=0.00001)


# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,10, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st1(pts))
# = 1.9641849485952467

# low, high = timestamp(2019,12,30, date_func=date_func), timestamp(2020,1,8,16, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st1(pts))
# = 1.871146456224659

# low, high = timestamp(2020,1,2, date_func=date_func), timestamp(2020,1,11,3, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st1(pts))
# = 1.9928564486485862


@pytest.mark.parametrize(
    "bounds, expected",
    [
        ((), 1.9641849485952467),
        (((2019, 12, 30), (2020, 1, 8, 16)), 1.871146456224659),
        (((2020, 1, 2), (2020, 1, 11, 3)), 1.9928564486485862),
    ],
)
def test_s1_std(date_func, bounds, expected):
    bounds = [timestamp(*args, date_func=date_func) for args in bounds]
    if len(bounds) > 0:
        bounds = [bounds]
    assert np.isclose(s1(date_func).std(*bounds), expected, atol=0.00001)


# low, high = (2020,1,1), timestamp(2020,1,10, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st2(pts))
# = 2.840536476886844

# low, high = timestamp(2019,12,30, date_func=date_func), timestamp(2020,1,8,16, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st2(pts))
# = 2.0697735491086395

# low, high = timestamp(2020,1,2, date_func=date_func), timestamp(2020,1,11,3, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# pts = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.std(st2(pts))
# = 2.6299586126728878


@pytest.mark.parametrize(
    "bounds, expected",
    [
        ((), 2.840536476886844),
        (((2019, 12, 30), (2020, 1, 8, 16)), 2.0697735491086395,),
        (((2020, 1, 2), (2020, 1, 11, 3)), 2.6299586126728878),
    ],
)
def test_s2_std(date_func, bounds, expected):
    bounds = [timestamp(*args, date_func=date_func) for args in bounds]
    if len(bounds) > 0:
        bounds = [bounds]
    assert np.isclose(s2(date_func).std(*bounds), expected, atol=0.00001)


# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,10, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(1, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, total_secs - lag_secs)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, total_secs - lag_secs)]
# np.corrcoef(st1(pts1), st1(pts2))[0,1]
# = 0.7242066313374523

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, total_secs - lag_secs)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, total_secs - lag_secs)]
# np.corrcoef(st1(pts1), st1(pts2))[0,1]
# = -0.4564262197588511

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.corrcoef(st1(pts1), st1.shift(-pd.Timedelta(2, unit='D'))(pts1))[0,1]
# = 0.2145983282751396


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (
            {
                "lower": [2020, 1, 1],
                "upper": [2020, 1, 10],
                "lag": pd.Timedelta(1, unit="D"),
            },
            0.7242066313374523,
        ),
        (
            {
                "lower": [2020, 1, 1],
                "upper": [2020, 1, 8],
                "lag": pd.Timedelta(2, unit="D"),
            },
            -0.4564262197588511,
        ),
        (
            {
                "lower": [2020, 1, 1],
                "upper": [2020, 1, 8],
                "lag": pd.Timedelta(2, unit="D"),
                "clip": "post",
            },
            0.2145983282751396,
        ),
    ],
)
def test_s1_autocorr(date_func, kwargs, expected):
    kwargs = kwargs.copy()
    lower = timestamp(*kwargs.pop("lower"), date_func=date_func)
    upper = timestamp(*kwargs.pop("upper"), date_func=date_func)
    new_kwargs = {**kwargs, "where": (lower, upper)}
    assert np.isclose(
        s1(date_func).corr(s1(date_func), **new_kwargs), expected, atol=0.00001,
    )


# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,10, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(1, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, total_secs - lag_secs)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, total_secs - lag_secs)]
# np.corrcoef(st2(pts1), st2(pts2))[0,1]
# = 0.41564870493583517

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, total_secs - lag_secs)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, total_secs - lag_secs)]
# np.corrcoef(st2(pts1), st2(pts2))[0,1]
# = -0.1856362783824296

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.corrcoef(st2(pts1), st2.shift(-pd.Timedelta(2, unit='D'))(pts1))[0,1]
# = -0.24047807541603636


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 10),
                "lag": pd.Timedelta(1, unit="D"),
            },
            0.41564870493583517,
        ),
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 8),
                "lag": pd.Timedelta(2, unit="D"),
            },
            -0.1856362783824296,
        ),
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 8),
                "lag": pd.Timedelta(2, unit="D"),
                "clip": "post",
            },
            -0.24047807541603636,
        ),
    ],
)
def test_s2_autocorr(date_func, kwargs, expected):
    kwargs = kwargs.copy()
    lower = timestamp(*kwargs.pop("lower"), date_func=date_func)
    upper = timestamp(*kwargs.pop("upper"), date_func=date_func)
    new_kwargs = {**kwargs, "where": (lower, upper)}
    assert np.isclose(
        s2(date_func).corr(s2(date_func), **new_kwargs), expected, atol=0.00001
    )


# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,10, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(1, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, total_secs - lag_secs)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, total_secs - lag_secs)]
# np.corrcoef(st1(pts1), st2(pts2))[0,1]
# = -0.5504768716400756

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, total_secs - lag_secs)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, total_secs - lag_secs)]
# np.corrcoef(st1(pts1), st2(pts2))[0,1]
# = -0.869050905054203

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.corrcoef(st1(pts1), st2.shift(-pd.Timedelta(2, unit='D'))(pts1))[0,1]
# = -0.962531150106436


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 10),
                "lag": pd.Timedelta(1, unit="D"),
            },
            -0.5504768716400756,
        ),
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 8),
                "lag": pd.Timedelta(2, unit="D"),
            },
            -0.869050905054203,
        ),
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 8),
                "lag": pd.Timedelta(2, unit="D"),
                "clip": "post",
            },
            -0.962531150106436,
        ),
    ],
)
def test_crosscorr(date_func, kwargs, expected):
    kwargs = kwargs.copy()
    lower = timestamp(*kwargs.pop("lower"), date_func=date_func)
    upper = timestamp(*kwargs.pop("upper"), date_func=date_func)
    new_kwargs = {**kwargs, "where": (lower, upper)}
    assert np.isclose(
        s1(date_func).corr(s2(date_func), **new_kwargs), expected, atol=0.00001
    )


# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,10, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(1, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, total_secs - lag_secs)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, total_secs - lag_secs)]
# np.cov(st1(pts1), st1(pts2))[0,1]
# = 2.9296901561636464

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, total_secs - lag_secs)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, total_secs - lag_secs)]
# np.cov(st1(pts1), st1(pts2))[0,1]
# = -1.2499884258990304

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs)]
# np.cov(st1(pts1), st1.shift(-pd.Timedelta(2, unit='D'))(pts1))[0,1]
# = 0.892856552342196


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 10),
                "lag": pd.Timedelta(1, unit="D"),
            },
            2.9296901561636464,
        ),
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 8),
                "lag": pd.Timedelta(2, unit="D"),
            },
            -1.2499884258990304,
        ),
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 8),
                "lag": pd.Timedelta(2, unit="D"),
                "clip": "post",
            },
            0.892856552342196,
        ),
    ],
)
def test_s1_autocov(date_func, kwargs, expected):
    kwargs = kwargs.copy()
    lower = timestamp(*kwargs.pop("lower"), date_func=date_func)
    upper = timestamp(*kwargs.pop("upper"), date_func=date_func)
    new_kwargs = {**kwargs, "where": (lower, upper)}
    assert np.isclose(
        s1(date_func).cov(s1(date_func), **new_kwargs), expected, atol=0.00001
    )


# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,10, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(1, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, total_secs - lag_secs + 1)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, total_secs - lag_secs + 1)]
# np.cov(st2(pts1), st2(pts2))[0,1]
# = 2.903313715908994

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, 2*(total_secs - lag_secs) + 1)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, 2*(total_secs - lag_secs) + 1)]
# np.cov(st2(pts1), st2(pts2))[0,1]
# = -0.5850255035016916

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs + 1)]
# np.cov(st2(pts1), st2.shift(-pd.Timedelta(2, unit='D'))(pts1))[0,1]
# = -1.2321516853124157


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 10),
                "lag": pd.Timedelta(1, unit="D"),
            },
            2.903313715908994,
        ),
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 8),
                "lag": pd.Timedelta(2, unit="D"),
            },
            -0.5850255035016916,
        ),
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 8),
                "lag": pd.Timedelta(2, unit="D"),
                "clip": "post",
            },
            -1.2321516853124157,
        ),
    ],
)
def test_s2_autocov(date_func, kwargs, expected):
    kwargs = kwargs.copy()
    lower = timestamp(*kwargs.pop("lower"), date_func=date_func)
    upper = timestamp(*kwargs.pop("upper"), date_func=date_func)
    new_kwargs = {**kwargs, "where": (lower, upper)}
    assert np.isclose(
        s2(date_func).cov(s2(date_func), **new_kwargs), expected, atol=0.0001
    )


# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,10, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(1, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, total_secs - lag_secs + 1)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, total_secs - lag_secs + 1)]
# np.cov(st1(pts1), st2(pts2))[0,1]
# = -2.9980440069170653

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs - lag_secs, 2*(total_secs - lag_secs) + 1)]
# pts2 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0 + lag_secs, total_secs, 2*(total_secs - lag_secs) + 1)]
# np.cov(st1(pts1), st2(pts2))[0,1]
# = -1.8000478009074565

# low, high = timestamp(2020,1,1, date_func=date_func), timestamp(2020,1,8, date_func=date_func)
# total_secs = int((high-low).total_seconds())
# lag_secs =  int(pd.Timedelta(2, unit='D').total_seconds())
# pts1 = [low + pd.Timedelta(x, unit='sec') for x in np.linspace(0, total_secs, total_secs + 1)]
# np.cov(st1(pts1), st2.shift(-pd.Timedelta(2, unit='D'))(pts1))[0,1]
# = -5.357139018807952


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 10),
                "lag": pd.Timedelta(1, unit="D"),
            },
            -2.9980440069170653,
        ),
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 8),
                "lag": pd.Timedelta(2, unit="D"),
            },
            -1.8000478009074565,
        ),
        (
            {
                "lower": (2020, 1, 1),
                "upper": (2020, 1, 8),
                "lag": pd.Timedelta(2, unit="D"),
                "clip": "post",
            },
            -5.357139018807952,
        ),
    ],
)
def test_crosscov(date_func, kwargs, expected):
    kwargs = kwargs.copy()
    lower = timestamp(*kwargs.pop("lower"), date_func=date_func)
    upper = timestamp(*kwargs.pop("upper"), date_func=date_func)
    new_kwargs = {**kwargs, "where": (lower, upper)}
    assert np.isclose(
        s1(date_func).cov(s2(date_func), **new_kwargs), expected, atol=0.0001
    )


# @pytest.mark.parametrize(
#     "kwargs, expected_index, expected_vals",
#     [
#         (
#             {"window": (-pd.Timedelta(1, "d"), pd.Timedelta(1, "d"))},
#             [
#                 (2019, 12, 31),
#                 (2020, 1, 2),
#                 (2020, 1, 4),
#                 (2020, 1, 5),
#                 (2020, 1, 6),
#                 (2020, 1, 7),
#                 (2020, 1, 9),
#                 (2020, 1, 11),
#             ],
#             [0.0, 2.0, 4.5, 3.25, 0.75, -0.5, -0.5, 0.0],
#         ),
#         (
#             {"window": (-pd.Timedelta(2, "d"), pd.Timedelta(0, "d"))},
#             [
#                 (2020, 1, 1),
#                 (2020, 1, 3),
#                 (2020, 1, 5),
#                 (2020, 1, 6),
#                 (2020, 1, 7),
#                 (2020, 1, 8),
#                 (2020, 1, 10),
#                 (2020, 1, 12),
#             ],
#             [0.0, 2.0, 4.5, 3.25, 0.75, -0.5, -0.5, 0.0],
#         ),
#         (
#             {
#                 "window": (-pd.Timedelta(1, "d"), pd.Timedelta(1, "d")),
#                 "lower": (2020, 1, 3),
#                 "upper": (2020, 1, 8),
#             },
#             [
#                 (2020, 1, 4),
#                 (2020, 1, 5),
#                 (2020, 1, 6),
#                 (2020, 1, 7),
#             ],
#             [4.5, 3.25, 0.75, -0.5],
#         ),
#     ],
# )
# def test_s1_rolling_mean(date_func, kwargs, expected_index, expected_vals):
#     expected_index = [timestamp(*args, date_func=date_func) for args in expected_index]
#     new_kwargs = {**kwargs}
#     if "lower" in kwargs:
#         new_kwargs["lower"] = timestamp(*kwargs["lower"], date_func=date_func)
#     if "upper" in kwargs:
#         new_kwargs["upper"] = timestamp(*kwargs["upper"], date_func=date_func)
#     new_kwargs

#     rm = s1(date_func).rolling_mean(**new_kwargs)
#     assert list(rm.values) == expected_vals
#     assert list(rm.index) == expected_index


def test_eq():
    assert Stairs(initial_value=3) == 3


def test_ne(date_func):
    assert s1(date_func) != 3


def test_make_test_data():
    assert isinstance(test_data.make_test_data(dates=True), pd.DataFrame)
