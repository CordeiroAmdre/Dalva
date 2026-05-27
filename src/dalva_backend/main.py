import logging

from fastapi import FastAPI

from dalva_backend.controllers import chat_controller, health_controller

logging.basicConfig(level=logging.INFO)


def create_app() -> FastAPI:
    application = FastAPI(
        title="Dalva API",
        version="0.3.0",
        description="LangChain-backed Dalva assistant with optional read-only PDV database queries.",
    )
    application.include_router(health_controller.router)
    application.include_router(chat_controller.router)
    return application


app = create_app()
