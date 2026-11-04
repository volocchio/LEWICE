"""
Geometry figure helpers.

Airfoil and ice-shape plots keep one data unit in x equal to one data unit
in y. Plotly holds that under resize and zoom with scaleanchor='x' and
scaleratio=1, and constrain='domain' so the extra space is a margin rather
than a stretched axis. Matplotlib uses set_aspect('equal').

Collection efficiency, heat transfer, and other line plots are intentionally
not equal-aspect.
"""
import math


def bounds(points, pad_frac=0.08, min_pad=0.004):
    """Data ranges with the same absolute padding on every side."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    span = max(xmax - xmin, ymax - ymin, 1e-6)
    pad = max(pad_frac * span, min_pad)
    return [xmin - pad, xmax + pad], [ymin - pad, ymax + pad]


def geometry_height(x_range, y_range, width_px=980, min_px=280, max_px=640):
    """Pixel height that roughly matches the data aspect at ``width_px``.

    scaleanchor still enforces the exact ratio inside whatever width the
    browser actually uses; this only keeps the empty margin modest.
    """
    xspan = max(x_range[1] - x_range[0], 1e-6)
    yspan = max(y_range[1] - y_range[0], 1e-6)
    height = int(round(width_px * yspan / xspan)) + 90
    return max(min_px, min(max_px, height))


def apply_equal_scale(fig, points, x_title="x/c", y_title="y/c", height=None, uirevision=None):
    """Lock a Plotly figure to equal x/y scale with padding around ``points``."""
    if not points:
        return fig
    x_range, y_range = bounds(points)
    if height is None:
        height = geometry_height(x_range, y_range)
    fig.update_layout(
        xaxis=dict(
            title=x_title,
            range=list(x_range),
            constrain="domain",
            zeroline=False,
        ),
        yaxis=dict(
            title=y_title,
            range=list(y_range),
            scaleanchor="x",
            scaleratio=1,
            constrain="domain",
            zeroline=False,
        ),
        height=height,
        uirevision=uirevision,
    )
    # Set again through the axis API. Some Plotly versions drop scaleratio
    # when it is only present on the layout dict built above.
    fig.update_yaxes(scaleanchor="x", scaleratio=1, constrain="domain")
    fig.update_xaxes(constrain="domain")
    return fig


def leading_edge_points(clean, ice, nose_fraction=0.22):
    """Points that belong in a leading-edge close-up.

    Includes everything within ``nose_fraction`` of the clean leading edge
    in x, plus any iced point that is radially inside that fraction (so a
    horn that sits slightly farther aft is not clipped).
    """
    clean = list(clean or [])
    ice = list(ice or [])
    pool = clean + ice
    if not pool:
        return []
    x_le = min(p[0] for p in (clean or pool))
    y_le = min(clean or pool, key=lambda p: p[0])[1]
    x_cut = x_le + nose_fraction
    selected = [p for p in pool if p[0] <= x_cut]
    for p in ice:
        if math.hypot(p[0] - x_le, p[1] - y_le) <= nose_fraction + 0.02:
            selected.append(p)
    if len(selected) < 4:
        return pool
    return selected


def configure_equal_axes(ax, points, title=""):
    """Matplotlib equivalent of apply_equal_scale. Returns the padded ranges."""
    x_range, y_range = bounds(points)
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x/c")
    ax.set_ylabel("y/c")
    if title:
        ax.set_title(title)
    return x_range, y_range
