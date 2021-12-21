import re

_x_agg_docstring = """
Returns a :class:`staircase.Stairs` object representing the {calc} of multiple step functions.

{params}

Returns
-------
:class:`Stairs`

See Also
--------
{see_also}

Examples
--------
{example}
"""

_toplevel_params = """
Parameters
----------
collection : tuple, list, numpy array, dict or pandas.Series
    The Stairs instances to aggregate"""


def _make_see_also(args):
    if args is None:
        return ""
    else:
        return f"See Also\n--------\n{args}"


_example = """
>>> import staircase as sc
>>> {arr_def}

.. plot::
    :context: close-figs
    :include-source: False

    >>> {arr_def}
    >>> stair_list = [{plots}]
    >>> fig, axes = plt.subplots(nrows=1, ncols={ncols},  figsize=({width},3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, {plot_titles}, stair_list):
    ...     stair_instance.plot(ax=ax, arrows=True)
    ...     ax.set_title(title)
"""


def _get_plot_titles(which, method):
    if method == "agg":
        result = (
            f"sc.{method}(arr, np.std)"
            if which == "toplevel"
            else f"arr.{method}(np.std)"
        )
    else:
        result = f"sc.{method}(arr)" if which == "toplevel" else f"arr.{method}()"
    return ["s1", "s2", result]


def _gen_example(plot_titles, arr_def):
    # plot_titles is a list of strings
    ncols = len(plot_titles)
    plots = ", ".join(plot_titles)
    return _example.format(
        arr_def=arr_def,
        plots=plots,
        ncols=ncols,
        plot_titles=plot_titles,
        width=ncols + 5,
    )


def make_docstring(which, method):

    if method in ("logical_or", "logical_and"):
        return _make_logical_docstring(which, method)

    if method in ("limit"):
        return _make_limit_docstring(which)

    if method in ("sample"):
        return _make_sample_docstring(which)

    if method in ("cov", "corr"):
        return _make_cov_corr_docstring(which, method)

    if method in ("plot"):
        return _make_plot_docstring(which)

    if which == "array":
        see_also = f":func:`staircase.{method}`, :meth:`pandas.Series.{method}`"
        params = ""
        arr_def = "arr = sc.StairsArray([s1,s2])"
    elif which == "toplevel":
        see_also = (
            f":meth:`staircase.StairsArray.{method}`, :meth:`pandas.Series.{method}`"
        )
        params = _toplevel_params.format(calc=method)
        arr_def = "arr = [s1, s2]"

    example = _gen_example(
        _get_plot_titles(which, method),
        arr_def=arr_def,
    )
    if method == "agg":
        example = ">>> import numpy as np\n" + example

    return re.sub(
        "\n\n+",
        "\n\n",
        _x_agg_docstring.format(
            calc={"min": "minimum", "max": "maximum", "agg": "aggregate"}.get(
                method, method
            ),
            params=params,
            see_also=see_also,
            example=example,
        ),
    )


_logical_base_docstring = """
Returns a boolean-valued step function resulting from a {logical_method} operation.

The operands are the Stairs instances in the object the accessor belongs to.

Returns
-------
:class:`staircase.Stairs`
    boolean-valued step function

Examples
---------

>>> {setup}

.. plot::
    :context: close-figs
    :include-source: False

    >>> {setup}
    >>> stair_list = [s1, s2, {result}]
    >>> fig, axes = plt.subplots(nrows=1, ncols=3,  figsize=(8,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ["s1", "s2", "{result}"], stair_list):
    ...     stair_instance.plot(ax=ax, arrows=True)
    ...     ax.set_title(title)
"""


def _make_logical_docstring(which, method):
    if which == "accessor":
        setup = 'arr = pd.Series([s1, s2], dtype="Stairs")'
        result = f"arr.sc.{method}()"
    elif which == "toplevel":
        setup = "arr = [s1, s2]"
        result = f"sc.{method}(arr)"
    elif which == "array":
        setup = "arr = sc.StairsArray([s1, s2])"
        result = f"arr.{method}()"

    logical_method = {
        "logical_or": "logical-or",
        "logical_and": "logical-and",
    }[method]
    return _logical_base_docstring.format(
        logical_method=logical_method, setup=setup, result=result
    )


