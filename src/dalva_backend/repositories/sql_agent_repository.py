"""LangChain SQL agent wiring for read-only PDV database access."""

from __future__ import annotations

import logging
from typing import Any

from langchain_classic.agents import AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_core.language_models import BaseLanguageModel

from dalva_backend.config import Settings
from dalva_backend.models.chat import AgentResult
from dalva_backend.prompts.sql_agent import APPROVED_TABLES, SQL_AGENT_PREFIX
from dalva_backend.repositories.database_repository import DatabaseRepository, QueryStatus
from dalva_backend.repositories.llm_repository import create_chat_model
from dalva_backend.repositories.readonly_sql_database import ReadOnlySQLDatabase

logger = logging.getLogger(__name__)

_QUERY_TOOL_NAMES = frozenset({"sql_db_query", "query_sql_db"})


class SqlAgentRepository:
    """Orchestrates LangChain SQL agent invocations (no business rules here)."""

    def __init__(
        self,
        settings: Settings,
        llm: BaseLanguageModel | None = None,
        database_repository: DatabaseRepository | None = None,
        agent: Any | None = None,
    ) -> None:
        self._settings = settings
        self._llm = llm or create_chat_model(settings)
        self._database_repository = database_repository or DatabaseRepository(
            database_url=settings.database_url or "",
            schema=settings.database_schema,
            query_timeout_sec=settings.database_query_timeout_sec,
            max_rows=settings.database_max_rows,
        )
        self._agent = agent

    def _ensure_agent(self) -> Any:
        if self._agent is None:
            self._agent = self._build_agent()
        return self._agent

    def _build_agent(self) -> Any:
        sql_database = ReadOnlySQLDatabase.from_uri(
            self._settings.database_url or "",
            database_repository=self._database_repository,
            schema=self._settings.database_schema,
            include_tables=list(APPROVED_TABLES),
            sample_rows_in_table_info=2,
            view_support=True,
            engine_args={"pool_pre_ping": True},
        )

        toolkit = SQLDatabaseToolkit(db=sql_database, llm=self._llm)
        return create_sql_agent(
            llm=self._llm,
            toolkit=toolkit,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            prefix=SQL_AGENT_PREFIX,
            top_k=self._settings.database_max_rows,
            max_iterations=self._settings.sql_agent_max_iterations,
            verbose=False,
        )

    def invoke(self, message: str) -> AgentResult:
        self._database_repository.clear_query_log()
        logger.info("SQL agent invocation started")
        try:
            result = self._ensure_agent().invoke({"input": message})
        except Exception:
            logger.exception("SQL agent invocation failed")
            raise

        output = result.get("output", "")
        if not isinstance(output, str):
            output = str(output)

        steps = result.get("intermediate_steps", [])
        used_database = _steps_used_database(steps) or any(
            entry.status == QueryStatus.SUCCESS
            for entry in self._database_repository.query_log
        )
        data_sources = self._database_repository.data_sources()

        logger.info(
            "SQL agent invocation finished",
            extra={
                "used_database": used_database,
                "iterations": len(steps),
                "data_sources": data_sources,
            },
        )
        return AgentResult(
            reply=output,
            used_database=used_database,
            data_sources=data_sources,
            iterations=len(steps),
        )


def _steps_used_database(steps: list[Any]) -> bool:
    for step in steps:
        if not isinstance(step, tuple) or len(step) < 1:
            continue
        action = step[0]
        tool = getattr(action, "tool", None)
        if tool in _QUERY_TOOL_NAMES:
            return True
    return False


def create_sql_agent_repository(settings: Settings) -> SqlAgentRepository:
    return SqlAgentRepository(settings=settings)
