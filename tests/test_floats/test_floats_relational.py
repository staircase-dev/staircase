import operator

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


def test_lt(s1_fix, s2_fix):
    calc = s1_fix < s2_fix
    expected = Stairs(initial_value=0)
    expected.layer(-4, -2)
    expected.layer(2, 2.5)
    expected.layer(7, 10)
    assert calc.identical(expected), "LT calculation not what it should be"
    assert expected.identical(calc), "LT calculation not what it should be"


def test_gt(s1_fix, s2_fix):
    calc = s1_fix > s2_fix
    expected = Stairs(initial_value=0)
    expected.layer(1, 2)
    expected.layer(2.5, 7)
    assert calc.identical(expected), "GT calculation not what it should be"
    assert expected.identical(calc), "GT calculation not what it should be"


def test_le(s1_fix, s2_fix):
    calc = s1_fix <= s2_fix
    expected = Stairs(initial_value=1)
    expected.layer(1, 2, -1)
    expected.layer(2.5, 7, -1)
    assert calc.identical(expected), "LE calculation not what it should be"
    assert expected.identical(calc), "LE calculation not what it should be"


def test_ge(s1_fix, s2_fix):
    calc = s1_fix >= s2_fix
    expected = Stairs(initial_value=1)
    expected.layer(-4, -2, -1)
    expected.layer(2, 2.5, -1)
    expected.layer(7, 10, -1)
    assert calc.identical(expected), "GE calculation not what it should be"
    assert expected.identical(calc), "GE calculation not what it should be"


def test_eq_1(s1_fix, s2_fix):
    calc = s1_fix == s2_fix
    expected = Stairs(initial_value=1)
    expected.layer(-4, -2, -1)
    expected.layer(1, 10, -1)
    assert calc.identical(expected), "EQ calculation not what it should be"
    assert expected.identical(calc), "EQ calculation not what it should be"


def test_eq_2(s1_fix, s2_fix):
    calc = s1_fix == s2_fix
    expected = Stairs(initial_value=1)
    expected.layer(-4, -2, -1)
    expected.layer(1, 10, -1)
    assert calc.identical(expected), "EQ calculation not what it should be"
    assert expected.identical(calc), "EQ calculation not what it should be"


def test_ne(s1_fix, s2_fix):
    calc = s1_fix != s2_fix
    expected = Stairs(initial_value=0)
    expected.layer(-4, -2, 1)
    expected.layer(1, 10, 1)
    assert calc.identical(expected), "NOT EQUAL calculation not what it should be"
    assert expected.identical(calc), "NOT EQUAL calculation not what it should be"


def test_eq_3():
    assert Stairs(initial_value=3) == 3


def test_ne_3(s1_fix):
    assert s1_fix != 3


@pytest.mark.parametrize(
    "op",
    [
        operator.eq,
        operator.ne,
        operator.lt,
        operator.gt,
        operator.le,
        operator.ge,
    ],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "operands",
    [("stairs", "stairs"), ("stairs", "scalar"), ("scalar", "stairs")],
)
def test_closed_binary_ops(op, closed, operands):
    operand_dict = {"stairs": Stairs(closed=closed), "scalar": 1}
    operand0 = operand_dict[operands[0]]
    operand1 = operand_dict[operands[1]]
    result = op(operand0, operand1)
    assert result.closed == closed


@pytest.mark.parametrize(
    "op",
    [
        operator.eq,
        operator.ne,
        operator.lt,
        operator.gt,
        operator.le,
        operator.ge,
    ],
)
@pytest.mark.parametrize(
    "nan_pos",
    ["first", "second"],
)
def test_binary_ops_with_nan(s1_fix, op, nan_pos):
    # GH109
    operands = (np.nan, s1_fix) if nan_pos == "first" else (s1_fix, np.nan)
    result = op(*operands)
    assert result._data is None, "wrong internal representation in resulting Stairs"
