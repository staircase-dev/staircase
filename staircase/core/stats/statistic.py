import numpy as np
from pandas import Timestamp
from staircase.core.stats.distribution import percentile_stairs
from staircase.core.tools.datetimes import _convert_date_to_float
from staircase.util._decorators import Appender
from staircase.core.stats import docstrings
import staircase as sc


@Appender(docstrings.integral_and_mean_docstring, join="\n", indents=1)
def _get_integral_and_mean(self, lower=float("-inf"), upper=float("inf")):
    new_instance = self.clip(lower, upper)
    if new_instance.number_of_steps() < 2:
        return 0, np.nan
    if lower != float("-inf"):
        new_instance[lower] = new_instance._get(lower, 0)
    if upper != float("inf"):
        new_instance[upper] = new_instance._get(upper, 0)
    cumulative = new_instance._cumulative()
    widths = np.subtract(cumulative.keys()[2:], cumulative.keys()[1:-1])
    heights = cumulative.values()[1:-1]
    area = np.multiply(widths, heights).sum()
    mean = area / (cumulative.keys()[-1] - cumulative.keys()[1])
    return area, mean


@Appender(docstrings.integral_and_mean_docstring, join="\n", indents=1)
def get_integral_and_mean(self, lower=float("-inf"), upper=float("inf")):
    if isinstance(lower, Timestamp):
        lower = _convert_date_to_float(lower, self.tz)
    if isinstance(upper, Timestamp):
        upper = _convert_date_to_float(upper, self.tz)
    return _get_integral_and_mean(self, lower, upper)


@Appender(docstrings.integrate_docstring, join="\n", indents=1)
def integrate(self, lower=float("-inf"), upper=float("inf")):
    area, _ = get_integral_and_mean(self, lower, upper)
    return area


@Appender(docstrings.mean_docstring, join="\n", indents=1)
def mean(self, lower=float("-inf"), upper=float("inf")):
    _, mean = get_integral_and_mean(self, lower, upper)
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
    df = (
        self.clip(lower, upper)
        .to_dataframe()
        .iloc[1:-1]
        .assign(duration=lambda df: df.end - df.start)
    )
    return df.value.loc[df.duration.idxmax()]


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
