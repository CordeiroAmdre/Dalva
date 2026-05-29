"""LLM-backed ECharts option generation from SQL query results."""

from __future__ import annotations

import json
import logging
import re

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage

from dalva_backend.models.chat import ChartSpec
from dalva_backend.prompts.chart_option import chart_option_prompt
from dalva_backend.repositories.database_repository import QueryExecution, QueryStatus
from dalva_backend.services.chart_option_validator import validate_echarts_option

logger = logging.getLogger(__name__)

_JSON_FENCE_PATTERN = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


class ChartOptionRepository:
    """Generate ECharts option JSON via LangChain (no business rules here)."""

    def __init__(self, llm: BaseChatModel) -> None:
        self._chain = chart_option_prompt | llm

    def generate(
        self,
        message: str,
        query_log: list[QueryExecution],
    ) -> ChartSpec | None:
        query_data = _format_query_log(query_log)
        if not query_data:
            return None
        try:
            result = self._chain.invoke(
                {"message": message, "query_data": query_data},
            )
        except Exception:
            logger.exception("Chart option LLM invocation failed")
            return None

        content = _extract_content(result)
        option = _parse_option_json(content)
        validated = validate_echarts_option(option)
        if validated is None:
            logger.info("Chart option rejected by validator")
            return None
        return ChartSpec(option=validated)


def _format_query_log(query_log: list[QueryExecution]) -> str:
    blocks: list[str] = []
    for entry in query_log:
        if entry.status != QueryStatus.SUCCESS:
            continue
        blocks.append(
            f"SQL: {entry.sql}\nRows: {entry.row_count}\nPreview:\n{entry.result_preview}"
        )
    return "\n\n---\n\n".join(blocks)


def _extract_content(result: object) -> str:
    if isinstance(result, AIMessage):
        content = result.content
    elif hasattr(result, "content"):
        content = result.content
    else:
        content = str(result)
    return content if isinstance(content, str) else str(content)


def _parse_option_json(content: str) -> object | None:
    cleaned = _JSON_FENCE_PATTERN.sub("", content.strip())
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger.info("Chart option response is not valid JSON")
        return None
