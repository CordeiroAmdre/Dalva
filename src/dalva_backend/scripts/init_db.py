"""Initialize DuckDB PDV schema and static Parquet seed data."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb

REPO_ROOT = Path(__file__).resolve().parents[3]
INIT_DIR = REPO_ROOT / "docker" / "duckdb" / "init"
PARQUET_DIR = REPO_ROOT / "docker" / "duckdb" / "parquet"
DEFAULT_DB_PATH = REPO_ROOT / "data" / "pdv_ai.duckdb"
SCHEMA_FILE = "01-schema.sql"

PARQUET_TABLES: tuple[tuple[str, str], ...] = (
    ("categorias", "id, nome"),
    ("formas_pagamento", "id, nome"),
    ("lojas", "id, nome, cidade, uf"),
    ("caixas", "id, loja_id, numero"),
    ("produtos", "id, codigo_barras, nome, categoria_id, preco, ativo"),
    (
        "vendas",
        "id, data_hora, caixa_id, forma_pagamento_id, valor_total, desconto, status",
    ),
    (
        "itens_venda",
        "id, venda_id, produto_id, quantidade, preco_unitario, subtotal",
    ),
)


def _repo_root() -> Path:
    return REPO_ROOT


def _execute_sql_file(conn: duckdb.DuckDBPyConnection, path: Path) -> None:
    sql = path.read_text(encoding="utf-8")
    conn.execute(sql)


def _load_parquet_seed(conn: duckdb.DuckDBPyConnection) -> None:
    """Load all PDV tables from static Parquet files."""
    for table, columns in PARQUET_TABLES:
        parquet_path = PARQUET_DIR / f"{table}.parquet"
        if not parquet_path.is_file():
            msg = f"Missing Parquet seed: {parquet_path}. Run build_parquet.py first."
            raise FileNotFoundError(msg)
        conn.execute(
            f"""
            INSERT INTO pdv.{table} ({columns})
            SELECT {columns} FROM read_parquet(?)
            """,
            [str(parquet_path)],
        )


def init_database(db_path: Path | None = None, *, force: bool = False) -> Path:
    """Create DuckDB file from schema SQL and static Parquet seed files."""
    target = db_path or DEFAULT_DB_PATH
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        if not force:
            msg = f"Database already exists at {target}. Use --force to recreate."
            raise FileExistsError(msg)
        target.unlink()

    conn = duckdb.connect(str(target))
    try:
        schema_path = INIT_DIR / SCHEMA_FILE
        if not schema_path.is_file():
            msg = f"Missing schema SQL: {schema_path}"
            raise FileNotFoundError(msg)
        _execute_sql_file(conn, schema_path)
        _load_parquet_seed(conn)
    finally:
        conn.close()

    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Initialize PDV DuckDB database")
    parser.add_argument(
        "--db-path",
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f"Output database file (default: {DEFAULT_DB_PATH})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Recreate database if file already exists",
    )
    args = parser.parse_args(argv)

    try:
        path = init_database(args.db_path, force=args.force)
    except (FileExistsError, FileNotFoundError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"DuckDB initialized at {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
