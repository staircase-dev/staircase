from pandas import Series, Timedelta, TimedeltaIndex, to_datetime, to_timedelta
import numpy as np

origin = to_datetime("2000-1-1")


def check_binop_timezones(first, second):
    assert first.tz == second.tz, "operands must have the same timezone, or none at all"


def _convert_date_to_float(val, tz=None):
    if val is None:
        return None
    if hasattr(val, "__iter__"):
        if not isinstance(val, Series):
            val = Series(val)
        deltas = TimedeltaIndex(val - origin.tz_localize(tz))
        return list(deltas / Timedelta(1, "h"))
    return (val - origin.tz_localize(tz)) / Timedelta(1, "h")


def _convert_float_to_date(val, tz=None):
    if hasattr(val, "__iter__"):
        if not isinstance(val, np.ndarray):
            val = np.array(val)
        return list(to_timedelta(val * 3600, unit="s") + origin.tz_localize(tz))
    return to_timedelta(val * 3600, unit="s") + origin.tz_localize(tz)
