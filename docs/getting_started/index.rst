.. _getting_started:


***************
Getting started
***************

Introduction
============

The staircase package is used to model step functions.  We discuss what a step function is below, but first let's talk application.  Step functions can be used to represent time series - think changes in state over time, queue counts over time, utilisation over time - you get the idea.  

The staircase package makes converting raw, temporal data into time series easy and readable.  Furthermore there is a rich variety of :ref:`arithmetic operations <api.arithmetic_operators>`, :ref:`relational operations <api.relational_operators>`, :ref:`logical operations <api.logical_operators>`, :ref:`statistical operations <api.statistical_operators>`, to enable analysis, in addition to functions for :ref:`univariate analysis <api.summary_statistics>`, :ref:`aggregations <api.module_funcs>` and compatibility with `pandas.Timestamp <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html>`_.


   
The staircase API
=================

The :ref:`API Reference <api>` contains a detailed description of the staircase API. The 
reference describes how the methods work and which parameters can be used. 
It assumes that you have an understanding of the key concepts.


.. toctree::
    :maxdepth: 1
    :hidden:

    install
    stepfunction
    endpoints
    small_example