.. _userguide:

===================
User Guide
===================

The code examples in the user guide assume the following setup:

.. code-block:: python

   >>> import staircase as sc
   >>> import pandas as pd
   >>> import numpy as numpy
   >>> import matplotlib.pyplot as plt

Below are a variety of resources to help with learning how to use the staircase package.  If you have a question please post to `Stack Overflow <https://stackoverflow.com/>`_ and use the tag **staircase**.

PyConline AU talk
=========================

The Staircase package was debuted during the `2020 PyCon Australia conference <https://2020.pycon.org.au/>`_ (4th-6th September) , renamed to *PyConline AU* after needing to transition to a completely online format due to Covid19.  

Watch the pre-recorded presentation below (`description here <https://2020.pycon.org.au/program/3tds8k/>`_).

.. raw:: html

    <div style="position: relative; padding-bottom: 35%; height: 0; overflow: hidden; max-width: 60%; height: auto; margin-left: auto; margin-right: auto;">
        <iframe src="https://www.youtube.com/embed/CS1dZ-01b-Q" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>


Tutorials
=========================

The tutorials linked below were introduced in the PyConline AU talk, but have since been extended.  They are designed to showcase a variety of staircase functionality, as opposed to a variety of use cases.

Live versions of these tutorials can also be accessed through `binder <https://mybinder.org/v2/gh/venaturum/staircase/CondaBuild?filepath=docs%2Fexamples/>`_.


Test data
=========================
	   
Ready to give **staircase** a spin?  Need some data?  The :func:`staircase.make_test_data` function will get you what you need to start playing.

.. code-block :: python

   >>> import staircase as sc
   >>> dataframe = sc.make_test_data()
   >>> dataframe_dates = sc.make_test_data(dates=True)
	   
	   
.. toctree::
    :maxdepth: 1
    :hidden:

    stepfunctionthinking
    endpoints
    layering
    dates
    masking
    slicing
    distributions
    faq