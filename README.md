<p align="center"><a href="https://github.com/venaturum/staircase"><img src="https://github.com/venaturum/staircase/blob/master/docs/img/staircase.png?raw=true" title="staircase logo" alt="staircase logo"></a></p>

[![Python version](https://img.shields.io/pypi/pyversions/staircase)](https://www.python.org/)
[![PyPI version](https://img.shields.io/pypi/v/staircase)](https://pypi.org/project/staircase/)
[![Conda version](https://img.shields.io/conda/v/venaturum/staircase)](https://anaconda.org/venaturum/staircase)
[![Read The Docs](https://readthedocs.org/projects/railing/badge/?version=latest)](https://railing.readthedocs.io/en/latest/?badge=latest) 
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://staircase.mit-license.org/) 


Description goes here:

```python
import staircase as sc

st = (sc.Stairs()
    .layer(1,3)
    .layer(2,5,2)
)
st.plot()
print(f'mean over 0,6 is {st.mean()}
```

### Installation

Staircase can be installed from PyPI:

```bash
pip install staircase
```

or also with conda:

```bash
conda install -c venaturum staircase
```

## Documentation
The complete guide to using staircase can be found at [Read the Docs](https://railing.readthedocs.io/en/latest/)


## Contributing

Please stay tuned for how you can contribute...


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/venaturum/staircase/tags). 


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* This project is heavily reliant on [sorted containers](http://www.grantjenks.com/docs/sortedcontainers/).  Grant Jenks has done a great job bringing this functionality to Python at lightning fast speeds.
* staircase began development from within the Hunter Valley Coal Chain Coordinator.  Thanks for the support!