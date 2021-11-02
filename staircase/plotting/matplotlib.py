import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters

from staircase.util._decorators import Appender

from . import docstrings


def _draw_arrows(frame, ax, color, linewidth, **kwargs):

    ax.get_ylim()  # bugfix to trigger axes transform

    axis_to_data = ax.transAxes + ax.transData.inverted()
    axes_lims = axis_to_data.transform([(0, 0), (1, 1)])
    head_width = (axes_lims[1, 1] - axes_lims[0, 1]) * 0.03
    arrow_length = (axes_lims[1, 0] - axes_lims[0, 0]) * 0.1

    if len(frame) == 1:
        y = frame.iloc[0, -1]
        x = sum(ax.get_xlim()) / 2
        frame = pd.DataFrame(
            {
                "start": [None, x],
                "end": [x, None],
                "value": [y, y],
            }
        )
    kwargs = {
        "head_width": head_width,
        "head_length": arrow_length * 0.5,
        "color": color,
        "linewidth": linewidth,
        **kwargs,
    }
    if not pd.isnull(frame.iloc[-1]["start"]):
        x = frame.iloc[-1]["start"]
        y = frame.iloc[-1]["value"]
        ax.arrow(
            x,
            y,
            arrow_length,
            0,
            **kwargs,
        )
    if not pd.isnull(frame.iloc[0]["value"]):
        x = frame.iloc[0]["end"]
        y = frame.iloc[0]["value"]
        ax.arrow(
            x,
            y,
            -arrow_length,
            0,
            **kwargs,
        )


def _plot_matplotlib_steps(frame, ax, **kwargs):
    frame.loc[0, "start"] = frame.loc[0, "end"]

    return ax.step(
        frame["start"],
        frame["value"],
        where="post",
        **kwargs,
    )


def _plot_matplotlib_hlines(frame, ax, **kwargs):
    plot_data = frame.iloc[1:-1].loc[lambda df: df["value"].notnull()]

    return ax.hlines(
        plot_data["value"],
        plot_data["start"],
        plot_data["end"],
        **kwargs,
    )


@Appender(docstrings.matplotlib_docstring, join="\n", indents=1)
def plot(
    self, ax=None, style="step", arrows=False, linewidth=1, arrow_kwargs=None, **kwargs
):
    assert style in ("step", "hlines")
    register_matplotlib_converters()
    # TODO warn if style is hlines and arrow is None
    if arrow_kwargs is None:
        arrow_kwargs = {}
    if ax is None:
        _, ax = plt.subplots()
    frame = self.to_frame()
    if len(frame) == 1:
        value = frame.iloc[0, -1]
        if not np.isnan(value):
            color = kwargs.get("color", None)
            if arrows:
                _draw_arrows(frame, ax, color, linewidth, **arrow_kwargs)
            else:
                ax.axhline(value, color=color, **kwargs)
        return ax
    if style == "step":
        lines = _plot_matplotlib_steps(frame, ax=ax, linewidth=linewidth, **kwargs)
        color = lines[0].get_color()
    else:
        lines = _plot_matplotlib_hlines(frame, ax=ax, linewidth=linewidth, **kwargs)
        color = lines.get_colors()[0]
    if arrows or style == "hlines":
        _draw_arrows(frame, ax, color, linewidth, **arrow_kwargs)
    return ax
