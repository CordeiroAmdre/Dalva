"""Validate that generated SQL is read-only before execution."""

from __future__ import annotations

import re

import sqlparse

FORBIDDEN_KEYWORDS = frozenset(
    {
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "GRANT",
        "REVOKE",
        "COPY",
        "CALL",
        "EXEC",
        "EXECUTE",
        "MERGE",
        "REPLACE",
    }
)

_COMMENT_PATTERN = re.compile(r"--.*?$|/\*.*?\*/", re.MULTILINE | re.DOTALL)


class SqlValidationError(ValueError):
    """Raised when SQL fails read-only policy checks."""


def _strip_comments(sql: str) -> str:
    return _COMMENT_PATTERN.sub(" ", sql)


def _leading_keyword(sql: str) -> str | None:
    stripped = sql.lstrip()
    for keyword in ("WITH", "EXPLAIN", "SELECT"):
        if stripped.upper().startswith(keyword):
            return keyword
    return None


def validate_readonly_sql(sql: str) -> None:
    """Ensure SQL is a single read-only statement (SELECT / WITH / EXPLAIN)."""
    cleaned = _strip_comments(sql).strip()
    if not cleaned:
        msg = "Empty SQL statement."
        raise SqlValidationError(msg)

    upper = cleaned.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper):
            msg = f"Forbidden SQL keyword: {keyword}"
            raise SqlValidationError(msg)

    statements = [s for s in sqlparse.parse(cleaned) if s.tokens]
    if len(statements) != 1:
        msg = "Only a single SQL statement is allowed per request."
        raise SqlValidationError(msg)

    first = _leading_keyword(cleaned)
    if first not in {"SELECT", "WITH", "EXPLAIN"}:
        msg = "Only SELECT, WITH, or EXPLAIN statements are allowed."
        raise SqlValidationError(msg)
