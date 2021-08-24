import numpy as np
import pandas as pd
from pandas.api.types import is_list_like

from staircase.docstrings import examples
from staircase.util import _is_datetime_like, _verify_window
from staircase.util._decorators import Appender


# capable of single or vector
@Appender(examples.sample_example, join="\n", indents=1)
def sample(self, x, include_index=False):
    """
    Evaluates the value of the step function at one, or more, points.

    The function can be called using parentheses.  See example below.

    Parameters
    ----------
    x : int, float or vector data
        Values at which to evaluate the function
    include_index : bool, default False
        Indicates if the values returned should be a :class:`numpy.ndarray`, or in a :class:`pandas.Series`
        indexed by the values in *x*

    Returns
    -------
    float, :class:`numpy.ndarray`, :class:`pandas.Series`

    See Also
    --------
    Stairs.limit
    staircase.sample
    """
    side = "right" if self._closed == "left" else "left"
    values = limit(self, x, side)
    if include_index:
        if not is_list_like(x):
            x = [x]
        values = pd.Series(values, index=x)
    return values


@Appender(examples.limit_example, join="\n", indents=1)
def limit(self, x, side, include_index=False):
    """
    Evaluates the limit of the step function as it approaches one, or more, points.

    The results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
    or :math:`\\lim_{x \\to z^{+}} f(x)`, when side = 'left' or side = 'right' respectively. See
    :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.

    Parameters
    ----------
    x : int, float or vector data
        Values at which to evaluate the function
    side : {'left', 'right'}, default 'right'
        If points where step changes occur do not coincide with x then this parameter
        has no effect.  Where a step change occurs at a point given by x, this parameter
        determines if the step function is evaluated at the interval to the left, or the right.
    include_index : bool, default False
        Indicates if the values returned should be a :class:`numpy.ndarray`, or in a :class:`pandas.Series`
        indexed by the values in *x*

    Returns
    -------
    float, :class:`numpy.ndarray`, :class:`pandas.Series`

    See Also
    --------
    Stairs.sample
    staircase.sample
    """
    assert side in ("left", "right")
    passed_x = x
    if self._data is None:
        if pd.api.types.is_list_like(x):
            return self.initial_value * np.ones_like(x)
        else:
            return self.initial_value
    amended_values = np.append(
        self._get_values().values, [self.initial_value]
    )  # hack for -1 index value
    if pd.api.types.is_list_like(x) and _is_datetime_like(next(iter(x))):
        x = pd.Series(x).values  # faster, but also bug free in numpy
    elif _is_datetime_like(x):
        x = pd.Series([x]).values[0]
    values = amended_values[np.searchsorted(self._data.index.values, x, side=side) - 1]
    if include_index:
        values = pd.Series(values, index=passed_x)
    return values


def add_methods(cls):
    cls.sample = sample
    cls.limit = limit
