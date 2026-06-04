"""Tests for monorepo path helpers."""

from pathlib import Path

from dalva_backend.paths import backend_dir, find_repo_root, resolve_duckdb_url


def test_find_repo_root_has_docker_duckdb() -> None:
    root = find_repo_root()
    assert (root / "docker" / "duckdb").is_dir()


def test_backend_dir() -> None:
    root = find_repo_root()
    assert backend_dir() == root / "backend"
    assert (backend_dir() / "src" / "dalva_backend").is_dir()


def test_resolve_duckdb_url_maps_data_to_repo_root() -> None:
    root = find_repo_root()
    resolved = resolve_duckdb_url("duckdb:///./data/pdv_ai.duckdb")
    assert resolved == f"duckdb:///{root / 'data' / 'pdv_ai.duckdb'}"


def test_resolve_duckdb_url_parent_data() -> None:
    root = find_repo_root()
    resolved = resolve_duckdb_url("duckdb:///../data/pdv_ai.duckdb")
    assert resolved == f"duckdb:///{root / 'data' / 'pdv_ai.duckdb'}"
