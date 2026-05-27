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
        engine = create_engine(database_uri)
        return cls(engine, database_repository=database_repository, **kwargs)

    def run(self, command: str, fetch: str = "all", **kwargs: Any) -> str:
        return self._database_repository.execute_readonly(command, fetch=fetch)
