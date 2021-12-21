import numbers
from collections.abc import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.api.extensions import (
    ExtensionArray,
    ExtensionDtype,
    register_extension_dtype,
)
from pandas.core.dtypes.inference import is_dict_like, is_list_like

from staircase.constants import inf
from staircase.core.arrays import docstrings
from staircase.core.stairs import Stairs
from staircase.core.stats.statistic import corr as _corr
from staircase.core.stats.statistic import cov as _cov
from staircase.util._decorators import Appender


@register_extension_dtype
class StairsDtype(ExtensionDtype):

    type = Stairs
    name = "Stairs"
    na_value = pd.NA

    @classmethod
    def construct_from_string(cls, string):
        if string == cls.name:
            return cls()
        else:
            raise TypeError("Cannot construct a '{}' from '{}'".format(cls, string))

    @classmethod
    def construct_array_type(cls):
        return StairsArray


def _isna(value):
    return pd.isna(value)


def _make_logical(func):
    def logical_func(x, axis=0):
        return np.where(
            np.logical_or.reduce(np.isnan(x), axis=axis),
            np.nan,
            func.reduce(x, axis=axis),
        )

    return logical_func


class StairsArray(ExtensionArray):

    _dtype = StairsDtype()
    ndim = 1

    def __init__(self, data):
        if isinstance(data, self.__class__):
            self.data = data.data
        elif isinstance(data, np.ndarray):
            if not data.ndim == 1:
                raise ValueError(
                    "'data' should be a 1-dimensional array of Stairs objects."
                )
            self.data = data
        elif is_dict_like(data):
            self.data = np.array([data[k] for k in data.keys()])
        elif isinstance(data, Stairs) or is_list_like(data):
            self.data = np.array(data, ndmin=1)
        else:
            raise TypeError("'data' should be array of Stairs objects.")

    @property
    def dtype(self):
        return self._dtype

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if isinstance(idx, numbers.Integral):
            return self.data[idx]
        elif isinstance(idx, (Iterable, slice)):
            return StairsArray(self.data[idx])
        else:
            raise TypeError("Index type not supported", idx)

    def __setitem__(self, key, value):
        if isinstance(value, Stairs) or _isna(value):
            if _isna(value):
                # internally only use None as missing value indicator
                # but accept others
                value = None
            if isinstance(key, (slice, Iterable)):
                value_array = np.empty(1, dtype=object)
                value_array[:] = [value]
                self.data[key] = value_array
            else:
                self.data[key] = value

    def copy(self):
        return StairsArray(self.data.copy())

    def take(self, indices, allow_fill=False, fill_value=None):
        from pandas.api.extensions import take

        result = take(self.data, indices, allow_fill=allow_fill, fill_value=fill_value)
        if allow_fill and fill_value is None:
            result[pd.isna(result)] = None
        return StairsArray(result)

    def isna(self):
        return np.array([g is None for g in self.data], dtype="bool")

    def bool(self):
        result = np.array([bool(s) for s in self.data])
        return result

    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        if isinstance(scalars, Stairs):
            scalars = [scalars]
        return StairsArray(scalars)

    @classmethod
    def _from_factorized(cls, values, original):
        return cls(values)

    @property
    def nbytes(self):
        return self._itemsize * len(self)

    @classmethod
    def _concat_same_type(cls, to_concat):
        print("hello")
        return cls(np.concatenate([array.data for array in to_concat]))

    @Appender(docstrings.make_docstring("array", "mean"), join="\n", indents=1)
    def mean(self):
        return self.agg(np.mean)

    @Appender(docstrings.make_docstring("array", "median"), join="\n", indents=1)
    def median(self):
        return self.agg(np.median)

    @Appender(docstrings.make_docstring("array", "sum"), join="\n", indents=1)
    def sum(self):
        return self.agg(np.sum)

    @Appender(docstrings.make_docstring("array", "min"), join="\n", indents=1)
    def min(self):
        return self.agg(np.min)

    @Appender(docstrings.make_docstring("array", "max"), join="\n", indents=1)
    def max(self):
        return self.agg(np.max)

    @Appender(docstrings.make_docstring("array", "agg"), join="\n", indents=1)
    def agg(self, func):
        index = pd.Index(
            np.unique(
                np.concatenate(
                    [
                        s.step_changes.index  # using .step_changes.index instead of .step_points to retain timezones
                        for s in (sf for sf in self.data if sf.number_of_steps)
                    ]
                )
            )
        )
        new_values = func([s.limit(index, "right") for s in self.data], axis=0)
        if new_values.dtype == "bool":
            new_values = new_values.astype(int)

        return Stairs._new(
            initial_value=func([s.initial_value for s in self.data]),
            data=pd.Series(
                new_values,
                index=index,
                name="value",
            ).to_frame(),
            closed=self.data[0].closed,
        )._remove_redundant_step_points()

    @Appender(docstrings.make_docstring("array", "sample"), join="\n", indents=1)
    def sample(self, x):
        array = pd.Series(self.data)
        return array.apply(Stairs.sample, x=x, include_index=True)

    @Appender(docstrings.make_docstring("array", "limit"), join="\n", indents=1)
    def limit(self, x, side="right"):
        array = pd.Series(self.data)
        return array.apply(Stairs.limit, x=x, side=side, include_index=True)

    @Appender(docstrings.make_docstring("array", "logical_or"), join="\n", indents=1)
    def logical_or(self):
        return self.agg(_make_logical(np.logical_or))

    @Appender(docstrings.make_docstring("array", "logical_and"), join="\n", indents=1)
    def logical_and(self):
        return self.agg(_make_logical(np.logical_and))

    @Appender(docstrings.make_docstring("array", "plot"), join="\n", indents=1)
    def plot(self, ax=None, labels=None, **kwargs):
        if ax is None:
            _, ax = plt.subplots()
        if labels is None:
            labels = range(len(self))
        elif len(labels) != len(self):
            raise ValueError(
                f"Number of labels supplied: {len(labels)}  Required: {len(self)}."
            )
        for s, l in zip(self, labels):
            s.plot(ax=ax, label=l, style="step", **kwargs)
        return ax

    def _reduce(self, name: str, *, skipna: bool = True, **kwargs):
        return {
            "sum": self.sum,
            "mean": self.mean,
            "min": self.min,
            "max": self.max,
            "median": self.median,
            "corr": self.corr,
            "agg": self.agg,
        }[name]()

    @Appender(docstrings.negate_docstring, join="\n", indents=1)
    def negate(self):
        return StairsArray(-self.data)

    __neg__ = negate


