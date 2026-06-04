from fastapi import APIRouter, Depends

from dalva_backend.controllers.dependencies import chat_service_dependency
from dalva_backend.exceptions import raise_http_for_database_error, raise_http_for_llm_error
from dalva_backend.models.chat import ChatDalvaRequest, ChatDalvaResponse
from dalva_backend.models.common import ErrorResponse
from dalva_backend.services.chat_service import ChatService

router = APIRouter(prefix="/dalva", tags=["dalva"])


@router.post(
    "/chat",
    response_model=ChatDalvaResponse,
    responses={
        502: {"model": ErrorResponse, "description": "Model provider error"},
        503: {"model": ErrorResponse, "description": "Database unavailable"},
    },
)
def dalva_chat(
    request: ChatDalvaRequest,
    service: ChatService = Depends(chat_service_dependency),
) -> ChatDalvaResponse:
    try:
        return service.generate_reply(request.message)
    except Exception as exc:
        if service.uses_database:
            raise_http_for_database_error(exc)
        raise_http_for_llm_error(exc)
