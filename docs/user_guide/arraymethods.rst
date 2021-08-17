.. _user_guide.arraymethods:


Array methods
==========================

There are plenty of binary operations in :mod:`staircase`.  These are ones which operate on two step functions to produce a result.  There are occasions however where we want to perform an operation on several step functions.  There is typically two cases that this arises:

1) We want to perform separate operations on multiple step functions, with a common parameter.  This could include sampling the collection of step functions with a common set of points, or plotting each step function in a collection to the same :class:`matplotlib.axes.Axes` instance.

2) We want to perform a single operation which acts upon a collection of step functions, such as creating an average step function, or calculating a co-variance matrix.

Currently the following array methods are defined in :mod:`staircase`:

- :func:`staircase.sum`
- :func:`staircase.mean`
- :func:`staircase.median`
- :func:`staircase.min`
- :func:`staircase.max`
- :func:`staircase.agg`
- :func:`staircase.sample`
- :func:`staircase.limit`
- :func:`staircase.cov`
- :func:`staircase.corr`

Note that equivalent calculations using python built-in methods, or :class:`pandas.Series` methods can sometimes be possible.  For example:

.. ipython:: python
    :suppress:
    
    import staircase as sc
    import pandas as pd
    from matplotlib.dates import YearLocator

    def sml(axes):
        for ax in axes:
            ax.xaxis.set_major_locator(YearLocator());


.. ipython:: python
    
    df = sc.make_test_data(groups=["a", "b", "c"])
    a = sc.Stairs(df.query("group == 'a'"), "start", "end");
    b = sc.Stairs(df.query("group == 'b'"), "start", "end");
    c = sc.Stairs(df.query("group == 'c'"), "start", "end");

    fig, axes = plt.subplots(ncols=3, figsize=(8,3), sharey=True, tight_layout=True);
    @suppress
    sml(axes); 
    sum([a,b,c]).plot(axes[0]);
    axes[0].set_title("sum([a,b,c])");
    pd.Series([a,b,c]).sum().plot(axes[1]);
    axes[1].set_title("pd.Series([a,b,c]).sum()");
    sc.sum([a,b,c]).plot(axes[2]);
    @savefig user_guide_array_methods.png
    axes[2].set_title("sc.sum([a,b,c])");


In the example above, the non-staircase methods work by leveraging the fact that the :class:`staircase.Stairs` class has an *add* operation, which is applied iteratively.  It should be not surprising that the corresponding function in staircase, which operates on the entire collection at once, is faster and more memory efficient.  Also be aware that some methods, such as `max([a,b,c])`, may superficially appear to work since a :class:`staircase.Stairs` instance is returned but the result is not what is expected.


