.. _development.documentation:


Contributing to the documentation
======================================

The documentation is written with `reStructuredText <https://docutils.sourceforge.io/rst.html>`_ and organised into files with *.rst* extensions.  This format can be turned into the html pages you are reading using `Sphinx <https://www.sphinx-doc.org/en/master/>`_.  See the `reStructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ for an introduction on using this language.

Sphinx also generates documentation from the docstrings in the code.  Docstrings are specific to a particular function and should not be confused with *code comments*, which are written for the developer.  Although Sphinx can work with several docstring formats, the only format used in staircase is the *Numpy Docstring Format* (`see examples here <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`_).  In addition, the `pandas docstring guide <https://pandas.pydata.org/docs/development/contributing_docstring.html>`_ is a valuable resource.

Note that Sphinx will ignore producing documentation for functions whose name starts with an underscore.  The conventions behind underscores in Python names are summed up well by Dan Bader in his `blog <https://dbader.org/blog/meaning-of-underscores-in-python>`_.


Code and plotting examples are facilitated through either the `IPython directive <https://matplotlib.org/sampledoc/ipython_directive.html>`_ or the `plot directive <https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html>`_.  Many examples of each can be found throughout staircase documentation.

Also note that while American English is used for function names, much of the documentation is written in British English.


Building the documentation locally
*********************************************

The documentation has its own environment, separate from the rest of the project, and is specified by a requirements file located in the *docs* folder in the root of the project.  To create the environment, navigate to the docs folder in a terminal window and run::

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt

With the environment activated the documentation can then be built using either *make.bat* or *Makefile*, depending on your operating system.  For example, in Powershell run::

    make.bat html

to produce the static html documentation that you are currently reading.  The resulting output can be found in the *_build* folder.  Sometimes Sphinx will utilise existing artifacts in the _build folder and you may not see the changes you expect.  To force a build from scratch use::

    make.bat clean html




