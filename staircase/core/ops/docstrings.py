_symbol_map = {
    "addition": "+",
    "subtraction": "-",
    "multiplication": r"*",
    "division": "/",
    "lt": "<",
    "le": "<=",
    "gt": ">",
    "ge": ">=",
    "eq": "==",
    "ne": "!=",
    "and": "&",
    "or": "|",
    "xor": "^",
    "negate": "-",
    "invert": "~",
    "raddition": "+",
    "rsubtraction": "-",
    "rmultiplication": r"*",
    "rdivision": "/",
    "rand": "&",
    "ror": "|",
    "rxor": "^",
}

_see_also_map = {
    "addition": "Stairs.subtract, Stairs.radd",
    "subtraction": "Stairs.add, Stairs.rsubtract",
    "multiplication": "Stairs.divide, Stairs.rmultiply",
    "division": "Stairs.multiply, Stairs.rdivide",
    "lt": "Stairs.gt, Stairs.le, Stairs.ge",
    "le": "Stairs.lt, Stairs.gt, Stairs.ge",
    "gt": "Stairs.lt, Stairs.le, Stairs.ge",
    "ge": "Stairs.lt, Stairs.gt, Stairs.le",
    "eq": "Stairs.ne, Stairs.identical",
    "ne": "Stairs.eq, Stairs.identical",
    "and": "Stairs.logical_or, Stairs.logical_rand",
    "or": "Stairs.logical_and, Stairs.logical_xor, Stairs.logical_ror",
    "xor": "Stairs.logical_or, Stairs.logical_rxor",
    "negate": "Stairs.subtract",
    "make_boolean": "Stairs.invert",
    "invert": "Stairs.make_boolean",
    "raddition": "Stairs.rsubtract, Stairs.add",
    "rsubtraction": "Stairs.radd, Stairs.subtract",
    "rmultiplication": "Stairs.rdivide, Stairs.multiply",
    "rdivision": "Stairs.rmultiply, Stairs.divide",
    "rand": "Stairs.logical_ror, Stairs.logical_and",
    "ror": "Stairs.logical_rand, Stairs.logical_or",
    "rxor": "Stairs.logical_ror, Stairs.logical_xor",
}

_relationship_map = {
    "lt": "strictly less than",
    "le": "less than, or equal to,",
    "gt": "strictly greater than",
    "ge": "greater than, or equal to,",
    "eq": "equal to",
    "ne": "not equal to",
}

_plot_titles_map = {
    "addition": ["s1", "s2", "s1+s2"],
    "subtraction": ["s1", "s2", "s1-s2"],
    "multiplication": ["s1", "s2", "s1*s2"],
    "division": ["s1", "s2", "s1/(s2+2)"],
    "lt": ["s1", "s2", "s1<s2"],
    "le": ["s1", "s2", "s1<=s2"],
    "gt": ["s1", "s2", "s1>s2"],
    "ge": ["s1", "s2", "s1>=s2"],
    "eq": ["s1", "s2", "s1==s2"],
    "ne": ["s1", "s2", "s1!=s2"],
    "and": ["s1", "s2", "s1&s2"],
    "or": ["s1", "s2", "s1|s2"],
    "xor": ["s1", "s2", "s1^s2"],
    "invert": ["s2", "~s2"],
    "make_boolean": ["s2", "s2.make_boolean()"],
    "negate": ["s1", "-s1"],
    "raddition": ["s1", "2+s1"],
    "rsubtraction": ["s1", "2-s1"],
    "rmultiplication": ["s1", "2*s1"],
    "rdivision": ["s1", "1/(s1+2)"],
    "rand": ["s1", "s2", "s2&s1"],
    "ror": ["s1", "s2", "s2|s1"],
    "rxor": ["s1", "s2", "s2^s1"],
}

_example = """
.. plot::
    :context: close-figs
    :include-source: False

    {setup}
    >>> stair_list = [{plots}]
    >>> fig, axes = plt.subplots(nrows=1, ncols={ncols},  figsize=({width},3), sharey=True, sharex=True, tight_layout=True, dpi=400)
    >>> for ax, title, stair_instance in zip(axes, {plot_titles}, stair_list):
    ...     stair_instance.plot(ax=ax, arrows=True)
    ...     ax.set_title(title)
"""


def _gen_example(plot_titles, setup=""):
    # plot_titles is a list of strings
    ncols = len(plot_titles)
    plots = ", ".join(plot_titles)
    return _example.format(
        plots=plots,
        ncols=ncols,
        plot_titles=plot_titles,
        setup=setup,
        width=ncols + 5,
    )


_arithmetic_binop_docstring_header = """
A binary operator facilitating the {operation} of step functions (and floats).
"""

_logical_binop_docstring_header = """
Returns a boolean-valued step function indicating where *self* {operation} *other* are non-zero.
"""

_relational_binop_docstring_header = """
Returns a boolean-valued step function indicating where *self* is {relationship} *other*.
"""

