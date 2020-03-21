"""Staircase
==============
:doc:`Staircase<index>` is a MIT licensed library, written in pure-Python, for
modelling step functions. See :doc:`Getting Started<getting_started>` for more information.
"""

#uses https://pypi.org/project/sortedcontainers/
from sortedcontainers import SortedDict, SortedSet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from .docstrings.decorator import add_doc, append_doc
from .docstrings import stairs_class as SC_docs
from .docstrings import stairs_module as SM_docs
warnings.simplefilter('default')

origin = pd.to_datetime('2000-1-1')

def _convert_date_to_float(val):
    if hasattr(val, "__iter__"):
        if not isinstance(val, pd.Series):
            val = pd.Series(val)
        deltas = pd.TimedeltaIndex(val - origin)
        return deltas.days*24 + deltas.seconds/3600
    return (val - origin).total_seconds()/3600
    
def _convert_float_to_date(val):
    if hasattr(val, "__iter__"):
        if not isinstance(val, pd.Series):
            val = pd.Series(val)
        return list(pd.to_datetime(val/24, unit='D', origin=origin))
    return pd.to_datetime(val/24, unit='D', origin=origin)

def _from_cumulative(cumulative, use_dates=False):
    return Stairs(dict(zip(cumulative.keys(),np.insert(np.diff(list(cumulative.values())), 0, [next(iter(cumulative.values()))]))), use_dates)

def _min_pair(stairs1, stairs2):
    """Calculates the minimum of two Stairs objects.  It can be thought of as calculating the minimum of two step functions.

    Parameters:
        stairs1 (Stairs)
        stairs2 (Stairs)

    Returns:
        Stairs: the result of the calculation

    """
    assert isinstance(stairs1, Stairs) and isinstance(stairs2, Stairs), f"Arguments to min must be both of type Stairs."
    new_instance = stairs1-stairs2
    cumulative = new_instance._cumulative()
    for key,value in cumulative.items():
        if value > 0:
            cumulative[key] = 0
    deltas = [cumulative.values()[0]]
    deltas.extend(np.subtract(cumulative.values()[1:], cumulative.values()[:-1])) 
    new_instance = Stairs(dict(zip(new_instance._keys(), deltas)), use_dates=stairs1.use_dates or stairs2.use_dates)
    return new_instance + stairs2
    
def _max_pair(stairs1, stairs2):
    """Calculates the maximum of two Stairs objects.  It can be thought of as calculating the maximum of two step functions.

    Parameters:
        stairs1 (Stairs)
        stairs2 (Stairs)

    Returns:
        Stairs: the result of the calculation

    """
    assert isinstance(stairs1, Stairs) and isinstance(stairs2, Stairs), f"Arguments to max must be both of type Stairs."
    new_instance = stairs1-stairs2
    cumulative = new_instance._cumulative()
    for key,value in cumulative.items():
        if value < 0:
            cumulative[key] = 0
    deltas = [cumulative.values()[0]]
    deltas.extend(np.subtract(cumulative.values()[1:], cumulative.values()[:-1]))   
    new_instance = Stairs(dict(zip(new_instance._keys(), deltas)), use_dates=stairs1.use_dates or stairs2.use_dates)
    return new_instance + stairs2

def _compare(cumulative, zero_comparator, use_dates=False):
    truth = cumulative.copy()
    for key,value in truth.items():
        new_val = int(zero_comparator(float(value)))
        truth[key] = new_val
    deltas = [truth.values()[0]]
    deltas.extend(np.subtract(truth.values()[1:], truth.values()[:-1]))
    new_instance = Stairs(dict(zip(truth.keys(), deltas)), use_dates=use_dates)
    new_instance._reduce()
    return new_instance

def _get_union_of_points(collection):
    
    def dict_common_points():
        return collection.values()
        
    def series_common_points():
        return collection.values
        
    def array_common_points():
        return collection
    
    for func in (dict_common_points, series_common_points, array_common_points):
        try:
            stairs_instances = func()
            points = []
            for stair_instance in stairs_instances:
                points += list(stair_instance._keys())
            return SortedSet(points)
        except:
            pass
    raise TypeError('Collection should be a tuple, list, numpy array, dict or pandas.Series.')
    
    
    

