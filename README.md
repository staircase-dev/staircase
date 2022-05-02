<p align="center"><a href="https://github.com/staircase-dev/staircase"><img src="https://github.com/staircase-dev/staircase/blob/master/docs/img/staircase2.png?raw=true" title="staircase logo" alt="staircase logo"></a></p>


<p align="center">
	<a href="https://pepy.tech/project/staircase/" alt="PyPI downloads">
        <img src="https://pepy.tech/badge/staircase" /></a>
    <a href="https://www.python.org/" alt="Python version">
        <img src="https://img.shields.io/pypi/pyversions/staircase" /></a>
    <a href="https://pypi.org/project/staircase/" alt="PyPI version">
        <img src="https://img.shields.io/pypi/v/staircase" /></a>
    <a href="https://anaconda.org/conda-forge/staircase" alt="Conda Forge version">
        <img src="https://anaconda.org/conda-forge/staircase/badges/version.svg?branch=master&kill_cache=1" /></a>
    <a href="https://github.com/staircase-dev/staircase/blob/master/LICENSE" alt="License">
        <img src="http://img.shields.io/:license-mit-blue.svg?style=flat-square"></a>
</p>
<p align="center">
	<a href="https://github.com/staircase-dev/staircase/actions/workflows/ci.yml" alt"Github CI">
		<img src="https://github.com/staircase-dev/staircase/actions/workflows/ci.yml/badge.svg"/></a>
    <a href="https://www.staircase.dev/en/latest/" alt="Documentation">
        <img src="https://readthedocs.org/projects/railing/badge/?version=latest" /></a>
	<a href="https://app.codacy.com/gh/staircase-dev/staircase/dashboard" alt="Codacy Grade">
        <img src="https://app.codacy.com/project/badge/Grade/845ecfb2fd6748cc87a66f9a97cd9492" /></a>	
	<a href="https://app.codecov.io/gh/staircase-dev/staircase"  alt="Codecov coverage">
		<img src="https://codecov.io/gh/staircase-dev/staircase/branch/master/graph/badge.svg"/></a>
</p>

The staircase package enables data analysis through mathematical step functions. Step functions can be used to represent continuous time series - think changes in state over time, queue size over time, utilisation over time, success rates over time etc.

