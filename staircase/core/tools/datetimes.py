from pandas import (
    Series,
    Timedelta,
    TimedeltaIndex,
    Timestamp,
    to_datetime,
    to_timedelta,
)
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


def _maybe_convert_from_timedeltas(iterable):
    def maybe_convert(x):
        return x / Timedelta("1 hr") if isinstance(x, Timedelta) else x

    return [maybe_convert(x) for x in iterable]


def _maybe_convert_from_timestamps(iterable, tz):
    def maybe_convert(x):
        return (
            _convert_date_to_float(x, tz)
            if isinstance(x, Timestamp) or hasattr(x, "__iter__")
            else x
        )

    return [maybe_convert(x) for x in iterable]


def _using_dates(collection):
    def dict_use_dates():
        s = next(iter(collection.values()))
        return s.use_dates, s.tz

    def series_use_dates():
        s = collection.values[0]
        return s.use_dates, s.tz

    def array_use_dates():
        s = collection[0]
        return s.use_dates, s.tz

    for func in (dict_use_dates, series_use_dates, array_use_dates):
        try:
            return func()
        except Exception:
            pass
    raise TypeError(
        "Could not determine if Stairs collection is using dates.  Collection should be a tuple, list, numpy array, dict or pandas.Series."
    )
