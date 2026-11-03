import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from .controllers import SessionController
from .models import ErrorResponse, Health, SavedSession, SessionHistory, SessionInput
from .repository import DEFAULT_DATABASE, SessionConflict, SessionRepository
from .config import load_settings
from .chat_repository import ChatRepository
from .chat_controller import ChatController
from .chat_models import (ChatError, ChatInput, Preferences, SavedPreferences,
                          ConversationList, ConversationHistory, Exchange)


def error_response(status: int, code: str, message: str):
    return JSONResponse(
        status_code=status, content={"error": {"code": code, "message": message}}
    )


def create_app(database_path: Path = DEFAULT_DATABASE, settings=None, provider=None):
    settings = settings or load_settings()
    repository = ChatRepository(database_path)
    controller = SessionController(repository)
    chat = ChatController(repository, settings, provider)

    @asynccontextmanager
    async def lifespan(app):
        # Keep health/errors available if the disk is unavailable at startup.
        try:
            repository.initialize()
        except (sqlite3.Error, OSError):
            pass
        yield

    app = FastAPI(
        title="Paced breathing coursework API",
        lifespan=lifespan,
        responses={503: {"model": ErrorResponse}},
    )

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request, exception):
        return error_response(422, "invalid_request", "Check the fields and URL parameters.")

    @app.exception_handler(ChatError)
    async def chat_error(request, exception):
        return error_response(exception.status, exception.code, exception.message)

    @app.exception_handler(SessionConflict)
    async def conflicting_save(request, exception):
        return error_response(409, "session_conflict", "This ID already belongs to a different session.")

    @app.exception_handler(sqlite3.Error)
    @app.exception_handler(OSError)
    async def unavailable_storage(request, exception):
        return error_response(503, "storage_unavailable", "Storage is unavailable. The operation was not confirmed.")

    @app.exception_handler(HTTPException)
    async def http_error(request, exception):
        return error_response(exception.status_code, "http_error", "The requested API operation is unavailable.")

    @app.get("/api/health", response_model=Health, responses={503: {"model": Health}})
    def health():
        mode = "mock" if settings.mode == "mock" else "openai"
        try:
            repository.check()
            usage = repository.usage(settings.demo_session)
        except (sqlite3.Error, OSError):
            return JSONResponse(
                status_code=503,
                content=Health(status="unavailable", storage_available=False,
                    provider_mode=mode, provider_configured=settings.configured).model_dump(),
            )
        return Health(status="ok", storage_available=True, provider_mode=mode,
                      provider_configured=settings.configured, live_calls_reserved=usage)

    @app.put(
        "/api/sessions/{session_id}",
        response_model=SavedSession,
        responses={409: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
    )
    def save_session(session_id: UUID, session: SessionInput):
        return controller.save(session_id, session)

    @app.get("/api/sessions", response_model=SessionHistory, responses={422: {"model": ErrorResponse}})
    def session_history(
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0, le=100000),
    ):
        return controller.history(limit, offset)

    @app.put("/api/conversations/{conversation_id}/messages/{request_id}", response_model=Exchange,
             responses={409: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
    async def submit_message(conversation_id: UUID, request_id: UUID, message: ChatInput):
        return await chat.submit(str(conversation_id), str(request_id), message.content)

    @app.get("/api/conversations", response_model=ConversationList)
    def conversations(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0, le=100000)):
        return {"conversations": repository.conversations(limit, offset), "limit": limit, "offset": offset}

    @app.get("/api/conversations/{conversation_id}", response_model=ConversationHistory)
    def messages(conversation_id: UUID, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0, le=100000), latest: bool = False):
        total = repository.message_count(str(conversation_id))
        if latest:
            offset = max(0, (total - 1) // limit) * limit
        return {"id": str(conversation_id), "messages": repository.messages(str(conversation_id), limit, offset), "limit": limit, "offset": offset, "total": total}

    @app.get("/api/preferences", response_model=SavedPreferences)
    def preferences():
        return repository.preferences()

    @app.put("/api/preferences", response_model=SavedPreferences)
    def update_preferences(values: Preferences):
        return repository.save_preferences(values)

    return app


app = create_app()