def _using_dates(collection):

    def dict_use_dates():
        return next(iter(collection.values())).use_dates
        
    def series_use_dates():
        return collection.values[0].use_dates
        
    def array_use_dates():
        return collection[0].use_dates
    
    for func in (dict_use_dates, series_use_dates, array_use_dates):
        try:
            return func()
        except:
            pass
    raise TypeError('Could not determine if Stairs collection is using dates.  Collection should be a tuple, list, numpy array, dict or pandas.Series.')
        
    
@append_doc(SM_docs.sample_example)    
def sample(collection, points=None, how='right', expand_key=True):
    """
    Takes a dict-like collection of Stairs instances and evaluates their values across a common set of points.
    
    Parameters
    ----------
    collection : dictionary or pandas.Series
        The Stairs instances at which to evaluate
    points : int, float or vector data
        The points at which to sample the Stairs instances
    how : {'left', 'right'}, default 'right'
        if points where step changes occur do not coincide with x then this parameter
        has no effect.  Where a step changes occurs at a point given by x, this parameter
        determines if the step function is evaluated at the interval to the left, or the right.
    expand_key: boolean, default True
        used when collection is a multi-index pandas.Series.  Indicates if index should be expanded from
        tuple to columns in a dataframe.
        
    Returns
    -------
    :class:`pandas.DataFrame`
        A dataframe, in tidy format, with three columns: points, key, value.  The column key contains
        the identifiers used in the dict-like object specified by 'collection'.
        
    See Also
    --------
    Stairs.sample
    """
    use_dates = _using_dates(collection)
    #assert len(set([type(x) for x in collection.values()])) == 1, "collection must contain values of same type"
    if points is None:
        points = _get_union_of_points(collection)
        if use_dates:
            points.discard(float('-inf'))
            points = _convert_float_to_date(points)
    else:
        if not hasattr(points, "__iter__"):
            points = [points]
    result = (pd.DataFrame({"points":points, **{key:stairs.sample(points, how=how) for key,stairs in collection.items()}})
        .melt(id_vars="points", var_name="key")
    )
    if isinstance(collection, pd.Series) and expand_key and len(collection.index.names) > 1:
        try:
            result = (result
                .join(pd.DataFrame(result.key.tolist(), columns=collection.index.names))
                .drop(columns='key')
            )     
        except:
            pass
    return result

@append_doc(SM_docs.aggregate_example)
def aggregate(collection, func, points=None):
    """
    Takes a collection of Stairs instances and returns a single instance representing the aggregation.
    
    Parameters
    ----------
    collection : tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate
    func: a function taking a 1 dimensional vector of floats, and returning a single float
        The function to apply, eg numpy.max
    points: vector of floats or dates
        Points at which to evaluate.  Defaults to union of all step changes.  Equivalent to applying Stairs.resample().
        
    Returns
    ----------
    :class:`Stairs`
    
    Notes
    -----
    The points at which to aggregate will include -infinity whether explicitly included or not.
    
    See Also
    --------
    staircase.mean, staircase.median, staircase.min, staircase.max
    """
    if isinstance(collection, dict) or isinstance(collection, pd.Series):
        Stairs_dict = collection
    else:
        Stairs_dict = dict(enumerate(collection))
    use_dates = _using_dates(collection)
    df = sample(Stairs_dict, points, expand_key=False)
    aggregation = df.pivot_table(index="points", columns="key", values="value").aggregate(func, axis=1)
    if use_dates:
        aggregation.index = _convert_date_to_float(aggregation.index)
    aggregation[float('-inf')] = func([val._sample(float('-inf')) for key,val in Stairs_dict.items()])
    step_changes = aggregation.sort_index().diff().fillna(0)
    #groupby.sum is necessary on next line as step_changes series may not have unique index elements
    return Stairs(dict(step_changes.groupby(level=0).sum()), use_dates=use_dates)._reduce()
    
