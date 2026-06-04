from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from dalva_backend.config import Settings
from dalva_backend.controllers.dependencies import chat_service_dependency
from dalva_backend.main import app
from dalva_backend.models.chat import AgentResult
from dalva_backend.repositories.llm_repository import LLMRepository
from dalva_backend.services.chat_service import ChatService


class FakeChatModel(BaseChatModel):
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
                ChatGeneration(message=AIMessage(content="LLM-only reply."))
            ]
        )

    def invoke(self, input: Any, config: Any = None, **kwargs: Any) -> AIMessage:
        return AIMessage(content="LLM-only reply.")


@pytest.fixture
def llm_only_client() -> TestClient:
    settings = Settings(openai_api_key="test-key", database_queries_enabled=False)
    service = ChatService(
        llm_repository=LLMRepository(FakeChatModel()),
        settings=settings,
    )
    app.dependency_overrides[chat_service_dependency] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def db_enabled_client() -> TestClient:
    sql_agent = MagicMock()
    sql_agent.invoke.return_value = AgentResult(
        reply="Total vendas: R$ 1200",
        used_database=True,
        data_sources=["pdv.vendas", "pdv.vw_vendas_detalhadas"],
    )
    settings = Settings(
        openai_api_key="test-key",
        database_queries_enabled=True,
        database_url="duckdb:///./data/pdv_ai.duckdb",
    )
    service = ChatService(
        llm_repository=LLMRepository(FakeChatModel()),
        settings=settings,
        sql_agent_repository=sql_agent,
    )
    app.dependency_overrides[chat_service_dependency] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_dalva_chat_llm_only_has_used_database_false(
    llm_only_client: TestClient,
) -> None:
    response = llm_only_client.post(
        "/dalva/chat",
        json={"message": "What is a POS system?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["reply"] == "LLM-only reply."
    assert body["used_database"] is False
    assert body["data_sources"] == []


def test_dalva_chat_data_question_returns_database_metadata(
    db_enabled_client: TestClient,
) -> None:
    response = db_enabled_client.post(
        "/dalva/chat",
        json={"message": "Qual o total de vendas ontem?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["used_database"] is True
    assert "pdv.vendas" in body["data_sources"]
    assert "1200" in body["reply"]
