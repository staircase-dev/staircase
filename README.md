<p align="center"><a href="https://github.com/venaturum/staircase"><img src="https://github.com/venaturum/staircase/blob/master/docs/img/staircase.png?raw=true" title="staircase logo" alt="staircase logo"></a></p>


<p align="center">
	<a href="https://pepy.tech/project/staircase/" alt="PyPI downloads">
        <img src="https://pepy.tech/badge/staircase" /></a>
    <a href="https://www.python.org/" alt="Python version">
        <img src="https://img.shields.io/pypi/pyversions/staircase" /></a>
    <a href="https://pypi.org/project/staircase/" alt="PyPI version">
        <img src="https://img.shields.io/pypi/v/staircase" /></a>
    <a href="https://anaconda.org/conda-forge/staircase" alt="Conda Forge version">
        <img src="https://anaconda.org/conda-forge/staircase/badges/version.svg?branch=master&kill_cache=1" /></a>
    <a href="https://staircase.mit-license.org/" alt="License">
        <img src="http://img.shields.io/:license-mit-blue.svg?style=flat-square"></a>
</p>
<p align="center">
	<a href="https://travis-ci.com/github/venaturum/staircase" alt"Travis CI">
		<img src="https://travis-ci.com/venaturum/staircase.svg"/></a>
    <a href="https://railing.readthedocs.io/en/latest/" alt="Read the Docs">
        <img src="https://readthedocs.org/projects/railing/badge/?version=latest" /></a>
	<a href="https://www.codacy.com/gh/venaturum/staircase/dashboard" alt="Codacy Grade">
        <img src="https://app.codacy.com/project/badge/Grade/04eb9240feec4b4e95b20b96d060d38c" /></a>	
	<a href="https://codecov.io/gh/venaturum/staircase"  alt="Codecov coverage">
		<img src="https://codecov.io/gh/venaturum/staircase/branch/master/graph/badge.svg"/></a>
</p>
<p align="center">
	<a href="https://mybinder.org/v2/gh/venaturum/staircase/master?filepath=docs%2Fexamples" alt="Binder">
        <img src="https://mybinder.org/badge_logo.svg" /></a>	
	<a href="https://colab.research.google.com/github/venaturum/staircase/blob/master/docs/examples/Index.ipynb" alt="Colab">
        <img src="https://colab.research.google.com/assets/colab-badge.svg" /></a>		
</p>

The leading use-case for the staircase package is for the creation and analysis of step functions.

Pretty exciting huh.

But don't hit the close button on the browser just yet.  Let us convince you that much of the world around you can be modelled as step functions.

For example, the number of users viewing this page over time can be modelled as a step function.  The value of the function increases by 1 every time a user arrives at the page, and decreases by 1 every time a user leaves the page.  Let's say we have this data in vector format (i.e. tuple, list, numpy array, pandas series).  Specifically, assume *arrive* and *leave* are vectors of times, expressed as minutes past midnight, for all page views occuring yesterday.  Creating the corresponding step function is simple.  To achieve it we use the *[Stairs](https://railing.readthedocs.io/en/latest/Stairs.html)* class:

```python
>>> import staircase as sc

>>> views = sc.Stairs()
>>> views.layer(arrive,leave)
```

We can visualise the function with the plot function:
```python
>>> views.plot()
```
<p align="left"><img src="https://github.com/venaturum/staircase/blob/master/docs/img/pageviews.png?raw=true" title="pageviews example" alt="pageviews example"></p>

We can find the total time in minutes the page was viewed:
```python
>>> views.integrate(0,1440)
9297.94622521079
```

We can find the average number of viewers:
```python
>>> views.mean(0,1440)
6.4569071008408265
```

We can find the average number of viewers, per hour of the day, and plot:
```python
>>> pd.Series([views.mean(60*i, 60*(i+1)) for i in range(24)]).plot()
```
<p align="left"><img src="https://github.com/venaturum/staircase/blob/master/docs/img/meanperhour.png?raw=true" title="mean page views per hour" alt="mean page views per hour"></p>

We can find the maximum concurrent views:
```python
>>> views.max(0,1440)
16
```

We can create histogram data showing relative frequency of concurrent viewers (and plot it):
```python
>>> views.hist(0,1440).plot.bar()
```
<p align="left"><img src="https://github.com/venaturum/staircase/blob/master/docs/img/pageviewshist.png?raw=true" title="concurrent viewers histogram" alt="concurrent viewers histogram"></p>


Plotting is based on [matplotlib](https://matplotlib.org) and it requires relatively little effort to take the previous chart and improve the aesthetics:
<p align="left"><img src="https://github.com/venaturum/staircase/blob/master/docs/img/pageviewshistpretty.png?raw=true" title="concurrent viewers histogram (aesthetic)" alt="concurrent viewers histogram (aesthetic)"></p>


There is plenty more analysis that could be done.  The staircase package provides a rich variety of [arithmetic operations](https://railing.readthedocs.io/en/latest/Stairs.html#arithmetic-operators), [relational operations](https://railing.readthedocs.io/en/latest/Stairs.html#relational-operators), [logical operations](https://railing.readthedocs.io/en/latest/Stairs.html#logical-operators), [statistical operations](https://railing.readthedocs.io/en/latest/Stairs.html#statistical-operators), for use with *Stairs*, in addition to functions for [univariate analysis](https://railing.readthedocs.io/en/latest/Stairs.html#summary-statistics), [aggregations](https://railing.readthedocs.io/en/latest/module_funcs.html) and compatibility with [pandas.Timestamp](https://pandas.pydata.org/pandas-docs/latest/reference/api/pandas.Timestamp.html).


## Installation

Staircase can be installed from PyPI:

```bash
python -m pip install staircase
```

or also with conda:

```bash
conda install -c conda-forge staircase
```

## Documentation
The complete guide to using staircase can be found at [Read the Docs](https://railing.readthedocs.io/en/latest/index.html)


## Need help?
Post your question on [Stack Overflow](https://stackoverflow.com/) and use the tag **staircase**.


## Contributing
There are many ways in which contributions can be made - the first and foremost being *using staircase and giving feedback*.

Bug reports, feature requests and ideas can be submitted via the [Github issue tracker](https://github.com/venaturum/staircase/issues).

Additionally, bug fixes. enhancements, and improvements to the code and documentation are also appreciated and can be done via pull requests.
Take a look at the current issues and if there is one you would like to work on please leave a comment to that effect.

See this [beginner's guide to contributing](https://github.com/firstcontributions/first-contributions), or [Pandas' guide to contributing](https://pandas.pydata.org/pandas-docs/stable/development/contributing.html), to learn more about the process.


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/venaturum/staircase/tags). 


## License

This project is licensed under the MIT License - see the [LICENSE](https://staircase.mit-license.org/) file for details

## Acknowledgments

* This project is heavily reliant on [sorted containers](http://www.grantjenks.com/docs/sortedcontainers/).  Grant Jenks has done a great job bringing this functionality to Python at lightning fast speeds.
* staircase began development from within the Hunter Valley Coal Chain Coordinator.  Thanks for the support!