_negate_header = """
An operator which produces a new Stairs instance representing the multiplication of the step function by -1.
"""

_invert_header = """
Returns a boolean-valued step function indicating where *self* is zero-valued.
"""

_common_docstring = """
Equivalent to {op_string}.  See examples below.
{params}
Returns
-------
:class:`Stairs`
     new instance representing the result of {op_string}

See Also
--------
{{see_also}}

Examples
--------
{{example}}
"""

params = """
Parameters
----------
other :  int, float, or :class:`Stairs`
"""
_common_unop_docstring = _common_docstring.format(
    op_string=r"{symbol}\ *self*", params="\n"
)
_common_binop_docstring = _common_docstring.format(
    op_string="*self* {symbol} *other*", params="\n".join([" ", params, " "])
)
_common_rbinop_docstring = _common_docstring.format(
    op_string="*other* {symbol} *self*", params="\n".join([" ", params, " "])
)

_arithmetic_binops = ("addition", "subtraction", "multiplication", "division")
_arithmetic_rbinops = ("raddition", "rsubtraction", "rmultiplication", "rdivision")
_relational_binops = ("lt", "le", "gt", "ge", "eq", "ne")
_logical_binops = {"and", "or", "xor"}
_logical_rbinops = {"rand", "ror", "rxor"}


def _get_header(operation):
    if operation in _arithmetic_binops:
        result = _arithmetic_binop_docstring_header.format(operation=operation)
        return result
    if operation in _arithmetic_rbinops:
        result = _arithmetic_binop_docstring_header.format(operation=operation[1:])
        return result
    if operation in _relational_binops:
        relationship = _relationship_map[operation]
        return _relational_binop_docstring_header.format(relationship=relationship)
    if operation in _logical_binops:
        return _logical_binop_docstring_header.format(operation=operation)
    if operation in _logical_rbinops:
        return _logical_binop_docstring_header.format(operation=operation[1:])
    if operation == "negate":
        return _negate_header
    if operation == "invert":
        return _invert_header


def _gen_op_docstring(operation):
    symbol = _symbol_map[operation]
    see_also = _see_also_map[operation]
    example = _gen_example(_plot_titles_map[operation])

    header = _get_header(operation)
    if operation in ("negate", "invert"):
        body = _common_unop_docstring
    elif operation in (
        "raddition",
        "rsubtraction",
        "rmultiplication",
        "rdivision",
        "rand",
        "ror",
        "rxor",
    ):
        body = _common_rbinop_docstring
    else:
        body = _common_binop_docstring
    docstring = header + body
    return docstring.format(
        symbol=symbol,
        see_also=see_also,
        example=example,
    )


add_docstring = _gen_op_docstring("addition")
subtract_docstring = _gen_op_docstring("subtraction")
multiply_docstring = _gen_op_docstring("multiplication")
divide_docstring = _gen_op_docstring("division")
negate_docstring = _gen_op_docstring("negate")
lt_docstring = _gen_op_docstring("lt")
le_docstring = _gen_op_docstring("le")
gt_docstring = _gen_op_docstring("gt")
ge_docstring = _gen_op_docstring("ge")
eq_docstring = _gen_op_docstring("eq")
ne_docstring = _gen_op_docstring("ne")
logical_and_docstring = _gen_op_docstring("and")
logical_or_docstring = _gen_op_docstring("or")
logical_xor_docstring = _gen_op_docstring("xor")
invert_docstring = _gen_op_docstring("invert")
radd_docstring = _gen_op_docstring("raddition")
rsubtract_docstring = _gen_op_docstring("rsubtraction")
rmultiply_docstring = _gen_op_docstring("rmultiplication")
rdivide_docstring = _gen_op_docstring("rdivision")
logical_rand_docstring = _gen_op_docstring("rand")
logical_ror_docstring = _gen_op_docstring("ror")
logical_rxor_docstring = _gen_op_docstring("rxor")


identical_docstring = """
Returns True if *self* and *other* represent the same step functions.

Returns
-------
boolean

See Also
--------
Stairs.eq, Stairs.ne

Examples
--------

>>> s1.identical(s1)
True
>>> s1.identical(s1.copy())
True
>>> s1.identical(s1.copy().layer(1,2))
False
"""

_make_boolean_docstring_body = """
Returns a boolean-valued step function indicating where *self* is non-zero.

Returns
-------
:class:`Stairs`
    A new instance representing where *self* is non-zero

See Also
--------
Stairs.invert

Examples
--------
"""

make_boolean_docstring = _make_boolean_docstring_body + _gen_example(
    ["s2", "s2.make_boolean()"]
)


clip_docstring = """
Returns a copy of *self* which is zero-valued everywhere outside of [lower, upper]

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

Examples
--------

{plot}
>>> s1.clip(2,4).mean()
0.5
""".format(
    plot=_gen_example(["s1", "s1.clip(2,4)"])
)

