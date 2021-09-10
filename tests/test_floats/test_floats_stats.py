import numpy as np
import pytest

from staircase import Stairs


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


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_base_integral_0_2(init_value):
    int_seq = Stairs(initial_value=init_value)
    assert int_seq.agg("integral", (0, 2)) == 2 * init_value


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_base_integral_neg1_1(init_value):
    int_seq = Stairs(initial_value=init_value)
    assert int_seq.agg("integral", (-1, 1)) == 2 * init_value


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_base_integral_neg2_0(init_value):
    int_seq = Stairs(initial_value=init_value)
    assert int_seq.agg("integral", (-2, 0)) == 2 * init_value


@pytest.mark.parametrize("init_value", [0, 1.25, -1.25, 2, -2])
def test_base_integral_point5_1(init_value):
    int_seq = Stairs(initial_value=init_value)
    assert int_seq.agg("integral", (0.5, 1)) == 0.5 * init_value


def test_integral1(s1_fix, s2_fix):
    assert s1_fix.integral() == -2.75
    assert s2_fix.integral() == -0.5


def test_integral2(s1_fix, s2_fix):
    assert s1_fix.agg("integral", (-1, 5.5)) == 3.5
    assert s2_fix.agg("integral", (-1, 5.5)) == -5


def test_mean1(s1_fix, s2_fix):
    assert abs(s1_fix.mean() - -0.19642857) < 0.000001
    assert abs(s2_fix.mean() - -0.04166666) < 0.000001


def test_mean2(s1_fix, s2_fix):
    assert abs(s1_fix.agg("mean", (2, 8)) - 1.125) < 0.000001
    assert abs(s2_fix.agg("mean", (2, 8)) - -0.45833333) < 0.000001


def test_integral_0():
    assert Stairs(initial_value=0).layer(None, 0).integral() is np.nan


def test_mean_nan():
    assert Stairs(initial_value=0).layer(None, 0).mean() is np.nan


# np.var(st1(np.linspace(-4,10, 10000000))) = 2.501594244387741
# np.var(st1(np.linspace(-5,10, 10000000))) = 2.3372686165530117
# np.var(st1(np.linspace(1,12, 10000000))) = 1.5433884747933315


@pytest.mark.parametrize(
    "bounds, expected",
    [
        ((), 2.501594244387741),
        (((-5, 10),), 2.3372686165530117),
        (((1, 12),), 1.5433884747933315),
    ],
)
def test_s1_var(bounds, expected):
    assert np.isclose(s1().agg("var", *bounds), expected, atol=0.0001)


# np.var(st2(np.linspace(-2, 10, 10000000))) = 7.024303861110942
# np.var(st2(np.linspace(-3, 7.5, 10000000))) = 2.2678568437499633
# np.var(st2(np.linspace(0, 14, 10000000))) = 5.538902194132663


@pytest.mark.parametrize(
    "bounds, expected",
    [
        ((), 7.024303861110942),
        (((-3, 7.5),), 2.2678568437499633),
        (((0, 14),), 5.538902194132663),
    ],
)
def test_s2_var(bounds, expected):
    assert np.isclose(s2().agg("var", *bounds), expected, atol=0.0001)


# np.std(st1(np.linspace(-4,10, 10000000))) = 1.5816428940780978
# np.std(st1(np.linspace(-5,10, 10000000))) = 1.528797568034358
# np.std(st1(np.linspace(1,12, 10000000))) = 1.242331869829206


@pytest.mark.parametrize(
    "bounds, expected",
    [
        ((), 1.5816428940780978),
        (((-5, 10),), 1.528797568034358),
        (((1, 12),), 1.242331869829206),
    ],
)
def test_s1_std(bounds, expected):
    assert np.isclose(s1().agg("std", *bounds), expected, atol=0.0001)


# np.std(st2(np.linspace(-2, 10, 10000000))) = 2.650340329299417
# np.std(st2(np.linspace(-3, 7.5, 10000000))) = 1.5059405179986238
# np.std(st2(np.linspace(0, 14, 10000000))) = 2.3534872411238315


