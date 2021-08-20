import operator

import numpy as np
import pandas as pd

import staircase as sc
from staircase.core.ops import docstrings
from staircase.core.ops.common import _combine_stairs_via_values
from staircase.util import _sanitize_binary_operands
from staircase.util._decorators import Appender


@Appender(docstrings.negate_docstring, join="\n", indents=1)
def negate(self):
    data = -self._data if self._data is not None else None
    return sc.Stairs._new(
        initial_value=-self.initial_value,
        data=data,
    )


def _add_or_sub_deltas_no_mask(self, other, series_op, float_op):
    # assume self and other have ._data, and at least one has valid _deltas
    # if not other._valid_deltas:
    #     other._create_deltas()
    # if not self._valid_deltas:
    #     self._create_deltas()

    deltas = series_op(self._get_deltas(), other._get_deltas(), fill_value=0)

    new_instance = sc.Stairs._new(
        initial_value=float_op(self.initial_value, other.initial_value),
        data=pd.DataFrame({"delta": deltas}),
    )
    new_instance._remove_redundant_step_points()
    return new_instance


def _make_add_or_sub_func(docstring, series_op, float_op, series_rop):
    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        self, other = _sanitize_binary_operands(self, other)
        if self._data is None and other._data is None:
            return sc.Stairs._new(
                initial_value=float_op(self.initial_value, other.initial_value),
                data=None,
            )
        elif other._data is None:  # means self._data is not None
            data = self._data.copy()
            if self._valid_values:
                data["value"] = series_op(data["value"], other.initial_value)
            return sc.Stairs._new(
                initial_value=float_op(self.initial_value, other.initial_value),
                data=data,
            )
        elif self._data is None:  # means other._data is not None
            data = other._data.copy()
            if other._valid_values:
                data["value"] = series_rop(data["value"], self.initial_value)
            if other._valid_deltas:
                data["delta"] = series_rop(data["delta"], 0)
            return sc.Stairs._new(
                initial_value=float_op(self.initial_value, other.initial_value),
                data=data,
            )
        # self._data or other._data exists
        elif self._has_na() or other._has_na():
            return _combine_stairs_via_values(self, other, series_op, float_op)
        elif self._valid_deltas or other._valid_deltas:
            return _add_or_sub_deltas_no_mask(self, other, series_op, float_op)
        elif self._valid_values and other._valid_values:
            return _combine_stairs_via_values(self, other, series_op, float_op)
        else:
            raise RuntimeError("This code should not execute")

    return func


add = _make_add_or_sub_func(
    docstrings.add_docstring,
    pd.Series.add,
    operator.add,
    pd.Series.radd,
)

subtract = _make_add_or_sub_func(
    docstrings.subtract_docstring,
    pd.Series.sub,
    operator.sub,
    pd.Series.rsub,
)


def _make_mul_div_func(docstring, series_op, float_op, series_rop, float_rop):
    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        def op_with_scalar(self, other, series_op, float_op):
            if other == 0 and series_op == pd.Series.divide:
                return sc.Stairs._new(np.nan, None)
            if self._data is None:
                data = None
            else:
                data = pd.DataFrame({"value": series_op(self._get_values(), other)})
                if series_op in (pd.Series.divide, pd.Series.rdiv):
                    data = data.replace(np.inf, np.nan)
            initial_value = float_op(self.initial_value, other)
            initial_value = initial_value if np.isfinite(initial_value) else np.nan
            return sc.Stairs._new(
                initial_value=initial_value,
                data=data,
            )

        self, other = _sanitize_binary_operands(self, other)
        if other._data is None:
            return op_with_scalar(self, other.initial_value, series_op, float_op)
        elif self._data is None:
            return op_with_scalar(other, self.initial_value, series_rop, float_rop)
        else:
            return _combine_stairs_via_values(self, other, series_op, float_op)

    return func


def float_rdiv(a, b):
    return np.divide(b, a)


multiply = _make_mul_div_func(
    docstrings.multiply_docstring,
    pd.Series.multiply,
    operator.mul,
    pd.Series.rmul,
    operator.mul,
)

divide = _make_mul_div_func(
    docstrings.divide_docstring,
    pd.Series.divide,
    np.divide,
    pd.Series.rdiv,
    float_rdiv,
)
