from functools import lru_cache

from fastapi import Depends

from dalva_backend.config import Settings, get_settings
from dalva_backend.repositories.chart_option_repository import ChartOptionRepository
from dalva_backend.repositories.llm_repository import LLMRepository, create_chat_model
from dalva_backend.repositories.sql_agent_repository import create_sql_agent_repository
from dalva_backend.services.chat_service import ChatService


@lru_cache
def get_chat_service() -> ChatService:
    settings = get_settings()
    llm = create_chat_model(settings)
    llm_repository = LLMRepository(llm)
    sql_agent_repository = None
    chart_option_repository = None
    if settings.database_queries_enabled:
        sql_agent_repository = create_sql_agent_repository(settings)
        chart_option_repository = ChartOptionRepository(llm)
    return ChatService(
        llm_repository=llm_repository,
        settings=settings,
        sql_agent_repository=sql_agent_repository,
        chart_option_repository=chart_option_repository,
    )


def chat_service_dependency(
    service: ChatService = Depends(get_chat_service),
) -> ChatService:
    return service
