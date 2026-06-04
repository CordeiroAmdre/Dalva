from pathlib import Path

import duckdb
import pytest

from dalva_backend.scripts import init_db


def test_init_database_creates_file_and_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "test.duckdb"
    result = init_db.init_database(db_path)

    assert result == db_path
    assert db_path.is_file()

    conn = duckdb.connect(str(db_path))
    try:
        tables = {
            row[0]
            for row in conn.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'pdv'
                """
            ).fetchall()
        }
        assert "produtos" in tables
        assert "vendas" in tables
        product_count = conn.execute(
            "SELECT COUNT(*) FROM pdv.produtos"
        ).fetchone()[0]
        assert product_count > 0
        sale_count = conn.execute("SELECT COUNT(*) FROM pdv.vendas").fetchone()[0]
        assert sale_count == 2500
    finally:
        conn.close()


def test_init_database_refuses_overwrite_without_force(tmp_path: Path) -> None:
    db_path = tmp_path / "test.duckdb"
    init_db.init_database(db_path)
    with pytest.raises(FileExistsError):
        init_db.init_database(db_path)


def test_init_database_force_recreates(tmp_path: Path) -> None:
    db_path = tmp_path / "test.duckdb"
    init_db.init_database(db_path)
    init_db.init_database(db_path, force=True)
    assert db_path.is_file()
