import numpy as np
import pandas as pd

import staircase as sc


def _not_arithmetic_op(series_op):
    return series_op not in (
        pd.Series.add,
        pd.Series.sub,
        pd.Series.mul,
        pd.Series.div,
    )


def _reindex_deltas(new_index, deltas, initial_value):
    mask = deltas.where(np.isnan(deltas.values), 0)
    deltas_reindexed = deltas.reindex(new_index, fill_value=0)
    mask_initial_value = np.nan if np.isnan(initial_value) else 0
    mask_reindexed = _reindex_values(new_index, mask, mask_initial_value)
    return deltas_reindexed + mask_reindexed


def _reindex_values(new_index, values, initial_value):
    """Conform values to new index

    Parameters
    ----------
    new_index : pandas.Index
    values : pandas.Series
    initial_value : float

    Returns
    -------
    pandas.Series
    """
    first_step = values.index[0]
    new_values = values.reindex(new_index, method="ffill")
    new_values.loc[new_values.index < first_step] = initial_value
    return new_values


def _combine_step_series(
    series_1, series_2, initial_value_1, initial_value_2, series_op, kind
):
    # kind = "values" or "deltas"
    new_index = series_1.index.union(series_2.index)

    reindex_method = _reindex_values if kind == "values" else _reindex_deltas
    reindexed_series_1 = reindex_method(new_index, series_1, initial_value_1)
    reindexed_series_2 = reindex_method(new_index, series_2, initial_value_2)

    new_series = series_op(
        reindexed_series_1,
        reindexed_series_2,
    ).astype(float)

    if series_op == pd.Series.divide:
        new_series.replace(np.inf, np.nan, inplace=True)

    return new_series


def _combine_stairs_via_values(stairs1, stairs2, series_op, float_op):
    # self.values and other._values should be able to be created
    values = _combine_step_series(
        stairs1._get_values(),
        stairs2._get_values(),
        stairs1.initial_value,
        stairs2.initial_value,
        series_op,
        "values",
    )

    requires_manual_masking = _not_arithmetic_op(series_op)

    if requires_manual_masking and (stairs1._has_na() or stairs2._has_na()):
        mask = _combine_step_series(
            stairs1._get_values().isnull(),
            stairs2._get_values().isnull(),
            np.isnan(stairs1.initial_value),
            np.isnan(stairs2.initial_value),
            np.logical_or,
            "values",
        ).astype(bool)
        values.loc[mask] = np.nan

    if requires_manual_masking and (
        np.isnan(stairs1.initial_value) or np.isnan(stairs2.initial_value)
    ):
        initial_value = np.nan
    elif series_op == pd.Series.divide and stairs2.initial_value == 0:
        initial_value = np.nan
    else:
        initial_value = float_op(stairs1.initial_value, stairs2.initial_value) * 1

    if series_op == pd.Series.divide:
        values = values.replace(np.inf, np.nan).replace(-np.inf, np.nan)

    new_instance = sc.Stairs._new(
        initial_value=initial_value,
        data=pd.DataFrame({"value": values}),
    )
    new_instance._remove_redundant_step_points()
    return new_instance