@pytest.mark.parametrize(
    "bounds, expected",
    [
        ((), 2.650340329299417),
        (((-3, 7.5),), 1.5059405179986238),
        (((0, 14),), 2.3534872411238315),
    ],
)
def test_s2_std(bounds, expected):
    assert np.isclose(s2().agg("std", *bounds), expected, atol=0.0001)


# # np.cov(st1(pts[:-100000]), st1(pts[100000:]))[0,1] = 1.9386094481108465
# # np.cov(st1(np.linspace(-4, 8, 12*100000 + 1)), st1(np.linspace(-2, 10, 12*100000 + 1)))[0,1] = 1.1184896017794723
# # np.cov(st1(np.linspace(-4, 8, 12*100000 + 1)), st1.shift(-2)(np.linspace(-4, 8, 12*100000 + 1)))[0,1] = 1.1184896017794723


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"where": (-4, 10), "lag": 1}, 1.9386094481108465),
        ({"where": (-4, 10), "lag": 2}, 1.1184896017794723),
        ({"where": (-4, 8), "lag": 2, "clip": "post"}, 1.1184896017794723),
    ],
)
def test_s1_autocov(kwargs, expected):
    assert np.isclose(s1().cov(s1(), **kwargs), expected, atol=0.00001)


# # np.cov(st2(np.linspace(-2, 9, 11*100000 + 1)), st2(np.linspace(-1, 10, 11*100000 + 1)))[0,1 = 3.1022721590913256
# # np.cov(st2(np.linspace(0, 6, 12*100000 + 1)), st2(np.linspace(2, 8, 12*100000 + 1)))[0,1] = -0.7291746267294938
# # np.cov(st2(np.linspace(0, 6, 12*100000 + 1)), st2.shift(-2)(np.linspace(0, 6, 12*100000 + 1)))[0,1] = -0.7291746267294938


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"where": (-2, 10), "lag": 1}, 3.1022721590913256),
        ({"where": (0, 8), "lag": 2}, -0.7291746267294938),
        ({"where": (0, 6), "lag": 2, "clip": "post"}, -0.7291746267294938),
    ],
)
def test_s2_autocov(kwargs, expected):
    assert np.isclose(s2().cov(s2(), **kwargs), expected, atol=0.00001)


# # np.cov(st1(np.linspace(-2, 9, 11*100000 + 1)), st2(np.linspace(-1, 10, 11*100000 + 1)))[0,1 = -0.08677679611199672
# # np.cov(st1(np.linspace(0, 6, 12*100000 + 1)), st2(np.linspace(2, 8, 12*100000 + 1)))[0,1] = -1.970493123547197
# # np.cov(st1(np.linspace(0, 6, 12*100000 + 1)), st2.shift(-2)(np.linspace(0, 6, 12*100000 + 1)))[0,1] = -1.970493123547197


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"where": (-2, 10), "lag": 1}, -0.08677679611199672),
        ({"where": (0, 8), "lag": 2}, -1.970493123547197),
        ({"where": (0, 6), "lag": 2, "clip": "post"}, -1.970493123547197),
    ],
)
def test_crosscov(kwargs, expected):
    assert np.isclose(s1().cov(s2(), **kwargs), expected, atol=0.00001)


# # np.corrcoef(st1(pts[:-100000]), st1(pts[100000:]))[0,1] = 0.6927353407369307
# # np.corrcoef(st1(np.linspace(-4, 8, 12*100000 + 1)), st1(np.linspace(-2, 10, 12*100000 + 1)))[0,1] = -0.2147502741669856
# # np.corrcoef(st1(np.linspace(-4, 8, 12*100000 + 1)), st1.shift(-2)(np.linspace(-4, 8, 12*100000 + 1)))[0,1] = -0.2147502741669856


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"where": (-2, 10), "lag": 1}, 0.6927353407369307),
        ({"where": (0, 8), "lag": 2}, -0.2147502741669856),
        ({"where": (0, 6), "lag": 2, "clip": "post"}, -0.2147502741669856),
    ],
)
def test_s1_autocorr(kwargs, expected):
    assert np.isclose(s1().corr(s1(), **kwargs), expected, atol=0.00001)


