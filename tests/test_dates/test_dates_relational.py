from datetime import datetime

import pandas as pd
import pytest
import pytz

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


def test_eq():
    assert Stairs(initial_value=3) == 3


def test_ne(date_func):
    assert s1(date_func) != 3