_limit_base = """
Takes a collection of Stairs instances and evaluates their limits across a set of points.

Technically the results of this function should be considered as :math:`\\lim_{{x \\to z^{{-}}}} f(x)`
or :math:`\\lim_{{x \\to z^{{+}}}} f(x)`, when *side* = 'left' or *side* = 'right' respectively. See
:ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.

Parameters
{collection_param}
x : scalar or vector data
    The points at which to sample the Stairs instances.  Must belong to the step function domain.
side : {{'left', 'right'}}, default 'right'
    if points where step changes occur do not coincide with x then this parameter
    has no effect.  Where a step changes occurs at a point given by x, this parameter
    determines if the step function is evaluated at the interval to the left, or the right.

Returns
-------
:class:`pandas.DataFrame`
    {return_desc}

See Also
--------
{see_also}

Examples
--------

.. plot::
    :context: close-figs
    :include-source: False

    >>> stair_list = [s2, s3]
    >>> fig, axes = plt.subplots(nrows=1, ncols=2,  figsize=(7,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ["s2", "s3"], stair_list):
    ...     stair_instance.plot(ax=ax, arrows=True)
    ...     ax.set_title(title)

>>> import staircase as sc
>>> {setup}
>>> [s2.closed, s3.closed]
["left", "left]

>>> {calc_preamble}[2,3,4], side="left"))
     2    3    4
0  0.5  0.0 -1.0
1  1.0  NaN  1.0

>>> {calc_preamble}[2,3,4], side="right"))
     2    3    4
0  0.0 -1.0 -1.0
1  0.0  NaN -1.0
"""

_collection_param = """----------
collection : array-like, dictionary or pandas.Series
    The Stairs instances at which to evaluate"""

_top_level_limit_extra_examples = """
>>> stairs = {"s2":s2, "s3":s3}
>>> sc.limit(stairs, [2,3,4], side="left"))
      2    3    4
s1  0.5  0.0 -1.0
s2  1.0  NaN  1.0

>>> index=pd.MultiIndex.from_tuples([("a", "s2"), ("b", "s3")])
>>> stairs = pd.Series([s2,s3], index=index)
>>> sc.limit(stairs, [2,3,4], side="left"))
        2    3    4
a s1  0.5  0.0 -1.0
b s2  1.0  NaN  1.0
"""


def _make_limit_docstring(which):
    if which == "toplevel":
        collection_param = _collection_param
        setup = "stairs = [s2, s3]"
        calc_preamble = "sc.limit(stairs, "
        return_desc = """A dataframe, where rows correspond to the Stairs instances in *collection*.
    and columns correspond to the points in *x*.  If *collection* is a dictionary then the
    resulting dataframe will be indexed by the dictionary keys.  If *collection* is a
    :class:`pandas.Series` then the dataframe will have the same index as the series."""
        see_also = ":meth:`staircase.core.arrays.accessor.StairsAccessor.limit`, :meth:`staircase.StairsArray.limit`, :meth:`staircase.sample`"
    elif which == "accessor":
        collection_param = "----------"
        setup = 'stairs = pd.Series([s2, s3], dtype="Stairs")'
        calc_preamble = "stairs.sc.limit("
        return_desc = """A dataframe, where rows correspond to the Stairs instances in the :class:`pandas.Series`.
    and columns correspond to the points in *x*.  The dataframe will have the same index as the Series."""
        see_also = ":meth:`staircase.limit`, :meth:`staircase.StairsArray.limit`, :meth:`staircase.core.arrays.accessor.StairsAccessor.sample`"
    elif which == "array":
        collection_param = "----------"
        setup = "stairs = sc.StairsArray([s2, s3])"
        calc_preamble = "stairs.limit("
        return_desc = """A dataframe, where rows correspond to the Stairs instances in the :class:`StairsArray`.
    and columns correspond to the points in *x*."""
        see_also = ":meth:`staircase.limit`, :meth:`staircase.core.arrays.accessor.StairsAccessor.limit`, :meth:`staircase.StairsArray.sample`"
    doc = _limit_base.format(
        collection_param=collection_param,
        setup=setup,
        calc_preamble=calc_preamble,
        return_desc=return_desc,
        see_also=see_also,
    )
    if which == "toplevel":
        doc += _top_level_limit_extra_examples
    return doc


_sample_base = """
Takes a collection of Stairs instances and evaluates their values across a set of points.

Parameters
{collection_param}
x : scalar or vector data
    The points at which to sample the Stairs instances.  Must belong to the step function domain.

Returns
-------
:class:`pandas.DataFrame`
    {return_desc}

See Also
--------
{see_also}

Examples
--------

.. plot::
    :context: close-figs
    :include-source: False

    >>> stair_list = [s2, s3]
    >>> fig, axes = plt.subplots(nrows=1, ncols=2,  figsize=(7,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ["s2", "s3"], stair_list):
    ...     stair_instance.plot(ax=ax, arrows=True)
    ...     ax.set_title(title)

>>> import staircase as sc
>>> {setup}
>>> [s2.closed, s3.closed]
["left", "left]

>>> {calc_preamble}[2,3,4]))
     2    3    4
0  0.0 -1.0 -1.0
1  0.0  NaN -1.0
"""