The package is built upon `numpy` and `pandas`, with a deliberate, stylistic alignment to the latter in order to integrate seamlessly into the [pandas ecosystem](https://pandas.pydata.org/docs/ecosystem.html).

The staircase package makes converting raw, temporal data into time series easy and readable. Furthermore there is a rich variety of [arithmetic operations](https://www.staircase.dev/en/latest/reference/Stairs.html#arithmetic-operators), [relational operations](https://www.staircase.dev/en/latest/reference/Stairs.html#relational-operators), [logical operations](https://www.staircase.dev/en/latest/reference/Stairs.html#logical-operators), [statistical operations](https://www.staircase.dev/en/latest/reference/Stairs.html#statistical-operators), to enable analysis, in addition to functions for [univariate analysis](https://www.staircase.dev/en/latest/reference/Stairs.html#summary-statistics), [aggregations](https://www.staircase.dev/en/latest/reference/arrays.html#aggregation) and compatibility with datetimes.

**New in 2022:** staircase now provides support for [pandas extension arrays](https://pandas.pydata.org/docs/ecosystem.html#extension-data-types) and a [Series accessor](https://www.staircase.dev/en/latest/user_guide/arraymethods.html).


## An example

In this example, we consider data corresponding to site views for a website in October 2021.  The start and end times have been logged for each session, in addition to one of three countries codes (AU, UK, US).  These times are recorded with `pandas.Timestamp` and any time which falls outside of October is logged as `NAT`.


```python
>>> data
                       start                   end   country
0                        NaT   2021-10-01 00:00:50        AU
1                        NaT   2021-10-01 00:07:45        AU
2                        NaT   2021-10-01 00:05:58        AU
3                        NaT   2021-10-01 00:08:48        AU
4                        NaT   2021-10-01 00:05:26        AU
...                      ...                   ...       ...
425728   2021-10-31 23:57:16                   NaT        US
425729   2021-10-31 23:57:25                   NaT        US
425730   2021-10-31 23:58:59                   NaT        US
425731   2021-10-31 23:59:45                   NaT        US
425732   2021-10-31 23:59:59                   NaT        US
```

Note that the number of users viewing the site over time can be modelled as a step function.  The value of the function increases by 1 every time a user arrives at the site, and decreases by 1 every time a user leaves the site.  This step function can be thought of as the sum of three step functions: AU users + UK users + US users.  Creating a step function for AU users, for example, is simple.  To achieve it we use the *[Stairs](https://www.staircase.dev/en/latest/reference/Stairs.html)* class, which represents a step function:


```python
>>> import staircase as sc

>>> views_AU = sc.Stairs(data.query("country == 'AU'"), "start", "end")
>>> views_AU
<staircase.Stairs, id=1609972469384>
```

We can visualise the function with the plot function:
```python
>>> views_AU.plot()
```

<p align="left"><img src="https://github.com/staircase-dev/staircase/blob/master/docs/img/AU_views.png?raw=true" title="AU views example" alt="AU views example"></p>

Rather than creating a separate variable for each country, we can create a `pandas.Series` to hold a step function for each country.  We can even give this Series a "Stairs" type.

```python
>>> october = (pd.Timestamp("2021-10"), pd.Timestamp("2021-11"))
>>> series_stepfunctions = (
...     data.groupby("country")
...     .apply(sc.Stairs, "start", "end")
...     .apply(sc.Stairs.clip, october)  # set step functions to be undefined outside of October
...     .astype("Stairs")
... )
>>> series_stepfunctions
country
AU    <staircase.Stairs, id=2516367680328>
UK    <staircase.Stairs, id=2516362550664>
US    <staircase.Stairs, id=2516363585928>
dtype: Stairs
```

The plotting backend to `staircase` is provided by `matplotlib`.

```python
>>> import matplotlib.pyplot as plt
>>> _, ax = plt.subplots(figsize=(15,4))
>>> series_stepfunctions.sc.plot(ax, alpha=0.7)
>>> ax.legend()
```
<p align="left"><img src="https://github.com/staircase-dev/staircase/blob/master/docs/img/all_views.png?raw=true" title="all views example" alt="all views example"></p>

Now plotting step functions is useful, but the real fun starts when we go beyond this:

<p align="left"><img src="https://github.com/staircase-dev/staircase/blob/master/docs/img/staircase_analysis.gif?raw=true" title="staircase analysis examples" alt="staircase analysis examples"></p>


## Installation

staircase can be installed from PyPI:

```bash
python -m pip install staircase
```

or also with conda:

```bash
conda install -c conda-forge staircase
```

## Documentation
The complete guide to using staircase can be found at [staircase.dev](https://www.staircase.dev)

## Contributing
There are many ways in which contributions can be made - the first and foremost being *using staircase and giving feedback*.

Bug reports, feature requests and ideas can be submitted via the [Github issue tracker](https://github.com/staircase-dev/staircase/issues).

Additionally, bug fixes. enhancements, and improvements to the code and documentation are also appreciated and can be done via pull requests.
Take a look at the current issues and if there is one you would like to work on please leave a comment to that effect.

See this [beginner's guide to contributing](https://github.com/firstcontributions/first-contributions), or [Pandas' guide to contributing](https://pandas.pydata.org/pandas-docs/stable/development/contributing.html), to learn more about the process.


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/staircase-dev/staircase/tags).  It is highly recommended to use staircase 2.*, for both performance and additional features.


## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/staircase-dev/staircase/blob/master/LICENSE) file for details

## Acknowledgments

The seeds of *staircase* began developing at the Hunter Valley Coal Chain Coordinator, where it finds strong application in analysing simulated data.  Thanks for the support!
