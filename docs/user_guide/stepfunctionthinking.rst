.. _user_guide.stepfunctionthinking:

Thinking in step functions
===========================

Most analysts and data-centric professionals probably go through their career without a modicum of thought dedicated to step functions.  It would be pretentious to declare step function thinking as necessary, or a missing piece of the puzzle, but below the case is made for it being a handy addition to the toolset.

.. raw:: html

    <h4>Where would I find step functions?</h4>

A step function is piecewise constant - it is made up of horizontal lines.  If the domain of the step function represents time, and the values represent some sort of state, then a step function describes changes in state over time.  We live in a world where things are always changing state.  Consequently, we are surrounded by step functions.

Currently, you are looking at a computer, or mobile device.  This device can be in a state of *on* or *off*, and the periods of time in each state define a step function whose values are 0 R(off) or 1 (on).  On this device, the web page you are reading is either in a state of *open*, or *not open*, or perhaps *active* and *inactive* to extend the *open* state.  The number of times you have visited this page is a step function which never decreases, jumping in value by 1 with each new visit.  The number of emails you've sent or received is also a non-decreasing step function with integer values, but may increase by several units at a time in the case of sending group emails.  The ratio of sent emails to received emails is a step function which can increase or decrease, whose values are positive rational numbers.  Still not convinced?  Here are some more examples of variables which correspond to "step functions in the wild":


- count of vehicles in a queue
- count of passengers in a vehicle queue
- average number of passengers per car in a queue
- machine utilisation
- bus fleet utilisation
- airplane seat capacity
- average win rate of sporting team
- rolling average win rate of sporting team (rolling window can be number of games, or time based)
- boolean indicating if a day is a weekday
- boolean indicating if the temperature is above a certain threshold
- boolean indicating if the temperature is above a certain threshold and it's a weekday
  

.. raw:: html

    <h4>Do I need step functions in my life?</h4>
|
    "If your only tool is a hammer, every problem looks like a nail"

The *law of the instrument*, quoted above, pertains to a cognitive bias involving over reliance on a particular tool [*]_.  Its significance here is to draw attention to both opportunities to use "step function thinking" may have been missed in the past, but to also acknowledge that there are instances where :mod:`staircase` could be applied, but yield no advantage.

Whether step-function-based-analysis is appropriate depends on your data, and the application.  There is no requirement that step functions modelled with :mod:`staircase` need to be time based (despite all the examples above being so) however many applications arise from this case.  If your data contains datetimes then perhaps thinking in step functions could be useful.  Let's consider the case that the datetime data represents a time series.  It is highly likely this time series has been derived by sampling a continuous process.  For example, some stock prices are constantly changing, jumping from one price to the next many times per minute.  Historical stock price data however is often a daily timeseries.  This can only arise by sampling the underlying step function (eg. *opening price*, *closing price*) or aggregating (eg. *max price*, *average price*).  The result can still be interpreted as a step function, but it one that has been "downsampled".

Downsampling in this way would generally lead to a loss of information, however this may not be significant for the application at hand.  Depending on how often the underlying step function changes, and the frequency of the time series, a step function representation may require less memory than a time series while retaining a higher fidelity of information.  However if dealing with time series data, :mod:`staircase` is unlikely to provide functionality (such as arithmetic, comparisons, statistics) that can't be paralleled with straightforward application of :mod:`pandas` and :mod:`numpy`.

As an example of *thinking with step functions*, consider the question of how to plot the time spent in a particular state for a collection of entities.  To make the example more concrete, assume we have a queue of objects and we're interested in visualising the time spent in the queue, as time moves forward.  The entry to, and departure from, the queue are marked by two times for each entity.  The distance between these points is the duration that entity spent in the queue.  Once we have calculated the durations for each entity, how do we chart this information?  One approach is to create a dataset of tuples *(departure time, duration)* and use a scatter plot.  Perhaps we could apply a rolling mean using a time window and use a line plot.  But what makes the departure time special?  Why not use the entry time?  Or the mid-point between the two (or any convex combination)?  Regardless of choice, this approach is fundamentally assigning the length of an interval to some point along it.  This is not uncommon.  When we describe past life expectancies it is commonplace to say "the average life span of someone born in X was Y".  This is an example of attributing the length of an interval to its start point.  What about an exercise app that logs time and duration?  Would you expect that time to be the start, or end point?  The choice seems arbitrary in this instance, and it would not be wrong to assume that either option could be found in such apps.

Using *step function thinking* an arbitrary choice can be avoided.  The size of the queue is a step function which immediately pops to mind the moment entry and departure times are introduced.  It can be constructed by adding together component step functions for each entity, which take value 0 or 1, and indicate whether the entity is queued or not.  But how do we incorporate the duration information?  If the value of each component step function, whenever the entity is queued, is the duration instead of 1, then the step function which results by adding these components answers the following question: "given a time *t*, what was the total queue time for all entities in the queue at time *t*".  If we divide this step function by the queue size step function we can answer "what was the average queue time for all entities in the queue at time *t*".  Furthermore, these step functions can be plotted, allowing a visualisation of how queue duration may change over time, without the need for arbitrary choices which possibly give rise to inconsistent visualisations.

In a similar vein, suppose we have jobs which can start at any time, and incur some period of time (in the order of days).  We want to obtain some measure of jobs per day.  The two simplest strategies are either to tally up the number of jobs started per day, or alternatively, tally up the jobs finished per day.  But again, this is introducing an arbitrary choice which can be avoided with *step function thinking*.   If the value of each component step function, corresponding to a job, is 1 then the step function resulting from adding these components gives us the number of jobs underway at any point in time.  Perhaps at this point the requirement that the measure is a daily time series is not required?  But let's assume it is.  If the value of each component step function is 1/duration, instead of 1, then integrating under the resulting step function, for each day, indicates the equivalent number of jobs that were completed on that day.  That is to say, if 10 jobs, each of duration 48 hours were all underway for an entire 24hr day, then this is equivalent to 240 hours, or 5 jobs.  Again, the step function facilitates a metric, and visualisation, which avoids arbitrary choice.

.. rubric:: Footnotes
    .. [*] This *law of the instrument* has been attributed to several people, so it is stated here without authorship.