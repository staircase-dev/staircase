import itertools

import numpy as np
import pandas as pd
import pytest

from staircase import Stairs


def _expand_interval_definition(start, end=None, value=1):
    return start, end, value


def _compare_iterables(it1, it2):
    it1 = [i for i in it1 if i is not None]
    it2 = [i for i in it2 if i is not None]
    if len(it2) != len(it1):
        return False
    for e1, e2 in zip(it1, it2):
        if e1 != e2:
            return False
    return True


def s1(closed="left"):
    int_seq1 = Stairs(initial_value=0, closed=closed)
    int_seq1.layer(1, 10, 2)
    int_seq1.layer(-4, 5, -1.75)
    int_seq1.layer(3, 5, 2.5)
    int_seq1.layer(6, 7, -2.5)
    int_seq1.layer(7, 10, -2.5)
    return int_seq1


def s2():
    int_seq2 = Stairs(initial_value=0)
    int_seq2.layer(1, 7, -2.5)
    int_seq2.layer(8, 10, 5)
    int_seq2.layer(2, 5, 4.5)
    int_seq2.layer(2.5, 4, -2.5)
    int_seq2.layer(-2, 1, -1.75)
    return int_seq2


def s3():  # boolean
    int_seq = Stairs(initial_value=0)
    int_seq.layer(-10, 10, 1)
    int_seq.layer(-8, -7, -1)
    int_seq.layer(-5, -2, -1)
    int_seq.layer(0.5, 1, -1)
    int_seq.layer(3, 3.5, -1)
    int_seq.layer(7, 9.5, -1)
    return int_seq


def s4():  # boolean
    int_seq = Stairs(initial_value=0)
    int_seq.layer(-11, 9, 1)
    int_seq.layer(-9.5, -8, -1)
    int_seq.layer(-7.5, -7, -1)
    int_seq.layer(0, 3, -1)
    int_seq.layer(6, 6.5, -1)
    int_seq.layer(7, 8.5, -1)
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


def test_init():
    assert Stairs(initial_value=0).identical(Stairs())
    assert Stairs().identical(Stairs(initial_value=0))


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_init2(init_value):
    int_seq = Stairs(initial_value=init_value)
    assert (
        int_seq.number_of_steps == 0
    ), "Initialised Stairs should have exactly one interval"


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_init3(init_value):
    int_seq = Stairs(initial_value=init_value)
    assert (
        len(int_seq.step_points) == 0
    ), "Initialised Stairs should not have any finite interval endpoints"


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_init4(init_value):
    int_seq = Stairs(initial_value=init_value)
    assert (
        int_seq(-1) == init_value
    ), "Initialised Stairs should have initial value everywhere"
    assert (
        int_seq(0) == init_value
    ), "Initialised Stairs should have initial value everywhere"
    assert (
        int_seq(1) == init_value
    ), "Initialised Stairs should have initial value everywhere"


@pytest.mark.parametrize(
    "init_value, added_interval",
    itertools.product(
        [0, 1.25, -1.25],
        [(-2, 1), (3, 5, 2), (1, 5, -1), (-5, -3, 3), (3,), (2, None, 2)],
    ),
)
def test_one_finite_interval(init_value, added_interval):
    e = 0.0001
    int_seq = Stairs(initial_value=init_value)
    int_seq.layer(*added_interval)
    start, end, value = _expand_interval_definition(*added_interval)
    assert int_seq.number_of_steps == 2 - (
        end is None
    ), "One finite interval added to initial infinite interval should result in 3 intervals"
    assert _compare_iterables(
        int_seq.step_points, (start, end)
    ), "Finite endpoints are not what is expected"
    assert (
        int_seq(float("-inf")) == init_value
    ), "Adding finite interval should not change initial value"
    assert int_seq(float("inf")) == init_value + value * (
        end is None
    ), "Adding finite interval should not change final value"
    assert int_seq(start - e) == init_value
    assert int_seq(start) == init_value + value
    assert int_seq(start + e) == init_value + value
    if end is not None:
        assert int_seq(end - e) == init_value + value
        assert int_seq(end) == init_value