_top_level_sample_extra_examples = """
>>> stairs = {"s2":s2, "s3":s3}
>>> sc.sample(stairs, [2,3,4]))
      2    3    4
s1  0.0 -1.0 -1.0
s2  0.0  NaN -1.0

>>> index=pd.MultiIndex.from_tuples([("a", "s2"), ("b", "s3")])
>>> stairs = pd.Series([s2,s3], index=index)
>>> sc.sample(stairs, [2,3,4], side="left"))
        2    3    4
a s1  0.0 -1.0 -1.0
b s2  0.0  NaN -1.0
"""


def _make_sample_docstring(which):
    if which == "toplevel":
        collection_param = _collection_param
        setup = "stairs = [s2, s3]"
        calc_preamble = "sc.sample(stairs, "
        return_desc = """A dataframe, where rows correspond to the Stairs instances in *collection*.
    and columns correspond to the points in *x*.  If *collection* is a dictionary then the
    resulting dataframe will be indexed by the dictionary keys.  If *collection* is a
    :class:`pandas.Series` then the dataframe will have the same index as the series."""
        see_also = ":meth:`staircase.core.arrays.accessor.StairsAccessor.sample`, :meth:`staircase.StairsArray.sample`, :meth:`staircase.limit`"
    elif which == "accessor":
        collection_param = "----------"
        setup = 'stairs = pd.Series([s2, s3], dtype="Stairs")'
        calc_preamble = "stairs.sc.sample("
        return_desc = """A dataframe, where rows correspond to the Stairs instances in the :class:`pandas.Series`.
    and columns correspond to the points in *x*.  The dataframe will have the same index as the Series."""
        see_also = ":meth:`staircase.sample`, :meth:`staircase.StairsArray.sample`, :meth:`staircase.core.arrays.accessor.StairsAccessor.limit`"
    elif which == "array":
        collection_param = "----------"
        setup = "stairs = sc.StairsArray([s2, s3])"
        calc_preamble = "stairs.sample("
        return_desc = """A dataframe, where rows correspond to the Stairs instances in the :class:`StairsArray`.
    and columns correspond to the points in *x*."""
        see_also = ":meth:`staircase.sample`, :meth:`staircase.core.arrays.accessor.StairsAccessor.sample`, :meth:`staircase.StairsArray.limit`"
    doc = _sample_base.format(
        collection_param=collection_param,
        setup=setup,
        calc_preamble=calc_preamble,
        return_desc=return_desc,
        see_also=see_also,
    )
    if which == "toplevel":
        doc += _top_level_sample_extra_examples
    return doc


_cov_corr_base = """
Calculates the {calc_name} matrix for a collection of :class:`Stairs` instances

Parameters
{collection_param}
lower : int, float or pandas.Timestamp
    lower bound of the interval on which to perform the calculation
upper : int, float or pandas.Timestamp
    upper bound of the interval on which to perform the calculation

Returns
-------
:class:`pandas.DataFrame`
    The {calc_name} matrix

See Also
--------
{see_also}

Examples
--------
{examples}
"""

_cov_examples = """
>>> import staircase as sc
>>> {setup}

>>> {calc_method}
          0          1          2
0  0.687500   0.140496   0.652893
1  0.140496   0.471074   0.611570
2  0.652893   0.611570   1.264463
"""

_corr_examples = """
>>> import staircase as sc
>>> {setup}
>>> {calc_method}
          0          1          2
0  1.000000   0.246878   0.700249
1  0.246878   1.000000   0.792407
2  0.700249   0.792407   1.000000
"""

_top_level_cov_extra_examples = """
>>> stairs = {"s1":s1, "s2":s2, "s1+s2":s1+s2}
>>> sc.cov(stairs, [2,3,4]))
              s1         s2      s1+s2
s1      0.687500   0.140496   0.652893
s2      0.140496   0.471074   0.611570
s1+ s2  0.652893   0.611570   1.264463
"""


