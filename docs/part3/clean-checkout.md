# Clean-checkout verification — November 2, 2026

Verified application source commit `9e3819006d56ae63379ceafe24ca677406d2c646`
in a separate `git clone --no-hardlinks --branch codex/part3-final` of the local
repository. This is a clean tracked-file checkout, not a copy of the working
folder. No private `.env`, virtual environment, node_modules, or existing SQLite
database was copied. Installation used public package registries and caches;
the clone source was local so this does not separately test GitHub authentication.

Followed the README from the clean project root:

```sh
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements-lock.txt
npm ci --prefix frontend
backend/.venv/bin/python -m pip check
backend/.venv/bin/python -W error::ResourceWarning -m unittest discover -s backend/tests -t backend -v
npm test --prefix frontend
npm run build --prefix frontend
```

Only cache-directory flags were added to keep installer caches in scratch space.
Python install passed; npm installed 37 packages and reported zero known
vulnerabilities at that time. `pip check` reported no broken requirements.
All 40 backend and 14 frontend tests passed; the Vite production build passed.
The known Starlette HTTPX TestClient deprecation warning remains. No warning
was hidden and no replacement package was added merely to silence it.

Started the clean checkout with the README's exact commands and standard ports:

```sh
backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
npm run dev --prefix frontend
```

Real browser/API verification confirmed empty session/conversation tables,
mock mode with no key, honest empty-history reply, stable saved message IDs after
reload, support-panel access, and a successfully saved stopped exercise. The
backend created its own database automatically. [Observed JSON](clean-browser.json)
and [home screenshot](clean-home.png) record this check. The process-restart test
independently checked retained records and idempotent retries after restart.

Logs: [Python install](clean-install-python.txt), [npm install](clean-install-node.txt),
[backend tests](clean-tests-backend.txt), [frontend tests](clean-tests-frontend.txt),
[production build](clean-build.txt). Later evidence/report/recording edits do not
change the application source or dependency locks tested here.

This check used the same macOS machine and installed Chrome. Another operating
system, an inexperienced human's setup time and live credential entry on a new
machine were not tested. A key is unnecessary for the required mock-mode setup.
