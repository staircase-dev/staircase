def add_methods(cls):
    from staircase.core.stats.distribution import (  # hist_from_ecdf,
        dist,
        ecdf,
        fractile,
        get_ecdf,
        get_fractiles,
        get_percentiles,
        hist,
        percentile,
    )
    from staircase.core.stats.statistic import (
        _max,
        _min,
        corr,
        cov,
        get_integral_and_mean,
        integrate,
        mean,
        median,
        mode,
        std,
        values_in_range,
        var,
    )

    cls.get_integral_and_mean = get_integral_and_mean
    cls.integrate = integrate
    cls.mean = mean
    cls.median = median
    cls.mode = mode
    cls.std = std
    cls.var = var
    cls.values_in_range = values_in_range
    cls.max = _max
    cls.min = _min
    cls.cov = cov
    cls.corr = corr

    cls.dist = dist
    cls.ecdf = ecdf
    cls.fractile = fractile
    cls.get_ecdf = get_ecdf
    cls.get_fractiles = get_fractiles
    cls.get_percentiles = get_percentiles
    cls.hist = hist
    cls.percentile = percentile
