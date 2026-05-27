from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

from dalva_backend.config import Settings
from dalva_backend.prompts.dalva import dalva_prompt


def create_chat_model(settings: Settings) -> BaseChatModel:
    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        temperature=0.2,
    )


class LLMRepository:
    """Data access to the external language model provider via LangChain."""

    def __init__(self, llm: BaseChatModel) -> None:
        self._chain = dalva_prompt | llm

    def generate(self, message: str) -> str:
        result = self._chain.invoke({"message": message})
        if isinstance(result, AIMessage):
            content = result.content
        elif hasattr(result, "content"):
            content = result.content
        else:
            content = str(result)
        return content if isinstance(content, str) else str(content)
