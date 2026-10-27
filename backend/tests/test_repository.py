import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path

from app.repository import DEFAULT_DATABASE, SessionConflict, SessionRepository


SESSION_ID = "11111111-1111-4111-8111-111111111111"


def fictional_session(**changes):
    return {
        "started_at": "2026-10-20T12:00:00.000000+00:00",
        "ended_at": "2026-10-20T12:00:25.000000+00:00",
        "status": "stopped",
        "active_duration_seconds": 20.0,
        "cycles_completed": 2,
        "display_mode": "text",
        **changes,
    }


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "test.sqlite3"
        self.repository = SessionRepository(self.path)
        self.repository.initialize()

    def test_startup_is_empty_and_does_not_seed(self):
        self.repository.initialize()
        self.assertEqual(self.repository.list(), [])
        with closing(sqlite3.connect(self.path)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM demo_profiles").fetchone()[0], 0)

    def test_retry_and_reopen_preserve_one_record(self):
        first = self.repository.save(SESSION_ID, fictional_session())
        self.assertEqual(self.repository.save(SESSION_ID, fictional_session()), first)
        reopened = SessionRepository(self.path)
        reopened.initialize()
        self.assertEqual(reopened.list(), [first])
        with closing(sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)) as connection:
            self.assertEqual(connection.execute("PRAGMA foreign_key_check").fetchall(), [])
            row = connection.execute(
                "SELECT id, status, active_duration_seconds, profile_id FROM sessions"
            ).fetchone()
            self.assertEqual(row, (SESSION_ID, "stopped", 20.0, "fictional-alex"))

    def test_conflict_preserves_original(self):
        original = self.repository.save(SESSION_ID, fictional_session())
        with self.assertRaises(SessionConflict):
            self.repository.save(SESSION_ID, fictional_session(display_mode="motion"))
        self.assertEqual(self.repository.list(), [original])

    def test_concurrent_identical_retries_create_one_row(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            records = list(executor.map(
                lambda _: self.repository.save(SESSION_ID, fictional_session()), range(8)
            ))
        self.assertTrue(all(record == records[0] for record in records))
        self.assertEqual(len(self.repository.list()), 1)

    def test_history_has_deterministic_order_and_pagination(self):
        for suffix in ("1", "3", "2"):
            self.repository.save(f"11111111-1111-4111-8111-11111111111{suffix}", fictional_session())
        rows = self.repository.list(limit=1, offset=1)
        self.assertEqual(rows[0]["id"], "11111111-1111-4111-8111-111111111112")
        self.assertEqual(self.repository.list(offset=10), [])

    def test_failed_transaction_leaves_no_session_or_profile(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.repository.save(SESSION_ID, fictional_session(status="completed"))
        self.assertEqual(self.repository.list(), [])
        with closing(sqlite3.connect(self.path)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM demo_profiles").fetchone()[0], 0)

    def test_default_database_is_project_relative(self):
        self.assertEqual(
            DEFAULT_DATABASE,
            Path(__file__).resolve().parents[2] / "data" / "app.sqlite3",
        )


if __name__ == "__main__":
    unittest.main()
