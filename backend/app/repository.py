"""SQLite storage; no provider or frontend code may open this database."""

import sqlite3
from contextlib import closing
from pathlib import Path

DEFAULT_DATABASE = Path(__file__).resolve().parents[2] / "data" / "app.sqlite3"
PROFILE_ID = "fictional-alex"


class SessionConflict(Exception):
    """An existing stable ID was reused with different session data."""


class SessionRepository:
    def __init__(self, path: Path = DEFAULT_DATABASE):
        self.path = Path(path)

    def connect(self):
        connection = sqlite3.connect(self.path, timeout=3)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self.connect()) as connection, connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS demo_profiles (
                    id TEXT PRIMARY KEY,
                    fictional INTEGER NOT NULL CHECK (fictional = 1)
                );
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    profile_id TEXT NOT NULL REFERENCES demo_profiles(id),
                    skill_key TEXT NOT NULL CHECK (skill_key = 'paced-breathing'),
                    skill_version INTEGER NOT NULL CHECK (skill_version = 1),
                    started_at TEXT NOT NULL,
                    ended_at TEXT NOT NULL CHECK (ended_at >= started_at),
                    status TEXT NOT NULL CHECK (status IN ('stopped', 'completed')),
                    active_duration_seconds REAL NOT NULL
                        CHECK (active_duration_seconds >= 0 AND active_duration_seconds <= 60),
                    cycles_completed INTEGER NOT NULL CHECK (
                        cycles_completed = CAST(active_duration_seconds / 10 AS INTEGER)
                    ),
                    display_mode TEXT NOT NULL CHECK (display_mode IN ('text', 'motion')),
                    fictional INTEGER NOT NULL CHECK (fictional = 1),
                    CHECK (
                        (status = 'completed' AND active_duration_seconds = 60) OR
                        (status = 'stopped' AND active_duration_seconds < 60)
                    )
                );
                CREATE INDEX IF NOT EXISTS sessions_profile_order
                    ON sessions(profile_id, started_at DESC, id DESC);
            """)

    def check(self):
        with closing(self.connect()) as connection:
            connection.execute("SELECT id FROM sessions LIMIT 1").fetchall()

    @staticmethod
    def record(row):
        result = dict(row)
        result["fictional"] = bool(result["fictional"])
        return result

    def save(self, session_id: str, values: dict):
        record = {
            "id": session_id,
            "profile_id": PROFILE_ID,
            "skill_key": "paced-breathing",
            "skill_version": 1,
            **values,
            "fictional": True,
        }
        with closing(self.connect()) as connection, connection:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                "SELECT * FROM sessions WHERE id = ?", (session_id,)
            ).fetchone()
            if existing is not None:
                if self.record(existing) != record:
                    raise SessionConflict()
                return self.record(existing)
            # The demo profile is created only with its first session, not at startup.
            connection.execute(
                "INSERT OR IGNORE INTO demo_profiles (id, fictional) VALUES (?, 1)",
                (PROFILE_ID,),
            )
            connection.execute(
                """INSERT INTO sessions (
                    id, profile_id, skill_key, skill_version, started_at, ended_at,
                    status, active_duration_seconds, cycles_completed, display_mode, fictional
                ) VALUES (
                    :id, :profile_id, :skill_key, :skill_version, :started_at, :ended_at,
                    :status, :active_duration_seconds, :cycles_completed, :display_mode, :fictional
                )""",
                record,
            )
        return record

    def list(self, limit: int = 20, offset: int = 0):
        with closing(self.connect()) as connection:
            rows = connection.execute(
                """SELECT * FROM sessions WHERE profile_id = ?
                   ORDER BY started_at DESC, id DESC LIMIT ? OFFSET ?""",
                (PROFILE_ID, limit, offset),
            ).fetchall()
        return [self.record(row) for row in rows]
