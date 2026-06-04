"""Resolve chart payloads for data-backed chat responses."""

from __future__ import annotations

import re

from dalva_backend.models.chat import ChartSpec
from dalva_backend.repositories.chart_option_repository import ChartOptionRepository
from dalva_backend.repositories.database_repository import QueryExecution, QueryStatus
from dalva_backend.services.chart_builder import ChartBuilder

_VISUALIZATION_PATTERN = re.compile(
    r"\b("
    r"gr[aá]fico|chart|plot|boxplot|box\s*plot|visualiz|histograma|"
    r"scatter|heatmap|dispers|barras|pizza|linha|pie|bar|line"
    r")\b",
    re.IGNORECASE,
)
_CHART_TYPE_PATTERN = re.compile(
    r"\b("
    r"boxplot|box\s*plot|"
    r"scatter|dispers[aã]o|"
    r"heatmap|mapa\s+de\s+calor|"
    r"pie|pizza|"
    r"bar|barras|histograma|"
    r"line|linha|"
    r"radar|treemap|sunburst|funnel|funil|sankey|gauge"
    r")\b",
    re.IGNORECASE,
)

_CHART_TYPE_ALIASES: dict[str, str] = {
    "boxplot": "boxplot",
    "box": "boxplot",
    "scatter": "scatter",
    "dispersão": "scatter",
    "dispersao": "scatter",
    "heatmap": "heatmap",
    "mapadecalor": "heatmap",
    "pie": "pie",
    "pizza": "pie",
    "bar": "bar",
    "barras": "bar",
    "histograma": "bar",
    "line": "line",
    "linha": "line",
    "radar": "radar",
    "treemap": "treemap",
    "sunburst": "sunburst",
    "funnel": "funnel",
    "funil": "funnel",
    "sankey": "sankey",
    "gauge": "gauge",
}


def resolve_chart(
    message: str,
    query_log: list[QueryExecution],
    chart_option_repository: ChartOptionRepository,
) -> ChartSpec | None:
    if count_distinct_requested_chart_types(message) > 1:
        return None

    requested_type = detect_requested_chart_type(message)
    heuristic = ChartBuilder.from_query_log(query_log)

    if heuristic is not None and requested_type is not None:
        actual_type = _series_type(heuristic)
        if actual_type != requested_type:
            heuristic = None

    if heuristic is not None:
        return heuristic

    if not should_attempt_chart(message):
        return None
    if not _has_successful_query(query_log):
        return None

    return chart_option_repository.generate(
        message,
        query_log,
        requested_chart_type=requested_type,
    )


def message_requests_visualization(message: str) -> bool:
    return _VISUALIZATION_PATTERN.search(message) is not None


def iter_requested_chart_types(message: str) -> set[str]:
    types: set[str] = set()
    for match in _CHART_TYPE_PATTERN.finditer(message):
        token = match.group(1).lower().replace(" ", "")
        canonical = _CHART_TYPE_ALIASES.get(token, token)
        types.add(canonical)
    return types


def count_distinct_requested_chart_types(message: str) -> int:
    return len(iter_requested_chart_types(message))


def detect_requested_chart_type(message: str) -> str | None:
    types = iter_requested_chart_types(message)
    if len(types) == 1:
        return next(iter(types))
    return None


def should_attempt_chart(message: str) -> bool:
    distinct = count_distinct_requested_chart_types(message)
    if distinct > 1:
        return False
    return message_requests_visualization(message) or distinct == 1


def _series_type(chart: ChartSpec) -> str | None:
    series = chart.option.get("series")
    if not isinstance(series, list) or not series:
        return None
    first = series[0]
    if isinstance(first, dict):
        chart_type = first.get("type")
        return chart_type if isinstance(chart_type, str) else None
    return None


def _has_successful_query(query_log: list[QueryExecution]) -> bool:
    return any(entry.status == QueryStatus.SUCCESS for entry in query_log)
