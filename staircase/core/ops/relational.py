import operator

import numpy as np
import pandas as pd

import staircase as sc
from staircase.core.ops import docstrings
from staircase.core.ops.common import _combine_stairs_via_values
from staircase.util import _sanitize_binary_operands
from staircase.util._decorators import Appender


def _make_relational_func(
    docstring, numpy_relational, series_relational, float_relational
):
    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        self, other = _sanitize_binary_operands(
            self, other
        )  # converts other to Stairs if not already
        if np.isnan(self.initial_value) or np.isnan(other.initial_value):
            initial_value = np.nan
        else:
            initial_value = (
                float_relational(self.initial_value, other.initial_value) * 1
            )

        if self._data is None and other._data is None:
            return sc.Stairs.new(
                initial_value=initial_value,
                data=None,
            )
        elif self._data is None or other._data is None:
            if other._data is None:  # self._data exists
                if not self._valid_values:
                    self._create_values()
                new_values = numpy_relational(self._data["value"], other.initial_value)
                new_index = self._data.index
            else:  # other._data exists
                if not other._valid_values:
                    other._create_values()
                new_values = numpy_relational(self.initial_value, other._data["value"])
                new_index = other._data.index

            new_instance = sc.Stairs.new(
                initial_value=initial_value,
                data=pd.DataFrame(
                    {"value": new_values * 1},
                    index=new_index,
                ),
            )
            new_instance._remove_redundant_step_points()
            return new_instance
        else:
            return _combine_stairs_via_values(
                self, other, series_relational, float_relational
            )

    return func


# TODO: docstring
# TODO: test
# TODO: what's new
def identical(self, other):
    self, other = _sanitize_binary_operands(self, other)
    if self.initial_value != other.initial_value:
        return False
    elif self._data is None and other._data is None:
        return True
    elif self._data is None or other._data is None:
        return False
    elif self._valid_values and other._valid_values:
        return pd.Series.eq(self._data["value"], other._data["value"]).all()
    else:
        if not self._valid_deltas:
            self._create_deltas()
        if not other._valid_deltas:
            other._create_deltas()
        return pd.Series.eq(self._data["delta"], other._data["delta"]).all()


# TODO: docstring
# TODO: test
# TODO: what's new
lt = _make_relational_func(
    docstrings.lt_docstring,
    np.less,
    pd.Series.lt,
    operator.lt,
)

# TODO: docstring
# TODO: test
# TODO: what's new
gt = _make_relational_func(
    docstrings.gt_docstring,
    np.greater,
    pd.Series.gt,
    operator.gt,
)

# TODO: docstring
# TODO: test
# TODO: what's new
le = _make_relational_func(
    docstrings.le_docstring,
    np.less_equal,
    pd.Series.le,
    operator.le,
)

# TODO: docstring
# TODO: test
# TODO: what's new
ge = _make_relational_func(
    docstrings.ge_docstring,
    np.greater_equal,
    pd.Series.ge,
    operator.ge,
)

# TODO: docstring
# TODO: test
# TODO: what's new
eq = _make_relational_func(
    docstrings.eq_docstring,
    np.equal,
    pd.Series.eq,
    operator.eq,
)

# TODO: docstring
# TODO: test
# TODO: what's new
ne = _make_relational_func(
    docstrings.ne_docstring,
    np.not_equal,
    pd.Series.ne,
    operator.ne,
)
