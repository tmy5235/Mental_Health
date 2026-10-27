from uuid import UUID

from .models import SavedSession, SessionHistory, SessionInput
from .repository import SessionRepository


class SessionController:
    def __init__(self, repository: SessionRepository):
        self.repository = repository

    def save(self, session_id: UUID, session: SessionInput):
        record = self.repository.save(str(session_id), session.storage_values())
        return SavedSession(session=record)

    def history(self, limit: int, offset: int):
        return SessionHistory(
            sessions=self.repository.list(limit, offset), limit=limit, offset=offset
        )
