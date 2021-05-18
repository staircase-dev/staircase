import numpy as np
from sortedcontainers import SortedSet
from staircase.core.tools.datetimes import check_binop_timezones
import staircase as sc


def _sanitize_binary_operands(self, other, copy_other=False):
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
        if copy_other:
            other = other.copy()
    return self.copy(), other


def _get_union_of_points(collection):
    def dict_common_points():
        return collection.values()

    def series_common_points():
        return collection.values

    def array_common_points():
        return collection

    for func in (dict_common_points, series_common_points, array_common_points):
        try:
            stairs_instances = func()
            points = []
            for stair_instance in stairs_instances:
                points += list(stair_instance._keys())
            return SortedSet(points)
        except (AttributeError, TypeError):
            pass
    raise TypeError(
        "Collection should be a tuple, list, numpy array, dict or pandas.Series."
    )


def _get_stairs_method(name):
    return {
        "mean": sc.Stairs.mean,
        "median": sc.Stairs.median,
        "mode": sc.Stairs.mode,
        "max": sc.Stairs.max,
        "min": sc.Stairs.min,
    }[name]


def _verify_window(left_delta, right_delta, zero):
    assert left_delta <= zero, "left_delta must not be positive"
    assert right_delta >= zero, "right_delta must not be negative"
    assert right_delta - left_delta > zero, "window length must be non-zero"


def _from_cumulative(cumulative, use_dates=False, tz=None):
    return sc.Stairs(
        dict(
            zip(
                cumulative.keys(),
                np.insert(
                    np.diff(list(cumulative.values())),
                    0,
                    [next(iter(cumulative.values()))],
                ),
            )
        ),
        use_dates,
        tz,
    )
