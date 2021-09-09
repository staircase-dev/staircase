.. _development.environment:


Creating a development environment
======================================

The following assumes that you 

    1) Have created a fork of staircase in your github account
    2) Have cloned your fork to your machine

If you’re *only* making changes to the rst documentation files you can skip to :ref:`development.documentation`.

The suggested development environment for staircase is achieved with a combination of Poetry, pre-commit and VS Code.

.. _development.environment_poetry:

Poetry
********

    *"Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you."*  -- `poetry docs <https://python-poetry.org/docs/>`_

We see Poetry as the best solution for an all-in-one project management tool in python, making it easy to ensure consistent environments between multiple developers.

Poetry is a python package, and can be pip-installed, however it is worth reviewing the `installation instructions <https://python-poetry.org/docs/master/#installation>`_ and following the recommended approach (which does not use pip) to isolate Poetry from the rest of the system.

Once Poetry is installed, navigate to the root of the staircase project in a terminal window and run::

    poetry install

Poetry will install the dependencies defined in *poetry.lock*.  The lock file ensures every developer is working with identical package versions.  Once the packages are installed you can activate the virtual environment by running::

    poetry shell

Note that Poetry will automatically create a name for the environment, and by default store environment data in the following directories:

    *Unix* : ~/.cache/pypoetry/virtualenvs

    *MacOS* : ~/Library/Caches/pypoetry/virtualenvs

    *Windows* : C:\\Users\\<username>\\AppData\\Local\\pypoetry\\Cache\\virtualenvs or %LOCALAPPDATA%\\pypoetry\\Cache\\virtualenvs

We share tips for working with Poetry in VS Code below.

.. _development.environment_precommit:

pre-commit
**********

Precommit is a pip-installable pre-commit hook manager.  Git hooks provide a way to trigger actions when certain git commands are executed and pre-commit hooks are those which are triggered the moment before a commit is created.  We use pre-commit hooks to enforce coding standards.

Note, if you are using Poetry, as suggested, then the pre-commit package will have been installed as a development dependency in your poetry environment.  If you are not using Poetry then installation instructions can be found at the `pre-commit docs <https://pre-commit.com/>`_.

Once the pre-commit package is installed, we use it to install some pre-commit hooks which are defined in *.pre-commit-config.yaml*.  To do this, navigate to the root of the staircase project in your terminal and run (from within your virtual environment)::

    pre-commit install

You can test the pre-commit functionality by running::

    pre-commit run --all-files

The pre-commit hooks currently used in staircase will are used to execute:

    - `black (code formatter) <https://black.readthedocs.io/en/stable/>`_
    - `flake8 (code linter) <https://flake8.pycqa.org/en/latest/>`_
    - `isort (imports formatter) <https://github.com/PyCQA/isort>`_

.. _development.environment_vscode:

Visual Studio Code
*******************

We all have our favourite IDE, and by all means you can use your favourite to work on staircase.  If you are on the fence, or have not used an full featured IDE then we recommend "VS Code", which ranked #1 in Stack Overflow's 2021 Developer Survey (being used by 70% of respondents).

VS Code is a free IDE produced by Microsoft which supports several languages including Python (and Jupyter Notebooks) and reStructuredText.  VS Code with Python provides many language support features including code completion, auto imports, code navigation, syntax highlighting, signature help.  Additionally there are many useful extensions that you can easily install from within VS Code to customise and extend the IDE.

See `Python projects with Poetry and VSCode. (Part 2) <https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-2/>`_ on www.pythoncheatsheet.org for a good introduction to setting up VS Code to work with Poetry, and with *flake8* and *black*.
