try:
    from ._version import get_versions
    __version__ = get_versions()['version']
    del get_versions
except:
    __version__ = '0.1.0'

from .stairs import Stairs, sample, aggregate
from .stairs import _mean as mean
from .stairs import _median as median
from .stairs import _min as min
from .stairs import _max as max
