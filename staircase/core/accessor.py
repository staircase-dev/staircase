"""
Taken from pandas.core.accessor.py, with minor adjustments.
"""


class CachedAccessor:
    """
    Custom property-like object.
    A descriptor for caching accessors.

    Parameters
    ----------
    name : str
        Namespace that will be accessed under, e.g. ``sc.plot``.
    accessor : cls
        Class with the extension methods.
    """

    def __init__(self, name: str, accessor) -> None:
        self._name = name
        self._accessor = accessor

    def __get__(self, obj, cls):
        if obj is None:
            # we're accessing the attribute of the class, i.e., Stairs.plot
            return self._accessor
        accessor_obj = self._accessor(obj)
        obj.__setattr__(self._name, accessor_obj)
        return accessor_obj