_top_level_corr_extra_examples = """
>>> stairs = {"s1":s1, "s2":s2, "s1+s2":s1+s2}
>>> sc.corr(stairs, [2,3,4]))
              s1         s2      s1+s2
s1      1.000000   0.246878   0.700249
s2      0.246878   1.000000   0.792407
s1+ s2  0.700249   0.792407   1.000000
"""


def _make_cov_corr_docstring(which, method):
    other = {"cov": "corr", "corr": "cov"}[method]
    calc_name = {"cov": "covariance", "corr": "correlation"}[method]
    examples = {"cov": _cov_examples, "corr": _corr_examples}[method]
    if which == "toplevel":
        collection_param = _collection_param
        setup = "stairs = [s1, s2, s1+s2]"
        calc_method = f"sc.{method}(stairs)"
        see_also = f":meth:`staircase.core.arrays.accessor.StairsAccessor.{method}`, :meth:`staircase.StairsArray.{method}`, :meth:`staircase.{other}`"
    elif which == "accessor":
        collection_param = "----------"
        setup = 'stairs = pd.Series([s1, s2, s1+s2], dtype="Stairs")'
        calc_method = f"stairs.sc.{method}()"
        see_also = f":meth:`staircase.{method}`, :meth:`staircase.StairsArray.{method}`, :meth:`staircase.core.arrays.accessor.StairsAccessor.{other}`"
    elif which == "array":
        collection_param = "----------"
        setup = "stairs = sc.StairsArray([s1, s2, s1+s2])"
        calc_method = f"stairs.{method}()"
        see_also = f":meth:`staircase.{method}`, :meth:`staircase.core.arrays.accessor.StairsAccessor.{method}`, :meth:`staircase.StairsArray.{other}`"
    doc = _cov_corr_base.format(
        collection_param=collection_param,
        calc_name=calc_name,
        see_also=see_also,
        examples=examples.format(setup=setup, calc_method=calc_method),
    )
    if which == "toplevel":
        if method == "cov":
            doc += _top_level_cov_extra_examples
        else:
            doc += _top_level_corr_extra_examples
    return doc


_plot_base = """
Plots a collection of :class:`Stairs` instances to a single axes

Parameters
{collection_param}
ax : :class:`matplotlib.axes.Axes`, optional
    If supplied will plot to this axes
labels : array-like, optional
    Used to label each step function.  Use `ax.legend()` to show.
**kwargs :
    Additional parameters are the same as those for :meth:`staircase.Stairs.plot`.

Returns
-------
:class:`matplotlib.axes.Axes`

See Also
--------
{see_also}

Examples
--------

>>> import staircase as sc
>>> import matplotlib.pyplot as plt

.. plot::
    :context: close-figs

    >>> {setup}
    >>> {calc_method}
    >>> ax.legend()
"""

_top_level_plot_extra_examples = """
.. plot::
    :context: close-figs

    >>> stairs = {"s1":s1, "s2":s2}
    >>> _, ax = plt.subplots(figsize=(4,3))
    >>> sc.plot(stairs, ax)
    >>> ax.legend()
"""

_accessor_plot_extra_examples = """
.. plot::
    :context: close-figs

    >>> stairs = pd.Series([s2, s3], index=["s2", "s3"], dtype="Stairs")
    >>> _, ax = plt.subplots(figsize=(4,3))
    >>> stairs.sc.plot(ax)
    >>> ax.legend()
"""

_array_plot_extra_examples = """
.. plot::
    :context: close-figs

    >>> stairs = sc.StairsArray([s2, s3])
    >>> _, ax = plt.subplots(figsize=(4,3))
    >>> stairs.plot(ax, labels=("s2", "s3"))
    >>> ax.legend()
"""


def _make_plot_docstring(which):
    if which == "toplevel":
        collection_param = _collection_param
        setup = "stairs = [s2, s3]\n    >>> _, ax = plt.subplots(figsize=(4,3))"
        calc_method = "sc.plot(stairs, ax), "
        see_also = ":meth:`staircase.core.arrays.accessor.StairsAccessor.plot`, :meth:`staircase.StairsArray.plot`, :meth:`staircase.Stairs.plot`"
    elif which == "accessor":
        collection_param = "----------"
        setup = 'stairs = pd.Series([s2, s3], dtype="Stairs")\n    >>> _, ax = plt.subplots(figsize=(4,3))'
        calc_method = "stairs.sc.plot(ax)"
        see_also = ":meth:`staircase.plot`, :meth:`staircase.StairsArray.plot`, :meth:`staircase.Stairs.plot`"
    elif which == "array":
        collection_param = "----------"
        setup = "stairs = sc.StairsArray([s2, s3])\n    >>> _, ax = plt.subplots(figsize=(4,3))"
        calc_method = "stairs.plot(ax)"
        see_also = ":meth:`staircase.plot`, :meth:`staircase.core.arrays.accessor.StairsAccessor.plot`, :meth:`staircase.Stairs.plot`"
    doc = _plot_base.format(
        collection_param=collection_param,
        setup=setup,
        calc_method=calc_method,
        see_also=see_also,
    )
    if which == "toplevel":
        doc += _top_level_plot_extra_examples
    elif which == "accessor":
        doc += _accessor_plot_extra_examples
    return doc


