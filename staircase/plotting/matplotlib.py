import matplotlib.pyplot as plt
import numpy as np


def _draw_arrows(frame, ax, color, linewidth, **kwargs):

    ax.get_ylim()  # bugfix to trigger axes transform

    axis_to_data = ax.transAxes + ax.transData.inverted()
    axes_lims = axis_to_data.transform([(0, 0), (1, 1)])
    head_width = (axes_lims[1, 1] - axes_lims[0, 1]) * 0.03
    arrow_length = (axes_lims[1, 0] - axes_lims[0, 0]) * 0.1

    # head_width, head_length = inv.transform((1,1), (0,0))
    if not np.isnan(frame.iloc[-1]["start"]):
        x = frame.iloc[-1]["start"]
        y = frame.iloc[-1]["value"]
        ax.arrow(
            x,
            y,
            arrow_length,
            0,
            head_width=head_width,
            head_length=arrow_length * 0.5,
            color=color,
            linewidth=linewidth,
            **kwargs,
        )
    if not np.isnan(frame.iloc[0]["value"]):
        x = frame.iloc[0]["end"]
        y = frame.iloc[0]["value"]
        ax.arrow(
            x,
            y,
            -arrow_length,
            0,
            head_width=head_width,
            head_length=arrow_length * 0.5,
            color=color,
            linewidth=linewidth,
            **kwargs,
        )


def _plot_matplotlib_steps(frame, ax, **kwargs):
    frame.loc[0, "start"] = frame.loc[0, "end"]

    ax.step(
        frame["start"], frame["value"], where="post", **kwargs,
    )


def _plot_matplotlib_hlines(frame, ax, **kwargs):
    plot_data = frame.iloc[1:-1].query("value.notnull()")

    ax.hlines(
        plot_data["value"], plot_data["start"], plot_data["end"], **kwargs,
    )


def plot(
    self,
    ax=None,
    style="step",
    arrows=False,
    # color="blue",
    linewidth=1,
    arrow_kwargs={},
    **kwargs
):
    assert style in ("step", "hlines")
    # TODO warn if style is hlines and arrow is None
    if ax is None:
        _, ax = plt.subplots()
    frame = self.to_frame()
    if style == "step":
        _plot_matplotlib_steps(frame, ax=ax, linewidth=linewidth, **kwargs)
    else:
        _plot_matplotlib_hlines(frame, ax=ax, linewidth=linewidth, **kwargs)
    if arrows or style == "hlines":
        _draw_arrows(frame, ax, linewidth, **arrow_kwargs)
    return ax