@pytest.mark.parametrize(
    "init_value, endpoints, value",
    itertools.product(
        [0, 1.25, -1.25, 2, -2],
        [(-2, 1, 3), (-2, -1, 3), (-3, -2, -1), (1, 2, 3)],
        [-1, 2, 3],
    ),
)
def test_two_adjacent_finite_interval_same_value(init_value, endpoints, value):
    e = 0.0001
    int_seq = Stairs(initial_value=init_value)
    point1, point2, point3 = endpoints
    int_seq.layer(point1, point2, value)
    int_seq.layer(point2, point3, value)
    assert int_seq.number_of_steps == 2, "Expected result to be 3 intervals"
    assert _compare_iterables(
        int_seq.step_points, (point1, point3)
    ), "Finite endpoints are not what is expected"
    assert (
        int_seq(float("-inf")) == init_value
    ), "Adding finite interval should not change initial value"
    assert (
        int_seq(float("inf")) == init_value
    ), "Adding finite interval should not change final value"
    assert int_seq(point1 - e) == init_value
    assert int_seq(point1) == init_value + value
    assert int_seq(point2) == init_value + value
    assert int_seq(point3 - e) == init_value + value
    assert int_seq(point3) == init_value


@pytest.mark.parametrize(
    "init_value, endpoints, value, delta",
    itertools.product(
        [0, 1.25, -1.25, 2, -2],
        [(-2, 1, 3), (-2, -1, 3), (-3, -2, -1), (1, 2, 3)],
        [-1, 2, 4],
        [3, -3, 1.5, -1.5],
    ),
)
def test_two_adjacent_finite_interval_different_value(
    init_value, endpoints, value, delta
):
    e = 0.0001
    int_seq = Stairs(initial_value=init_value)
    point1, point2, point3 = endpoints
    int_seq.layer(point1, point2, value)
    int_seq.layer(point2, point3, value + delta)
    assert int_seq.number_of_steps == 3, "Expected result to be 4 intervals"
    assert _compare_iterables(
        int_seq.step_points, (point1, point2, point3)
    ), "Finite endpoints are not what is expected"
    assert (
        int_seq(float("-inf")) == init_value
    ), "Adding finite interval should not change initial value"
    assert (
        int_seq(float("inf")) == init_value
    ), "Adding finite interval should not change final value"
    assert int_seq(point1 - e) == init_value
    assert int_seq(point1) == init_value + value
    assert int_seq(point2) == init_value + value + delta
    assert int_seq(point3 - e) == init_value + value + delta
    assert int_seq(point3) == init_value


@pytest.mark.parametrize(
    "init_value, endpoints, value, delta",
    itertools.product(
        [0, 1.25, -1.25, 2, -2],
        [(-2, 1, 2, 3), (-3, -2, -1, 3), (-4, -3, -2, -1), (0, 1, 2, 3)],
        [-1, 2, 4],
        [3, -3, 1.5, -1.5],
    ),
)
def test_two_overlapping_finite_interval(init_value, endpoints, value, delta):
    e = 0.0001
    int_seq = Stairs(initial_value=init_value)
    point1, point2, point3, point4 = endpoints
    int_seq.layer(point1, point3, value)
    int_seq.layer(point2, point4, value + delta)
    assert int_seq.number_of_steps == 4, "Expected result to be 5 intervals"
    assert _compare_iterables(
        int_seq.step_points, (point1, point2, point3, point4)
    ), "Finite endpoints are not what is expected"
    assert (
        int_seq(float("-inf")) == init_value
    ), "Adding finite interval should not change initial value"
    assert (
        int_seq(float("inf")) == init_value
    ), "Adding finite interval should not change final value"
    assert int_seq(point1 - e) == init_value
    assert int_seq(point1) == init_value + value
    assert int_seq(point2) == init_value + 2 * value + delta
    assert int_seq(point3 - e) == init_value + 2 * value + delta
    assert int_seq(point3) == init_value + value + delta
    assert int_seq(point4 - e) == init_value + value + delta
    assert int_seq(point4) == init_value


