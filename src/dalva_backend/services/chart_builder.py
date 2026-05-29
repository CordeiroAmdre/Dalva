"""Derive ECharts option objects from read-only query result previews."""

from __future__ import annotations

import ast
import re
from decimal import Decimal

from dalva_backend.models.chat import ChartSpec
from dalva_backend.repositories.database_repository import QueryExecution, QueryStatus

_MAX_CHART_ROWS = 12
_PIE_MAX_CATEGORIES = 8
_MIN_BOXPLOT_VALUES = 5
_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}")
_DECIMAL_PREVIEW = re.compile(r"Decimal\('([^']+)'\)")


class ChartBuilder:
    """Build ChartSpec instances from successful query log entries."""

    @staticmethod
    def from_query_log(entries: list[QueryExecution]) -> ChartSpec | None:
        successful = [
            entry
            for entry in entries
            if entry.status == QueryStatus.SUCCESS and entry.row_count >= 1
        ]
        for entry in reversed(successful):
            chart = ChartBuilder.from_result_preview(entry.result_preview)
            if chart is not None:
                return chart
        return None

    @staticmethod
    def from_result_preview(preview: str) -> ChartSpec | None:
        categorical = _build_categorical_chart(preview)
        if categorical is not None:
            return categorical
        return _build_boxplot_chart(preview)


def _build_categorical_chart(preview: str) -> ChartSpec | None:
    rows = _parse_preview_rows(preview)
    if len(rows) < 2:
        return None

    labels: list[str] = []
    values: list[float] = []
    for row in rows:
        mapped = _row_to_label_value(row)
        if mapped is None:
            continue
        label, value = mapped
        labels.append(label)
        values.append(value)

    if len(labels) < 2:
        return None

    if len(labels) > _MAX_CHART_ROWS:
        labels = labels[:_MAX_CHART_ROWS]
        values = values[:_MAX_CHART_ROWS]

    chart_type = _infer_chart_type(labels)
    if chart_type == "pie" and len(labels) > _PIE_MAX_CATEGORIES:
        chart_type = "bar"

    return ChartSpec(option=_categorical_option(chart_type, labels, values))


def _build_boxplot_chart(preview: str) -> ChartSpec | None:
    values: list[float] = []
    for row in _parse_preview_rows(preview):
        numeric = _coerce_float(row[-1]) if row else None
        if numeric is None:
            continue
        if len(row) == 1:
            values.append(numeric)
            continue
        if _row_to_label_value(row) is not None:
            continue
        values.append(numeric)

    if len(values) < _MIN_BOXPLOT_VALUES:
        return None

    stats = _five_number_summary(values)
    if stats is None:
        return None

    return ChartSpec(
        option={
            "title": {"text": "Distribuição dos valores"},
            "tooltip": {"trigger": "item", "axisPointer": {"type": "shadow"}},
            "grid": {"left": 48, "right": 24, "bottom": 48, "containLabel": True},
            "xAxis": {"type": "category", "data": ["Valores"], "boundaryGap": True},
            "yAxis": {"type": "value", "name": "Valor"},
            "series": [{"name": "Distribuição", "type": "boxplot", "data": [stats]}],
        }
    )


def _categorical_option(
    chart_type: str,
    labels: list[str],
    values: list[float],
) -> dict[str, object]:
    if chart_type == "pie":
        return {
            "tooltip": {"trigger": "item"},
            "series": [
                {
                    "type": "pie",
                    "radius": "60%",
                    "data": [
                        {"name": label, "value": value}
                        for label, value in zip(labels, values, strict=True)
                    ],
                }
            ],
        }

    return {
        "tooltip": {"trigger": "axis"},
        "grid": {
            "left": 48,
            "right": 24,
            "bottom": 80 if len(labels) > 4 else 48,
            "containLabel": True,
        },
        "xAxis": {
            "type": "category",
            "data": labels,
            "axisLabel": {"rotate": 30 if len(labels) > 4 else 0},
        },
        "yAxis": {"type": "value"},
        "series": [{"name": "Valor", "type": chart_type, "data": values}],
    }


def _parse_preview_rows(preview: str) -> list[tuple[object, ...]]:
    parsed: list[tuple[object, ...]] = []
    for line in preview.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("(Results truncated"):
            continue
        row = _parse_preview_row(stripped)
        if row is not None:
            parsed.append(row)
    return parsed


def _parse_preview_row(stripped: str) -> tuple[object, ...] | None:
    try:
        row = ast.literal_eval(stripped)
    except (SyntaxError, ValueError):
        normalized = _DECIMAL_PREVIEW.sub(r"\1", stripped)
        try:
            row = ast.literal_eval(normalized)
        except (SyntaxError, ValueError):
            return None
    if isinstance(row, tuple) and len(row) >= 1:
        return row
    return None


def _row_to_label_value(cells: tuple[object, ...]) -> tuple[str, float] | None:
    text_parts: list[str] = []
    numeric_values: list[float] = []

    for cell in cells:
        numeric = _coerce_float(cell)
        if numeric is not None:
            numeric_values.append(numeric)
        else:
            text_parts.append(str(cell))

    if numeric_values and text_parts:
        return " — ".join(text_parts), numeric_values[-1]

    if len(cells) == 2:
        direct_numeric = _coerce_float(cells[1])
        if direct_numeric is not None:
            return str(cells[0]), direct_numeric

    return None


def _coerce_float(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, Decimal):
        return float(value)
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _infer_chart_type(labels: list[str]) -> str:
    if any(" — " in label for label in labels):
        return "bar"
    date_like = sum(1 for label in labels if _looks_like_date(label))
    if date_like >= max(2, int(len(labels) * 0.6)):
        return "line"
    if len(labels) <= _PIE_MAX_CATEGORIES:
        return "pie"
    return "bar"


def _looks_like_date(label: str) -> bool:
    return bool(_DATE_PATTERN.match(label.strip()))


def _five_number_summary(values: list[float]) -> list[float] | None:
    if len(values) < 2:
        return None
    sorted_values = sorted(values)
    count = len(sorted_values)

    def percentile(proportion: float) -> float:
        position = (count - 1) * proportion
        lower = int(position)
        upper = min(lower + 1, count - 1)
        weight = position - lower
        return sorted_values[lower] + weight * (sorted_values[upper] - sorted_values[lower])

    return [
        sorted_values[0],
        percentile(0.25),
        percentile(0.5),
        percentile(0.75),
        sorted_values[-1],
    ]
