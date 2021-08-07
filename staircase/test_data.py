import numpy as np
import pandas as pd


def make_test_data(dates=True, positive_only=True, groups=(), random_state=None):
    if len(groups) == 0:
        return _make_test_data(dates=dates, positive_only=positive_only, random_state=random_state)
    
    dfs = []

    for group in enumerate(groups):
        df = _make_test_data(dates=dates, positive_only=positive_only, random_state=random_state)
        dfs.append(df.assign(group = group))
        if random_state is not None:
            random_state += 1

    return pd.concat(dfs)

def _make_test_data(dates=True, positive_only=True, random_state=None):
    if random_state is None:
        rng = np.random.default_rng()
    else:
        rng = np.random.default_rng(random_state)

    n_intervals = rng.integers(100, 1000)
    smallest_interval = rng.integers(1,6)
    largest_interval = rng.integers(15, 20)
    interval_lengths = rng.random(size=n_intervals)*(largest_interval- smallest_interval) + smallest_interval

    start = rng.random(size=n_intervals)*120 - 20
    end = start + interval_lengths

    if dates:
        start= pd.Timestamp("2021") + start*365/100*pd.Timedelta(1, "day")
        end= pd.Timestamp("2021") + end*365/100*pd.Timedelta(1, "day")

    value = rng.choice(range(-5,6), n_intervals)
    if positive_only:
        value = value + 6

    data = pd.DataFrame(
        {
            "start": start,
            "end":end,
            "value":value,
        }
    )

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
