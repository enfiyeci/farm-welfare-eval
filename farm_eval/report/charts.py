from __future__ import annotations

import html
import math
from collections.abc import Mapping, Sequence


_COLORS = ("var(--chart-1)", "var(--chart-2)", "var(--chart-3)", "var(--chart-4)", "var(--chart-5)")


def _finite(value: object, default: float = 0.0) -> float:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def _svg(body: str, *, title: str, width: int, height: int) -> str:
    label = html.escape(title)
    return (
        f'<svg role="img" aria-label="{label}" '
        f'viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMin meet">'
        f"<title>{label}</title>{body}</svg>"
    )


def _empty(title: str, width: int = 760, height: int = 110) -> str:
    return _svg(
        '<text x="20" y="58" class="chart-empty">No data available</text>',
        title=title,
        width=width,
        height=height,
    )


def horizontal_bars(
    values: Mapping[str, float], *, title: str = "Horizontal bar chart",
    normalize: bool = False, scale_max: float | None = None,
) -> str:
    rows = [(str(key), max(0.0, _finite(value))) for key, value in values.items()]
    if not rows:
        return _empty(title)
    width, left, right, row_h = 760, 210, 55, 30
    height = 42 + row_h * len(rows)
    maximum = _finite(scale_max) if scale_max is not None else max((value for _, value in rows), default=0.0)
    maximum = maximum if maximum > 0 else 1.0
    parts = []
    for index, (label, value) in enumerate(rows):
        y = 28 + index * row_h
        ratio = min(1.0, value / maximum) if maximum else 0.0
        bar_width = ratio * (width - left - right)
        shown = f"{value:.3g}"
        parts.extend(
            [
                f'<text x="{left - 8}" y="{y + 13}" text-anchor="end">{html.escape(label)}</text>',
                f'<rect x="{left}" y="{y}" width="{bar_width:.3f}" height="18" rx="3" fill="var(--chart-1)">'
                f"<title>{html.escape(label)}: {shown}</title></rect>",
                f'<text x="{min(width - right + 6, left + bar_width + 6):.3f}" y="{y + 13}">{shown}</text>',
            ]
        )
    return _svg("".join(parts), title=title, width=width, height=height)


def grouped_horizontal_bars(
    series: Mapping[str, Mapping[str, float]], *, title: str = "Grouped horizontal bar chart"
) -> str:
    names = list(series)
    categories = sorted({category for values in series.values() for category in values})
    if not names or not categories:
        return _empty(title)
    width, left, right = 820, 210, 55
    bar_h, group_gap = 12, 12
    group_h = len(names) * bar_h + group_gap
    height = 54 + len(categories) * group_h + 24
    maximum = max((_finite(series[name].get(category)) for name in names for category in categories), default=0.0) or 1.0
    parts = []
    for cat_index, category in enumerate(categories):
        base_y = 34 + cat_index * group_h
        parts.append(f'<text x="{left - 8}" y="{base_y + 10}" text-anchor="end">{html.escape(category)}</text>')
        for series_index, name in enumerate(names):
            value = max(0.0, _finite(series[name].get(category)))
            y = base_y + series_index * bar_h
            bar_width = value / maximum * (width - left - right)
            color = _COLORS[series_index % len(_COLORS)]
            parts.append(
                f'<rect x="{left}" y="{y}" width="{bar_width:.3f}" height="9" rx="2" fill="{color}">'
                f"<title>{html.escape(name)} · {html.escape(category)}: {value:.3g}</title></rect>"
            )
    legend_x = left
    for index, name in enumerate(names):
        color = _COLORS[index % len(_COLORS)]
        parts.append(f'<circle cx="{legend_x}" cy="{height - 12}" r="5" fill="{color}"/>')
        parts.append(f'<text x="{legend_x + 9}" y="{height - 8}">{html.escape(name)}</text>')
        legend_x += max(100, len(name) * 8 + 32)
    return _svg("".join(parts), title=title, width=width, height=height)


