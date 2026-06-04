"""SQLDatabase wrapper that routes execution through read-only validation."""

from __future__ import annotations

from typing import Any

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from dalva_backend.repositories.database_repository import DatabaseRepository


class ReadOnlySQLDatabase(SQLDatabase):
    """LangChain SQLDatabase that enforces read-only execution."""

    def __init__(
        self,
        engine: Engine,
        database_repository: DatabaseRepository,
        **kwargs: Any,
    ) -> None:
        self._database_repository = database_repository
        super().__init__(engine, **kwargs)

    @classmethod
    def from_uri(
        cls,
        database_uri: str,
        *,
        database_repository: DatabaseRepository,
        **kwargs: Any,
    ) -> ReadOnlySQLDatabase:
        kwargs.pop("engine_args", None)
        kwargs.setdefault("lazy_table_reflection", True)
        engine = create_engine(database_uri)
        return cls(engine, database_repository=database_repository, **kwargs)

    def get_table_info(
        self,
        table_names: list[str] | None = None,
        get_col_comments: bool = False,
    ) -> str:
        """Return schema DDL without foreign keys (duckdb-engine FK reflection is broken)."""
        from langchain_community.utilities import sql_database as lc_sql
        from sqlalchemy import Table
        from sqlalchemy.schema import CreateTable

        original_create_table = lc_sql.CreateTable

        def create_table_without_foreign_keys(table: Table) -> CreateTable:
            return CreateTable(table, include_foreign_key_constraints=[])

        lc_sql.CreateTable = create_table_without_foreign_keys
        try:
            return super().get_table_info(table_names, get_col_comments=get_col_comments)
        finally:
            lc_sql.CreateTable = original_create_table

    def run(self, command: str, fetch: str = "all", **kwargs: Any) -> str:
        return self._database_repository.execute_readonly(command, fetch=fetch)
