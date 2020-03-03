#uses https://pypi.org/project/sortedcontainers/
from sortedcontainers import SortedDict, SortedSet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import functools
import warnings
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


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
    new_instance = Stairs(dict(zip(new_instance.keys(), deltas)), use_dates=stairs1.use_dates or stairs2.use_dates)
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
    new_instance = Stairs(dict(zip(new_instance.keys(), deltas)), use_dates=stairs1.use_dates or stairs2.use_dates)
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

def _get_common_points(Stairs_list):
    points = []
    for stairs in Stairs_list:
        points += list(stairs.keys())
    return SortedSet(points)

def _using_dates(Stairs_dict_or_list):
    try:
        return next(iter(Stairs_dict_or_list.values())).use_dates
    except:
        try:
            return Stairs_dict_or_list.values[0].use_dates
        except:
            try:
                return Stairs_dict_or_list[0]
            except:
                return False
        
    
    
def sample(Stairs_dict, points=None):
    """Merge DataFrame or named Series objects with a database-style join.
    
    The join is done on columns or indexes. If joining columns on
    columns, the DataFrame indexes *will be ignored*. Otherwise if joining indexes
    on indexes or indexes on a column or columns, the index will be passed on.
    
    Parameters
    ----------
    right : DataFrame or named Series
        Object to merge with.
    how : {'left', 'right', 'outer', 'inner'}, default 'inner'
        Type of merge to be performed.
        
        * left: use only keys from left frame, similar to a SQL left outer join;
          preserve key order.
        * right: use only keys from right frame, similar to a SQL right outer join;
          preserve key order.
        * outer: use union of keys from both frames, similar to a SQL full outer
          join; sort keys lexicographically.
        * inner: use intersection of keys from both frames, similar to a SQL inner
          join; preserve the order of the left keys.
    on : label or list
        Column or index level names to join on. These must be found in both
        DataFrames. If `on` is None and not merging on indexes then this defaults
        to the intersection of the columns in both DataFrames.
    left_on : label or list, or array-like
        Column or index level names to join on in the left DataFrame. Can also
        be an array or list of arrays of the length of the left DataFrame.
        These arrays are treated as if they are columns.
    right_on : label or list, or array-like
        Column or index level names to join on in the right DataFrame. Can also
        be an array or list of arrays of the length of the right DataFrame.
        These arrays are treated as if they are columns.
    left_index : bool, default False
        Use the index from the left DataFrame as the join key(s). If it is a
        MultiIndex, the number of keys in the other DataFrame (either the index
        or a number of columns) must match the number of levels.
    right_index : bool, default False
        Use the index from the right DataFrame as the join key. Same caveats as
        left_index.
    sort : bool, default False
        Sort the join keys lexicographically in the result DataFrame. If False,
        the order of the join keys depends on the join type (how keyword).
    suffixes : tuple of (str, str), default ('_x', '_y')
        Suffix to apply to overlapping column names in the left and right
        side, respectively. To raise an exception on overlapping columns use
        (False, False).
    copy : bool, default True
        If False, avoid copy if possible.
    indicator : bool or str, default False
        If True, adds a column to output DataFrame called "_merge" with
        information on the source of each row.
        If string, column with information on source of each row will be added to
        output DataFrame, and column will be named value of string.
        Information column is Categorical-type and takes on a value of "left_only"
        for observations whose merge key only appears in 'left' DataFrame,
        "right_only" for observations whose merge key only appears in 'right'
        DataFrame, and "both" if the observation's merge key is found in both.  
    validate : str, optional
        If specified, checks if merge is of specified type.
        
        * "one_to_one" or "1:1": check if merge keys are unique in both
          left and right datasets.
        * "one_to_many" or "1:m": check if merge keys are unique in left
          dataset.
        * "many_to_one" or "m:1": check if merge keys are unique in right
          dataset.
        * "many_to_many" or "m:m": allowed, but does not result in checks.
        
        .. versionadded:: 0.21.0
    
    Returns
    -------
    DataFrame
        A DataFrame of the two merged objects.
    
    See Also
    --------
    merge_ordered : Merge with optional filling/interpolation.
    merge_asof : Merge on nearest keys.
    DataFrame.join : Similar method using indices.
    
    Notes
    -----
    Support for specifying index levels as the `on`, `left_on`, and
    `right_on` parameters was added in version 0.23.0
    Support for merging named Series objects was added in version 0.24.0
    
    Examples
    --------
    
    >>> df1 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],
    ...                     'value': [1, 2, 3, 5]})
    >>> df2 = pd.DataFrame({'rkey': ['foo', 'bar', 'baz', 'foo'],
    ...                     'value': [5, 6, 7, 8]})
    >>> df1
        lkey value
    0   foo      1
    1   bar      2
    2   baz      3
    3   foo      5
    >>> df2
        rkey value
    0   foo      5
    1   bar      6
    2   baz      7
    3   foo      8
    
    Merge df1 and df2 on the lkey and rkey columns. The value columns have
    the default suffixes, _x and _y, appended.
    
    >>> df1.merge(df2, left_on='lkey', right_on='rkey')
      lkey  value_x rkey  value_y
    0  foo        1  foo        5
    1  foo        1  foo        8
    2  foo        5  foo        5
    3  foo        5  foo        8
    4  bar        2  bar        6
    5  baz        3  baz        7
    
    Merge DataFrames df1 and df2 with specified left and right suffixes
    appended to any overlapping columns.
    
    >>> df1.merge(df2, left_on='lkey', right_on='rkey',
    ...           suffixes=('_left', '_right'))
      lkey  value_left rkey  value_right
    0  foo           1  foo            5
    1  foo          
     1  foo            8
    2  foo           5  foo            5
    3  foo           5  foo            8
    4  bar           2  bar            6
    5  baz           3  baz            7
    
    Merge DataFrames df1 and df2, but raise an exception if the DataFrames have
    any overlapping columns.
    
    >>> df1.merge(df2, left_on='lkey', right_on='rkey', suffixes=(False, False))
    Traceback (most recent call last):
    ...
    ValueError: columns overlap but no suffix specified:
        Index(['value'], dtype='object')
        
    .. plot::
        :context: close-figs
        
        >>> df = pd.DataFrame(
        ...     np.random.randint(1, 7, 6000),
        ...     columns = ['one'])
        >>> df['two'] = df['one'] + np.random.randint(1, 7, 6000)
        >>> ax = df.plot.hist(bins=12, alpha=0.5)
        
    """
    use_dates = _using_dates(Stairs_dict)
    #assert len(set([type(x) for x in Stairs_dict.values()])) == 1, "Stairs_dict must contain values of same type"
    if points is None:
        points = _get_common_points(Stairs_dict.values())
    result = (pd.DataFrame({"points":points, **{key:stairs(points) for key,stairs in Stairs_dict.items()}})
        .melt(id_vars="points", var_name="key")
    )
    
    try:
        if len(Stairs_dict.index.names) > 1:
            result = (result
                .join(pd.DataFrame(result.key.tolist(), columns=Stairs_dict.index.names))
                .drop(columns='key')
            )     
    except:
        pass
    return result