# _mask_where_2_col_example = """
# .. plot::
#     :context: close-figs

#     >>> masker = {masker}
#     >>> stairs_list = [s2, s2.{func}(masker)]
#     >>> fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(6,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
#     >>> for ax, title, stair_instance in zip(axes, ("s2", "s2.{func}(masker)"), stairs_list):
#     ...     stair_instance.plot(ax=ax)
#     ...     ax.set_title(title)
# """

# _mask_where_3_col_example = """
# .. plot::
#     :context: close-figs

#     >>> masker = {masker}
#     >>> stairs_list = [s2, masker, s2.{func}(masker)]
#     >>> fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(8,3), sharey=True, sharex=True, tight_layout=True, dpi=400)
#     >>> for ax, title, stair_instance in zip(axes, ("s2", "masker", "s2.{func}(masker)"), stairs_list):
#     ...     stair_instance.plot(ax=ax)
#     ...     ax.set_title(title)
# """

# mask_examples = f"""

# {_mask_where_2_col_example.format(masker="(2,4)", func="mask")}

# {_mask_where_3_col_example.format(masker="sc.Stairs(initial_value=2).layer(1,2,-1).layer(4,5,-2)", func="where")}
# """

# where_examples = f"""

# {_mask_where_2_col_example.format(masker="(1,4)", func="where")}

# {_mask_where_3_col_example.format(masker="sc.Stairs().layer(1,2).layer(4,5,-2)", func="where")}
# """

mask_examples = "\n".join(
    [
        _gen_example(["s2", "s2.mask((2,4))"], ">>> masker = (2,4)"),
        _gen_example(
            ["s2", "masker", "s2.mask(masker)"],
            ">>> masker = sc.Stairs(initial_value=2).layer(1,2,-2).layer(4,5,-2)",
        ),
    ]
)

where_examples = "\n".join(
    [
        _gen_example(["s2", "s2.where((1,4))"], ">>> masker = (1,4)"),
        _gen_example(
            ["s2", "masker", "s2.where(masker)"],
            ">>> masker = sc.Stairs().layer(1,2).layer(4,5,-2)",
        ),
    ]
)

_mask_where_docstring = """
Returns a new step function where *self* has been {operation} by *other*.

Note when *other* is as Stairs instance, is is considered equivalent to its
boolean value, that is, the result of :meth:`Stairs.make_boolean`.  As a result any part
of the domain where *other* is {value}, or not defined, will be undefined in the resulting
step function.

Also note that ``.{func}((a,b))`` is equivalent to ``.{func}(sc.Stairs().layer(a,b))`` but defers
to a faster implementation.

Parameters
----------
other : :class:`Stairs`, or tuple
    If *other* is a tuple *(a,b)* then it is assumed that a < b and that
    *a* and *b* both belong to the domain of the step function represented by *self*

Returns
-------
:class:`Stairs`

See Also
--------
{see_also}

Examples
--------
{examples}
"""

mask_docstring = _mask_where_docstring.format(
    operation="masked",
    value="zero-valued",
    func="mask",
    examples=mask_examples,
    see_also="Stairs.where",
)

where_docstring = _mask_where_docstring.format(
    operation="'inversely masked'",
    value="not zero-valued",
    func="where",
    examples=where_examples,
    see_also="Stairs.mask, Stairs.clip",
)


_isna_notna_docstring = """
Returns a new 'boolean valued' step function indicating where the
domain of *self* is not defined.

The value of the step function is {def_value} where *self* is defined, and {not_def_value} where
*self* is not defined.

Returns
-------
:class:`Stairs`

See Also
--------
{see_also}

Examples
--------
{examples}
"""

isna_docstring = _isna_notna_docstring.format(
    def_value=0,
    not_def_value=1,
    see_also="Stairs.notna",
    examples=_gen_example(["s3", "s3.isna()"]),
)
notna_docstring = _isna_notna_docstring.format(
    def_value=1,
    not_def_value=0,
    see_also="Stairs.isna",
    examples=_gen_example(["s3", "s3.notna()"]),
)

fillna_examples = "\n".join(
    [
        _gen_example(["s3", "s3.fillna(0.5)"]),
        _gen_example(["s3", 's3.fillna("ffill")']),
        _gen_example(["s3", 's3.fillna("bfill")']),
    ]
)

fillna_docstring = """
Define values for (a copy of) *self* where it is undefined.

Parameters
----------
value : {{int, float, "backfill", "bfill", "pad", "ffill"}}
    If *value* is and int or float, then it is used to provide values
    where *self* is undefined.  If *value* is a string then it indicates
    a method for propagating values of the step function across undefined
    intervals:

    - ``pad / ffill`` propagate last defined value forward
    - ``backfill / bfill`` propagate next defined value backward

Returns
-------
:class:`Stairs`

See Also
--------
Stairs.isna

Examples
--------
{examples}
""".format(
    examples=fillna_examples
)
