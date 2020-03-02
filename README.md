<p align="center"><a href="https://github.com/venaturum/staircase"><img src="https://github.com/venaturum/staircase/blob/master/docs/img/staircase.png?raw=true" title="staircase logo" alt="staircase logo"></a></p>

<p align="center">
[![Python version](https://images1-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url=https://img.shields.io/pypi/pyversions/staircase)](https://www.python.org/)
[![PyPI version](https://images1-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url=https://img.shields.io/pypi/v/staircase)](https://pypi.org/project/staircase/)
[![Conda version](https://images1-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url=https://img.shields.io/conda/v/venaturum/staircase)](https://anaconda.org/venaturum/staircase)
[![Read The Docs](https://images1-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url=https://readthedocs.org/projects/railing/badge/?version=latest)](https://railing.readthedocs.io/en/latest/?badge=latest) 
[![License](https://images1-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url=http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://staircase.mit-license.org/) 
</p>

The leading use-case for the staircase package is for the creation and analysis of step functions.

Pretty exciting huh.

But don't hit the close button on the browser just yet.  Let us convince you that much of the world around you can be modelled as step functions.

For example, the number of users viewing this page over time can be modelled as a step function.  The value of the function increases by 1 every time a user arrives at the page, and decreases by 1 every time a user leaves the page.  Let's say we have this data in vector format (i.e. tuple, list, numpy array, pandas series).  Specifically, assume *arrive* and *leave* are vectors of times, expressed as minutes past midnight, for all page views occuring yesterday.  Creating the corresponding step function is simple.  To achieve it we use the *[Stairs](https://railing.readthedocs.io/en/latest/Stairs.html)* class:

```python
import staircase as sc

views = sc.Stairs()
views.layer(arrive,leave)
```

We can visualise the function with the plot function:
```python
views.plot()
```
<p align="left"><img src="docs/img/pageviews.png?raw=true" title="pageviews example" alt="pageviews example"></p>

We can find the total time the page was viewed:
```python
views.integrate(0,1440)
```

We can find the average number of viewers:
```python
views.mean(0,1440)
```

We can find the average number of viewers for each hour of the day:
```python
[views.mean(60*i, 60*(i+1)) for i in range(24)]
```

We can find the maximum concurrent views:
```python
views.max(0,1440)
```

There is plenty more analysis that could be done.  The staircase package provides a rich variety of [arithmetic operations](https://railing.readthedocs.io/en/latest/Stairs.html#arithmetic-operators), [relational operations](https://railing.readthedocs.io/en/latest/Stairs.html#relational-operators), [logical operations](https://railing.readthedocs.io/en/latest/Stairs.html#logical-operators), for use with *Stairs*, in addition to functions for [univariate analysis](https://railing.readthedocs.io/en/latest/Stairs.html#summary-statistics), [aggregations](https://railing.readthedocs.io/en/latest/multi_stair.html) and compatibility with [pandas.Timestamp](https://railing.readthedocs.io/en/latest/multi_stair.html).


## Installation

Staircase can be installed from PyPI:

```bash
pip install staircase
```

or also with conda:

```bash
conda install -c venaturum staircase
```

## Documentation
The complete guide to using staircase can be found at [Read the Docs](https://railing.readthedocs.io/en/latest/index.html)


## Contributing

Please stay tuned for how you can contribute...


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/venaturum/staircase/tags). 


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* This project is heavily reliant on [sorted containers](http://www.grantjenks.com/docs/sortedcontainers/).  Grant Jenks has done a great job bringing this functionality to Python at lightning fast speeds.
* staircase began development from within the Hunter Valley Coal Chain Coordinator.  Thanks for the support!