# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#from numpydoc.docscrape import NumpyDocString
#from sphinx.ext.autosummary import _import_by_name
import guzzle_sphinx_theme
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import staircase as sc



# -- Project information -----------------------------------------------------

project = 'staircase'
copyright = '2020, Riley Clement'
author = 'Riley Clement'
version = sc.__version__
if 'untagged' in version:
    version = 'latest'
version = version.split('+')[0]

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 
    'sphinx.ext.autosummary', 
    'sphinx.ext.coverage', 
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',   
    'matplotlib.sphinxext.plot_directive',    
    #'numpydoc',  # handle NumPy documentation formatted docstrings]
    'nbsphinx',
    'guzzle_sphinx_theme',
]

source_suffix = ['.rst', '.ipynb']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'examples/.ipynb_checkpoints']

autosummary_generate = True

master_doc = 'index'

# matplotlib plot directive
plot_include_source = True
plot_formats = [("png", 90)]
plot_html_show_formats = False
plot_html_show_source_link = False
plot_pre_code = """
import numpy as np
import pandas as pd
import staircase as sc
import matplotlib.pyplot as plt
s1 = sc.Stairs().layer(1,2).layer(3,4).layer(4,5,-1)
s2 = sc.Stairs().layer(0, 2, 0.5).layer(3,4,-1).layer(4,5.5,-1)
"""

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"
#html_theme = "nature"
#html_theme = "bizstyle"
html_theme = "guzzle_sphinx_theme"

html_theme_path = guzzle_sphinx_theme.html_theme_path()

html_logo = 'img/staircase.png'


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

def setup(app):
    app.add_css_file('custom.css')

html_sidebars = {
    "**":["logo.html", "globaltoc.html", "relations.html", "searchbox.html", "gumroad.html",]
}
