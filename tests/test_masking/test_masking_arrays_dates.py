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
            [
                "pandas",
                "pydatetime",
                "numpy",
                "pandas_tz",
                "pydatetime_tz",
                "pandas_str",
            ],
            indirect=True,
        )


def pandas_str(ts):
    return pd.Timestamp(ts)


@pytest.fixture
def date_func(request):
    # returns a func which takes a pandas timestamp
    if request.param == "pandas":
        return lambda x: x
    elif request.param == "pandas_str":
        return pandas_str
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


def timestamp(*args, date_func, use_str=False, **kwargs):
    ts = pd.Timestamp(*args, **kwargs)
    if use_str and date_func == pandas_str:
        return str(ts)
    return date_func(ts)


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
    return (
        sc.Stairs()
        .layer(start=timestamp(2019, 12, 29, date_func=date_func), value=-1.75)
        .layer(start=timestamp(2020, 1, 1, date_func=date_func), value=-0.75)
        .layer(start=timestamp(2020, 1, 2, date_func=date_func), value=4.5)
        .layer(start=timestamp(2020, 1, 2, 12, date_func=date_func), value=-2.5)
        .layer(start=timestamp(2020, 1, 7, date_func=date_func), value=2.5)
        .layer(start=timestamp(2020, 1, 8, date_func=date_func), value=-4.5)
        .layer(start=timestamp(2020, 1, 10, date_func=date_func), value=2.5)
        .layer(start=timestamp(2020, 1, 11, date_func=date_func), value=5)
        .layer(start=timestamp(2020, 1, 13, date_func=date_func), value=-5)
    )


