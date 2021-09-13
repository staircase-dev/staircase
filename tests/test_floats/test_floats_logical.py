import itertools
import operator

import numpy as np
import pandas as pd
import pytest

import staircase.test_data as test_data
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


def test_logical_and_scalar_1(s3_fix):
    assert (s3_fix & 1).identical(s3_fix)


def test_logical_rand_scalar_1(s3_fix):
    assert (1 & s3_fix).identical(s3_fix)


def test_logical_and_scalar_2(s3_fix):
    assert (s3_fix & 0).identical(0)


def test_logical_rand_scalar_2(s3_fix):
    assert (0 & s3_fix).identical(0)


def test_logical_and_scalar_3(s3_fix):
    assert (s3_fix & np.nan).identical(np.nan)


def test_logical_rand_scalar_3(s3_fix):
    assert (np.nan & s3_fix).identical(np.nan)


def test_logical_or_scalar_1(s3_fix):
    assert (s3_fix | 1).identical(1)


def test_logical_ror_scalar_1(s3_fix):
    assert (1 | s3_fix).identical(1)


def test_logical_or_scalar_2(s3_fix):
    assert (s3_fix | 0).identical(s3_fix)


def test_logical_ror_scalar_2(s3_fix):
    assert (0 | s3_fix).identical(s3_fix)


def test_logical_or_scalar_3(s3_fix):
    assert (s3_fix | np.nan).identical(np.nan)


def test_logical_ror_scalar_3(s3_fix):
    assert (np.nan | s3_fix).identical(np.nan)


def test_logical_xor_scalar_1(s3_fix):
    assert (s3_fix ^ 1).identical(~s3_fix)


def test_logical_rxor_scalar_1(s3_fix):
    assert (1 ^ s3_fix).identical(~s3_fix)


def test_logical_xor_scalar_2(s3_fix):
    assert (s3_fix ^ 0).identical(s3_fix)


def test_logical_rxor_scalar_2(s3_fix):
    assert (0 ^ s3_fix).identical(s3_fix)


def test_logical_xor_scalar_3(s3_fix):
    assert (s3_fix ^ np.nan).identical(np.nan)


def test_logical_rxor_scalar_3(s3_fix):
    assert (np.nan ^ s3_fix).identical(np.nan)


def test_logical_xor_stairs_1(s3_fix):
    assert (s3_fix ^ s3_fix).identical(0)


def test_logical_xor_stairs_2(s3_fix):
    assert (s3_fix ^ ~s3_fix).identical(1)


def test_make_boolean(s2_fix):
    int_seq = s2_fix
    calc = int_seq.make_boolean()
    expected = Stairs()
    expected.layer(-2, 7, 1)
    expected.layer(8, 10, 1)
    assert calc.identical(expected), "Boolean calculation not what it should be"
    assert expected.identical(calc), "Boolean calculation not what it should be"


def test_invert(s2_fix):
    int_seq = s2_fix
    calc = ~int_seq
    expected = Stairs(initial_value=1)
    expected.layer(-2, 7, -1)
    expected.layer(8, 10, -1)
    assert calc.identical(expected), "Invert calculation not what it should be"
    assert expected.identical(calc), "Invert calculation not what it should be"


def test_and(s3_fix, s4_fix):
    calc = s3_fix & s4_fix
    expected = Stairs(initial_value=0)
    expected.layer(-10, -9.5)
    expected.layer(-7, -5)
    expected.layer(-2, 0)
    expected.layer(3.5, 6)
    expected.layer(6.5, 7)
    assert calc.identical(expected), "AND calculation not what it should be"
    assert expected.identical(calc), "AND calculation not what it should be"


def test_or(s3_fix, s4_fix):
    calc = s3_fix | s4_fix
    expected = Stairs(initial_value=0)
    expected.layer(-11, -7.5)
    expected.layer(-7, 0.5)
    expected.layer(1, 7)
    expected.layer(8.5, 9)
    expected.layer(9.5, 10)
    assert calc.identical(expected), "OR calculation not what it should be"
    assert expected.identical(calc), "OR calculation not what it should be"


@pytest.mark.parametrize(
    "op",
    [
        operator.and_,
        operator.or_,
        operator.xor,
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
        operator.and_,
        operator.or_,
        operator.xor,
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
