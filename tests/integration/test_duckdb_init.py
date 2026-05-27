from pathlib import Path

import duckdb
import pytest

from dalva_backend.scripts import init_db


@pytest.fixture
def seeded_duckdb(tmp_path: Path) -> Path:
    db_path = tmp_path / "pdv_ai.duckdb"
    init_db.init_database(db_path)
    return db_path


def test_seeded_duckdb_has_queryable_products(seeded_duckdb: Path) -> None:
    conn = duckdb.connect(str(seeded_duckdb))
    try:
        row = conn.execute(
            "SELECT nome, preco FROM pdv.produtos WHERE nome = 'Leite Integral 1L'"
        ).fetchone()
        assert row is not None
        assert row[0] == "Leite Integral 1L"
        assert float(row[1]) == pytest.approx(4.89)
    finally:
        conn.close()


def test_seeded_duckdb_view_returns_rows(seeded_duckdb: Path) -> None:
    conn = duckdb.connect(str(seeded_duckdb))
    try:
        count = conn.execute(
            "SELECT COUNT(*) FROM pdv.vw_vendas_detalhadas"
        ).fetchone()[0]
        assert count > 0
    finally:
        conn.close()
