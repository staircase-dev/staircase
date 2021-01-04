import numpy as np
from staircase.core.tools.datetimes import check_binop_timezones
from staircase.util._decorators import Appender
from staircase.core.ops import docstrings
import staircase as sc

def _compare(cumulative, zero_comparator, use_dates=False, tz=None):
    truth = cumulative.copy()
    for key,value in truth.items():
        new_val = int(zero_comparator(float(value)))
        truth[key] = new_val
    deltas = [truth.values()[0]]
    deltas.extend(np.subtract(truth.values()[1:], truth.values()[:-1]))
    new_instance = sc.Stairs(dict(zip(truth.keys(), deltas)), use_dates, tz)
    new_instance._reduce()
    return new_instance

@Appender(docstrings.lt_example, join='\n', indents=1)
def lt(self, other):
    """
    Returns a boolean-valued step function indicating where *self* is strictly less than *other*.
    
    Equivalent to *self* < *other*.  See examples below.
          
    Returns
    -------
    :class:`Stairs`
        A new instance representing where *self* < *other*
        
    See Also
    --------
    Stairs.gt, Stairs.le, Stairs.ge
    """
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__lt__
    return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)    

@Appender(docstrings.gt_example, join='\n', indents=1)
def gt(self, other):
    """
    Returns a boolean-valued step function indicating where *self* is strictly greater than *other*.
    
    Equivalent to *self* > *other*.  See examples below.
          
    Returns
    -------
    :class:`Stairs`
        A new instance representing where *self* > *other*
        
    See Also
    --------
    Stairs.lt, Stairs.le, Stairs.ge
    """
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__gt__
    return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)

@Appender(docstrings.le_example, join='\n', indents=1)
def le(self, other):
    """
    Returns a boolean-valued step function indicating where *self* is less than, or equal to, *other*.
    
    Equivalent to *self* <= *other*.  See examples below.
          
    Returns
    -------
    :class:`Stairs`
        A new instance representing where *self* <= *other*
        
    See Also
    --------
    Stairs.lt, Stairs.gt, Stairs.ge
    """
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__le__
    return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)

@Appender(docstrings.ge_example, join='\n', indents=1)
def ge(self, other):
    """
    Returns a boolean-valued step function indicating where *self* is greater than, or equal to, *other*.
    
    Equivalent to *self* >= *other*.  See examples below.
          
    Returns
    -------
    :class:`Stairs`
        A new instance representing where *self* >= *other*
        
    See Also
    --------
    Stairs.lt, Stairs.gt, Stairs.le
    """
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__ge__
    return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)

@Appender(docstrings.eq_example, join='\n', indents=1)
def eq(self, other):
    """
    Returns a boolean-valued step function indicating where *self* is equal to *other*.
    
    Equivalent to *self* == *other*.  See examples below.
          
    Returns
    -------
    :class:`Stairs`
        A new instance representing where *self* == *other*
        
    See Also
    --------
    Stairs.ne, Stairs.identical
    """
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__eq__
    return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)

@Appender(docstrings.ne_example, join='\n', indents=1)
def ne(self, other):
    """
    Returns a boolean-valued step function indicating where *self* is not equal to *other*.
    
    Equivalent to *self* != *other*.  See examples below.
          
    Returns
    -------
    :class:`Stairs`
        A new instance representing where *self* != *other*
        
    See Also
    --------
    Stairs.eq, Stairs.identical
    """
    if not isinstance(other, sc.Stairs):
        other = sc.Stairs(other, self.use_dates, self.tz)
    else:
        check_binop_timezones(self, other)
    comparator = float(0).__ne__
    return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)
    
@Appender(docstrings.identical_example, join='\n', indents=1)
def identical(self, other):
    """
    Returns True if *self* and *other* represent the same step functions.
    
    Returns
    -------
    boolean
    
    See Also
    --------
    Stairs.eq, Stairs.ne
    """
    check_binop_timezones(self, other)
    return bool(self == other)