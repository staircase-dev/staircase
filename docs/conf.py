# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# from numpydoc.docscrape import NumpyDocString
# from sphinx.ext.autosummary import _import_by_name


import inspect

# for sphinx
import os
import sys
from datetime import datetime

from numpydoc.docscrape import NumpyDocString
from sphinx.ext.autosummary import _import_by_name

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import staircase as sc  # isort:skip

# for nbsphinx
os.environ["PYTHONPATH"] = os.path.abspath(parentdir)


# -- Project information -----------------------------------------------------

project = "staircase"
copyright = f"2020-{datetime.now().year}, Riley Clement"
author = "Riley Clement"
version = sc.__version__
if "untagged" in version:
    version = "latest"
elif "unknown" in version:  # for when not installed
    try:
        import toml

        version = dict(toml.load(parentdir + "/pyproject.toml"))["tool"]["poetry"][
            "version"
        ]
    except:  # noqa E722
        pass
version = version.split("+")[0]

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "matplotlib.sphinxext.plot_directive",
    "sphinx.ext.extlinks",
    # "sphinx.ext.linkcode",
    "numpydoc",  # handle NumPy documentation formatted docstrings]
    "nbsphinx",
    "sphinx_design",
]

source_suffix = [".rst"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    "examples/.ipynb_checkpoints",
    "articles/.ipynb_checkpoints",
    "examples/Index.ipynb",
]

suppress_warnings = [
    "nbsphinx.ipykernel",
]

autosummary_generate = True

# sphinx-panels shouldn't add bootstrap css since the pydata-sphinx-theme
# already loads it
#panels_add_bootstrap_css = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


master_doc = "index"

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
from matplotlib.dates import DateFormatter
plt.rcParams['figure.autolayout'] = True
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

    fn = os.path.relpath(fn, start=os.path.dirname(sc.__file__))

    if "+" in sc.__version__:
        return f"https://github.com/staircase-dev/staircase/blob/master/staircase/{fn}{linespec}"
    else:
        return (
            f"https://github.com/staircase-dev/staircase/blob/"
            f"v{sc.__version__}/staircase/{fn}{linespec}"
        )


intersphinx_mapping = {
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "statsmodels": ("https://www.statsmodels.org/devel/", None),
    "sortedcontainers": ("http://www.grantjenks.com/docs/sortedcontainers", None),
    "seaborn": ("https://seaborn.pydata.org", None),
}


import sphinx  # isort:skip
from sphinx.ext.autodoc import (  # isort:skip
    AttributeDocumenter,
    Documenter,
    MethodDocumenter,
)
from sphinx.ext.autosummary import Autosummary  # isort:skip


class AccessorDocumenter(MethodDocumenter):
    """
    Specialized Documenter subclass for accessors.
    """

    objtype = "accessor"
    directivetype = "method"

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6

    def format_signature(self):
        # this method gives an error/warning for the accessors, therefore
        # overriding it (accessor has no arguments)
        return ""


class AccessorLevelDocumenter(Documenter):
    """
    Specialized Documenter subclass for objects on accessor level (methods,
    attributes).
    """

    # This is the simple straightforward version
    # modname is None, base the last elements (eg 'hour')
    # and path the part before (eg 'Series.dt')
    # def resolve_name(self, modname, parents, path, base):
    #     modname = 'pandas'
    #     mod_cls = path.rstrip('.')
    #     mod_cls = mod_cls.split('.')
    #
    #     return modname, mod_cls + [base]
    def resolve_name(self, modname, parents, path, base):
        if modname is None:
            if path:
                mod_cls = path.rstrip(".")
            else:
                mod_cls = None
                # if documenting a class-level object without path,
                # there must be a current class, either from a parent
                # auto directive ...
                mod_cls = self.env.temp_data.get("autodoc:class")
                # ... or from a class directive
                if mod_cls is None:
                    mod_cls = self.env.temp_data.get("py:class")
                # ... if still None, there's no way to know
                if mod_cls is None:
                    return None, []
            # HACK: this is added in comparison to ClassLevelDocumenter
            # mod_cls still exists of class.accessor, so an extra
            # rpartition is needed
            modname, _, accessor = mod_cls.rpartition(".")
            modname, _, cls = modname.rpartition(".")
            parents = [cls, accessor]
            # if the module name is still missing, get it like above
            if not modname:
                modname = self.env.temp_data.get("autodoc:module")
            if not modname:
                if sphinx.__version__ > "1.3":
                    modname = self.env.ref_context.get("py:module")
                else:
                    modname = self.env.temp_data.get("py:module")
            # ... else, it stays None, which means invalid
        return modname, parents + [base]


