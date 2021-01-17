from staircase.core.stats.statistic import (
    integrate,
    mean,
    median,
    mode,
    percentile,
    std,
    var,
)

from staircase.core.stats.distribution import (
    ecdf_stairs,
    hist,
    hist_from_ecdf,
    percentile_stairs,
    percentile_Stairs,
)


def add_methods(cls):
    cls.integrate = integrate
    cls.mean = mean
    cls.median = median
    cls.mode = mode
    cls.percentile = percentile
    cls.std = std
    cls.var = var

    cls.ecdf_stairs = ecdf_stairs
    cls.hist = hist
    cls.hist_from_ecdf = hist_from_ecdf
    cls.percentile_stairs = percentile_stairs
    cls.percentile_Stairs = percentile_Stairs
