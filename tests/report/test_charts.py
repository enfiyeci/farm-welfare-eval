from __future__ import annotations

import math
import xml.etree.ElementTree as ET

import pytest

from farm_eval.report import charts


CHART_CASES = [
    (charts.horizontal_bars, ({"a": 0.2, "b": 0.1},), {"scale_max": 1.0}),
    (charts.grouped_horizontal_bars, ({"current": {"a": 2}, "prior": {"a": 1}},), {}),
    (charts.line_chart, ({"current": [{"day": 0, "value": 1}, {"day": 8, "value": 2}]},), {}),
    (charts.node_score_strip, ({"DP01": 9.0, "DP02": 4.0},), {"variance": {"DP01": {"min": 8, "max": 10}}}),
    (charts.delta_bars, ({"DP01": 2.0, "DP02": -1.0},), {}),
]


@pytest.mark.parametrize(("fn", "args", "kwargs"), CHART_CASES)
def test_chart_svg_is_well_formed_and_finite(fn, args, kwargs) -> None:
    svg = fn(*args, **kwargs)
    root = ET.fromstring(svg)
    assert root.tag.endswith("svg")
    assert "NaN" not in svg and "Infinity" not in svg
    assert "<title>" in svg


@pytest.mark.parametrize(("fn", "args", "kwargs"), [
    (charts.horizontal_bars, ({},), {}),
    (charts.grouped_horizontal_bars, ({},), {}),
    (charts.line_chart, ({"empty": []},), {}),
    (charts.node_score_strip, ({},), {}),
    (charts.delta_bars, ({},), {}),
])
def test_chart_svg_handles_empty_and_degenerate_series(fn, args, kwargs) -> None:
    svg = fn(*args, **kwargs)
    ET.fromstring(svg)
    assert "NaN" not in svg and "Infinity" not in svg


def test_line_chart_wraps_eight_unique_series_within_viewbox() -> None:
    names = [f"dimension_{index}" for index in range(8)]
    svg = charts.line_chart(
        {name: [{"day": 0, "value": index}, {"day": 1, "value": index + 1}] for index, name in enumerate(names)}
    )

    root = ET.fromstring(svg)
    _, _, width, height = (float(value) for value in root.attrib["viewBox"].split())
    legend_labels = [element for element in root.findall("text") if element.text in names]
    strokes = {element.attrib["stroke"] for element in root.findall("polyline")}

    assert len(legend_labels) == 8
    assert all(
        0 <= float(label.attrib["x"])
        and float(label.attrib["x"]) + len(label.text or "") * 7 <= width
        for label in legend_labels
    )
    assert len(strokes) == 8
    assert height > 270