class AccessorAttributeDocumenter(AccessorLevelDocumenter, AttributeDocumenter):
    objtype = "accessorattribute"
    directivetype = "attribute"

    # lower than AttributeDocumenter so this is not chosen for normal
    # attributes
    priority = 0.6


class AccessorMethodDocumenter(AccessorLevelDocumenter, MethodDocumenter):
    objtype = "accessormethod"
    directivetype = "method"

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6


class AccessorCallableDocumenter(AccessorLevelDocumenter, MethodDocumenter):
    """
    This documenter lets us removes .__call__ from the method signature for
    callable accessors like Series.plot
    """

    objtype = "accessorcallable"
    directivetype = "method"

    # lower than MethodDocumenter; otherwise the doc build prints warnings
    priority = 0.5

    def format_name(self):
        return MethodDocumenter.format_name(self).rstrip(".__call__")


class StaircaseAutosummary(Autosummary):
    """
    This alternative autosummary class lets us override the table summary for
    Stairs.plot in the API docs.
    """

    def _replace_staircase_items(self, display_name, sig, summary, real_name):
        # this a hack: ideally we should extract the signature from the
        # .__call__ method instead of hard coding this
        if display_name == "Stairs.plot":
            sig = "([x, y, kind, ax, ....])"
            summary = "Stairs plotting accessor and method"
        return (display_name, sig, summary, real_name)

    @staticmethod
    def _is_deprecated(real_name):
        try:
            obj, parent, modname = _import_by_name(real_name)
        except ImportError:
            return False
        doc = NumpyDocString(obj.__doc__ or "")
        summary = "".join(doc["Summary"] + doc["Extended Summary"])
        return ".. deprecated::" in summary

    def _add_deprecation_prefixes(self, items):
        for item in items:
            display_name, sig, summary, real_name = item
            if self._is_deprecated(real_name):
                summary = f"(DEPRECATED) {summary}"
            yield display_name, sig, summary, real_name

    def get_items(self, names):
        items = Autosummary.get_items(self, names)
        items = [self._replace_staircase_items(*item) for item in items]
        items = list(self._add_deprecation_prefixes(items))
        return items


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "pydata_sphinx_theme"

# html_theme = "guzzle_sphinx_theme"
# html_theme_path = guzzle_sphinx_theme.html_theme_path()

html_theme_options = {
    #"google_analytics_id": "UA-27880019-2",
    "github_url": "https://github.com/staircase-dev/staircase",
    "navbar_end": ["navbar-icon-links"],
}


html_show_sourcelink = False

html_logo = "img/staircase-wide-inverse.svg"
html_favicon = "img/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "custom.css",
]

html_context = {
   # ...
   "default_mode": "light"
}



def setup(app):
    # app.add_css_file("custom.css")
    app.add_autodocumenter(AccessorDocumenter)
    app.add_autodocumenter(AccessorAttributeDocumenter)
    app.add_autodocumenter(AccessorMethodDocumenter)
    app.add_autodocumenter(AccessorCallableDocumenter)
    app.add_directive("autosummary", StaircaseAutosummary)


# html_sidebars = {
# #"**":["logo.html", "globaltoc.html", "relations.html", "searchbox.html", "gumroad.html",]
# "**":["globaltoc.html", "relations.html", "searchbox.html",]
# }