def aggregate(Stairs_dict_or_list, func, points=None):
    '''An aggregating function
    
    '''
    if isinstance(Stairs_dict_or_list, dict) or isinstance(Stairs_dict_or_list, pd.Series):
        Stairs_dict = Stairs_dict_or_list
    else:
        Stairs_dict = dict(enumerate(Stairs_dict_or_list))
    df = sample(Stairs_dict, points)
    aggregation = df.pivot_table(index="points", columns="key", values="value").aggregate(func, axis=1)
    step_changes = aggregation.diff().fillna(0)
    return Stairs(dict(step_changes))

    
def _mean(Stairs_dict_or_list):
    return aggregate(Stairs_dict_or_list, np.mean)

def _median(Stairs_dict_or_list):
    return aggregate(Stairs_dict_or_list, np.median)
        
def _min(Stairs_dict_or_list):
    return aggregate(Stairs_dict_or_list, np.min)

def _max(Stairs_dict_or_list):
    return aggregate(Stairs_dict_or_list, np.max)
        
class Stairs(SortedDict):
    '''Intervals are considered left-closed, right-open. '''
    
    def __init__(self, value=0, use_dates=False):
        if isinstance(value, dict):
            super().__init__(value)
        else:
            super().__init__()
            self[float('-inf')] = value
        self.use_dates = use_dates
        self.cached_cumulative = None

    def copy(self):
        """Returns a deep copy of this Stairs instance

        Returns
        -------
        copy : Stairs

        """ 
        new_instance = Stairs(use_dates=self.use_dates)
        for key,value in self.items():
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
            step_points = _convert_float_to_date(np.array(step_points[1:]))
        ax.step(step_points, list(cumulative.values())[1:], where='post', **kwargs)
        return ax

    def evaluate(self, x):
        """Evaluates the value of the step function at one, or more, points.

        The function should be called using parentheses.  See example below.

        Parameters
        ----------
        x : int, float or vector data
            values at which to evaluate the function
            
        Returns
        -------
        float, or list of floats
        
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> s1(3.5)
            1
            >>> s1([1, 2, 4.5, 6])
            [1, 0, -1, 0]
        
        """
        if self.use_dates:
            x = _convert_date_to_float(x)
        if hasattr(x, "__iter__"):
            new_instance = self.copy()._layer_multiple(x, None, [0]*len(x))
            cumulative = new_instance._cumulative()
            return [val for key,val in cumulative.items() if key in x]
        else:
            cumulative = self._cumulative()
            preceding_boundary_index = cumulative.bisect_right(x) - 1
            return cumulative.values()[preceding_boundary_index]    

            
    def layer(self, start, end=None, value=None):
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
        
        
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> import staircase as sc
            ... (sc.Stairs()
            ...     .layer(1,3)
            ...     .layer(4,5,-2)
            ...     .plot()
            ... )
            
        .. plot::
            :context: close-figs
            
            >>> import pandas as pd
            >>> import staircase as sc
            >>> data = pd.DataFrame({"starts":[1,4,5.5],
            ...                      "ends":[3,5,7],
            ...                      "values":[-1,2,-3]})
            >>> data
               starts  ends  values
            0     1.0     3      -1
            1     4.0     5       2
            2     5.5     7      -3
            >>> (sc.Stairs(1.5)
            ...     .layer(data["starts"], data["ends"], data["values"])
            ...     .plot()
            ... )
        """
        if hasattr(start, "__iter__"):
            if self.use_dates:
                start = _convert_date_to_float(start)
                if end is not None:
                    end = _convert_date_to_float(end)
            layer_func = self._layer_multiple
        else:
            layer_func = self._layer_single
            if value is None:
                value = 1
        return layer_func(start, end, value)
        
    def _layer_single(self, start, end=None, value=1):
        """
        Implementation of the layer function for when start parameter is single-valued
        """
        if self.use_dates:
            start = _convert_date_to_float(start)
        self[start] = self.get(start,0) + value
        if self[start] == 0:
            self.pop(start)
        
        if end != None:
            if self.use_dates:
                end = _convert_date_to_float(end)
            self[end] = self.get(end,0) - value
            if self[end] == 0 or end == float('inf'):
                self.pop(end)
                
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
                self[start] = self.get(start,0) + value
            if not np.isnan(end):
                self[end] = self.get(end,0) - value
        self.cached_cumulative = None
        return self

    def step_changes(self):
        """
        Returns a dictionary of key, value pairs of indicating where step changes occur in the step function, and the change in value 
        
        Returns
        -------
        dictionary
        
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> s1.step_changes()
            {1: 1, 2: -1, 3: 1, 4: -2, 5: 1}
        
        
        """
        return dict(self.items()[1:])

            
    def negate(self):
        """
        An operator which produces a new Stairs instance representing the multiplication of the step function by -1.
        
        Should be used as an operator, i.e. by utilising the symbol -.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the multiplication of the step function by -1
        
        
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> (-s1).plot(color='r')
        """    
        
        new_instance = self.copy()
        for key,delta in new_instance.items():
            new_instance[key] = -delta
        new_instance.cached_cumulative = None
        return new_instance
        
    def add(self, other):
        """
        An operator facilitating the addition of two step functions.
        
        Should be used as an operator, i.e. by utilising the symbol +.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the addition of two step functions
        
        
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1+s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1+s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        if not isinstance(other, Stairs):
            other = Stairs(other)
        new_instance = self.copy()
        for key, value in other.items():
            new_instance[key] = self.get(key,0) + value
        new_instance._reduce()
        new_instance.use_dates = self.use_dates or other.use_dates
        new_instance.cached_cumulative = None
        return new_instance
        
    def subtract(self, other):
        """
        An operator facilitating the subtraction of one step function from another.
        
        Should be used as an operator, i.e. by utilising the symbol -.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the subtraction of one step function from another
        
        
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1-s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1-s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        if not isinstance(other, Stairs):
            other = Stairs(other)
        other = -other
        return self + other
    
    def _mul_or_div(self, other, func):
        a = self.copy()
        b = other.copy()
        a_keys = a.keys()
        b_keys = b.keys()
        a.layer(b_keys, None, [0]*len(b_keys))
        b.layer(a_keys, None, [0]*len(a_keys))
        
        multiplied_cumulative_values = func(a._cumulative().values(), b._cumulative().values())
        new_instance = _from_cumulative(dict(zip(a.keys(), multiplied_cumulative_values)), use_dates=self.use_dates)
        new_instance._reduce()   
        return new_instance
        
        
    def divide(self, other):
        """
        An operator facilitating the division of one step function by another.
        
        The divisor should cannot be zero-valued anywhere.
        
        Should be used as an operator, i.e. by utilising the symbol /.  See examples below.      
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the division of one step function by another
        
        
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, (s2+2), s1/(s2+2)]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2+2", "S1/(s2+2)"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        if not bool(other.make_boolean()):
            raise ZeroDivisionError("Divisor Stairs instance must not be zero-valued at any point")
        
        return self._mul_or_div(other, np.divide)
    
    def multiply(self, other):
        r"""
        An operator facilitating the multiplication of one step function with another.
        
        Should be used as an operator, i.e. by utilising the symbol \*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the multiplication of one step function from another
        
        
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1*s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1*s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        return self._mul_or_div(other, np.multiply)
        
    def _cumulative(self):
        if self.cached_cumulative == None:
            self.cached_cumulative = SortedDict(zip(self.keys(), np.cumsum(self.values())))
        return self.cached_cumulative
        
    def make_boolean(self):
        """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s2, s2.make_boolean()]
            >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s2", "s2.make_boolean()"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        new_instance = self != Stairs(0)
        return new_instance
    
    def invert(self):
        """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s2, ~s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s2", "~s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        new_instance = self.make_boolean()
        new_instance = Stairs(1) - new_instance
        return new_instance
    
    def logical_and(self, other):
        """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 & s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 & s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        assert isinstance(other, type(self)), f"Arguments must be both of type Stairs."
        self_bool = self.make_boolean()
        other_bool = other.make_boolean()
        return _min_pair(self_bool, other_bool)
    
    def logical_or(self, other):
        """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 | s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 | s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        assert isinstance(other, type(self)), f"Arguments must be both of type Stairs."
        self_bool = self.make_boolean()
        other_bool = other.make_boolean()
        return _max_pair(self_bool, other_bool)

    
    def lt(self, other):
        """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 < s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 < s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__lt__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)    
        
    def gt(self, other):
        """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 > s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 > s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__gt__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)        
        
    def le(self, other):
        """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 <= s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 <= s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__le__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)        

    def ge(self, other):
        """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 >= s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 >= s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__ge__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)                
    
    def eq(self, other):
        """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 == s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 == s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__eq__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)           
    
    def ne(self, other):
        """
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> stair_list = [s1, s2, s1 != s2]
            >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(17,5), sharey=True, sharex=True)
            >>> for ax, title, stair_instance in zip(axes, ("s1", "s2", "s1 != s2"), stair_list):
            ...     stair_instance.plot(ax)
            ...     ax.set_title(title)
        """
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__ne__
        return _compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)    
        
    def identical(self, IntSeq):
        return bool(self == IntSeq)
    
    def _reduce(self):
        to_remove = [key for key,val in self.items()[1:] if val == 0]
        for key in to_remove:
            self.pop(key)
        
    def __bool__(self):
        self._reduce()
        if len(self) != 1:
            return False
        value = self.values()[0]
        return value == 1
        
    def get_integral_and_mean(self, lower=float('-inf'), upper=float('inf')):
        if self.use_dates:
            if isinstance(lower, pd.Timestamp):
                lower = _convert_date_to_float(lower)
            if isinstance(upper, pd.Timestamp):
                upper = _convert_date_to_float(upper) 
        new_instance = self.clip(lower, upper)
        if lower != float('-inf'):
            new_instance[lower] = new_instance.get(lower,0)
        if upper != float('inf'):
            new_instance[upper] = new_instance.get(upper,0)
        cumulative = new_instance._cumulative()
        widths = np.subtract(cumulative.keys()[2:], cumulative.keys()[1:-1])
        heights = cumulative.values()[1:-1]
        area = np.multiply(widths, heights).sum()
        mean = area/(cumulative.keys()[-1] - cumulative.keys()[1])
        return area, mean
            
    def integrate(self, lower=float('-inf'), upper=float('inf')):
        area, mean = self.get_integral_and_mean(lower, upper)
        return area
     
    def mean(self, lower=float('-inf'), upper=float('inf')):
        area, mean = self.get_integral_and_mean(lower, upper)
        return mean
    
    def median(self, lower=float('-inf'), upper=float('inf')):
        return self.percentiles(lower, upper)(0.5)
    
    def mode(self, lower=float('-inf'), upper=float('inf')):
        df = (self.clip(lower,upper)
                .to_dataframe().iloc[1:-1]
                .assign(duration = lambda df: df.end-df.start)
        )
        return df.value.iloc[df.duration.argmax()]

    def _values_in_range(self, lower, upper):
        points = [key for key in self.keys() if lower < key < upper]
        if lower > float('-inf'):
            points.append(self(lower))
        if upper < float('inf'):
            points.append(self(upper))
        return self(points)
        
    def min(self, lower=float('-inf'), upper=float('inf')):
        return np.min(self._values_in_range(lower, upper))
        
    def max(self, lower=float('-inf'), upper=float('inf')):
        return np.min(self._values_in_range(lower, upper))
        
    def percentiles(self, lower=float('-inf'), upper=float('inf')):
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
            percentile_step_func.layer(start,end,value)
        return percentile_step_func
                
        
    def clip(self, lower=float('-inf'), upper=float('inf')):
        assert lower is not None or upper is not None, "clip function should not be called with no parameters."
        if self.use_dates:
            if isinstance(lower, pd.Timestamp):
                lower = _convert_date_to_float(lower)
            if isinstance(upper, pd.Timestamp):
                upper = _convert_date_to_float(upper) 
        cumulative = self._cumulative()
        left_boundary_index = cumulative.bisect_right(lower) - 1
        right_boundary_index = cumulative.bisect_right(upper) - 1
        value_at_left = cumulative.values()[left_boundary_index]
        value_at_right = cumulative.values()[right_boundary_index]
        s = dict(self.items()[left_boundary_index+1:right_boundary_index+1])
        s[float('-inf')] = 0
        if lower != float('-inf'):
            s[float('-inf')] = 0
            s[lower] = value_at_left
        else:
            s[float('-inf')] = self[float('-inf')]
        if upper != float('inf'):
            s[upper] = s.get(upper,0)-value_at_right 
        return Stairs(s, use_dates=self.use_dates)
              
    def to_dataframe(self):
        cumulative = self._cumulative()
        starts = cumulative.keys()
        ends = cumulative.keys()[1:]
        if self.use_dates:
            starts = [pd.NaT] + _convert_float_to_date(np.array(starts[1:]))
            ends = _convert_float_to_date(np.array(ends)) + [pd.NaT]
        else:
            ends.append(float('inf'))
        values = cumulative.values()
        df = pd.DataFrame({"start":starts, "end":ends, "value":values})
        return df
        
    def __str__(self):
        if len(self) < 11:
            return super().__repr__()
        return ''.join(['Stairs({', ', '.join([f'{key}: {val}' for key,val in self.items()[:10]]), '...})'])
        
    def __repr__(self):
        return str(self)
        
    
    def number_of_steps(self):
        """Calculates the number of step changes

        Returns
        -------
        int
        
        Examples
        --------
            
        .. plot::
            :context: close-figs
            
            >>> s1.plot()
            >>> s1.number_of_steps()
            5
        
        """
        return len(self.keys())-1
    
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
    __call__ = evaluate