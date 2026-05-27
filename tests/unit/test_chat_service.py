from typing import Any
from unittest.mock import MagicMock

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import RunnableConfig

from dalva_backend.config import Settings
from dalva_backend.models.chat import AgentResult
from dalva_backend.repositories.llm_repository import LLMRepository
from dalva_backend.services.chat_service import ChatService


class FakeChatModel(BaseChatModel):
    """Test double that never calls external APIs."""

    @property
    def _llm_type(self) -> str:
        return "fake"

    def _generate(
        self,
        messages: list,
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        return ChatResult(
            generations=[
                ChatGeneration(message=AIMessage(content="Mocked reply from PDV-AI."))
            ]
        )

    def invoke(
        self,
        input: Any,
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> AIMessage:
        return AIMessage(content="Mocked reply from PDV-AI.")


def test_generate_reply_returns_mocked_content() -> None:
    settings = Settings(openai_api_key="test-key")
    repository = LLMRepository(FakeChatModel())
    service = ChatService(llm_repository=repository, settings=settings)

    response = service.generate_reply("Hello")

    assert response.reply == "Mocked reply from PDV-AI."
    assert response.model == settings.openai_model
    assert response.used_database is False
    assert response.data_sources == []


def test_generate_reply_uses_sql_agent_when_enabled() -> None:
    settings = Settings(
        openai_api_key="test-key",
        database_queries_enabled=True,
        database_url="duckdb:///./data/pdv_ai.duckdb",
    )
    sql_agent = MagicMock()
    sql_agent.invoke.return_value = AgentResult(
        reply="Sales total: 500",
        used_database=True,
        data_sources=["pdv.vendas"],
    )
    service = ChatService(
        llm_repository=LLMRepository(FakeChatModel()),
        settings=settings,
        sql_agent_repository=sql_agent,
    )

    response = service.generate_reply("Sales yesterday?")

    assert response.reply == "Sales total: 500"
    assert response.used_database is True
    assert response.data_sources == ["pdv.vendas"]
    sql_agent.invoke.assert_called_once_with("Sales yesterday?")


def test_uses_database_flag() -> None:
    settings = Settings(
        openai_api_key="test-key",
        database_queries_enabled=True,
        database_url="duckdb:///./data/pdv_ai.duckdb",
    )
    service = ChatService(
        llm_repository=LLMRepository(FakeChatModel()),
        settings=settings,
        sql_agent_repository=MagicMock(),
    )
    assert service.uses_database is True

    disabled = ChatService(
        llm_repository=LLMRepository(FakeChatModel()),
        settings=Settings(openai_api_key="test-key"),
    )
    assert disabled.uses_database is False