# # np.corrcoef(st2(pts[:-100000]), st2(pts[100000:]))[0,1] = 0.5038199912440895
# # np.corrcoef(st2(np.linspace(-4, 8, 12*100000 + 1)), st2(np.linspace(-2, 10, 12*100000 + 1)))[0,1] = -0.2419504099129966
# # np.corrcoef(st2(np.linspace(-4, 8, 12*100000 + 1)), st2.shift(-2)(np.linspace(-4, 8, 12*100000 + 1)))[0,1] = -0.2419504099129966


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"where": (-2, 10), "lag": 1}, 0.5038199912440895),
        ({"where": (0, 8), "lag": 2}, -0.2419504099129966),
        ({"where": (0, 6), "lag": 2, "clip": "post"}, -0.2419504099129966),
    ],
)
def test_s2_autocorr(kwargs, expected):
    assert np.isclose(s2().corr(s2(), **kwargs), expected, atol=0.00001)


# # np.corrcoef(st1(pts[:-100000]), st2(pts[100000:]))[0,1] = -0.01966642657198049
# # np.corrcoef(st1(np.linspace(-4, 8, 12*100000 + 1)), st2(np.linspace(-2, 10, 12*100000 + 1)))[0,1] = -0.7086484036832666
# # np.corrcoef(st1(np.linspace(-4, 8, 12*100000 + 1)), st2.shift(-2)(np.linspace(-4, 8, 12*100000 + 1)))[0,1] = -0.7086484036832666


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"where": (-2, 10), "lag": 1}, -0.01966642657198049),
        ({"where": (0, 8), "lag": 2}, -0.7086484036832666),
        ({"where": (0, 6), "lag": 2, "clip": "post"}, -0.7086484036832666),
    ],
)
def test_crosscorr(kwargs, expected):
    assert np.isclose(s1().corr(s2(), **kwargs), expected, atol=0.00001)


@pytest.mark.parametrize(
    "closed, kwargs, expected_val",
    [
        (
            "left",
            {},
            -1.75,
        ),
        (
            "left",
            {"where": (1, 6)},
            0.25,
        ),
        (
            "right",
            {"where": (1, 6), "closed": "left"},
            -1.75,
        ),
        (
            "left",
            {"where": (1, 6), "closed": "right"},
            -0.5,
        ),
    ],
)
def test_s1_min(closed, kwargs, expected_val):
    from staircase.core import stats

    assert stats.min(s1(closed=closed), **kwargs) == expected_val


@pytest.mark.parametrize(
    "closed, kwargs, expected_val",
    [
        (
            "left",
            {},
            2.75,
        ),
        (
            "left",
            {"where": (-4, 1)},
            -1.75,
        ),
        (
            "right",
            {"where": (-4, 1), "closed": "left"},
            0.0,
        ),
        (
            "left",
            {"where": (-4, 1), "closed": "right"},
            0.25,
        ),
    ],
)
def test_s1_max(closed, kwargs, expected_val):
    from staircase.core import stats

    assert stats.max(s1(closed=closed), **kwargs) == expected_val


@pytest.mark.parametrize(
    "closed, kwargs, expected_val",
    [
        (
            "left",
            {},
            np.array([-1.75, -0.5, 0.0, 0.25, 2.0, 2.75]),
        ),
        (
            "left",
            {"where": (-4, 10)},
            np.array([-1.75, -0.5, 0.25, 2.0, 2.75]),
        ),
        (
            "left",
            {"where": (1, 6)},
            np.array([0.25, 2.0, 2.75]),
        ),
        (
            "right",
            {"where": (1, 6), "closed": "left"},
            np.array([-1.75, 0.25, 2.0, 2.75]),
        ),
        (
            "left",
            {"where": (1, 6), "closed": "right"},
            np.array([-0.5, 0.25, 2.0, 2.75]),
        ),
    ],
)
def test_s1_values_in_range(closed, kwargs, expected_val):
    assert np.array_equal(s1(closed=closed).values_in_range(**kwargs), expected_val)
