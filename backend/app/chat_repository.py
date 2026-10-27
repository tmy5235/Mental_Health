"""Application-owned writes. Retrieval never uses this connection."""
import json
import time
from contextlib import closing
from datetime import datetime, timezone
from uuid import uuid4
from .repository import SessionRepository, PROFILE_ID
from .chat_models import ChatError, Preferences


def now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


class ChatRepository(SessionRepository):
    def initialize(self):
        super().initialize()
        with closing(self.connect()) as db, db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY, profile_id TEXT NOT NULL REFERENCES demo_profiles(id),
                    created_at TEXT NOT NULL, updated_at TEXT NOT NULL, title TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS chat_requests (
                    id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL REFERENCES conversations(id),
                    content TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('pending','failed','completed')),
                    lease_until REAL NOT NULL, attempt TEXT NOT NULL, error_code TEXT,
                    provider_mode TEXT NOT NULL DEFAULT 'mock', model TEXT NOT NULL DEFAULT 'demo-v1',
                    budget_fallback INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS messages (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT NOT NULL UNIQUE,
                    conversation_id TEXT NOT NULL REFERENCES conversations(id),
                    profile_id TEXT NOT NULL REFERENCES demo_profiles(id),
                    request_id TEXT NOT NULL REFERENCES chat_requests(id),
                    role TEXT NOT NULL CHECK(role IN ('user','assistant')), content TEXT NOT NULL,
                    created_at TEXT NOT NULL, record_ids TEXT NOT NULL DEFAULT '[]', retrieval_status TEXT,
                    UNIQUE(request_id, role)
                );
                CREATE INDEX IF NOT EXISTS message_order ON messages(conversation_id, sequence);
                CREATE TABLE IF NOT EXISTS preferences (
                    profile_id TEXT PRIMARY KEY REFERENCES demo_profiles(id),
                    mode TEXT NOT NULL CHECK(mode IN ('text','motion')),
                    simple INTEGER NOT NULL CHECK(simple IN (0,1)),
                    font_size TEXT NOT NULL CHECK(font_size IN ('standard','large'))
                );
                CREATE TABLE IF NOT EXISTS provider_usage (
                    demo_session TEXT PRIMARY KEY, reserved_calls INTEGER NOT NULL CHECK(reserved_calls BETWEEN 0 AND 50)
                );
            """)

    def begin(self, conversation_id, request_id, content):
        stamp, attempt = now(), str(uuid4())
        with closing(self.connect()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            existing = db.execute("SELECT * FROM chat_requests WHERE id = ?", (request_id,)).fetchone()
            if existing:
                if existing["conversation_id"] != conversation_id or existing["content"] != content:
                    raise ChatError("request_conflict", "This request ID already belongs to another message.", 409)
                if existing["status"] == "completed":
                    return None
                if existing["status"] == "pending" and existing["lease_until"] > time.time():
                    raise ChatError("request_pending", "This reply is still pending. Refresh chat shortly.", 409)
            # Serialize exchanges within a conversation so reply order stays intelligible.
            pending = db.execute("SELECT id FROM chat_requests WHERE conversation_id = ? AND status = 'pending' AND lease_until > ? AND id != ?", (conversation_id, time.time(), request_id)).fetchone()
            if pending:
                raise ChatError("request_pending", "Another reply is still pending. Refresh chat shortly.", 409)
            db.execute("INSERT OR IGNORE INTO demo_profiles VALUES (?, 1)", (PROFILE_ID,))
            db.execute("INSERT OR IGNORE INTO conversations VALUES (?, ?, ?, ?, ?)",
                       (conversation_id, PROFILE_ID, stamp, stamp, content[:60]))
            owned = db.execute("SELECT id FROM conversations WHERE id = ? AND profile_id = ?", (conversation_id, PROFILE_ID)).fetchone()
            if not owned:
                raise ChatError("conversation_missing", "Conversation not found.", 404)
            if existing:
                db.execute("UPDATE chat_requests SET status = 'pending', error_code = NULL, lease_until = ?, attempt = ? WHERE id = ?", (time.time() + 90, attempt, request_id))
            else:
                db.execute("INSERT INTO chat_requests(id, conversation_id, content, status, lease_until, attempt) VALUES (?, ?, ?, 'pending', ?, ?)", (request_id, conversation_id, content, time.time() + 90, attempt))
                db.execute("INSERT INTO messages(id, conversation_id, profile_id, request_id, role, content, created_at) VALUES (?, ?, ?, ?, 'user', ?, ?)",
                           (str(uuid4()), conversation_id, PROFILE_ID, request_id, content, stamp))
            db.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (stamp, conversation_id))
        return attempt

    def reserve_live(self, demo_session):
        with closing(self.connect()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("INSERT OR IGNORE INTO provider_usage VALUES (?, 0)", (demo_session,))
            changed = db.execute("UPDATE provider_usage SET reserved_calls = reserved_calls + 2 WHERE demo_session = ? AND reserved_calls <= 48", (demo_session,)).rowcount
        return bool(changed)

    def usage(self, demo_session):
        with closing(self.connect()) as db:
            row = db.execute("SELECT reserved_calls FROM provider_usage WHERE demo_session = ?", (demo_session,)).fetchone()
        return row[0] if row else 0

    def set_provider(self, request_id, attempt, mode, model, fallback):
        with closing(self.connect()) as db, db:
            db.execute("UPDATE chat_requests SET provider_mode = ?, model = ?, budget_fallback = ? WHERE id = ? AND attempt = ?", (mode, model, fallback, request_id, attempt))

    def fail(self, request_id, attempt, code):
        with closing(self.connect()) as db, db:
            db.execute("UPDATE chat_requests SET status = 'failed', error_code = ?, lease_until = 0 WHERE id = ? AND attempt = ? AND status = 'pending'", (code, request_id, attempt))

    def finish(self, conversation_id, request_id, attempt, content, record_ids, retrieval_status):
        stamp = now()
        with closing(self.connect()) as db, db:
            db.execute("BEGIN IMMEDIATE")
            changed = db.execute("UPDATE chat_requests SET status = 'completed', lease_until = 0, error_code = NULL WHERE id = ? AND attempt = ? AND status = 'pending'", (request_id, attempt)).rowcount
            if not changed:
                raise ChatError("attempt_expired", "A newer attempt replaced this reply. Refresh chat.", 409)
            db.execute("INSERT INTO messages(id, conversation_id, profile_id, request_id, role, content, created_at, record_ids, retrieval_status) VALUES (?, ?, ?, ?, 'assistant', ?, ?, ?, ?)",
                       (str(uuid4()), conversation_id, PROFILE_ID, request_id, content, stamp, json.dumps(record_ids), retrieval_status))
            db.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (stamp, conversation_id))

    def messages(self, conversation_id, limit=50, offset=0, request_id=None):
        with closing(self.connect()) as db:
            owned = db.execute("SELECT id FROM conversations WHERE id = ? AND profile_id = ?", (conversation_id, PROFILE_ID)).fetchone()
            if not owned:
                raise ChatError("conversation_missing", "Conversation not found.", 404)
            sql = """SELECT m.*, r.status, r.error_code, r.provider_mode, r.model, r.lease_until
                     FROM messages m JOIN chat_requests r ON r.id = m.request_id
                     WHERE m.conversation_id = ? AND m.profile_id = ?"""
            params = [conversation_id, PROFILE_ID]
            if request_id:
                sql += " AND m.request_id = ?"
                params.append(request_id)
            rows = db.execute(sql + " ORDER BY m.sequence LIMIT ? OFFSET ?", (*params, limit, offset)).fetchall()
        output = []
        for row in rows:
            item = dict(row)
            item.pop("profile_id")
            if item.pop("lease_until") < time.time() and item["status"] == "pending":
                item.update(status="failed", error_code="attempt_interrupted")
            item["record_ids"] = json.loads(item["record_ids"])
            output.append(item)
        return output

    def exchange(self, conversation_id, request_id):
        with closing(self.connect()) as db:
            row = db.execute("SELECT * FROM chat_requests WHERE id = ? AND status = 'completed'", (request_id,)).fetchone()
        if not row:
            raise ChatError("reply_unconfirmed", "The reply save was not confirmed. Refresh chat.")
        return {"saved": True, "conversation_id": conversation_id, "request_id": request_id,
                "messages": self.messages(conversation_id, request_id=request_id),
                "provider_mode": row["provider_mode"], "budget_fallback": bool(row["budget_fallback"])}

    def conversations(self, limit, offset):
        with closing(self.connect()) as db:
            return [dict(row) for row in db.execute("SELECT id, created_at, updated_at, title FROM conversations WHERE profile_id = ? ORDER BY updated_at DESC, id DESC LIMIT ? OFFSET ?", (PROFILE_ID, limit, offset))]

    def preferences(self):
        with closing(self.connect()) as db:
            row = db.execute("SELECT mode, simple, font_size FROM preferences WHERE profile_id = ?", (PROFILE_ID,)).fetchone()
        return {"saved": row is not None, "preferences": Preferences(**dict(row)).model_dump() if row else Preferences().model_dump()}

    def save_preferences(self, values):
        with closing(self.connect()) as db, db:
            db.execute("INSERT OR IGNORE INTO demo_profiles VALUES (?, 1)", (PROFILE_ID,))
            db.execute("INSERT INTO preferences VALUES (?, ?, ?, ?) ON CONFLICT(profile_id) DO UPDATE SET mode = excluded.mode, simple = excluded.simple, font_size = excluded.font_size", (PROFILE_ID, values.mode, values.simple, values.font_size))
        return {"saved": True, "preferences": values.model_dump()}
