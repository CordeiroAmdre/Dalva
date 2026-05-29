from pathlib import Path

import duckdb

from dalva_backend.repositories.database_repository import DatabaseRepository
from dalva_backend.repositories.readonly_sql_database import ReadOnlySQLDatabase


def _create_db_with_foreign_keys(path: Path) -> None:
    conn = duckdb.connect(str(path))
    conn.execute("CREATE SCHEMA pdv")
    conn.execute(
        """
        CREATE TABLE pdv.formas_pagamento (
            id INTEGER PRIMARY KEY,
            nome VARCHAR NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE pdv.vendas (
            id INTEGER PRIMARY KEY,
            forma_pagamento_id INTEGER NOT NULL,
            FOREIGN KEY (forma_pagamento_id) REFERENCES pdv.formas_pagamento (id)
        )
        """
    )
    conn.close()


def test_get_table_info_omits_foreign_keys(tmp_path: Path) -> None:
    db_path = tmp_path / "test.duckdb"
    _create_db_with_foreign_keys(db_path)

    database_url = f"duckdb:///{db_path}"
    db_repo = DatabaseRepository(database_url=database_url, schema="pdv")
    sql_db = ReadOnlySQLDatabase.from_uri(
        database_url,
        database_repository=db_repo,
        schema="pdv",
        include_tables=["vendas", "formas_pagamento"],
    )

    info = sql_db.get_table_info(["vendas", "formas_pagamento"])

    assert "CREATE TABLE" in info
    assert "forma_pagamento_id" in info
    assert "FOREIGN KEY" not in info
