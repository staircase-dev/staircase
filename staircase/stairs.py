#uses https://pypi.org/project/sortedcontainers/
from sortedcontainers import SortedDict, SortedSet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import functools
import warnings
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
    
def sample(Stairs_dict, points=None):
    use_dates = False
    if isinstance(Stairs_dict, dict) and Stairs_dict.values()[0].use_dates:
        use_dates = True
    if isinstance(Stairs_dict, pd.Series) and Stairs_dict.values[0].use_dates:
        use_dates = True
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
    if isinstance(Stairs_dict_or_list, dict):
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
    
    
    def number_of_steps(self):
        return len(self.keys())-1
        
    def step_changes(self):
        return self.keys()[1:]
            
    def __call__(self, points):
        if self.use_dates:
            points = _convert_date_to_float(points)
        if hasattr(points, "__iter__"):
            new_instance = self.copy()._layer_multiple(points, None, [0]*len(points))
            cumulative = new_instance._cumulative()
            return [val for key,val in cumulative.items() if key in points]
        else:
            cumulative = self._cumulative()
            preceding_boundary_index = cumulative.bisect_right(points) - 1
            return cumulative.values()[preceding_boundary_index]    
        
    def layer(self, start, end=None, value=None):
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
        """Adds an interval to the Stairs instance

        Parameters:
            start (numeric): start time of the interval
            end (numeric): end time of the interval
            value (numeric, optional): the value of the interval

        Returns:
            self

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
        """Given interval data, adds them to the Stairs instance

        SHOULD NOT HAVE DATES
        
        Parameters:
            starts (list-like): a series of numbers representing the start times of the intervals
            end (list-like): a series of numbers representing the end times of the intervals
            values (list-like, optional): a series of numbers representing the value of each interval.  If not supplied values of 1 are assumed.

        Returns:
            self

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
        
    def __neg__(self):
        new_instance = self.copy()
        for key,delta in new_instance.items():
            new_instance[key] = -delta
        new_instance.cached_cumulative = None
        return new_instance
        
    def __add__(self, other):
        if not isinstance(other, Stairs):
            other = Stairs(other)
        new_instance = self.copy()
        for key, value in other.items():
            new_instance[key] = self.get(key,0) + value
        new_instance._reduce()
        new_instance.use_dates = self.use_dates or other.use_dates
        new_instance.cached_cumulative = None
        return new_instance
        
    def __sub__(self, other):
        if not isinstance(other, Stairs):
            other = Stairs(other)
        other = -other
        return self + other
    
    def copy(self, keep_cache=False):
        """Returns a deep copy

        Returns:
            Stairs

        """ 
        new_instance = Stairs(use_dates=self.use_dates)
        for key,value in self.items():
            new_instance[key] = value
        if keep_cache:
            new_instance.cached_cumulative = self.cached_cumulative
        return new_instance
    
    
    def _cumulative(self):
        if self.cached_cumulative == None:
            self.cached_cumulative = SortedDict(zip(self.keys(), np.cumsum(self.values())))
        return self.cached_cumulative
            
    def make_boolean(self):
        new_instance = self != Stairs(0)
        return new_instance
    
    def __invert__(self):
        new_instance = self.make_boolean()
        new_instance = Stairs(1) - new_instance
        return new_instance
    
    def __and__(self, other):
        assert isinstance(other, type(self)), f"Arguments to {cls.__name__}.min must be both of type {cls}."
        self_bool = self.make_boolean()
        other_bool = other.make_boolean()
        return _min_pair(self_bool, other_bool)
        
    def __or__(self, other):
        assert isinstance(other, type(self)), f"Arguments to {cls.__name__}.min must be both of type {cls}."
        self_bool = self.make_boolean()
        other_bool = other.make_boolean()
        return _max_pair(self_bool, other_bool)

    
    def __lt__(self, other):
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__lt__
        return self.__class__._compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)    
        
    def __gt__(self, other):
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__gt__
        return self.__class__._compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)        
        
    def __le__(self, other):
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__le__
        return self.__class__._compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)        

    def __ge__(self, other):
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__ge__
        return self.__class__._compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)                
    
    def __eq__(self, other):
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__eq__
        return self.__class__._compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or other.use_dates)           
    
    def __ne__(self, other):
        if not isinstance(other, Stairs):
            other = Stairs(other)
        comparator = float(0).__ne__
        return self.__class__._compare((other-self)._cumulative(), comparator, use_dates = self.use_dates or IntSeq2.use_dates)    
        
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
        
    def plot(self, *args, **kwargs):
        """Line plot for Stairs.
        
        Parameters:
            ax: (matplotlib.axes, optional) An axis to be plotted to - specified either as first positional argument, or as named argument
            **kwargs: Additional parameters are the same as those for plot.
        """
        assert len(args) <= 1
        if len(args) == 1:
            ax = args[0]
        else:
            if "ax" in kwargs:
                ax = kwargs.pop("ax")
            else:
                fig, ax = plt.subplots()
                
        cumulative = self._cumulative()
        step_points = cumulative.keys()
        if self.use_dates:
            step_points = [np.NaT] + _convert_float_to_date(np.array(step_points[1:]))
        ax.step(step_points, cumulative.values(), where='post', **kwargs)
    
