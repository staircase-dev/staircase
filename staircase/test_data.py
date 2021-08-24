import numpy as np
import pandas as pd


def make_test_data(dates=True, positive_only=True, groups=(), seed=None):
    """
    Creates interval data for use with staircase.

    The result will be a :class:`pandas.DataFrame` with columns "start", "end", "value", and optionally "group".

    Parameters
    ----------
    dates : bool, default True
        Indicates whether to return data associated with a datetime domain or numerical.
        If dates is true the data will be confined to the year 2021.
        If dates is false the data will be confined to the interval [0, 100]
    positive_only : bool, default True
        If True then *value* column will only consist of positive values
    groups : array-like of strings, optional
        If specified will create data for each string specified in *groups*.  A column
        named "group" will be added to identify the subsets of data.
    seed : int, optional
        If specified will seed a random number generator to facilitate reproducability.

    Returns
    -------
    :class:`pandas.DataFrame`

    Examples
    --------

    .. plot::
        :context: close-figs

        >>> df = sc.make_test_data()
        >>> sc.Stairs(df, "start", "end").plot()

    .. plot::
        :context: close-figs

        >>> df = sc.make_test_data(dates=False, positive_only=False, seed=42)
        >>> sc.Stairs(df, "start", "end", "value").plot()

    .. plot::
        :context: close-figs

        >>> df = sc.make_test_data(groups=["A", "B", "C"])
        >>> stairs = df.groupby("group").apply(sc.Stairs, "start", "end")
        >>> ax = stairs["A"].plot(label="A")
        >>> stairs["B"].plot(ax, label="B")
        >>> stairs["C"].plot(ax, label="C")
        >>> ax.legend()

    """
    if len(groups) == 0:
        return _make_test_data(dates=dates, positive_only=positive_only, seed=seed)

    dfs = []

    for group in groups:
        df = _make_test_data(dates=dates, positive_only=positive_only, seed=seed)
        dfs.append(df.assign(group=group))
        if seed is not None:
            seed += 1

    return pd.concat(dfs)


def _make_test_data(dates=True, positive_only=True, seed=None):
    if seed is None:
        rng = np.random.default_rng()
    else:
        rng = np.random.default_rng(seed)

    n_intervals = rng.integers(100, 1000)
    smallest_interval = rng.integers(1, 6)
    largest_interval = rng.integers(15, 20)
    interval_lengths = (
        rng.random(size=n_intervals) * (largest_interval - smallest_interval)
        + smallest_interval
    )

    start = rng.random(size=n_intervals) * 120 - 20
    end = start + interval_lengths

    if dates:
        start = pd.Timestamp("2021") + pd.TimedeltaIndex(
            start * 365 / 100 * pd.Timedelta(1, "day")
        )
        end = pd.Timestamp("2021") + pd.TimedeltaIndex(
            end * 365 / 100 * pd.Timedelta(1, "day")
        )

    value = rng.choice(range(-5, 6), n_intervals)
    if positive_only:
        value = value + 6

    data = pd.DataFrame({"start": start, "end": end, "value": value,})

    if dates:
        data["start"] = data["start"].dt.floor("min")
        data["end"] = data["end"].dt.floor("min")
        data = data.loc[(data["end"] > "2021") & (data["start"] < "2022")]
        data.loc[data["start"] < "2021", "start"] = pd.NaT
        data.loc[data["end"] >= "2022", "end"] = pd.NaT
    else:
        data = data.loc[(data["end"] > 0) & (data["start"] < 100)]
        data.loc[data["start"] < 0, "start"] = np.nan
        data.loc[data["end"] >= 100, "end"] = np.nan

    return data.sort_values(["end", "start"]).reset_index(drop=True)
