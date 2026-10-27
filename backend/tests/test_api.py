import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app
from tests.test_repository import SESSION_ID, fictional_session


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "test.sqlite3"
        self.client = self.enterContext(TestClient(create_app(self.path)))
        self.url = f"/api/sessions/{SESSION_ID}"

    def test_health_and_empty_history(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "ok", "storage_available": True, "provider_mode": "mock", "provider_configured": True,
            "live_calls_reserved": 0, "live_call_limit": 50,
        })
        self.assertEqual(self.client.get("/api/sessions").json()["sessions"], [])

    def test_save_retry_and_restart_match_sqlite(self):
        saved = self.client.put(self.url, json=fictional_session())
        self.assertEqual(saved.status_code, 200)
        self.assertTrue(saved.json()["saved"])
        self.assertEqual(self.client.put(self.url, json=fictional_session()).json(), saved.json())
        # A second app lifecycle uses the same database, not a reseeded fixture.
        with TestClient(create_app(self.path)) as restarted:
            rows = restarted.get("/api/sessions").json()["sessions"]
        self.assertEqual(rows, [saved.json()["session"]])
        with closing(sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)) as connection:
            self.assertEqual(
                connection.execute("SELECT id, status, active_duration_seconds FROM sessions").fetchall(),
                [(SESSION_ID, "stopped", 20.0)],
            )

    def test_conflicting_retry_has_consistent_error(self):
        self.client.put(self.url, json=fictional_session())
        response = self.client.put(self.url, json=fictional_session(display_mode="motion"))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["error"]["code"], "session_conflict")

    def test_invalid_requests_do_not_write(self):
        cases = [
            {"active_duration_seconds": -1},
            {"active_duration_seconds": 61},
            {"cycles_completed": 3},
            {"cycles_completed": True},
            {"status": "completed"},
            {"started_at": "2026-10-20T12:00:00"},
            {"ended_at": "2026-10-20T11:00:00Z"},
            {"ended_at": "2026-10-20T12:00:10Z"},
            {"display_mode": "unknown"},
            {"profile_id": "another-profile"},
        ]
        for changes in cases:
            with self.subTest(changes=changes):
                response = self.client.put(self.url, json=fictional_session(**changes))
                self.assertEqual(response.status_code, 422)
                self.assertEqual(response.json()["error"]["code"], "invalid_request")
        self.assertEqual(self.client.get("/api/sessions").json()["sessions"], [])

    def test_completed_session_and_timezone_normalization(self):
        response = self.client.put(self.url, json=fictional_session(
            started_at="2026-10-20T08:00:00-04:00",
            ended_at="2026-10-20T08:01:00-04:00",
            active_duration_seconds=60, cycles_completed=6, status="completed",
        ))
        self.assertEqual(response.status_code, 200)
        equivalent = self.client.put(self.url, json=fictional_session(
            ended_at="2026-10-20T12:01:00Z",
            active_duration_seconds=60, cycles_completed=6, status="completed",
        ))
        self.assertEqual(equivalent.json(), response.json())

    def test_url_and_pagination_validation(self):
        self.assertEqual(self.client.put("/api/sessions/not-a-uuid", json=fictional_session()).status_code, 422)
        for query in ("limit=0", "limit=101", "offset=-1", "offset=100001"):
            self.assertEqual(self.client.get(f"/api/sessions?{query}").status_code, 422)

    def test_unavailable_database_does_not_claim_save(self):
        # A directory cannot be used as a SQLite file; no chmod assumptions.
        with TestClient(create_app(Path(self.directory.name))) as unavailable:
            health = unavailable.get("/api/health")
            self.assertEqual(health.status_code, 503)
            self.assertEqual(health.json(), {
                "status": "unavailable", "storage_available": False,
                "provider_mode": "mock", "provider_configured": True,
            "live_calls_reserved": 0, "live_call_limit": 50,
            })
            schema = unavailable.get("/openapi.json").json()
            self.assertEqual(
                schema["paths"]["/api/health"]["get"]["responses"]["503"]
                ["content"]["application/json"]["schema"]["$ref"],
                "#/components/schemas/Health",
            )
            response = unavailable.put(self.url, json=fictional_session())
            self.assertEqual(response.status_code, 503)
            self.assertEqual(response.json()["error"]["code"], "storage_unavailable")
            self.assertNotIn(str(self.directory.name), response.text)
            self.assertNotIn("saved", response.json())


if __name__ == "__main__":
    unittest.main()
