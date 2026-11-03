from typing import Literal
from uuid import UUID
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class ChatInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    content: str = Field(min_length=1, max_length=1000)


class Preferences(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["text", "motion"] = "text"
    simple: bool = True
    font_size: Literal["standard", "large"] = "standard"


class SavedPreferences(BaseModel):
    saved: bool
    preferences: Preferences


class MessageRecord(BaseModel):
    id: UUID
    conversation_id: UUID
    request_id: UUID
    role: Literal["user", "assistant"]
    content: str
    created_at: AwareDatetime
    sequence: int
    status: Literal["pending", "failed", "completed"]
    error_code: str | None
    provider_mode: Literal["mock", "openai", "local"]
    model: str
    record_ids: list[str]
    retrieval_status: Literal["selected", "empty", "not_requested"] | None


class ConversationSummary(BaseModel):
    id: UUID
    created_at: AwareDatetime
    updated_at: AwareDatetime
    title: str


class ConversationList(BaseModel):
    conversations: list[ConversationSummary]
    limit: int
    offset: int


class ConversationHistory(BaseModel):
    id: UUID
    messages: list[MessageRecord]
    limit: int
    offset: int
    total: int


class Exchange(BaseModel):
    saved: Literal[True] = True
    conversation_id: UUID
    request_id: UUID
    messages: list[MessageRecord]
    provider_mode: Literal["mock", "openai", "local"]
    budget_fallback: bool = False


class ChatError(Exception):
    def __init__(self, code, message, status=503):
        self.code, self.message, self.status = code, message, status
        super().__init__(code)
