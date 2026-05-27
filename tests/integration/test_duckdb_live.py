from pathlib import Path

import pytest

from dalva_backend.repositories.database_repository import DatabaseRepository, QueryStatus


@pytest.mark.db
def test_live_duckdb_readonly_select(duckdb_file: Path) -> None:
    url = f"duckdb:///{duckdb_file}"
    repo = DatabaseRepository(database_url=url, schema="pdv", max_rows=5)
    result = repo.execute_readonly(
        "SELECT nome FROM pdv.produtos WHERE nome = 'Leite Integral 1L'"
    )
    assert "Leite Integral 1L" in result
    assert repo.query_log[0].status == QueryStatus.SUCCESS


@pytest.mark.db
def test_live_duckdb_blocks_delete(duckdb_file: Path) -> None:
    url = f"duckdb:///{duckdb_file}"
    repo = DatabaseRepository(database_url=url, schema="pdv")
    result = repo.execute_readonly("DELETE FROM pdv.vendas")
    assert "Error" in result
    assert repo.query_log[0].status == QueryStatus.BLOCKED