def test_sum(date_func):
    s1mask = s1(date_func).mask(
        (
            timestamp(2020, 1, 2, date_func=date_func, use_str=True),
            timestamp(2020, 1, 4, date_func=date_func, use_str=True),
        )
    )
    s2mask = s2(date_func).mask(
        (
            timestamp(2020, 1, 7, date_func=date_func, use_str=True),
            timestamp(2020, 1, 9, date_func=date_func, use_str=True),
        )
    )
    pd.testing.assert_series_equal(
        sc.sum([s1mask, s2mask, s1mask + s2mask]).step_values,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -3.5,
                timestamp(2019, 12, 29, date_func=date_func): -7.0,
                timestamp(2020, 1, 1, date_func=date_func): -4.5,
                timestamp(2020, 1, 2, date_func=date_func): np.nan,
                timestamp(2020, 1, 4, date_func=date_func): 4.5,
                timestamp(2020, 1, 5, date_func=date_func): 3.0,
                timestamp(2020, 1, 6, date_func=date_func): -2.0,
                timestamp(2020, 1, 7, date_func=date_func): np.nan,
                timestamp(2020, 1, 9, date_func=date_func): -6.0,
                timestamp(2020, 1, 10, date_func=date_func): 0.0,
                timestamp(2020, 1, 11, date_func=date_func): 10.0,
                timestamp(2020, 1, 13, date_func=date_func): 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_max(date_func):
    s1mask = s1(date_func).mask(
        (
            timestamp(2020, 1, 2, date_func=date_func, use_str=True),
            timestamp(2020, 1, 4, date_func=date_func, use_str=True),
        )
    )
    s2mask = s2(date_func).mask(
        (
            timestamp(2020, 1, 7, date_func=date_func, use_str=True),
            timestamp(2020, 1, 9, date_func=date_func, use_str=True),
        )
    )
    pd.testing.assert_series_equal(
        sc.max([s1mask, s2mask]).step_values,
        pd.Series(
            {
                timestamp(2019, 12, 29, date_func=date_func): -1.75,
                timestamp(2020, 1, 1, date_func=date_func): 0.25,
                timestamp(2020, 1, 2, date_func=date_func): np.nan,
                timestamp(2020, 1, 4, date_func=date_func): 2.75,
                timestamp(2020, 1, 5, date_func=date_func): 2.0,
                timestamp(2020, 1, 6, date_func=date_func): -0.5,
                timestamp(2020, 1, 7, date_func=date_func): np.nan,
                timestamp(2020, 1, 9, date_func=date_func): -0.5,
                timestamp(2020, 1, 10, date_func=date_func): 0.0,
                timestamp(2020, 1, 11, date_func=date_func): 5.0,
                timestamp(2020, 1, 13, date_func=date_func): 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_min(date_func):
    s1mask = s1(date_func).mask(
        (
            timestamp(2020, 1, 2, date_func=date_func, use_str=True),
            timestamp(2020, 1, 4, date_func=date_func, use_str=True),
        )
    )
    s2mask = s2(date_func).mask(
        (
            timestamp(2020, 1, 7, date_func=date_func, use_str=True),
            timestamp(2020, 1, 9, date_func=date_func, use_str=True),
        )
    )
    pd.testing.assert_series_equal(
        sc.min([s1mask, s2mask]).step_values,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -1.75,
                timestamp(2020, 1, 1, date_func=date_func): -2.5,
                timestamp(2020, 1, 2, date_func=date_func): np.nan,
                timestamp(2020, 1, 4, date_func=date_func): -0.5,
                timestamp(2020, 1, 7, date_func=date_func): np.nan,
                timestamp(2020, 1, 9, date_func=date_func): -2.5,
                timestamp(2020, 1, 10, date_func=date_func): 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_1(date_func):
    s1mask = s1(date_func).mask(
        (
            timestamp(2020, 1, 2, date_func=date_func, use_str=True),
            timestamp(2020, 1, 4, date_func=date_func, use_str=True),
        )
    )
    s2mask = s2(date_func).mask(
        (
            timestamp(2020, 1, 7, date_func=date_func, use_str=True),
            timestamp(2020, 1, 9, date_func=date_func, use_str=True),
        )
    )
    pd.testing.assert_series_equal(
        sc.mean([s1mask, s2mask]).step_values,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -0.875,
                timestamp(2019, 12, 29, date_func=date_func): -1.75,
                timestamp(2020, 1, 1, date_func=date_func): -1.125,
                timestamp(2020, 1, 2, date_func=date_func): np.nan,
                timestamp(2020, 1, 4, date_func=date_func): 1.125,
                timestamp(2020, 1, 5, date_func=date_func): 0.75,
                timestamp(2020, 1, 6, date_func=date_func): -0.5,
                timestamp(2020, 1, 7, date_func=date_func): np.nan,
                timestamp(2020, 1, 9, date_func=date_func): -1.5,
                timestamp(2020, 1, 10, date_func=date_func): 0.0,
                timestamp(2020, 1, 11, date_func=date_func): 2.5,
                timestamp(2020, 1, 13, date_func=date_func): 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_mean_2(date_func):
    s1mask = s1(date_func).mask(
        (
            timestamp(2020, 1, 2, date_func=date_func, use_str=True),
            timestamp(2020, 1, 4, date_func=date_func, use_str=True),
        )
    )
    s2mask = (
        s2(date_func)
        .mask(
            (
                timestamp(2020, 1, 7, date_func=date_func, use_str=True),
                timestamp(2020, 1, 9, date_func=date_func, use_str=True),
            )
        )
        .mask((None, timestamp(2019, 12, 31, date_func=date_func, use_str=True)))
    )
    result = sc.mean([s1mask, s2mask])
    pd.testing.assert_series_equal(
        result.step_values,
        pd.Series(
            {
                timestamp(2019, 12, 31, date_func=date_func): -1.75,
                timestamp(2020, 1, 1, date_func=date_func): -1.125,
                timestamp(2020, 1, 2, date_func=date_func): np.nan,
                timestamp(2020, 1, 4, date_func=date_func): 1.125,
                timestamp(2020, 1, 5, date_func=date_func): 0.75,
                timestamp(2020, 1, 6, date_func=date_func): -0.5,
                timestamp(2020, 1, 7, date_func=date_func): np.nan,
                timestamp(2020, 1, 9, date_func=date_func): -1.5,
                timestamp(2020, 1, 10, date_func=date_func): 0.0,
                timestamp(2020, 1, 11, date_func=date_func): 2.5,
                timestamp(2020, 1, 13, date_func=date_func): 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )
    assert np.isnan(result.initial_value)


def test_median(date_func):
    s1mask = s1(date_func).mask(
        (
            timestamp(2020, 1, 2, date_func=date_func, use_str=True),
            timestamp(2020, 1, 4, date_func=date_func, use_str=True),
        )
    )
    s2mask = s2(date_func).mask(
        (
            timestamp(2020, 1, 7, date_func=date_func, use_str=True),
            timestamp(2020, 1, 9, date_func=date_func, use_str=True),
        )
    )
    pd.testing.assert_series_equal(
        sc.median([s1mask, s2mask, s1mask + s2mask]).step_values,
        pd.Series(
            {
                timestamp(2019, 12, 27, date_func=date_func): -1.75,
                timestamp(2020, 1, 1, date_func=date_func): -2.25,
                timestamp(2020, 1, 2, date_func=date_func): np.nan,
                timestamp(2020, 1, 4, date_func=date_func): 2.25,
                timestamp(2020, 1, 5, date_func=date_func): 1.5,
                timestamp(2020, 1, 6, date_func=date_func): -0.5,
                timestamp(2020, 1, 7, date_func=date_func): np.nan,
                timestamp(2020, 1, 9, date_func=date_func): -2.5,
                timestamp(2020, 1, 10, date_func=date_func): 0.0,
                timestamp(2020, 1, 11, date_func=date_func): 5.0,
                timestamp(2020, 1, 13, date_func=date_func): 0.0,
            }
        ),
        check_names=False,
        check_index_type=False,
    )


def test_sample(date_func):
    s1mask = s1(date_func).mask(
        (
            timestamp(2020, 1, 2, date_func=date_func, use_str=True),
            timestamp(2020, 1, 4, date_func=date_func, use_str=True),
        )
    )
    s2mask = s2(date_func).mask(
        (
            timestamp(2020, 1, 7, date_func=date_func, use_str=True),
            timestamp(2020, 1, 9, date_func=date_func, use_str=True),
        )
    )
    expected = pd.DataFrame(
        {
            timestamp(2020, 1, 1, date_func=date_func): [0.25, -2.5, -2.25],
            timestamp(2020, 1, 3, date_func=date_func): [np.nan, -0.5, np.nan],
            timestamp(2020, 1, 5, date_func=date_func): [2.0, -0.5, 1.5],
            timestamp(2020, 1, 7, date_func=date_func): [-0.5, np.nan, np.nan],
            timestamp(2020, 1, 9, date_func=date_func): [-0.5, -2.5, -3.0],
        }
    )
    pd.testing.assert_frame_equal(
        sc.sample(
            [s1mask, s2mask, s1mask + s2mask],
            [
                timestamp(2020, 1, 1, date_func=date_func),
                timestamp(2020, 1, 3, date_func=date_func),
                timestamp(2020, 1, 5, date_func=date_func),
                timestamp(2020, 1, 7, date_func=date_func),
                timestamp(2020, 1, 9, date_func=date_func),
            ],
        ),
        expected,
        check_names=False,
        check_index_type=False,
    )
