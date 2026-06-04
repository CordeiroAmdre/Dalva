from typing import Any

import pytest
from fastapi.testclient import TestClient
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from dalva_backend.config import Settings
from dalva_backend.controllers.dependencies import chat_service_dependency
from dalva_backend.main import app
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
                ChatGeneration(message=AIMessage(content="Integration mock reply."))
            ]
        )

    def invoke(self, input: Any, config: Any = None, **kwargs: Any) -> AIMessage:
        return AIMessage(content="Integration mock reply.")


@pytest.fixture
def client() -> TestClient:
    settings = Settings(openai_api_key="test-key")
    repository = LLMRepository(FakeChatModel())
    service = ChatService(llm_repository=repository, settings=settings)
    app.dependency_overrides[chat_service_dependency] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_dalva_chat_returns_mocked_reply(client: TestClient) -> None:
    response = client.post(
        "/dalva/chat",
        json={"message": "Say hello"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["reply"] == "Integration mock reply."
    assert body["model"] == "gpt-4o-mini"
    assert body["used_database"] is False
    assert body["data_sources"] == []


def test_dalva_chat_rejects_empty_message(client: TestClient) -> None:
    response = client.post("/dalva/chat", json={"message": ""})
    assert response.status_code == 422


def test_deprecated_demo_chat_path_returns_not_found(client: TestClient) -> None:
    response = client.post(
        "/demo/chat",
        json={"message": "Say hello"},
    )
    assert response.status_code == 404
