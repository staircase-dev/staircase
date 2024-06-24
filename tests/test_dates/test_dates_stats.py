from datetime import datetime

import numpy as np
import pandas as pd
import pytest
import pytz

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
                "pandas_timedelta",
                "pytimedelta",
                "numpy_timedelta",
            ],
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
    elif request.param == "pandas_timedelta":
        return lambda ts: ts - pd.Timestamp(2019, 12, 31)
    elif request.param == "pytimedelta":
        return lambda ts: (ts - pd.Timestamp(2019, 12, 31)).to_pytimedelta()
    elif request.param == "numpy_timedelta":
        return lambda ts: (ts - pd.Timestamp(2019, 12, 31)).to_timedelta64()
    else:
        assert False, "should not happen"


def timestamp(*args, date_func, **kwargs):
    ts = pd.Timestamp(*args, **kwargs)
    return date_func(ts)


def assert_expected_type(stairs, date_func):
    if stairs._data is None:
        return
    example_type = timestamp(2020, 1, 1, date_func=date_func)
    try:  # TODO this is a hack
        example_type = pd.Timedelta(example_type)
    except:  # noqa
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
        s1(date_func).agg("max", (None, timestamp(2020, 1, 2, date_func=date_func)))
        == 2
    ), "Expected maximum to be 2"


def test_max_dates_3(date_func):
    assert (
        s1(date_func).agg("max", (timestamp(2020, 1, 5, 12, date_func=date_func), None))
        == 2
    ), "Expected maximum to be 2"


def test_max_dates_4(date_func):
    assert (
        s1(date_func).agg(
            "max",
            (
                timestamp(2020, 1, 8, date_func=date_func),
                timestamp(2020, 1, 9, date_func=date_func),
            ),
        )
        == -0.5
    ), "Expected maximum to be -0.5"


def test_min_dates_1(date_func):
    assert s1(date_func).min() == -0.5, "Expected minimum to be -0.5"


def test_min_dates_2(date_func):
    assert (
        s1(date_func).agg("min", (None, timestamp(2020, 1, 4, date_func=date_func)))
        == 0
    ), "Expected minimum to be 0"


def test_min_dates_3(date_func):
    assert (
        s1(date_func).agg(
            "min", (timestamp(2020, 1, 10, 12, date_func=date_func), None)
        )
        == 0
    ), "Expected minimum to be 0"


def test_min_dates_4(date_func):
    assert (
        s1(date_func).agg(
            "min",
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 4, 12, date_func=date_func),
            ),
        )
        == 4.5
    ), "Expected minimum to be 4.5"


def test_mode_dates_1(date_func):
    assert s1(date_func).mode() == -0.5, "Expected mode to be -0.5"


def test_mode_dates_2(date_func):
    assert (
        s1(date_func).agg("mode", (None, timestamp(2020, 1, 4, date_func=date_func)))
        == 2
    ), "Expected mode to be 2"


def test_mode_dates_3(date_func):
    assert (
        s1(date_func).agg("mode", (timestamp(2019, 12, 27, date_func=date_func), None))
        == 0
    ), "Expected mode to be 0"


def test_mode_dates_4(date_func):
    assert (
        s1(date_func).agg(
            "mode",
            (
                timestamp(2020, 1, 4, 12, date_func=date_func),
                timestamp(2020, 1, 6, 12, date_func=date_func),
            ),
        )
        == 2
    ), "Expected mode to be 2"


def test_median_dates_1(date_func):
    assert s1(date_func).median() == 2, "Expected median to be 2"


def test_median_dates_2(date_func):
    assert (
        s1(date_func).agg("median", (None, timestamp(2020, 1, 17, date_func=date_func)))
        == 0
    ), "Expected median to be 0"


def test_median_dates_3(date_func):
    assert (
        s1(date_func).agg("median", (timestamp(2020, 1, 3, date_func=date_func), None))
        == -0.5
    ), "Expected median to be -0.5"


def test_median_dates_4(date_func):
    assert (
        s1(date_func).agg(
            "median",
            (
                timestamp(2020, 1, 4, 12, date_func=date_func),
                timestamp(2020, 1, 6, 12, date_func=date_func),
            ),
        )
        == 2
    ), "Expected median to be 2"


def test_mean_dates_1(date_func):
    assert abs(s1(date_func).mean() - 13 / 9) <= 0.00001, "Expected mean to be 13/9"


def test_mean_dates_2(date_func):
    assert (
        s1(date_func).agg("mean", (None, timestamp(2020, 1, 6, date_func=date_func)))
        == 3
    ), "Expected mean to be 3"


def test_mean_dates_3(date_func):
    assert (
        s1(date_func).agg("mean", (timestamp(2020, 1, 4, date_func=date_func), None))
        == 0.75
    ), "Expected mean to be 0.75"


def test_mean_dates_4(date_func):
    assert (
        s1(date_func).agg(
            "mean",
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 8, date_func=date_func),
            ),
        )
        == 1.375
    ), "Expected mean to be 1.375"


def test_integral_dates_1(date_func):
    assert (
        s1(date_func).integral() / pd.Timedelta("1 D") == 13
    ), "Expected integral to be 13 days"


def test_integral_dates_2(date_func):
    assert (
        s1(date_func).agg(
            "integral", (None, timestamp(2020, 1, 6, date_func=date_func))
        )
        / pd.Timedelta("1 D")
        == 15
    ), "Expected integral to be 15 days"


def test_integral_dates_3(date_func):
    assert (
        s1(date_func).agg(
            "integral", (timestamp(2020, 1, 4, date_func=date_func), None)
        )
        / pd.Timedelta("1 h")
        == 108
    ), "Expected integral to be 108 hours"


def test_integral_dates_4(date_func):
    assert (
        s1(date_func).agg(
            "integral",
            (
                timestamp(2020, 1, 4, date_func=date_func),
                timestamp(2020, 1, 8, date_func=date_func),
            ),
        )
        / pd.Timedelta("1 h")
        == 132
    ), "Expected integral to be 132 hours"


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
    bounds2 = [timestamp(*args, date_func=date_func) for args in bounds]
    if len(bounds2) > 0:
        bounds2 = [bounds2]
    assert np.isclose(s1(date_func).agg("var", *bounds2), expected, atol=0.00001)


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
    assert np.isclose(s2(date_func).agg("var", *bounds), expected, atol=0.00001)


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
    assert np.isclose(s1(date_func).agg("std", *bounds), expected, atol=0.00001)


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
        (
            ((2019, 12, 30), (2020, 1, 8, 16)),
            2.0697735491086395,
        ),
        (((2020, 1, 2), (2020, 1, 11, 3)), 2.6299586126728878),
    ],
)
def test_s2_std(date_func, bounds, expected):
    bounds = [timestamp(*args, date_func=date_func) for args in bounds]
    if len(bounds) > 0:
        bounds = [bounds]
    assert np.isclose(s2(date_func).agg("std", *bounds), expected, atol=0.00001)


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
        s1(date_func).corr(s1(date_func), **new_kwargs),
        expected,
        atol=0.00001,
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


def test_integral_overflow():
    with pytest.raises(OverflowError):
        s = (
            Stairs()
            .layer(pd.Timestamp("1980"), pd.Timestamp("2050"), 5000)
            .layer(pd.Timestamp("1990"), pd.Timestamp("2060"), 4000)
        )
        s.integral()


def test_mean_no_overflow():
    s = (
        Stairs()
        .layer(pd.Timestamp("1980"), pd.Timestamp("2050"), 5000)
        .layer(pd.Timestamp("1990"), pd.Timestamp("2060"), 4000)
    )
    s.mean()
