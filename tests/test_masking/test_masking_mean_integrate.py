import math

import pytest

from staircase import Stairs


def s1_adj():
    return (
        Stairs()
        .layer(start=-4, value=-1.75)
        .layer(start=1, value=2)
        .layer(start=5, value=2.5)
        .layer(start=7, value=-0.75)
        .layer(start=8, value=-2.5)
        .layer(start=12, value=0.5)
        .mask((2, 4))
    )


def s2_adj():
    return (
        Stairs()
        .layer(start=-2, value=-1.75)
        .layer(start=1, value=-0.75)
        .layer(start=2, value=4.5)
        .layer(start=2.5, value=-2.5)
        .layer(start=7, value=2.5)
        .layer(start=8, value=-4.5)
        .layer(start=10, value=2.5)
        .layer(start=11, value=5)
        .layer(start=13, value=-5)
        .mask((4, 7))
        .mask((None, -2))
    )


@pytest.fixture
def s1_fix():
    return s1_adj()


@pytest.fixture
def s2_fix():
    return s2_adj()


def test_integrate1(s1_fix, s2_fix):
    assert s1_fix.integrate() == -2.75
    assert s2_fix.integrate() == -0.5


def test_integrate2(s1_fix, s2_fix):
    assert s1_fix.integrate((-1, 7.5)) == 3.5
    assert s2_fix.integrate((-1, 8.5)) == -5


def test_mean1(s1_fix, s2_fix):
    assert math.isclose(s1_fix.mean(), -0.19642857, abs_tol=1e-6)
    assert math.isclose(s2_fix.mean(), -0.04166666, abs_tol=1e-6)


def test_mean2(s1_fix, s2_fix):
    assert math.isclose(s1_fix.mean((2, 10)), 1.125, abs_tol=1e-6)
    assert math.isclose(s2_fix.mean((2, 11)), -0.45833333, abs_tol=1e-6)
