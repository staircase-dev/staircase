import math

import numpy as np
import pandas as pd

import staircase as sc
from staircase.constants import inf
from staircase.core.stats import docstrings
from staircase.util import _replace_none_with_infs
from staircase.util._decorators import Appender


class Xtiles(sc.core.stairs.Stairs):

    class_name = None
    scale_factor = None

    def sample(self, x):
        return (self.limit(x, side="left") + self.limit(x, side="right")) / 2

    def __call__(self, *args, **kwargs):
        return self.sample(*args, **kwargs)

    @classmethod
    def from_ecdf(cls, ecdf):
        assert ecdf._data is not None
        return cls.new(
            initial_value=ecdf._data.index[0],
            data=pd.DataFrame(
                {"value": np.append(ecdf._data.index, ecdf._data.index[-1])},
                index=np.append(0, ecdf._get_values().values * cls.scale_factor),
            ),
        )


class Percentiles(Xtiles):

    class_name = "Percentiles"
    scale_factor = 100


class Fractiles(Xtiles):

    class_name = "Fractiles"
    scale_factor = 1

    def to_percentiles(self):

        data = self._get_values().copy()
        data.index = data.index * 100
        return Percentiles.new(initial_value=self.initial_value, data=data.to_frame())


class ECDF(sc.core.stairs.Stairs):

    class_name = "ECDF"

    @staticmethod
    def from_stairs(stairs):
        # widths = np.diff(stairs._data.index.values)
        # heights = stairs._get_values().values[:-1]
        # ecdf_deltas = pd.Series(widths).groupby(heights).sum().rename("delta")
        ecdf_deltas = stairs.value_sums(dropna=True).rename("delta")
        deltas_sum = ecdf_deltas.sum()
        normalized_probability_deltas = ecdf_deltas / deltas_sum

        ecdf = ECDF.new(
            initial_value=0,
            data=normalized_probability_deltas.to_frame(),
            closed="left",
        )
        ecdf._denormalize_probability_factor = deltas_sum
        return ecdf

    def hist(self, bins="unit", closed="left", stat="sum"):

        step_points = self.step_points
        if isinstance(bins, str) and bins == "unit":
            round_func = math.floor if closed == "left" else math.ceil
            bins = range(
                round_func(min(step_points)) - (closed == "right"),
                round_func(max(step_points)) + (closed == "left") + 1,
            )

        if not isinstance(bins, pd.IntervalIndex):
            bins = pd.IntervalIndex.from_breaks(bins, closed=closed)

        values = self.limit(bins.right, side=bins.closed) - self.limit(
            bins.left, side=bins.closed
        )

        # inspired by seaborn.histplot
        if stat != "probability":
            values = values * self._denormalize_probability_factor
            if stat in ("frequency", "density"):
                widths = bins.map(lambda i: i.right - i.left)
                if stat == "frequency":
                    values = values / widths
                elif stat == "density":
                    values = values / np.dot(values, widths)

        return pd.Series(
            data=values,
            index=bins,
            # dtype="float64",
        )

    def percentiles(self):
        return Percentiles.from_ecdf(self)

    def fractiles(self):
        return Fractiles.from_ecdf(self)


class Dist:
    def __init__(self, stairs):
        self._ecdf = None
        self._fractiles = None
        self._percentiles = None
        self._stairs = stairs
        self._ecdf = ECDF.from_stairs(stairs)

    def hist(self, bins="unit", closed="left", stat="sum"):
        return self._ecdf.hist(bins, closed, stat)

    def _create_fractiles(self):
        self._fractiles = Fractiles.from_ecdf(self._ecdf)

    def _create_percentiles(self):
        self._percentiles = Percentiles.from_ecdf(self._ecdf)

    @property
    def fractile(self):
        if self._fractiles is None:
            self._create_fractiles()
        return self._fractiles

    @property
    def percentile(self):
        if self._percentiles is None:
            self._create_percentiles()
        return self._percentiles

    @property
    def ecdf(self):
        return self._ecdf

    def quantiles(self, n):
        assert n > 0 and isinstance(n, int)
        return self.fractile(np.linspace(0, 1, n + 1)[1:-1])


def _get_dist(self):
    if self._dist is None:
        self._dist = Dist(self)
    return self._dist
