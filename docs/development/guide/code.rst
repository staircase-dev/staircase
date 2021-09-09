.. _development.code:


Contributing to the code
======================================

The process
*****************************

The process for contributing the code is almost identical to that described in the `pandas guide to contributing <https://pandas.pydata.org/docs/development/contributing.html#working-with-the-code>`_ and we refer users there.

Note that if you are using Poetry then updates from upstream repositories may contain changes to *poetry.lock*.  This becomes more and more likely as time passes.  If the incoming commits do contain changes to *poetry.lock* then this reflects a change to the development environment.  To ensure consistency with all developers you will need to run `poetry install` from the command line, in the root of the project, in order to update your environment.


Coding standards
*****************************

Good code is important, as is style.  A style guide for Python was laid out in `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ which staircase conforms to.  A consistent code format aligning to this style is enforced in staircase using `Black <https://black.readthedocs.io/en/stable/>`_ and ` `Flake8 <https://flake8.pycqa.org/en/latest/>`_.  If you setup your development environment using :ref:`development.environment_poetry` then you will already have Black and Flake8 installed.

The most useful application of these tools is through an IDE, such as VS Code, which applies them as you code (or save changes).  Setup instructions for :ref:`development.environment_vscode` are provided.

Additionally, by setting up :ref:`development.environment_precommit` (which is strongly encouraged), these tools can be applied automatically at the time of creating local commits.  They are also applied by automated pipelines when pushing changes to remote repositories or creating merge requests.

Lastly, these tools can be run from the command line, in the project root directory (assuming they have been installed into the active environment)::

    black staircase
    git diff upstream/master -u -- "*.py" | flake8 --diff


For those wanting to improve their coding style these three resources are recommended:

1) The Code Style chapter of `The Hitchhiker’s Guide to Python <https://docs.python-guide.org/writing/style/>`_.

2) `The Little Book of Python Anti-Patterns <https://docs.quantifiedcode.com/python-anti-patterns/index.html>`_.

3) Writing Idiomatic Python by Jeff Knupp


Running pytest locally
*****************************

Tests are important for helping ensure staircase is as close to bug-free as possible.  When adding a new feature to staircase, tests will be required - edge case testing is particularly useful.  Bug fixes should also include a corresponding test.

The tests written with the `pytest <https://docs.pytest.org/>`_ framework.  If you setup your development environment using :ref:`development.environment_poetry` then you will already have pytest installed.  To run the full suite of tests navigate to the root of the staircase project in a terminal and run (from within your environment)::

    pytest tests

To run an individual test file you can use::

    pytest path\to\test.py



Respecting dependencies
**************************

Developers should make themselves aware of the dependencies defined in *pyproject.toml*.  Any changes to the code must be compatible with all dependency versions possible.  For example, if the minimum supported version of Python is 3.6.1 then we cannot use features of the language introduced in 3.7+, such as the walrus operator (Python 3.8+), dictionary merge and update operators (Python 3.9+), or type hinting generics (Python 3.8+).  

If you setup your development environment using :ref:`development.environment_poetry` then you will have `tox <https://tox.readthedocs.io>`_ installed in your environment.  Tox can be used to check that staircase passes tests with different package versions.  In particular the code can be tested against the minimum dependencies for pandas (1.0) and numpy (1.14) by running the following from the command line in the project root directory::

    tox --recreate -e py37-pandas10-numpy114