import numpy as np
import pandas as pd
import pytest

import staircase as sc
from staircase.core.ops.common import ClosedMismatchError


def s1(initial_value=0):
    int_seq1 = sc.Stairs(initial_value=initial_value)
    int_seq1.layer(1, 10, 2)
    int_seq1.layer(-4, 5, -1.75)
    int_seq1.layer(3, 5, 2.5)
    int_seq1.layer(6, 7, -2.5)
    int_seq1.layer(7, 10, -2.5)
    return int_seq1


def s2(initial_value=0):
    int_seq2 = sc.Stairs(initial_value=initial_value)
    int_seq2.layer(1, 7, -2.5)
    int_seq2.layer(8, 10, 5)
    int_seq2.layer(2, 5, 4.5)
    int_seq2.layer(2.5, 4, -2.5)
    int_seq2.layer(-2, 1, -1.75)
    return int_seq2


@pytest.fixture
def s1_fix():
    return s1(0)


def test_fillna(s1_fix):
    s = s1_fix.clip(None, 10).mask((-2, 0)).mask((4, 7)).fillna(1)
    pd.testing.assert_series_equal(
        s.step_values,
        pd.Series(
            [-1.75, 1, -1.75, 0.25, 2.75, 1, -0.5, 1],
            index=[-4, -2, 0, 1, 3, 4, 7, 10],
        ),
        check_names=False,
        check_index_type=False,
    )
    assert s.initial_value == s1_fix.initial_value


@pytest.mark.parametrize(
    "method",
    ["ffill", "pad"],
)
def test_fillna_ffill(s1_fix, method):
    s = s1_fix.mask((None, -2)).mask((0, 2)).mask((8, None)).fillna(method)
    pd.testing.assert_series_equal(
        s.step_values,
        pd.Series(
            [-1.75, 0.25, 2.75, 2.0, -0.5],
            index=[-2, 2, 3, 5, 6],
        ),
        check_names=False,
        check_index_type=False,
    )
    assert np.isnan(s.initial_value)


@pytest.mark.parametrize(
    "method",
    ["bfill", "backfill"],
)
def test_fillna_bfill(s1_fix, method):
    s = s1_fix.mask((None, -2)).mask((0, 2)).mask((8, None)).fillna(method)
    pd.testing.assert_series_equal(
        s.step_values,
        pd.Series(
            [0.25, 2.75, 2.0, -0.5, np.nan],
            index=[0, 3, 5, 6, 8],
        ),
        check_names=False,
        check_index_type=False,
    )
    assert s.initial_value == -1.75


def test_fillna_stairs(s1_fix, s2_fix):
    s = (
        s1_fix.mask((None, -2))
        .mask((0, 2))
        .mask((8, None))
        .fillna(s2_fix.mask((11, None)).mask((0.5, 1.5)))
    )
    pd.testing.assert_series_equal(
        s.step_values,
        pd.Series(
            [-1.75, np.nan, -2.5, 0.25, 2.75, 2.0, -0.5, 5.0, 0.0, np.nan],
            index=[-2.0, 0.5, 1.5, 2.0, 3.0, 5.0, 6.0, 8.0, 10.0, 11.0],
        ),
        check_names=False,
        check_index_type=False,
    )
    assert s.initial_value == 0


def test_fillna_stairs_error(s1_fix):
    with pytest.raises(ClosedMismatchError):
        s1_fix.fillna(sc.Stairs(start=1, end=2, closed="right"))
