from staircase.core.tools.datetimes import check_binop_timezones
from staircase.core.aggregation import _min_pair, _max_pair
from staircase.util._decorators import Appender
from staircase.core.ops import docstrings
import staircase as sc


@Appender(docstrings.make_boolean_docstring, join="\n", indents=1)
def make_boolean(self):
    new_instance = self != sc.Stairs(0)
    return new_instance


@Appender(docstrings.invert_docstring, join="\n", indents=1)
def invert(self):
    new_instance = make_boolean(self)
    new_instance = sc.Stairs(1, self.use_dates, self.tz) - new_instance
    return new_instance


def _make_logical_func(pair_func, docstring):
    @Appender(docstring, join="\n", indents=1)
    def func(self, other):
        assert isinstance(other, type(self)), "Arguments must be both of type Stairs."
        check_binop_timezones(self, other)
        self_bool = self.make_boolean()
        other_bool = other.make_boolean()
        return pair_func(self_bool, other_bool)

    return func


logical_and = _make_logical_func(_min_pair, docstrings.logical_and_docstring)
logical_or = _make_logical_func(_max_pair, docstrings.logical_or_docstring)
