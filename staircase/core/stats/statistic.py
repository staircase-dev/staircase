import numpy as np
from pandas import Timestamp
from staircase.core.stats.distribution import percentile_stairs
from staircase.core.tools.datetimes import (
    check_binop_timezones,
    _convert_date_to_float,
    _convert_float_to_date,
)
from staircase.util._decorators import Appender
from staircase.core.stats import docstrings
import staircase as sc


@Appender(docstrings.integral_and_mean_example, join="\n", indents=1)
def _get_integral_and_mean(self, lower=float("-inf"), upper=float("inf")):
    """
    Calculates the integral, and the mean of the step function.
    
    
    Parameters
    ----------
    lower : int, float or pandas.Timestamp
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the interval on which to perform the calculation
          
    Returns
    -------
    tuple
        The area and mean are returned as a pair
        
    See Also
    --------
    Stairs.integrate, Stairs.mean
    """
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


@Appender(docstrings.integral_and_mean_example, join="\n", indents=1)
def get_integral_and_mean(self, lower=float("-inf"), upper=float("inf")):
    if isinstance(lower, Timestamp):
        lower = _convert_date_to_float(lower, self.tz)
    if isinstance(upper, Timestamp):
        upper = _convert_date_to_float(upper, self.tz)
    return _get_integral_and_mean(self, lower, upper)


@Appender(docstrings.integrate_example, join="\n", indents=1)
def integrate(self, lower=float("-inf"), upper=float("inf")):
    """
    Calculates the integral of the step function.
    
    Parameters
    ----------
    lower : int, float or pandas.Timestamp
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the interval on which to perform the calculation
          
    Returns
    -------
    float
        The area
        
    See Also
    --------
    Stairs.get_integral_and_mean
    """
    area, _ = get_integral_and_mean(self, lower, upper)
    return area


@Appender(docstrings.mean_example, join="\n", indents=1)
def mean(self, lower=float("-inf"), upper=float("inf")):
    """
    Calculates the mean of the step function.
    
    Parameters
    ----------
    lower : int, float or pandas.Timestamp
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the interval on which to perform the calculation
          
    Returns
    -------
    float
        The mean
    
    See Also
    --------
    Stairs.rolling_mean, Stairs.get_integral_and_mean, Stairs.median, Stairs.mode
    """
    _, mean = get_integral_and_mean(self, lower, upper)
    return mean


@Appender(docstrings.percentile_example, join="\n", indents=1)
def percentile(self, x, lower=float("-inf"), upper=float("inf")):
    """
    Calculates the x-th percentile of the step function's values
    
    Parameters
    ----------
    lower : int, float or pandas.Timestamp
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the interval on which to perform the calculation
          
    Returns
    -------
    float
        The x-th percentile
        
    See Also
    --------
    Stairs.median, Stairs.percentile_stairs
    """
    assert 0 <= x <= 100
    percentiles = percentile_stairs(self, lower, upper)
    return (percentiles(x, how="left") + percentiles(x, how="right")) / 2


@Appender(docstrings.median_example, join="\n", indents=1)
def median(self, lower=float("-inf"), upper=float("inf")):
    """
    Calculates the median of the step function.
    
    Parameters
    ----------
    lower : int, float or pandas.Timestamp
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the interval on which to perform the calculation
          
    Returns
    -------
    float
        The median
        
    See Also
    --------
    Stairs.mean, Stairs.mode, Stairs.percentile, Stairs.percentile_Stairs
    """
    return percentile(self, 50, lower, upper)


@Appender(docstrings.mode_example, join="\n", indents=1)
def mode(self, lower=float("-inf"), upper=float("inf")):
    """
    Calculates the mode of the step function.
    
    If there is more than one mode only the smallest is returned
    
    Parameters
    ----------
    lower : int, float or pandas.Timestamp, optional
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp, optional
        upper bound of the interval on which to perform the calculation
          
    Returns
    -------
    float
        The mode
        
    See Also
    --------
    Stairs.mean, Stairs.median
    """
    df = (
        self.clip(lower, upper)
        .to_dataframe()
        .iloc[1:-1]
        .assign(duration=lambda df: df.end - df.start)
    )
    return df.value.loc[df.duration.idxmax()]


@Appender(docstrings.var_example, join="\n", indents=1)
def var(self, lower=float("-inf"), upper=float("inf")):
    """
    Calculates the variance of the step function.
    
    Parameters
    ----------
    lower : int, float or pandas.Timestamp
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the interval on which to perform the calculation
          
    Returns
    -------
    float
        The variance of the step function
        
    See Also
    --------
    Stairs.std
    """
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


@Appender(docstrings.std_example, join="\n", indents=1)
def std(self, lower=float("-inf"), upper=float("inf")):
    """
    Calculates the standard deviation of the step function.
    
    Parameters
    ----------
    lower : int, float or pandas.Timestamp
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the interval on which to perform the calculation
          
    Returns
    -------
    float
        The standard deviation of the step function
        
    See Also
    --------
    Stairs.var
    """
    return np.sqrt(var(self, lower, upper))
