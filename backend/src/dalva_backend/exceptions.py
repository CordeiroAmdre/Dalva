import logging
from typing import NoReturn

logger = logging.getLogger(__name__)


def raise_http_for_llm_error(exc: Exception) -> NoReturn:
    """Map provider/LangChain errors to safe HTTP responses."""
    from fastapi import HTTPException

    logger.exception("LLM request failed")

    name = type(exc).__name__
    message = str(exc).lower()

    if name == "AuthenticationError" or "invalid api key" in message:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key. Check OPENAI_API_KEY in your .env file.",
        ) from exc

    if name == "RateLimitError" or "insufficient_quota" in message or "quota" in message:
        raise HTTPException(
            status_code=503,
            detail=(
                "OpenAI quota exceeded or rate limited. "
                "Check billing and usage at https://platform.openai.com/"
            ),
        ) from exc

    if name in ("APIConnectionError", "APITimeoutError") or "connection" in message:
        raise HTTPException(
            status_code=503,
            detail="Could not reach the language model provider. Try again later.",
        ) from exc

    raise HTTPException(
        status_code=502,
        detail="The language model provider returned an error. Try again later.",
    ) from exc


def raise_http_for_database_error(exc: Exception) -> NoReturn:
    """Map database connectivity errors to safe HTTP responses."""
    from fastapi import HTTPException

    logger.exception("Database request failed")

    message = str(exc).lower()
    if (
        "connection" in message
        or "could not connect" in message
        or "operationalerror" in message
        or "timeout" in message
        or "password authentication failed" in message
        or "authentication failed" in message
    ):
        raise HTTPException(
            status_code=503,
            detail=(
                "The store database is temporarily unavailable. "
                "Try again later or disable DATABASE_QUERIES_ENABLED."
            ),
        ) from exc

    raise HTTPException(
        status_code=502,
        detail="A database error occurred while processing your question.",
    ) from exc
