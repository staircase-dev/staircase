import numpy as np
from pandas import Timestamp
from staircase.core.stats.distribution import percentile_stairs
from staircase.core.tools.datetimes import _convert_date_to_float
from staircase.util._decorators import Appender
from staircase.core.stats import docstrings
import staircase as sc


@Appender(docstrings.integrate_docstring, join="\n", indents=1)
def integrate(self, lower=float("-inf"), upper=float("inf")):
    area, _ = self.get_integral_and_mean(lower, upper)
    return area


@Appender(docstrings.mean_docstring, join="\n", indents=1)
def mean(self, lower=float("-inf"), upper=float("inf")):
    _, mean = self.get_integral_and_mean(lower, upper)
    return mean


@Appender(docstrings.percentile_docstring, join="\n", indents=1)
def percentile(self, x, lower=float("-inf"), upper=float("inf")):
    assert 0 <= x <= 100
    percentiles = percentile_stairs(self, lower, upper)
    return (percentiles(x, how="left") + percentiles(x, how="right")) / 2


@Appender(docstrings.median_docstring, join="\n", indents=1)
def median(self, lower=float("-inf"), upper=float("inf")):
    return percentile(self, 50, lower, upper)


@Appender(docstrings.mode_docstring, join="\n", indents=1)
def mode(self, lower=float("-inf"), upper=float("inf")):
    value_count = (
        self.clip(lower, upper)
        .to_dataframe()
        .iloc[1:-1]
        .assign(duration=lambda df: df.end - df.start)
        .groupby("value")["duration"]
        .sum()
    )
    return value_count.idxmax()


@Appender(docstrings.var_docstring, join="\n", indents=1)
def var(self, lower=float("-inf"), upper=float("inf")):
    percentile_minus_mean = (
        percentile_stairs(self, lower, upper) - self.mean(lower, upper)
    )._cumulative()
    return (
        sc.Stairs.from_cumulative(
            dict(
                zip(
                    percentile_minus_mean.keys(),
                    (val * val for val in percentile_minus_mean.values()),
                )
            )
        ).integrate(0, 100)
        / 100
    )


@Appender(docstrings.std_docstring, join="\n", indents=1)
def std(self, lower=float("-inf"), upper=float("inf")):
    return np.sqrt(var(self, lower, upper))
