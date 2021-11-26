import pandas as pd
from pandas.api.extensions import register_series_accessor

from staircase.constants import inf
from staircase.core.arrays import docstrings
from staircase.core.arrays.extension import StairsDtype
from staircase.util._decorators import Appender


@register_series_accessor("sc")
class StairsAccessor:
    def __init__(self, pandas_obj):
        if not isinstance(pandas_obj.dtype, StairsDtype):
            raise TypeError(
                'sc accessor only valid for Series with Stairs dtype.  Convert using .astype("Stairs").'
            )
        self._obj = pandas_obj

    @Appender(docstrings.make_docstring("accessor", "corr"), join="\n", indents=1)
    def corr(self, where=(-inf, inf)):
        return pd.DataFrame(
            self._obj.values.corr(where),
            index=self._obj.index,
            columns=self._obj.index,
        )

    @Appender(docstrings.make_docstring("accessor", "cov"), join="\n", indents=1)
    def cov(self, where=(-inf, inf)):
        return pd.DataFrame(
            self._obj.values.cov(where),
            index=self._obj.index,
            columns=self._obj.index,
        )

    @Appender(docstrings.make_docstring("accessor", "logical_or"), join="\n", indents=1)
    def logical_or(self):
        return self._obj.values.logical_or()

    @Appender(
        docstrings.make_docstring("accessor", "logical_and"), join="\n", indents=1
    )
    def logical_and(self):
        return self._obj.values.logical_and()

    @Appender(docstrings.make_docstring("accessor", "sample"), join="\n", indents=1)
    def sample(self, x):
        result = self._obj.values.sample(x)
        result.index = self._obj.index
        return result

    @Appender(docstrings.make_docstring("accessor", "limit"), join="\n", indents=1)
    def limit(self, x, side="right"):
        result = self._obj.values.limit(x, side)
        result.index = self._obj.index
        return result

    @Appender(docstrings.make_docstring("accessor", "plot"), join="\n", indents=1)
    def plot(self, ax=None, **kwargs):
        labels = self._obj.index
        return self._obj.values.plot(ax, labels, **kwargs)
