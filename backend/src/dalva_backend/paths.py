"""Monorepo path helpers for backend scripts and configuration."""

from __future__ import annotations

from pathlib import Path

_DUCKDB_MARKER = Path("docker") / "duckdb"


def find_repo_root(start: Path | None = None) -> Path:
    """Return the repository root (directory containing ``docker/duckdb``)."""
    current = (start or Path(__file__)).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / _DUCKDB_MARKER).is_dir():
            return candidate
    msg = f"Could not find monorepo root (missing {_DUCKDB_MARKER}) from {current}"
    raise FileNotFoundError(msg)


def backend_dir() -> Path:
    """Return the ``backend/`` project directory."""
    return find_repo_root() / "backend"


def resolve_duckdb_url(url: str | None) -> str | None:
    """Map repo-relative ``./data`` or ``../data`` DuckDB URLs to absolute paths."""
    if not url or not url.startswith("duckdb:///"):
        return url
    path_part = url.removeprefix("duckdb:///")
    data_prefixes = ("./data/", "../data/")
    for prefix in data_prefixes:
        if path_part.startswith(prefix):
            db_file = find_repo_root() / "data" / path_part[len(prefix) :]
            return f"duckdb:///{db_file}"
    return url