_extension_array_setup = """
>>> {var} = sc.StairsArray({stair_list})

.. plot::
    :context: close-figs
    :include-source: False

    >>> stair_list = {stair_list}
    >>> fig, axes = plt.subplots(nrows=1, ncols=2,  figsize=(7,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ["{var}[0]", "{var}[1]"], stair_list):
    ...     stair_instance.plot(ax=ax, arrows=True)
    ...     ax.set_title(title)
"""

_extension_array_result = """
>>> result = {result1}

.. plot::
    :context: close-figs
    :include-source: False

    >>> arr = sc.StairsArray({stair_list})
    >>> result = {result2}
    >>> fig, axes = plt.subplots(nrows=1, ncols=2,  figsize=(7,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ["result[0]", "result[1]"], result):
    ...     stair_instance.plot(ax=ax, arrows=True)
    ...     ax.set_title(title)
"""


def _make_extension_array_example(sym, rop=False):
    result = f"0.5 {sym} arr" if rop else f"arr {sym} 0.5"
    example = _extension_array_setup.format(
        var="arr", stair_list="[s1,s2]"
    ) + _extension_array_result.format(
        result1=result,
        sym=sym,
        stair_list="[s1,s2]",
        result2=result,
    )
    if not rop:
        example += _extension_array_setup.format(
            var="other", stair_list="[s4,s3]"
        ) + _extension_array_result.format(
            result1=f"arr {sym} other",
            sym=sym,
            stair_list="[s1,s2]",
            result2=f"arr {sym} sc.StairsArray([s4,s3])",
        )
    return example


_extension_array_binop = """
Binary operator for :class:`staircase.StairsArray` (and :class:`pandas.Series` with "Stairs" dtype).

Equivalent to {equiv}.

Parameters
-----------
other : int, float, :class:`staircase.Stairs` or array-like of these
    If array-like must have same length as *self*.

Returns
-------
:class:`staircase.StairsArray`

See Also
---------
:meth:`staircase.Stairs.{funcstr}`

Examples
--------
{examples}
"""


def make_binop_docstring(funcstr):
    sym = {
        "ge": ">=",
        "gt": ">",
        "le": "<=",
        "lt": "<",
        "eq": "==",
        "ne": "!=",
        "add": "+",
        "subtract": "-",
        "multiply": "*",
        "divide": "/",
        "radd": "+",
        "rsubtract": "-",
        "rmultiply": "*",
        "rdivide": "/",
    }[funcstr]

    rop = funcstr in ("radd", "rsubtract", "rmultiply", "rdivide")
    if rop:
        equiv = f"*other* {sym} *self*"
    else:
        equiv = f"*self* {sym} *other*"
    return _extension_array_binop.format(
        funcstr=funcstr,
        equiv=equiv,
        examples=_make_extension_array_example(sym, rop),
    )


negate_docstring = """
Unary operator for :class:`staircase.StairsArray` (and :class:`pandas.Series` with "Stairs" dtype).

Equivalent to -*self*.

Returns
-------
:class:`staircase.StairsArray`

See Also
---------
:meth:`staircase.Stairs.negate`

Examples
--------

>>> arr = sc.StairsArray([s1, s2])

.. plot::
    :context: close-figs
    :include-source: False

    >>> arr = sc.StairsArray([s1, s2])
    >>> fig, axes = plt.subplots(nrows=1, ncols=2,  figsize=(7,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ["arr[0]", "arr[1]"], arr):
    ...     stair_instance.plot(ax=ax, arrows=True)
    ...     ax.set_title(title)

>>> result = -arr

.. plot::
    :context: close-figs
    :include-source: False

    >>> arr = sc.StairsArray([s1, s2])
    >>> result = -arr
    >>> fig, axes = plt.subplots(nrows=1, ncols=2,  figsize=(7,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, ["result[0]", "result[1]"], result):
    ...     stair_instance.plot(ax=ax, arrows=True)
    ...     ax.set_title(title)
"""
