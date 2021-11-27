import numpy as np
import pandas as pd
import pytest
import pytz

import staircase as sc
from staircase import Stairs


def perform_array_func(how, func_str, arr, *args, **kwargs):
    obj = {
        "toplevel": sc,
        "series": pd.Series(arr, dtype="Stairs"),
        "accessor": pd.Series(arr, dtype="Stairs").sc,
        "array": sc.StairsArray(arr),
    }[how]
    if how == "toplevel":
        args = [arr] + list(args)
    return getattr(obj, func_str)(*args, **kwargs)


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


@pytest.mark.parametrize(
    "how",
    ["toplevel", "series", "array"],
)
def test_mean_1(date_func, how):
    pd.testing.assert_series_equal(
        perform_array_func(how, "mean", [s1(date_func), s2(date_func)]).step_changes,
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


@pytest.mark.parametrize(
    "how",
    ["toplevel", "series", "array"],
)
def test_median_1(date_func, how):
    pd.testing.assert_series_equal(
        perform_array_func(
            how, "median", [s1(date_func), s2(date_func), s1(date_func) + s2(date_func)]
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


@pytest.mark.parametrize(
    "how",
    ["toplevel", "series", "array"],
)
def test_max_1(date_func, how):
    pd.testing.assert_series_equal(
        perform_array_func(how, "max", [s1(date_func), s2(date_func)]).step_changes,
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


@pytest.mark.parametrize(
    "how",
    ["toplevel", "series", "array"],
)
def test_min_1(date_func, how):
    pd.testing.assert_series_equal(
        perform_array_func(how, "min", [s1(date_func), s2(date_func)]).step_changes,
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


@pytest.mark.parametrize(
    "how",
    ["toplevel", "series", "array"],
)
def test_sum_1(date_func, how):
    pd.testing.assert_series_equal(
        perform_array_func(
            how, "sum", [s1(date_func), s2(date_func), s1(date_func) + s2(date_func)]
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


@pytest.mark.parametrize(
    "how",
    ["toplevel", "accessor", "array"],
)
def test_logical_or(date_func, how):
    result = perform_array_func(
        how,
        "logical_or",
        [s3(date_func), s4(date_func)],
    )
    expected = s3(date_func) | s4(date_func)
    assert result.identical(expected)


@pytest.mark.parametrize(
    "how",
    ["toplevel", "accessor", "array"],
)
def test_logical_and(date_func, how):
    result = perform_array_func(
        how,
        "logical_and",
        [s3(date_func), s4(date_func)],
    )
    expected = s3(date_func) & s4(date_func)
    assert result.identical(expected)


@pytest.mark.parametrize(
    "how",
    ["toplevel", "accessor", "array"],
)
def test_sample_1(date_func, how):
    sample = perform_array_func(
        how,
        "sample",
        [s1(date_func), s2(date_func)],
        timestamp(2020, 1, 3, date_func=date_func),
    )
    expected = pd.DataFrame({timestamp(2020, 1, 3, date_func=date_func): [2.75, -0.5]})
    pd.testing.assert_frame_equal(
        sample,
        expected,
        check_names=False,
        check_index_type=False,
    )


@pytest.mark.parametrize(
    "how",
    ["toplevel", "accessor", "array"],
)
def test_sample_2(date_func, how):
    ts3 = timestamp(2020, 1, 3, date_func=date_func)
    ts6 = timestamp(2020, 1, 6, date_func=date_func)
    ts8 = timestamp(2020, 1, 8, date_func=date_func)
    sample = perform_array_func(
        how,
        "sample",
        [s1(date_func), s2(date_func)],
        [ts3, ts6, ts8],
    )
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


@pytest.mark.parametrize(
    "how",
    ["toplevel", "accessor", "array"],
)
def test_limit_1(date_func, how):
    ts3 = timestamp(2020, 1, 3, date_func=date_func)
    ts6 = timestamp(2020, 1, 6, date_func=date_func)
    ts8 = timestamp(2020, 1, 8, date_func=date_func)
    limits = perform_array_func(
        how,
        "limit",
        [s1(date_func), s2(date_func)],
        [ts3, ts6, ts8],
        side="left",
    )

    expected = pd.DataFrame({ts3: [0.25, -0.5], ts6: [2.0, -2.5], ts8: [-0.5, 0.0]})
    pd.testing.assert_frame_equal(
        limits,
        expected,
        check_names=False,
        check_index_type=False,
    )


@pytest.mark.parametrize(
    "how",
    ["toplevel", "accessor", "array"],
)
def test_limit_2(date_func, how):
    ts3 = timestamp(2020, 1, 3, date_func=date_func)
    ts6 = timestamp(2020, 1, 6, date_func=date_func)
    ts8 = timestamp(2020, 1, 8, date_func=date_func)
    limits = perform_array_func(
        how,
        "limit",
        [s1(date_func), s2(date_func)],
        [ts3, ts6, ts8],
        side="right",
    )
    expected = pd.DataFrame({ts3: [2.75, -0.5], ts6: [-0.5, -2.5], ts8: [-0.5, 5.0]})
    pd.testing.assert_frame_equal(
        limits,
        expected,
        check_names=False,
        check_index_type=False,
    )


@pytest.mark.parametrize(
    "relational",
    ["ge", "gt", "le", "lt", "eq", "ne"],
)
def test_StairsArray_relational(date_func, relational):
    ia1 = sc.StairsArray([s3(date_func), s4(date_func)])
    ia2 = sc.StairsArray([s4(date_func), s3(date_func)])
    result = getattr(ia1, relational)(ia2)
    expected = sc.StairsArray([getattr(x1, relational)(x2) for x1, x2 in zip(ia1, ia2)])
    assert (result == expected).bool().all()


def _matrix_close_to_zeros(x):
    return all(map(lambda v: np.isclose(v, 0, atol=0.00001), x.flatten()))


# # np.cov(st1(np.linspace(-4,10,10000000)), st2(np.linspace(-4,10,10000000))) = array([[2.50159449, 0.28762709], [0.28762709, 6.02104508]])
@pytest.mark.parametrize(
    "how",
    ["toplevel", "accessor", "array"],
)
def test_cov_matrix1(date_func, how):
    result = perform_array_func(
        how,
        "cov",
        [s1(date_func), s2(date_func)],
        where=(
            timestamp(2019, 12, 27, date_func=date_func),
            timestamp(2020, 1, 10, date_func=date_func),
        ),
    )
    if how != "array":
        result = result.values
    assert _matrix_close_to_zeros(
        result - np.array([[2.50159449, 0.28762709], [0.28762709, 6.02104508]])
    )


# # np.cov(st1(np.linspace(0,12,10000000)), st2(np.linspace(0,12,10000000))) = array([[ 1.81727486, -0.25520783],[-0.25520783,  6.45312616]])
@pytest.mark.parametrize(
    "how",
    ["toplevel", "accessor", "array"],
)
def test_cov_matrix2(date_func, how):
    result = perform_array_func(
        how,
        "cov",
        [s1(date_func), s2(date_func)],
        where=(
            timestamp(2019, 12, 31, date_func=date_func),
            timestamp(2020, 1, 12, date_func=date_func),
        ),
    )
    if how != "array":
        result = result.values
    assert _matrix_close_to_zeros(
        result - np.array([[1.81727486, -0.25520783], [-0.25520783, 6.45312616]])
    )


# # np.corrcoef(st1(np.linspace(-4,10,10000000)), st2(np.linspace(-4,10,10000000))) = array([[1, 0.07411146], [0.07411146, 1]])
@pytest.mark.parametrize(
    "how",
    ["toplevel", "accessor", "array"],
)
def test_corr_matrix1(date_func, how):
    result = perform_array_func(
        how,
        "corr",
        [s1(date_func), s2(date_func)],
        where=(
            timestamp(2019, 12, 27, date_func=date_func),
            timestamp(2020, 1, 10, date_func=date_func),
        ),
    )
    if how != "array":
        result = result.values
    assert _matrix_close_to_zeros(result - np.array([[1, 0.07411146], [0.07411146, 1]]))


# # np.corrcoef(st1(np.linspace(0,12,10000000)), st2(np.linspace(0,12,10000000))) = array([[1, -0.07452442], [-0.07452442,  1]])
@pytest.mark.parametrize(
    "how",
    ["toplevel", "accessor", "array"],
)
def test_corr_matrix2(date_func, how):
    result = perform_array_func(
        how,
        "corr",
        [s1(date_func), s2(date_func)],
        where=(
            timestamp(2019, 12, 31, date_func=date_func),
            timestamp(2020, 1, 12, date_func=date_func),
        ),
    )
    if how != "array":
        result = result.values
    assert _matrix_close_to_zeros(
        result - np.array([[1, -0.07452442], [-0.07452442, 1]])
    )


@pytest.mark.parametrize(
    "klass",
    [list, np.array, pd.Series, tuple, dict],
)
def test_StairsArray_construction(date_func, klass):
    list_data = [s1(date_func), s2(date_func)]
    if klass == dict:
        data = dict(enumerate(list_data))
    else:
        data = klass(list_data)
    result = sc.StairsArray(data)
    for x, y in zip(result, list_data):
        assert x.identical(y)


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