def _make_binary_func(func_str):

    stairs_func = getattr(Stairs, func_str)
    docstring = docstrings.make_binop_docstring(funcstr)

    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        if isinstance(other, (int, float, Stairs)):
            result = StairsArray([stairs_func(s, other) for s in self.data])
        elif is_list_like(other):
            if len(other) != len(self):
                return ValueError("Arrays have different lengths.")
            result = StairsArray(
                [stairs_func(s1, s2) for s1, s2 in zip(self.data, other.data)]
            )
        else:
            return NotImplemented
        return result

    return func


for funcstr in (
    "ge",
    "gt",
    "le",
    "lt",
    "eq",
    "ne",
    "add",
    "subtract",
    "multiply",
    "divide",
    "radd",
    "rsubtract",
    "rmultiply",
    "rdivide",
):
    func = _make_binary_func(funcstr)
    setattr(StairsArray, funcstr, func)
    magic = {
        "subtract": "sub",
        "multiply": "mul",
        "divide": "truediv",
        "rsubtract": "rsub",
        "rmultiply": "rmul",
        "rdivide": "rtruediv",
    }.get(funcstr, funcstr)
    setattr(StairsArray, f"__{magic}__", func)


def _make_corr_cov_func(docstring, stairs_method, assume_ones_diagonal):
    @Appender(docstring, join="\n", indents=1)
    def func(self, where=(-inf, inf)):
        size = len(self.data)
        vals = np.ones(shape=(size, size))
        for i in range(size):
            for j in range(i + assume_ones_diagonal, size):
                vals[i, j] = stairs_method(self.data[i], self.data[j], where=where)
                vals[j, i] = vals[i, j]
        return vals

    return func


StairsArray.corr = _make_corr_cov_func(
    docstrings.make_docstring("array", "corr"), _corr, assume_ones_diagonal=True
)
StairsArray.cov = _make_corr_cov_func(
    docstrings.make_docstring("array", "cov"), _cov, assume_ones_diagonal=False
)
