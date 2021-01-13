import operator
import numpy as np
import staircase as sc


def _make_extremum_func(extrema):
    """
    Used to generate _min_pair and _max_pair respectively to cut code duplication

    Parameters
    ----------
    extrema : {"minimum", "maximum"}

    Returns:
        Callable
    """
    comparator = {"minimum": operator.gt, "maximum": operator.lt}[extrema]

    def extremum_func(stairs1, stairs2):
        f"""
        Calculates the {extrema} of two Stairs objects.  It can be thought of as calculating the {extrema} of two step functions.

        Parameters:
            stairs1 (Stairs)
            stairs2 (Stairs)

        Returns:
            Stairs: the result of the calculation
        """
        assert isinstance(stairs1, sc.Stairs) and isinstance(
            stairs2, sc.Stairs
        ), "Arguments must be both of type Stairs."
        assert stairs1.tz == stairs2.tz
        new_instance = stairs1 - stairs2
        cumulative = new_instance._cumulative()
        for key, value in cumulative.items():
            if comparator(value, 0):
                cumulative[key] = 0
        deltas = [cumulative.values()[0]]
        deltas.extend(np.subtract(cumulative.values()[1:], cumulative.values()[:-1]))
        new_instance = sc.Stairs(
            dict(zip(new_instance._keys(), deltas)),
            use_dates=stairs1.use_dates or stairs2.use_dates,
            tz=stairs1.tz,
        )
        return new_instance + stairs2

    return extremum_func


_min_pair = _make_extremum_func("minimum")
_max_pair = _make_extremum_func("maximum")