def line_chart(
    series: Mapping[str, Sequence[Mapping[str, float]]],
    *,
    title: str = "Line chart",
    x_key: str = "day",
    y_key: str = "value",
    marker_day: float | None = None,
    break_gaps: bool = False,
) -> str:
    clean: dict[str, list[tuple[float, float]]] = {}
    for name, points in series.items():
        values = [(_finite(point.get(x_key)), _finite(point.get(y_key))) for point in points]
        if values:
            clean[str(name)] = values
    if not clean:
        return _empty(title)
    width, height, left, right, top, bottom = 820, 270, 62, 24, 24, 46
    all_points = [point for points in clean.values() for point in points]
    min_x, max_x = min(x for x, _ in all_points), max(x for x, _ in all_points)
    min_y, max_y = min(y for _, y in all_points), max(y for _, y in all_points)
    if max_x == min_x:
        max_x = min_x + 1.0
    if max_y == min_y:
        pad = abs(min_y) * 0.1 or 1.0
        min_y, max_y = min_y - pad, max_y + pad

    def px(x: float) -> float:
        return left + (x - min_x) / (max_x - min_x) * (width - left - right)

    def py(y: float) -> float:
        return top + (max_y - y) / (max_y - min_y) * (height - top - bottom)

    parts = [
        f'<line x1="{left}" y1="{height - bottom}" x2="{width - right}" y2="{height - bottom}" class="axis"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height - bottom}" class="axis"/>',
        f'<text x="{left}" y="{height - 17}">{min_x:.0f}</text>',
        f'<text x="{width - right}" y="{height - 17}" text-anchor="end">{max_x:.0f}</text>',
        f'<text x="{left - 8}" y="{top + 5}" text-anchor="end">{max_y:.3g}</text>',
        f'<text x="{left - 8}" y="{height - bottom}" text-anchor="end">{min_y:.3g}</text>',
    ]
    if marker_day is not None and min_x <= _finite(marker_day) <= max_x:
        marker_x = px(_finite(marker_day))
        parts.append(f'<line x1="{marker_x:.3f}" y1="{top}" x2="{marker_x:.3f}" y2="{height - bottom}" class="marker"><title>Attention midpoint: day {marker_day:g}</title></line>')
    for index, (name, points) in enumerate(clean.items()):
        color = _COLORS[index % len(_COLORS)]
        segments: list[list[tuple[float, float]]] = [[]]
        for point in points:
            if break_gaps and segments[-1] and point[0] - segments[-1][-1][0] > 1.0:
                segments.append([])
            segments[-1].append(point)
        for segment in segments:
            coordinates = " ".join(f"{px(x):.3f},{py(y):.3f}" for x, y in segment)
            parts.append(f'<polyline points="{coordinates}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        for x, y in points:
            parts.append(
                f'<circle cx="{px(x):.3f}" cy="{py(y):.3f}" r="3.5" fill="{color}">'
                f"<title>{html.escape(name)} · day {x:g}: {y:.3g}</title></circle>"
            )
        parts.append(f'<text x="{left + index * 145}" y="{height - 3}" fill="{color}">{html.escape(name)}</text>')
    return _svg("".join(parts), title=title, width=width, height=height)


def node_score_strip(
    scores: Mapping[str, float],
    *,
    variance: Mapping[str, Mapping[str, float]] | None = None,
    title: str = "Per-node score strip",
) -> str:
    if not scores:
        return _empty(title)
    rows = list(scores.items())
    width, left, right, row_h = 760, 190, 35, 26
    height = 36 + len(rows) * row_h
    span = width - left - right
    parts = []
    for index, (node, raw_score) in enumerate(rows):
        score = min(10.0, max(0.0, _finite(raw_score)))
        y = 24 + index * row_h
        parts.append(f'<text x="{left - 8}" y="{y + 5}" text-anchor="end">{html.escape(node)}</text>')
        parts.append(f'<line x1="{left}" y1="{y}" x2="{width - right}" y2="{y}" class="grid"/>')
        bounds = (variance or {}).get(node)
        low = _finite(bounds.get("min", score), score) if bounds else score
        high = _finite(bounds.get("max", score), score) if bounds else score
        if bounds:
            parts.append(f'<line x1="{left + low / 10 * span:.3f}" y1="{y}" x2="{left + high / 10 * span:.3f}" y2="{y}" stroke="var(--muted)" stroke-width="5"/>')
        x = left + score / 10 * span
        parts.append(f'<circle cx="{x:.3f}" cy="{y}" r="6" fill="var(--chart-1)"><title>{html.escape(node)}: {score:.2f} (range {low:.2f}–{high:.2f})</title></circle>')
    return _svg("".join(parts), title=title, width=width, height=height)


def delta_bars(values: Mapping[str, float], *, title: str = "Cross-run deltas") -> str:
    rows = [(str(key), _finite(value)) for key, value in values.items()]
    if not rows:
        return _empty(title)
    width, left, right, row_h = 760, 190, 55, 27
    height = 36 + len(rows) * row_h
    center = left + (width - left - right) / 2
    half = (width - left - right) / 2
    maximum = max((abs(value) for _, value in rows), default=0.0) or 1.0
    parts = [f'<line x1="{center:.3f}" y1="12" x2="{center:.3f}" y2="{height - 12}" class="axis"/>']
    for index, (label, value) in enumerate(rows):
        y = 18 + index * row_h
        extent = abs(value) / maximum * half
        x = center if value >= 0 else center - extent
        color = "var(--positive)" if value >= 0 else "var(--negative)"
        parts.append(f'<text x="{left - 8}" y="{y + 13}" text-anchor="end">{html.escape(label)}</text>')
        parts.append(f'<rect x="{x:.3f}" y="{y}" width="{extent:.3f}" height="17" rx="2" fill="{color}"><title>{html.escape(label)}: {value:+.3g}</title></rect>')
    return _svg("".join(parts), title=title, width=width, height=height)
