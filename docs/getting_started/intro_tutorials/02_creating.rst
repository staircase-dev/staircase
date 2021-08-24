.. _intro_tutorials.creating:

How do I create my step function?
=================================

Step functions are represented with by the :class:`staircase.Stairs` class.  The terms *step function* and *stairs* are often used interchangeably throughout the documentation.
It is a data structure, with associated methods, for modelling and manipulating step functions.  The Stairs class is to staircase, what :class:`pandas.DataFrame` is to :mod:`pandas`. Almost everything you do in staircase will be centred around this class.  So how do we create an instance?

.. ipython:: python

    import staircase as sc
    
    sf = sc.Stairs()

That was easy wasn't it?  Surely there must be more to it than that?  There is.  Let's look at the constructor signature using Python's inspect module:

.. ipython:: python
 
    import inspect
    inspect.signature(sc.Stairs)


We'll return to the first four parameters later.  First let's discuss *initial_value* and *closed*.

Every step function in staircase begins life as a single interval, stretching from negative infinity to positive infinity.  The value of this interval is given by *initial_value*, which by default is zero.  Let's confirm this for our step function *sf* using :meth:`staircase.Stairs.to_frame`

.. ipython:: python
 
    sf.to_frame()

The *closed* parameter can either be "left" or "right" and indicates whether this step function is be composed of left-closed, or right-closed intervals.

Now, we have a step function, but it might not be the one you want.  We can manipulate the values of the step function using :meth:`staircase.Stairs.layer`, which in its simplest form takes three arguments: *start*, *end*, *value*.  The effect of this method is to increase the values of the step function by *value* between the points *start* and *end*.  If you are a fan of irrelevant details then know that the *layer* method is essentially adding `boxcar functions <https://en.wikipedia.org/wiki/Boxcar_function>`_. to the existing step function.  Let's add a 'layer' (and use the default of 1 for *value*):

.. ipython:: python
 
    sf.layer(1,3)
    sf.to_frame()

and another,

.. ipython:: python
 
    sf.layer(4,6)
    sf.to_frame()

and another.

.. ipython:: python
 
    sf.layer(2,5,2)
    sf.to_frame()

This is what our step function now looks like:

.. plot::
    :context: close-figs
    :include-source: False

    sc.Stairs().layer([1,4,2], [3,6,5], [1,1,2]).plot(arrows=True)


Now building up our step function one 'layer' at a time is not computationally efficient, at least not compared to the alternative approach of using vectors as arguments to the layer method.  The following builds the same step function but does so utilising vectors:

.. ipython:: python
 
    sc.Stairs().layer(
        start = [1,4,2],
        end = [3,6,5],
        value = [1,1,2],
    )

In a similar vein, inspired by a popular pattern found in :mod:`seaborn`, the layer function can take a parameter *data* - a :class:`pandas.DataFrame` - and the values of the other parameters may be strings referring to column names:

.. ipython:: python

    import pandas as pd

    df = pd.DataFrame({
        "a":[1,4,2],
        "b":[3,6,5],
        "c":[1,1,2],
    })

    sc.Stairs().layer(start="a", end="b", value="c", frame=df)

Lastly, to bring us back full circle, the parameters in the *layer* method also appear in the :class:`staircase.Stairs` constructor method, allowing the full construction of our step function in one step (excuse the pun):

.. ipython:: python

    df = pd.DataFrame({
        "a":[1,4,2],
        "b":[3,6,5],
        "c":[1,1,2],
    })

    sc.Stairs(start="a", end="b", value="c", frame=df)


For a more in depth look at :meth:`staircase.Stairs.layer`, including potential "gotchas", please refer to <insert section>.
For masking refer to...