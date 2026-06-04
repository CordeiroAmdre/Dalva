from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import RunnableConfig

from dalva_backend.repositories.llm_repository import LLMRepository


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
            generations=[ChatGeneration(message=AIMessage(content="Repo mock."))]
        )

    def invoke(
        self,
        input: Any,
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> AIMessage:
        return AIMessage(content="Repo mock.")


def test_repository_generate_returns_text() -> None:
    repository = LLMRepository(FakeChatModel())
    assert repository.generate("test") == "Repo mock."
