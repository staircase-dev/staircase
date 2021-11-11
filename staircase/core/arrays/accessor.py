import pandas as pd
from pandas.api.extensions import register_series_accessor

from staircase.constants import inf


@register_series_accessor("sc")
class StairsAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def corr(self, where=(-inf, inf)):
        return pd.DataFrame(
            self._obj.values.corr(where),
            index=self._obj.index,
            columns=self._obj.index,
        )

    def cov(self, where=(-inf, inf)):
        return pd.DataFrame(
            self._obj.values.cov(where),
            index=self._obj.index,
            columns=self._obj.index,
        )

    def logical_or(self):
        return self._obj.values.logical_or()

    def logical_and(self):
        return self._obj.values.logical_and()

    def sample(self, x):
        result = self._obj.values.sample(x)
        result.index = self._obj.index
        return result

    def limit(self, x, side="right"):
        result = self._obj.values.limit(x, side)
        result.index = self._obj.index
        return result
