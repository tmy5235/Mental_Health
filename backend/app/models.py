from datetime import timezone
from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator


class SessionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    started_at: AwareDatetime
    ended_at: AwareDatetime
    status: Literal["stopped", "completed"]
    active_duration_seconds: float = Field(ge=0, le=60, allow_inf_nan=False)
    cycles_completed: int = Field(ge=0, le=6, strict=True)
    display_mode: Literal["text", "motion"]

    @model_validator(mode="after")
    def check_sequence(self):
        wall_seconds = (self.ended_at - self.started_at).total_seconds()
        if wall_seconds < self.active_duration_seconds:
            raise ValueError("Active duration must fit within the session timestamps.")
        if self.cycles_completed != int(self.active_duration_seconds // 10):
            raise ValueError("Cycle count must match the fixed ten-second cycles.")
        if (self.status == "completed") != (self.active_duration_seconds == 60):
            raise ValueError("Only a full sixty-second sequence is completed.")
        return self

    def storage_values(self):
        values = self.model_dump()
        for field in ("started_at", "ended_at"):
            values[field] = values[field].astimezone(timezone.utc).isoformat(
                timespec="microseconds"
            )
        return values


class SessionRecord(SessionInput):
    id: UUID
    profile_id: Literal["fictional-alex"]
    skill_key: Literal["paced-breathing"]
    skill_version: Literal[1]
    fictional: Literal[True]


class SavedSession(BaseModel):
    saved: Literal[True] = True
    session: SessionRecord


class SessionHistory(BaseModel):
    sessions: list[SessionRecord]
    limit: int
    offset: int


class Health(BaseModel):
    status: Literal["ok", "unavailable"]
    storage_available: bool
    provider_mode: Literal["mock", "openai"] = "mock"
    provider_configured: bool = True
    live_calls_reserved: int = 0
    live_call_limit: Literal[50] = 50


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
