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


#for sphinx
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

#for nbsphinx
os.environ['PYTHONPATH'] = os.path.abspath(parentdir)

import staircase as sc
from datetime import datetime


# -- Project information -----------------------------------------------------

project = 'staircase'
copyright = f'2020-{datetime.now().year}, Riley Clement'
author = 'Riley Clement'
version = sc.__version__
if 'untagged' in version:
    version = 'latest'
elif 'unknown' in version:  #for when not installed
    try:
        import toml
        version = dict(toml.load(parentdir + "/pyproject.toml"))["tool"]["poetry"]["version"]
    except:
        pass
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
    #'sphinx.ext.napoleon',   
    'matplotlib.sphinxext.plot_directive',  
    'sphinx.ext.extlinks',    
    #"sphinx.ext.linkcode",
    'numpydoc',  # handle NumPy documentation formatted docstrings]
    'nbsphinx',
    "sphinx_panels",
]

source_suffix = ['.rst', '.ipynb']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv',
    'examples/.ipynb_checkpoints',
    'articles/.ipynb_checkpoints',
    'examples/Index.ipynb',
]

suppress_warnings = [
    "nbsphinx.ipykernel",
]

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
s3 = sc.Stairs().layer(1,2).layer(3,4).layer(4,5,-1).mask((2.5, 3.5))
s4 = sc.Stairs().layer(0, 2, 0.5).layer(3,4,-1).layer(4,5.5,-1).mask((4,5))
"""


def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != "py":
        return None

    modname = info["module"]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError:
            return None

    try:
        fn = inspect.getsourcefile(inspect.unwrap(obj))
    except TypeError:
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except OSError:
        lineno = None

    if lineno:
        linespec = f"#L{lineno}-L{lineno + len(source) - 1}"
    else:
        linespec = ""

    fn = os.path.relpath(fn, start=os.path.dirname(staircase.__file__))

    if "+" in staircase.__version__:
        return f"https://github.com/staircase-dev/staircase/blob/master/staircase/{fn}{linespec}"
    else:
        return (
            f"https://github.com/staircase-dev/staircase/blob/"
            f"v{staircase.__version__}/staircase/{fn}{linespec}"
        )


intersphinx_mapping = {
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "statsmodels": ("https://www.statsmodels.org/devel/", None),
}

    
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "pydata_sphinx_theme"

#html_theme = "guzzle_sphinx_theme"
#html_theme_path = guzzle_sphinx_theme.html_theme_path()

html_theme_options = {
    "google_analytics_id": "UA-27880019-2",
    "github_url": "https://github.com/staircase-dev/staircase",
}


html_logo = "img/staircase-wide-transparent.svg"
html_favicon = "img/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

def setup(app):
    app.add_css_file('custom2.css')

# html_sidebars = {
    # #"**":["logo.html", "globaltoc.html", "relations.html", "searchbox.html", "gumroad.html",]
    # "**":["globaltoc.html", "relations.html", "searchbox.html",]
# }
