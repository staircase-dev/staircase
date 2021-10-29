import datetime

import numpy as np
import pandas as pd

import staircase as sc
from staircase.constants import inf


def _is_datetime_like(x):
    return isinstance(
        x,
        (
            pd.Timestamp,
            pd.Timedelta,
            datetime.timedelta,
            datetime.datetime,
            datetime.date,
            np.datetime64,
            np.timedelta64,
        ),
    )


def _sanitize_binary_operands(self, other, copy_other=False):
    if not isinstance(self, sc.Stairs):
        self = sc.Stairs(initial_value=self, closed=other.closed)
    else:
        self = self.copy()

    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(initial_value=other, closed=self.closed)
    else:
        if copy_other:
            other = other.copy()
    return self, other


def _get_lims(stairs, closed):

    if stairs._closed == "left":
        return {
            "both": ("right", "right"),
            "left": ("right", "left"),
            "right": ("right", "right"),
            "neither": ("right", "left"),
        }[closed]
    else:
        return {
            "both": ("left", "left"),
            "left": ("left", "left"),
            "right": ("right", "left"),
            "neither": ("right", "left"),
        }[closed]


def _replace_none_with_infs(tuple_):
    if tuple_ == (-inf, inf):
        return tuple_
    left, right = tuple_
    if left is None:
        left = -inf
    if right is None:
        right = inf
    return (left, right)
