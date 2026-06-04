"""Validate and sanitize ECharts option payloads returned to the frontend."""

from __future__ import annotations

import json
from typing import Any

_MAX_OPTION_BYTES = 50_000
_MAX_SERIES = 8
_FORBIDDEN_SUBSTRINGS = ("javascript:", "<script", "function(", "=>")


def validate_echarts_option(option: Any) -> dict[str, Any] | None:
    if not isinstance(option, dict):
        return None
    if "series" not in option or not isinstance(option["series"], list):
        return None
    if not option["series"]:
        return None
    if len(option["series"]) > _MAX_SERIES:
        return None
    if len(json.dumps(option, default=str)) > _MAX_OPTION_BYTES:
        return None
    if _contains_forbidden_content(option):
        return None
    return option


def _contains_forbidden_content(value: Any) -> bool:
    if isinstance(value, str):
        lowered = value.lower()
        return any(token in lowered for token in _FORBIDDEN_SUBSTRINGS)
    if isinstance(value, dict):
        return any(_contains_forbidden_content(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_content(item) for item in value)
    return False