@pytest.mark.parametrize(
    "init_value, endpoints, value, delta",
    itertools.product(
        [0, 1.25, -1.25, 2, -2],
        [(-2, 1, 2, 3), (-3, -2, -1, 3), (-4, -3, -2, -1), (0, 1, 2, 3)],
        [-1, 2, 4],
        [3, -3, 1.5, -1.5],
    ),
)
def test_two_finite_interval_one_subinterval(init_value, endpoints, value, delta):
    e = 0.0001
    int_seq = Stairs(initial_value=init_value)
    point1, point2, point3, point4 = endpoints
    int_seq.layer(point1, point4, value)
    int_seq.layer(point2, point3, value + delta)
    assert int_seq.number_of_steps == 4, "Expected result to be 5 intervals"
    assert _compare_iterables(
        int_seq.step_points, (point1, point2, point3, point4)
    ), "Finite endpoints are not what is expected"
    assert (
        int_seq.initial_value == init_value
    ), "Adding finite interval should not change initial value"
    assert (
        int_seq(float("inf")) == init_value
    ), "Adding finite interval should not change final value"
    assert int_seq(point1 - e) == init_value
    assert int_seq(point1) == init_value + value
    assert int_seq(point2) == init_value + 2 * value + delta
    assert int_seq(point3 - e) == init_value + 2 * value + delta
    assert int_seq(point3) == init_value + value
    assert int_seq(point4 - e) == init_value + value
    assert int_seq(point4) == init_value


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_layer1(init_value):
    intervals_to_add = [(-2, 1), (3, 5), (1, 5), (-5, -3), (None, 0), (0, None)]
    int_seq = Stairs(initial_value=init_value)
    int_seq2 = Stairs(initial_value=init_value)
    for start, end in intervals_to_add:
        int_seq.layer(start, end)
    starts, ends = list(zip(*intervals_to_add))
    starts = [{None: np.nan}.get(x, x) for x in starts]
    ends = [{None: np.nan}.get(x, x) for x in ends]
    int_seq2.layer(starts, ends)
    assert int_seq.identical(int_seq2)
    assert int_seq2.identical(int_seq)


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_layer2(init_value):
    intervals_to_add = [(-2, 1, 1), (3, 5, 2), (1, 5, -1), (-5, -3, 3)]
    int_seq = Stairs(initial_value=init_value)
    int_seq2 = Stairs(initial_value=init_value)
    for interval in intervals_to_add:
        int_seq.layer(*interval)
    starts, ends, values = list(zip(*intervals_to_add))
    int_seq2.layer(starts, ends, values)
    assert int_seq.identical(int_seq2)
    assert int_seq2.identical(int_seq)


def test_layering_index(s1_fix):
    result = Stairs(
        start=pd.Index([1, -4, 3, 6, 7]),
        end=pd.Index([10, 5, 5, 7, 10]),
        value=pd.Index([2, -1.75, 2.5, -2.5, -2.5]),
    )
    assert result.identical(s1_fix)


def test_layering_frame(s1_fix):
    df = pd.DataFrame(
        {
            "start": [1, -4, 3, 6, 7],
            "end": [10, 5, 5, 7, 10],
            "value": [2, -1.75, 2.5, -2.5, -2.5],
        }
    )
    assert Stairs(df, "start", "end", "value").identical(s1_fix)


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "initial_value",
    [0, -1, 1],
)
def test_from_values(initial_value, closed):
    # this corresponds to the step function produced by S1 method
    values = pd.Series([-1.75, 0.25, 2.75, 2.00, -0.5, 0], index=[-4, 1, 3, 5, 6, 10])
    sf = Stairs.from_values(
        initial_value=initial_value,
        values=values + initial_value,
        closed=closed,
    )
    assert sf.identical(s1(closed) + initial_value)


@pytest.mark.parametrize(
    "index, values",
    [
        ([-np.inf], [0]),
        ([np.inf], [0]),
        ([1, 0], [10, 20]),
        ([0], ["1"]),
        ([], []),
    ],
)
def test_from_values_exception(index, values):
    with pytest.raises(ValueError):
        Stairs.from_values(
            initial_value=0,
            values=pd.Series(values, index=index),
            closed="left",
        )


def test_layering_trivial_1(s1_fix):
    assert s1_fix.copy().layer(1, 1).identical(s1_fix)


def test_layering_series_with_different_index():
    # GH112
    result = Stairs(
        start=pd.Series([0, 2, 4], index=[0, 2, 4]),
        end=pd.Series([1, 3, 5], index=[1, 3, 5]),
    )
    expected = pd.Series([1, 0, 1, 0, 1, 0])
    pd.testing.assert_series_equal(
        result.step_values,
        expected,
        check_names=False,
        check_index_type=False,
        check_dtype=False,
    )
    assert result.initial_value == 0
