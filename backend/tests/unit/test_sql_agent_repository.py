from unittest.mock import MagicMock

from dalva_backend.config import Settings
from dalva_backend.models.chat import AgentResult
from dalva_backend.repositories.sql_agent_repository import SqlAgentRepository


def test_invoke_returns_agent_result() -> None:
    mock_agent = MagicMock()
    mock_agent.invoke.return_value = {
        "output": "Total sales: R$ 1000",
        "intermediate_steps": [
            (MagicMock(tool="sql_db_query"), "rows"),
        ],
    }

    settings = Settings(
        openai_api_key="test-key",
        database_queries_enabled=True,
        database_url="duckdb:///./data/pdv_ai.duckdb",
    )
    db_repo = MagicMock()
    db_repo.data_sources.return_value = ["pdv.vendas"]
    db_repo.query_log = []

    repository = SqlAgentRepository(
        settings=settings,
        llm=MagicMock(),
        database_repository=db_repo,
        agent=mock_agent,
    )
    result = repository.invoke("Total sales yesterday?")

    assert isinstance(result, AgentResult)
    assert result.reply == "Total sales: R$ 1000"
    assert result.used_database is True
    assert result.data_sources == ["pdv.vendas"]
    db_repo.clear_query_log.assert_called_once()