@append_doc(SM_docs.mean_example)      
def _mean(collection):
    """
    Takes a collection of Stairs instances and returns the mean of the corresponding step functions.
    
    Parameters
    ----------
    collection : tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate using a mean function
    
    Returns
    -------
    :class:`Stairs`
    
    See Also
    --------
    staircase.aggregate, staircase.median, staircase.min, staircase.max
    """
    return aggregate(collection, np.mean)

@append_doc(SM_docs.median_example)  
def _median(collection):
    """
    Takes a collection of Stairs instances and returns the median of the corresponding step functions.
    
    Parameters
    ----------
    collection : tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate using a median function
    
    Returns
    -------
    :class:`Stairs`
    
    See Also
    --------
    staircase.aggregate, staircase.mean, staircase.min, staircase.max
    """
    return aggregate(collection,np.mean)

@append_doc(SM_docs.min_example)          
def _min(collection):
    """
    Takes a collection of Stairs instances and returns the minimum of the corresponding step functions.
    
    Parameters
    ----------
    collection : tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate using a min function
    
    Returns
    -------
    :class:`Stairs`
    
    See Also
    --------
    staircase.aggregate, staircase.mean, staircase.median, staircase.max
    """
    return aggregate(collection, np.min)

@append_doc(SM_docs.max_example)  
def _max(collection):
    """
    Takes a collection of Stairs instances and returns the maximum of the corresponding step functions.
    
    Parameters
    ----------
    collection : tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate using a max function
    
    Returns
    -------
    :class:`Stairs`
    
    See Also
    --------
    staircase.aggregate, staircase.mean, staircase.median, staircase.min
    """
    return aggregate(collection, np.max)


def resample(container, x, how='right'):
    """
    Applies the Stairs.resample function to a 1D container, eg tuple, list, numpy array, pandas series, dictionary
    
    Returns
    -------
    type(container)
    
    See Also
    --------
    Stairs.resample
    """
    if isinstance(container, dict):
        return {key:s.resample(x, how) for key,s in container}
    if isinstance(container, pd.Series):
        return pd.Series([s.resample(x, how) for s in container.values], index=container.index)
    if isinstance(container, np.ndarray):
        return np.array([s.resample(x, how) for s in container])
    return type(container)([s.resample(x, how) for s in container])
    
    
