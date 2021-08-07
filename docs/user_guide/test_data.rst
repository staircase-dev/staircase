.. _resources.test_data:

Test data
=========================
	   
Ready to give **staircase** a spin?  Need some data?  The :func:`staircase.make_test_data` function will get you what you need to start playing.

.. code-block :: python

   >>> import staircase as sc
   >>> dataframe = sc.make_test_data()
   >>> dataframe_dates = sc.make_test_data(dates=True)