from dalva_backend.config import Settings
from dalva_backend.models.chat import AgentResult, ChatDalvaResponse
from dalva_backend.repositories.chart_option_repository import ChartOptionRepository
from dalva_backend.repositories.llm_repository import LLMRepository
from dalva_backend.repositories.sql_agent_repository import SqlAgentRepository
from dalva_backend.services.chart_resolver import resolve_chart


class ChatService:
    """Application business logic for the Dalva chat assistant."""

    def __init__(
        self,
        llm_repository: LLMRepository,
        settings: Settings,
        sql_agent_repository: SqlAgentRepository | None = None,
        chart_option_repository: ChartOptionRepository | None = None,
    ) -> None:
        self._llm_repository = llm_repository
        self._sql_agent_repository = sql_agent_repository
        self._chart_option_repository = chart_option_repository
        self._settings = settings

    def generate_reply(self, message: str) -> ChatDalvaResponse:
        if self._settings.database_queries_enabled and self._sql_agent_repository:
            agent_result = self._invoke_sql_agent(message)
            chart = None
            if agent_result.used_database and self._chart_option_repository is not None:
                chart = resolve_chart(
                    message,
                    self._sql_agent_repository.get_query_log(),
                    self._chart_option_repository,
                )
            return ChatDalvaResponse(
                reply=agent_result.reply,
                model=self._settings.openai_model,
                used_database=agent_result.used_database,
                data_sources=agent_result.data_sources,
                chart=chart,
            )

        reply = self._llm_repository.generate(message)
        return ChatDalvaResponse(
            reply=reply,
            model=self._settings.openai_model,
            used_database=False,
            data_sources=[],
            chart=None,
        )

    @property
    def uses_database(self) -> bool:
        return bool(
            self._settings.database_queries_enabled and self._sql_agent_repository
        )

    def _invoke_sql_agent(self, message: str) -> AgentResult:
        if self._sql_agent_repository is None:
            msg = "SQL agent is not configured."
            raise RuntimeError(msg)
        return self._sql_agent_repository.invoke(message)