class Stairs():
    """An instance of a Stairs class is used to represent a :ref:`step function <getting_started.step_function>`.
    
    The Stairs class encapsulates a `SortedDict <http://www.grantjenks.com/docs/sortedcontainers/sorteddict.html>`_
    which is used to hold the points at which the step function changes, and by how much.
    
    See the :ref:`Stairs API <api.Stairs>` for details of methods.
    """
    
    def __init__(self, value=0, use_dates=False):
        """
        Initialise a Stairs instance. 
        
        Parameters
        ----------
        value : float, default 0
            The value of the step function at negative infinity.
        use_dates: bool, default False
            Allows the step function to be defined with `Pandas.Timestamp <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html>`_.
        
        Returns
        -------
        :class:`Stairs`
        """
        self._sorted_dict = SortedDict()
        if isinstance(value, dict):
            self._sorted_dict = SortedDict(value)
        else:
            self._sorted_dict = SortedDict()
            self._sorted_dict[float('-inf')] = value
        self.use_dates = use_dates
        self.cached_cumulative = None
        
        #bypass date mapping
        if not use_dates:
            self.sample = self._sample
            self.resample = self._resample
            self.layer = self._layer
            self.get_integral_and_mean = self._get_integral_and_mean
            self.clip = self._clip
            self.values_in_range = self._values_in_range
            self.step_changes = self._step_changes
            
        
        self._get = self._sorted_dict.get
        self._items = self._sorted_dict.items
        self._keys = self._sorted_dict.keys
        self._values = self._sorted_dict.values
        self._pop = self._sorted_dict.pop
        self._len = self._sorted_dict.__len__
    
    # DO NOT IMPLEMENT __len__ or __iter__, IT WILL CAUSE ISSUES WITH PANDAS SERIES PRETTY PRINTING 
       
    def __getitem__(self,*args, **kwargs):
        return self._sorted_dict.__getitem__(*args, **kwargs)
        
    def __setitem__(self, key, value):
        self._sorted_dict.__setitem__(key, value)
        
    def _popitem(self, index=-1):
        #SortedDict.popitem cannot be used, as definitions of __bool__ are different between SortedDict and Stairs
        key = self._sorted_dict._list_pop(index)
        value = self._sorted_dict._dict_pop(key)
        return (key, value)
    
    def copy(self):
        """
        Returns a deep copy of this Stairs instance

        Returns
        -------
        copy : Stairs
        """
        new_instance = Stairs(use_dates=self.use_dates)
        for key,value in self._items():
            new_instance[key] = value
        return new_instance

    def plot(self, ax=None, **kwargs):
        """
        Makes a step plot representing the finite intervals belonging to the Stairs instance. 
        
        Uses matplotlib as a backend.

        Parameters
        ----------
        ax : :class:`matplotlib.axes.Axes`, default None
            Allows the axes, on which to plot, to be specified
        **kwargs
            Options to pass to :function: `matplotlib.pyplot.step`
        
        Returns
        -------
        :class:`matplotlib.axes.Axes`
        """
        if ax is None:
            fig, ax = plt.subplots()
                
        cumulative = self._cumulative()
        step_points = cumulative.keys()
        if self.use_dates:
            register_matplotlib_converters()
            x = list(cumulative.keys())
            x[0] = x[1]-0.00001
            ax.step(_convert_float_to_date(x), list(cumulative.values()), where='post', **kwargs)
        else:
            ax.step(cumulative.keys(), cumulative.values(), where='post', **kwargs)
        return ax

    @append_doc(SC_docs.sample_example)
    def _sample(self, x, how='right'):
        """Evaluates the value of the step function at one, or more, points.

        The function should be called using parentheses.  See example below.

        Parameters
        ----------
        x : int, float or vector data
            values at which to evaluate the function
        how : {'left', 'right'}, default 'right'
            if points where step changes occur do not coincide with x then this parameter
            has no effect.  Where a step changes occurs at a point given by x, this parameter
            determines if the step function is evaluated at the interval to the left, or the right.
            
        Returns
        -------
        float, or list of floats
        
        See Also
        --------
        staircase.sample
        """
        assert how in ("right", "left")
        if hasattr(x, "__iter__"):
            new_instance = self.copy()._layer_multiple(x, None, [0]*len(x))
            cumulative = new_instance._cumulative()
            if how == "right":
                return [cumulative[_x] for _x in x]
            else:
                shifted_cumulative = SortedDict(zip(cumulative.keys()[1:], cumulative.values()[:-1]))
                if float('-inf') in x:
                    vals = [self[float('-inf')]]
                else:
                    vals = []
                vals.extend([val for key,val in shifted_cumulative.items() if key in x])
                return vals
        else:
            cumulative = self._cumulative()
            if how == "right":
                preceding_boundary_index = cumulative.bisect_right(x) - 1
            else:
                preceding_boundary_index = cumulative.bisect_left(x) - 1
            return cumulative.values()[preceding_boundary_index]    

            
    @add_doc(_sample.__doc__)
    def sample(self, x, how='right'):
        x = _convert_date_to_float(x)      
        return self._sample(x,how)
        
    def evaluate(self, x, how='right'):
        """Deprecated.  Use Stairs.sample"""
        warnings.warn(
            "Stairs.evaluate will be deprecated in version 1.0.0, use Stairs.sample instead",
             PendingDeprecationWarning
        )
        return self.sample(x, how)
    
    @append_doc(SC_docs.resample_example)
    def _resample(self, x, how='right'):
        """Evaluates the value of the step function at one, or more, points and
        creates a new Stairs instance whose step changes occur at a subset of these
        points.  The new instance and self have the same values when evaluated at x.

        Parameters
        ----------
        x : int, float or vector data
            values at which to evaluate the function
        how : {'left', 'right'}, default 'right'
            if points where step changes occur do not coincide with x then this parameter
            has no effect.  Where a step changes occurs at a point given by x, this parameter
            determines if the step function is evaluated at the interval to the left, or the right.
            
        Returns
        -------
        :class:`Stairs`
      
        See Also
        --------
        staircase.resample
        """
        if not hasattr(x, "__iter__"):
            x = [x,]
        new_cumulative = SortedDict({float('-inf'):self._sample(float('-inf'))})
        new_cumulative.update({point:self._sample(point, how) for point in x})
        return _from_cumulative(new_cumulative, self.use_dates)    

    @add_doc(_resample.__doc__)
    def resample(self, x, how='right'):
        x = _convert_date_to_float(x)
        return self._resample(x, how)

    
    @append_doc(SC_docs.layer_example)        
    def _layer(self, start, end=None, value=None):
        """
        Changes the value of the step function.
        
        
        Parameters
        ----------
        start : int, float or vector data
            start time(s) of the interval(s)
        end : int, float or vector data, optional
            end time(s) of the interval(s)
        value: int, float or vector data, optional
            value(s) of the interval(s)
              
        Returns
        -------
        :class:`Stairs`
            The current instance is returned to facilitate method chaining
        
        """
        if hasattr(start, "__iter__"):
            layer_func = self._layer_multiple
        else:
            layer_func = self._layer_single
        return layer_func(start, end, value)

    @add_doc(_layer.__doc__)        
    def layer(self, start, end=None, value=None):
        start = _convert_date_to_float(start)
        if end is not None:
            end = _convert_date_to_float(end)
        return self._layer(start, end, value)

        
    def _layer_single(self, start, end=None, value=None):
        """
        Implementation of the layer function for when start parameter is single-valued
        """
        if value is None:
            value = 1
        self[start] = self._get(start,0) + value
        if self[start] == 0:
            self._pop(start)
        
        if end != None:
            self[end] = self._get(end,0) - value
            if self[end] == 0 or end == float('inf'):
                self._pop(end)
                
        self.cached_cumulative = None
        return self
                
    
    def _layer_multiple(self, starts, ends=None, values = None):
        """
        Implementation of the layer function for when start parameter is vector data
        """        
        
        if ends is None:
            ends = [np.nan]*len(starts)
            
        assert len(starts) == len(ends)
        
        if values is not None:
            assert len(starts) == len(values)
        else:
            values = [1]*len(starts)
        for start, end, value in zip(starts, ends, values):
            if not np.isnan(start):
                self[start] = self._get(start,0) + value
            if not np.isnan(end):
                self[end] = self._get(end,0) - value
        self.cached_cumulative = None
        return self

    @append_doc(SC_docs.step_changes_example)
    def _step_changes(self):
        """
        Returns a dictionary of key, value pairs of indicating where step changes occur in the step function, and the change in value 
        
        Returns
        -------
        dictionary
        
        See Also
        --------
        Stairs.number_of_steps
        """
        return dict(self._items()[1:])
    
    @add_doc(_step_changes.__doc__)
    def step_changes(self):
        return dict(zip(_convert_float_to_date(self._keys()[1:]), self._values()[1:]))

    @append_doc(SC_docs.negate_example)        
    def negate(self):
        """
        An operator which produces a new Stairs instance representing the multiplication of the step function by -1.
        
        Should be used as an operator, i.e. by utilising the symbol -.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the multiplication of the step function by -1
            
        See Also
        --------
        Stairs.subtract
        """    
        
        new_instance = self.copy()
        for key,delta in new_instance._items():
            new_instance[key] = -delta
        new_instance.cached_cumulative = None
        return new_instance
    
    @append_doc(SC_docs.add_example)
    def add(self, other):
        """
        An operator facilitating the addition of two step functions.
        
        Should be used as an operator, i.e. by utilising the symbol +.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the addition of two step functions
            
        See Also
        --------
        Stairs.subtract
        """
        if not isinstance(other, Stairs):
            other = Stairs(other)
        new_instance = self.copy()
        for key, value in other._items():
            new_instance[key] = self._get(key,0) + value
        new_instance._reduce()
        new_instance.use_dates = self.use_dates or other.use_dates
        new_instance.cached_cumulative = None
        return new_instance
    
    @append_doc(SC_docs.subtract_example)    
    def subtract(self, other):
        """
        An operator facilitating the subtraction of one step function from another.
        
        Should be used as an operator, i.e. by utilising the symbol -.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the subtraction of one step function from another
        
        See Also
        --------
        Stairs.add
        """
        if not isinstance(other, Stairs):
            other = Stairs(other)
        other = -other
        return self + other
    
    def _mul_or_div(self, other, func):
        a = self.copy()
        b = other.copy()
        a_keys = a._keys()
        b_keys = b._keys()
        a._layer_multiple(b_keys, None, [0]*len(b_keys))
        b._layer_multiple(a_keys, None, [0]*len(a_keys))
        
        multiplied_cumulative_values = func(a._cumulative().values(), b._cumulative().values())
        new_instance = _from_cumulative(dict(zip(a._keys(), multiplied_cumulative_values)), use_dates=self.use_dates)
        new_instance._reduce()   
        return new_instance
        
    @append_doc(SC_docs.divide_example)
    def divide(self, other):
        """
        An operator facilitating the division of one step function by another.
        
        The divisor should cannot be zero-valued anywhere.
        
        Should be used as an operator, i.e. by utilising the symbol /.  See examples below.      
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the division of one step function by another
            
        See Also
        --------
        Stairs.multiply
        """
        if not bool(other.make_boolean()):
            raise ZeroDivisionError("Divisor Stairs instance must not be zero-valued at any point")
        
        return self._mul_or_div(other, np.divide)
    
    @append_doc(SC_docs.multiply_example)
    def multiply(self, other):
        r"""
        An operator facilitating the multiplication of one step function with another.
        
        Should be used as an operator, i.e. by utilising the symbol \*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the multiplication of one step function from another
        
        See Also
        --------
        Stairs.divide
        """
        return self._mul_or_div(other, np.multiply)
        
    def _cumulative(self):
        if self.cached_cumulative == None:
            self.cached_cumulative = SortedDict(zip(self._keys(), np.cumsum(self._values())))
        return self.cached_cumulative
    
    @append_doc(SC_docs.make_boolean_example)
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
        new_instance = self != Stairs(0)
        return new_instance
    
    @append_doc(SC_docs.invert_example)
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
        new_instance = self.make_boolean()
        new_instance = Stairs(1) - new_instance
        return new_instance
    
    @append_doc(SC_docs.logical_and_example)
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
        assert isinstance(other, type(self)), f"Arguments must be both of type Stairs."
        self_bool = self.make_boolean()
        other_bool = other.make_boolean()
        return _min_pair(self_bool, other_bool)
    
    @append_doc(SC_docs.logical_or_example)
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
        assert isinstance(other, type(self)), f"Arguments must be both of type Stairs."
        self_bool = self.make_boolean()
        other_bool = other.make_boolean()
        return _max_pair(self_bool, other_bool)

    @append_doc(SC_docs.lt_example)
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
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__lt__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)    
    
    @append_doc(SC_docs.gt_example)
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
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__gt__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)        
    
    @append_doc(SC_docs.le_example)    
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
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__le__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)        

    @append_doc(SC_docs.ge_example)
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
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__ge__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)                
    
    @append_doc(SC_docs.eq_example)
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
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__eq__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)           
    
    @append_doc(SC_docs.ne_example)
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
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__ne__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)    
    
    @append_doc(SC_docs.identical_example)    
    def identical(self, other):
        """
        Returns True if *self* and *other* represent the same step functions
        
        Returns
        -------
        boolean
        
        See Also
        --------
        Stairs.eq, Stairs.ne
        """
        return bool(self == other)
    
    def _reduce(self):
        to_remove = [key for key,val in self._items()[1:] if val == 0]
        for key in to_remove:
            self._pop(key)
        return self
        
    def __bool__(self):
        if self.number_of_steps() >= 2:
            return float((~self).integrate()) < 0.0000001
        return dict(self._sorted_dict) == {float('-inf'): 1}

    
    # def __bool__(self):
        # self._reduce()
        # if self._len() != 1:
            # return False
        # value = self._values()[0]
        # return value == 1
    
    @append_doc(SC_docs.integral_and_mean_example)
    def _get_integral_and_mean(self, lower=float('-inf'), upper=float('inf')):
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
        if lower != float('-inf'):
            new_instance[lower] = new_instance._get(lower,0)
        if upper != float('inf'):
            new_instance[upper] = new_instance._get(upper,0)
        cumulative = new_instance._cumulative()
        widths = np.subtract(cumulative.keys()[2:], cumulative.keys()[1:-1])
        heights = cumulative.values()[1:-1]
        area = np.multiply(widths, heights).sum()
        mean = area/(cumulative.keys()[-1] - cumulative.keys()[1])
        return area, mean

    @add_doc(_get_integral_and_mean.__doc__)
    def get_integral_and_mean(self, lower=float('-inf'), upper=float('inf')):
        if isinstance(lower, pd.Timestamp):
            lower = _convert_date_to_float(lower)
        if isinstance(upper, pd.Timestamp):
            upper = _convert_date_to_float(upper)
        return self._get_integral_and_mean(lower, upper)
                
    @append_doc(SC_docs.integrate_example)    
    def integrate(self, lower=float('-inf'), upper=float('inf')):
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
        area, mean = self.get_integral_and_mean(lower, upper)
        return area
    
    @append_doc(SC_docs.mean_example) 
    def mean(self, lower=float('-inf'), upper=float('inf')):
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
        Stairs.get_integral_and_mean, Stairs.median, Stairs.mode
        """
        area, mean = self.get_integral_and_mean(lower, upper)
        return mean
    
    @append_doc(SC_docs.median_example) 
    def median(self, lower=float('-inf'), upper=float('inf')):
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
        return self.percentile(50, lower, upper)
    
    @append_doc(SC_docs.percentile_example) 
    def percentile(self, x, lower=float('-inf'), upper=float('inf')):
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
        Stairs.median, Stairs.percentile_Stairs
        """
        assert 0 <= x <= 100
        percentiles = self.percentile_Stairs(lower, upper)
        return (percentiles(x, how='left') + percentiles(x, how='right'))/2

    @append_doc(SC_docs.percentile_stairs_example)
    def percentile_Stairs(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates a percentile function (and returns a corresponding Stairs instance)
        
        This method can be used for efficiency gains if subtituting for multiple calls
        to percentile() with the same lower and upper parameters
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        :class:`Stairs`
            An instance representing a percentile function
            
        See Also
        --------
        Stairs.percentile
        """
        temp_df = (self.clip(lower,upper)
             .to_dataframe()
             .iloc[1:-1]
             .assign(duration = lambda df: df.end-df.start)
             .groupby('value').sum()
             .assign(duration = lambda df: np.cumsum(df.duration/df.duration.sum()))
             .assign(duration = lambda df: df.duration.shift())
             .fillna(0)
        )
        percentile_step_func = Stairs()
        for start,end,value in zip(temp_df.duration.values, np.append(temp_df.duration.values[1:],1), temp_df.index):
            percentile_step_func.layer(start*100,end*100,value)
        percentile_step_func._popitem()
        percentile_step_func[100]=0
        return percentile_step_func
    
    @append_doc(SC_docs.mode_example)    
    def mode(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the mode of the step function.  
        
        If there is more than one mode only the smallest is returned
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        float
            The mode
            
        See Also
        --------
        Stairs.mean, Stairs.median
        """
        df = (self.clip(lower,upper)
                .to_dataframe().iloc[1:-1]
                .assign(duration = lambda df: df.end-df.start)
        )
        return df.value.loc[df.duration.idxmax()]

    def values_in_range(self, lower=float('-inf'), upper=float('inf')):
        if isinstance(lower, pd.Timestamp):
            lower = _convert_date_to_float(lower)
        if isinstance(upper, pd.Timestamp):
            upper = _convert_date_to_float(upper)
        return self._values_in_range(lower, upper)
        
    def _values_in_range(self, lower, upper):
        points = [key for key in self._keys() if lower < key < upper]
        if lower > float('-inf'):
            points.append(lower)
        if upper < float('inf'):
            points.append(upper)
        return self._sample(points)
    
    @append_doc(SC_docs.min_example)
    def min(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the minimum value of the step function.
        
        If an interval which to calculate over is specified it is interpreted
        as a closed interval
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        float
            The minimum value of the step function
            
        See Also
        --------
        Stairs.max, staircase.min
        """
        return np.min(self.values_in_range(lower, upper))

    @append_doc(SC_docs.max_example)    
    def max(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the maximum value of the step function.
        
        If an interval which to calculate over is specified it is interpreted
        as a closed interval
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        float
            The maximum value of the step function
            
        See Also
        --------
        Stairs.min, staircase.max
        """
        return np.max(self.values_in_range(lower, upper))
     
    @append_doc(SC_docs.clip_example)        
    def _clip(self, lower=float('-inf'), upper=float('inf')):
        """
        Returns a copy of *self* which is zero-valued everywhere outside of [lower, upper)
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval
        upper : int, float or pandas.Timestamp
            upper bound of the interval
              
        Returns
        -------
        :class:`Stairs`
            Returns a copy of *self* which is zero-valued everywhere outside of [lower, upper)
        """
        assert lower is not None or upper is not None, "clip function should not be called with no parameters." 
        cumulative = self._cumulative()
        left_boundary_index = cumulative.bisect_right(lower) - 1
        right_boundary_index = cumulative.bisect_right(upper) - 1
        value_at_left = cumulative.values()[left_boundary_index]
        value_at_right = cumulative.values()[right_boundary_index]
        s = dict(self._items()[left_boundary_index+1:right_boundary_index+1])
        s[float('-inf')] = 0
        if lower != float('-inf'):
            s[float('-inf')] = 0
            s[lower] = value_at_left
        else:
            s[float('-inf')] = self[float('-inf')]
        if upper != float('inf'):
            s[upper] = s.get(upper,0)-value_at_right 
        return Stairs(s, use_dates=self.use_dates)

    @add_doc(_clip.__doc__)        
    def clip(self, lower=float('-inf'), upper=float('inf')):
        if isinstance(lower, pd.Timestamp):
            lower = _convert_date_to_float(lower)
        if isinstance(upper, pd.Timestamp):
            upper = _convert_date_to_float(upper)
        return self._clip(lower, upper)
            
    def to_dataframe(self):
        """
        Returns a pandas.DataFrame with columns 'start', 'end' and 'value'
        
        The rows of the dataframe can be interpreted as the interval definitions
        which make up the step function.
        
        Returns
        -------
        :class:`pandas.DataFrame`        
        """
        starts = self._keys()
        ends = self._keys()[1:]
        if self.use_dates:
            starts = [pd.NaT] + _convert_float_to_date(np.array(starts[1:]))
            ends = _convert_float_to_date(np.array(ends)) + [pd.NaT]
        else:
            ends.append(float('inf'))
        values = self._cumulative().values()
        df = pd.DataFrame({"start":starts, "end":ends, "value":values})
        return df
            
    @append_doc(SC_docs.number_of_steps_example)
    def number_of_steps(self):
        """Calculates the number of step changes

        Returns
        -------
        int
        
        See Also
        --------
        Stairs.step_changes
        """
        return len(self._keys())-1
        
    def __str__(self):
        return f"<staircase.Stairs, id={id(self)}, dates={self.use_dates}>"

    def __repr__(self):
        return str(self)
    
        
    def __call__(self, *args, **kwargs):
        return self.sample(*args, **kwargs)
    
    __neg__ = negate
    __mul__ = multiply
    __truediv__ = divide
    __add__ = add
    __sub__ = subtract
    __or__ = logical_or
    __and__ = logical_and
    __invert__ = invert
    __eq__ = eq
    __ne__ = ne
    __lt__ = lt
    __gt__ = gt
    __le__ = le
    __ge__ = ge