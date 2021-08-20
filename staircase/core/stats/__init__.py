from staircase.core.accessor import CachedAccessor
from staircase.core.stats.statistic import _max as max
from staircase.core.stats.statistic import _min as min
from staircase.core.stats.statistic import (
    agg,
    corr,
    cov,
    integral,
    mean,
    median,
    mode,
    std,
    value_sums,
    values_in_range,
    var,
)


def add_methods(cls):
    from staircase.core.stats.distribution import Dist

    cls.value_sums = value_sums
    cls.values_in_range = values_in_range
    cls.cov = cov
    cls.corr = corr
    cls.agg = agg

    cls.integral = integral
    cls.mean = mean
    cls.median = median
    cls.mode = mode
    cls.std = std
    cls.var = var

    cls.dist = CachedAccessor("dist", Dist)
