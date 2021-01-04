from staircase.core.tools.datetimes import check_binop_timezones
from staircase.core.aggregation import _min_pair, _max_pair
from staircase.util._decorators import Appender
from staircase.core.ops import docstrings
import staircase as sc


@Appender(docstrings.make_boolean_example, join='\n', indents=1)
def make_boolean(self):
    """
    Returns a boolean-valued step function indicating where *self* is non-zero.
    
    Returns
    -------
    :class:`Stairs`
        A new instance representing where *self* is non-zero
    
    See Also
    --------
    Stairs.invert
    """
    new_instance = self != sc.Stairs(0)
    return new_instance

@Appender(docstrings.invert_example, join='\n', indents=1)
def invert(self):
    """
    Returns a boolean-valued step function indicating where *self* is zero-valued.
    
    Equivalent to ~*self*
    
    Returns
    -------
    :class:`Stairs`
        A new instance representing where *self* is zero-valued
    
    See Also
    --------
    Stairs.make_boolean
    """
    new_instance = make_boolean(self)
    new_instance = sc.Stairs(1, self.use_dates, self.tz) - new_instance
    return new_instance

@Appender(docstrings.logical_and_example, join='\n', indents=1)
def logical_and(self, other):
    """
    Returns a boolean-valued step function indicating where *self* and *other* are non-zero.
    
    Equivalent to *self* & *other*.  See examples below.
          
    Returns
    -------
    :class:`Stairs`
        A new instance representing where *self* & *other*
        
    See Also
    --------
    Stairs.logical_or
    """
    assert isinstance(other, type(self)), "Arguments must be both of type Stairs."
    check_binop_timezones(self, other)
    self_bool = self.make_boolean()
    other_bool = other.make_boolean()
    return _min_pair(self_bool, other_bool)

@Appender(docstrings.logical_or_example, join='\n', indents=1)
def logical_or(self, other):
    """
    Returns a boolean-valued step function indicating where *self* or *other* are non-zero.
    
    Equivalent to *self* | *other*.  See examples below.
          
    Returns
    -------
    :class:`Stairs`
        A new instance representing where *self* | *other*
    
    See Also
    --------
    Stairs.logical_and
    """
    assert isinstance(other, type(self)), "Arguments must be both of type Stairs."
    check_binop_timezones(self, other)
    self_bool = self.make_boolean()
    other_bool = other.make_boolean()
    return _max_pair(self_bool, other_bool)
