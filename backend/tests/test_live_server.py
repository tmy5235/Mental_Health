"""Real localhost HTTP and process-restart check using temporary fictional data."""

import json
import signal
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import closing
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener

from tests.test_repository import SESSION_ID, fictional_session

BACKEND = Path(__file__).resolve().parents[1]
SERVER_CODE = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import uvicorn
from app.main import create_app
from app.config import Settings
uvicorn.run(create_app(Path(sys.argv[2]), Settings()), host="127.0.0.1",
            port=int(sys.argv[3]), log_level="info")
"""


class LiveServerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "live.sqlite3"
        self.process = None
        self.log = self.enterContext(tempfile.TemporaryFile(mode="w+"))
        self.opener = build_opener(ProxyHandler({}))
        self.addCleanup(self.stop_server)

    def start_server(self):
        with closing(socket.socket()) as listener:
            listener.bind(("127.0.0.1", 0))
            port = listener.getsockname()[1]
        self.base = f"http://127.0.0.1:{port}"
        self.process = subprocess.Popen(
            [sys.executable, "-c", SERVER_CODE, str(BACKEND), str(self.path), str(port)],
            cwd=self.directory.name,
            stdout=self.log,
            stderr=self.log,
        )
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                self.log.seek(0)
                self.fail(f"Server exited before readiness: {self.log.read()}")
            try:
                status, body = self.request("GET", "/api/health")
                if status == 200 and body["storage_available"]:
                    return
            except (URLError, TimeoutError):
                pass
            time.sleep(0.05)
        self.fail("Local server did not become ready within ten seconds.")

    def stop_server(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)

    def request(self, method, path, payload=None):
        request = Request(
            self.base + path,
            data=None if payload is None else json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method=method,
        )
        try:
            response = self.opener.open(request, timeout=2)
        except HTTPError as error:
            response = error
        with response:
            return response.status, json.load(response)

    def test_saved_records_survive_real_server_restart_without_duplicates(self):
        self.start_server()
        self.assertEqual(self.request("GET", "/api/sessions")[1]["sessions"], [])
        with closing(sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM sessions").fetchone()[0], 0)
        url = f"/api/sessions/{SESSION_ID}"
        status, saved = self.request("PUT", url, fictional_session())
        self.assertEqual(status, 200)
        self.assertTrue(saved["saved"])
        self.assertEqual(self.request("PUT", url, fictional_session()), (200, saved))
        self.assertEqual(self.request("PUT", url, fictional_session(display_mode="motion"))[0], 409)
        self.assertEqual(self.request("PUT", url, fictional_session(cycles_completed=6))[0], 422)
        completed_id = "22222222-2222-4222-8222-222222222222"
        completed = fictional_session(
            started_at="2026-10-20T13:00:00Z", ended_at="2026-10-20T13:01:00Z",
            status="completed", active_duration_seconds=60, cycles_completed=6,
        )
        self.assertEqual(self.request("PUT", f"/api/sessions/{completed_id}", completed)[0], 200)
        status, history = self.request("GET", "/api/sessions")
        self.assertEqual(status, 200)
        expected = [(completed_id, "completed", 60.0), (SESSION_ID, "stopped", 20.0)]
        self.assertEqual(
            [(row["id"], row["status"], row["active_duration_seconds"]) for row in history["sessions"]],
            expected,
        )
        conversation = "33333333-3333-4333-8333-333333333333"
        request_id = "44444444-4444-4444-8444-444444444444"
        chat_url = f"/api/conversations/{conversation}/messages/{request_id}"
        chat_input = {"content": "What happened in my last session?"}
        chat_status, exchange = self.request("PUT", chat_url, chat_input)
        self.assertEqual(chat_status, 200)
        self.assertEqual(exchange["messages"][1]["record_ids"], [completed_id])
        self.stop_server()
        # Uvicorn restores and re-raises SIGTERM after graceful shutdown.
        self.assertIn(self.process.returncode, (0, -signal.SIGTERM))
        self.log.seek(0)
        self.assertIn("Application shutdown complete.", self.log.read())
        with closing(sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)) as connection:
            self.assertEqual(connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(connection.execute("PRAGMA foreign_key_check").fetchall(), [])
            self.assertEqual(connection.execute(
                "SELECT id, status, active_duration_seconds FROM sessions ORDER BY started_at DESC, id DESC"
            ).fetchall(), expected)
        self.start_server()
        self.assertEqual(self.request("GET", "/api/sessions"), (200, history))
        self.assertEqual(self.request("PUT", url, fictional_session()), (200, saved))
        self.assertEqual(len(self.request("GET", "/api/sessions")[1]["sessions"]), 2)
        self.assertEqual(self.request("PUT", chat_url, chat_input), (200, exchange))
        restored = self.request("GET", f"/api/conversations/{conversation}")[1]["messages"]
        self.assertEqual(restored, exchange["messages"])
        with closing(sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM messages").fetchone()[0], 2)
        self.stop_server()
        self.assertIn(self.process.returncode, (0, -signal.SIGTERM))
        self.log.seek(0)
        self.assertEqual(self.log.read().count("Application shutdown complete."), 2)


if __name__ == "__main__":
    unittest.main()
