from functools import lru_cache

from fastapi import Depends

from dalva_backend.config import Settings, get_settings
from dalva_backend.repositories.llm_repository import LLMRepository, create_chat_model
from dalva_backend.repositories.sql_agent_repository import create_sql_agent_repository
from dalva_backend.services.chat_service import ChatService


@lru_cache
def get_chat_service() -> ChatService:
    settings = get_settings()
    llm_repository = LLMRepository(create_chat_model(settings))
    sql_agent_repository = None
    if settings.database_queries_enabled:
        sql_agent_repository = create_sql_agent_repository(settings)
    return ChatService(
        llm_repository=llm_repository,
        settings=settings,
        sql_agent_repository=sql_agent_repository,
    )


def chat_service_dependency(
    service: ChatService = Depends(get_chat_service),
) -> ChatService:
    return service
