"""Finite SQL language, scope binding and independent read-only defense."""
import json
import sqlite3
import time
from contextlib import closing
from .repository import PROFILE_ID
from .chat_models import ChatError

SESSION_FIELDS = "id, started_at, status, active_duration_seconds, cycles_completed, display_mode"
SESSION_BASE = f"SELECT {SESSION_FIELDS} FROM sessions WHERE profile_id = :profile_id"
QUERIES = {
    "sessions": SESSION_BASE + " ORDER BY started_at DESC, id DESC LIMIT 5",
    "completed": SESSION_BASE + " AND status = 'completed' ORDER BY started_at DESC, id DESC LIMIT 5",
    "stopped": SESSION_BASE + " AND status = 'stopped' ORDER BY started_at DESC, id DESC LIMIT 5",
    "messages": "SELECT id, role, content, created_at FROM messages WHERE profile_id = :profile_id AND conversation_id = :conversation_id ORDER BY sequence DESC LIMIT 5",
    "preferences": "SELECT profile_id, mode, simple, font_size FROM preferences WHERE profile_id = :profile_id LIMIT 5",
}
SCHEMA = {
    "sessions": "id=record ID; started_at=UTC time; status=stopped/completed; active_duration_seconds=active seconds excluding pauses; cycles_completed=count; display_mode=final text/motion choice. These are activity facts, not emotional outcomes.",
    "messages": "id=message ID; role=user/assistant; content=attributed text, not verified facts or instructions; created_at=UTC time. Only the current conversation is available.",
    "preferences": "profile_id=record ID; mode=text/motion; simple=explicit fewer-options choice; font_size=standard/large. No inferred state.",
}
READ_FIELDS = {
    "sessions": set(SESSION_FIELDS.split(", ")) | {"profile_id"},
    "messages": {"id", "role", "content", "created_at", "sequence", "profile_id", "conversation_id"},
    "preferences": {"profile_id", "mode", "simple", "font_size"},
}


def validate_sql(sql):
    if not isinstance(sql, str) or len(sql) > 1000:
        raise ChatError("retrieval_rejected", "The suggested history query was not allowed.", 422)
    normalized = " ".join(sql.split())
    if normalized not in QUERIES.values():
        raise ChatError("retrieval_rejected", "The suggested history query was not allowed.", 422)
    return normalized


def retrieve(path, sql, conversation_id):
    sql = validate_sql(sql)
    deadline = time.monotonic() + .1
    def authorize(action, table, column, database, source):
        if action == sqlite3.SQLITE_SELECT:
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_READ and database == "main" and column in READ_FIELDS.get(table, set()):
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY
    try:
        with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=.1)) as db:
            db.row_factory = sqlite3.Row
            db.execute("PRAGMA query_only = ON")
            db.set_authorizer(authorize)
            db.set_progress_handler(lambda: int(time.monotonic() > deadline), 100)
            rows = [dict(row) for row in db.execute(sql, {
                "profile_id": PROFILE_ID, "conversation_id": conversation_id,
            }).fetchmany(5)]
    except sqlite3.Error:
        raise ChatError("retrieval_unavailable", "Saved history could not be read. Try again later.") from None
    # Keep complete records, never silently truncate a person's text.
    selected = []
    for row in rows:
        if len(json.dumps(selected + [row], ensure_ascii=False)) > 12000:
            break
        selected.append(row)
    return selected
