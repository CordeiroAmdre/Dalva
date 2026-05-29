import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dalva_backend.controllers import chat_controller, health_controller

logging.basicConfig(level=logging.INFO)

_CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def create_app() -> FastAPI:
    application = FastAPI(
        title="Dalva API",
        version="0.5.0",
        description="LangChain-backed Dalva assistant with optional read-only PDV database queries.",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )
    application.include_router(health_controller.router)
    application.include_router(chat_controller.router)
    return application


app = create_app()
