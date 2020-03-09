.. _getting_started:


***************
Getting started
***************

Introduction
============

If you are new to staircase, this is the place to begin. The goal of this
tutorial is to get you set-up and rolling with staircase.

What is a step function?
=========================

A step function, also known as a staircase function, is a piecewise constant function defined over the real numbers.  It can be characterised as a function f defined over a sequence of disjoint intervals, whose union is the set of all real numbers, and where f(x) = f(y) whenever x and y belong to the same interval.

The staircase package can be used to model step functions where intervals have non-zero length (i.e. intervals must be defined by two distinct endpoints) and are either all left closed right-open, or all left-open right-closed.

.. figure:: img/staircase_function_examples.png
   :width: 100%
   :alt: examples of step functions
   :align: center
   
   **Two examples of step functions**
   

.. figure:: img/not_staircase_function_examples.png
   :width: 100%
   :alt: not step functions
   :align: center
   
   **Examples of mappings which are not step functions**
   
.. code-block :: python

   import staircase as sc
   
   sf = sc.Stairs()
   sc.layer(1,5)
   
   
This example shows the most basic of usages.

API
===

The :ref:`API Reference <api>` contains a detailed description of the staircase API. The 
reference describes how the methods work and which parameters can be used. 
It assumes that you have an understanding of the key concepts.