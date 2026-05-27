"""Read-only SQL execution against PostgreSQL with limits and audit metadata."""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from enum import StrEnum

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from dalva_backend.repositories.sql_validator import SqlValidationError, validate_readonly_sql

logger = logging.getLogger(__name__)

_TABLE_PATTERN = re.compile(
    r"\b(?:FROM|JOIN|INTO|UPDATE)\s+([a-zA-Z_][\w.]*)",
    re.IGNORECASE,
)


class QueryStatus(StrEnum):
    SUCCESS = "success"
    BLOCKED = "blocked"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class QueryExecution:
    sql: str
    status: QueryStatus
    row_count: int = 0
    duration_ms: int = 0
    blocked_reason: str | None = None
    result_preview: str = ""


@dataclass
class DatabaseRepository:
    database_url: str
    schema: str = "pdv"
    query_timeout_sec: int = 10
    max_rows: int = 100
    _engine: Engine | None = field(default=None, init=False, repr=False)
    _query_log: list[QueryExecution] = field(default_factory=list, init=False, repr=False)

    def clear_query_log(self) -> None:
        self._query_log.clear()

    @property
    def query_log(self) -> list[QueryExecution]:
        return list(self._query_log)

    def data_sources(self) -> list[str]:
        sources: set[str] = set()
        for entry in self._query_log:
            if entry.status != QueryStatus.SUCCESS:
                continue
            for match in _TABLE_PATTERN.finditer(entry.sql):
                name = match.group(1)
                if "." not in name:
                    name = f"{self.schema}.{name}"
                sources.add(name.lower())
        return sorted(sources)

    def _get_engine(self) -> Engine:
        if self._engine is None:
            self._engine = create_engine(
                self.database_url,
                pool_pre_ping=True,
            )
        return self._engine

    def execute_readonly(self, sql: str, fetch: str = "all") -> str:
        """Run validated read-only SQL and return a string for the agent."""
        started = time.perf_counter()
        execution = QueryExecution(sql=sql, status=QueryStatus.ERROR)

        try:
            validate_readonly_sql(sql)
        except SqlValidationError as exc:
            execution.status = QueryStatus.BLOCKED
            execution.blocked_reason = str(exc)
            execution.duration_ms = int((time.perf_counter() - started) * 1000)
            self._query_log.append(execution)
            logger.info(
                "SQL blocked",
                extra={
                    "status": execution.status,
                    "duration_ms": execution.duration_ms,
                    "reason": execution.blocked_reason,
                },
            )
            return f"Error: {exc}"

        timeout_ms = self.query_timeout_sec * 1000
        try:
            engine = self._get_engine()
            with engine.connect() as conn:
                conn.execute(text(f"SET statement_timeout = {timeout_ms}"))
                conn.execute(text(f"SET search_path TO {self.schema}, public"))
                result = conn.execute(text(sql))
                if fetch == "one":
                    row = result.fetchone()
                    rows = [row] if row else []
                else:
                    rows = result.fetchmany(self.max_rows + 1)

            truncated = len(rows) > self.max_rows
            if truncated:
                rows = rows[: self.max_rows]

            preview = _format_rows(rows, truncated=truncated)
            execution.status = QueryStatus.SUCCESS
            execution.row_count = len(rows)
            execution.result_preview = preview
            execution.duration_ms = int((time.perf_counter() - started) * 1000)
            self._query_log.append(execution)
            logger.info(
                "SQL executed",
                extra={
                    "status": execution.status,
                    "row_count": execution.row_count,
                    "duration_ms": execution.duration_ms,
                },
            )
            return preview
        except Exception as exc:
            message = str(exc).lower()
            if "timeout" in message or "canceling statement" in message:
                execution.status = QueryStatus.TIMEOUT
            else:
                execution.status = QueryStatus.ERROR
            execution.duration_ms = int((time.perf_counter() - started) * 1000)
            execution.blocked_reason = "Query failed"
            self._query_log.append(execution)
            logger.info(
                "SQL failed",
                extra={
                    "status": execution.status,
                    "duration_ms": execution.duration_ms,
                },
            )
            return f"Error: {exc}"


def _format_rows(rows: list, *, truncated: bool) -> str:
    if not rows:
        return "No rows returned."
    lines = [str(tuple(row)) for row in rows]
    if truncated:
        lines.append("(Results truncated to row limit.)")
    return "\n".join(lines)
