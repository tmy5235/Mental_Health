# Breathing Room — paced breathing

IST 402 · Final Part 3 assignment prototype · November 2, 2026

A simple Vue interface guides six cycles: four counts in, six out. Pause, Stop,
still-text pacing and an independent crisis-support panel remain available.
FastAPI and SQLite save sessions, conversations, actual replies, request status
and explicit display preferences. Optional chat retrieves scoped records through
a two-stage SQL RAG pipeline.

**Default mode: labeled mock replies.** The final evaluation used 18 fictional browser
scenarios, repeatable backend/frontend tests, and eight live exchanges (16 model
calls). The live results exposed ambiguous pause-history wording and weak crisis
redirection. Narrow application-owned rules now answer recognized crisis phrases
and past-pause questions before any model call; these are labeled **App reply ·
fixed guidance**. They are not a distress detector. See [Part 3 evaluation](docs/part3/evaluation.md).

This is a fictional-use assignment prototype, not therapy, diagnosis, monitoring or
a public support service. Only fictional content belongs in its local database.

## Fresh checkout and run

Prerequisites: Python 3.14, Node.js 24/npm, and Git. The verified versions below
are the tested environment, not a claim that all older versions work.

From the extracted submission or local repository root (the final branch is not
yet published):

```sh
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements-lock.txt
npm ci --prefix frontend
```

No API key or existing database is needed. Use two terminals from the project root:

```sh
backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

```sh
npm run dev --prefix frontend
```

Open [the app](http://127.0.0.1:5173/). Stop each server with Ctrl+C.
Vite forwards `/api` to FastAPI on port 8000. Only Python opens SQLite at
`data/app.sqlite3`, resolved from the project location. Startup creates missing
schema without reseeding or replacing existing records.

No key is required for mock mode. **Do not share a real API key in chat, source,
screenshots or submitted documents.** To configure optional live chat privately:

```sh
backend/.venv/bin/python backend/setup_live.py
```

The helper accepts hidden terminal input, verifies `.env` is ignored, creates
`backend/.env` with owner-only access and refuses to overwrite an existing file.
It makes no API calls. Its noninteractive cancellation path has been checked;
real credential entry has not been exercised. Alternatively, create `.env`
locally using `.env.example` as the format without overwriting existing settings.

Set `PROVIDER_MODE=openai`, `OPENAI_API_KEY`, and `OPENAI_MODEL` (suggested supported
model: `gpt-4.1-mini`). Restart FastAPI and refresh Chat. Environment variables
have precedence over `.env`. Health reports configuration presence, not credential
validity. A successful reply labeled **AI reply** is required to verify live use.
API usage may incur charges; two calls are reserved per live exchange, with a
persistent 50-call cap for the configured `DEMO_SESSION_ID`, then labeled mock
fallback. Keep that ID unchanged during one demonstration. Failed/unused reserved
calls count conservatively. The recorded evaluations used four calls in Part 2 and 16 in Part 3; replaying saved IDs added none. No further paid calls were used for final review.

For repeatable evaluation, use `PROVIDER_MODE=mock` and restart. The mock adapter
is fixed demonstration logic (`demo-v1`), not an AI or a clinical classifier.
Live requests send the question and selected fictional records to OpenAI.

## Verified environment

- Python 3.14.7, SQLite 3.50.4, FastAPI 0.156.0, Uvicorn 0.54.0,
  HTTPX 0.28.1, Pydantic 2.14.1.
- Node 24.18.1, npm 11.16.0, Vue 3.5.44, Vite 7.3.7,
  @vitejs/plugin-vue 6.0.10; Playwright 1.64.1 for development-only browser checks.
- Browser evaluation: installed Google Chrome 156.0.8078.80 on macOS.

Fresh installation creates project-local dependencies. No dependencies or secret
files from the Part 2 checkout are required. npm reported pending optional install
scripts; the installed Vite build and server worked without approving extra scripts.
See [clean-checkout evidence](docs/part3/clean-checkout.md) for actual commands/results.

## Checks

```sh
npm test --prefix frontend
npm run build --prefix frontend
backend/.venv/bin/python -m pip check
cd backend
.venv/bin/python -W error::ResourceWarning -m unittest discover -s tests -t . -v
```

The backend process test needs permission to bind localhost ports. Starlette's
HTTPX TestClient deprecation warning is known; no replacement dependency was
installed. See [verification](docs/verification.md) for actual observations,
commands, screenshots and boundaries. Automated provider checks are HTTP-mocked,
not live API evidence.

## Design and responsibilities

- Immediate Start; no questionnaire, required chat, mood score or click tracking.
- Fixed application-owned timing and exits. Model output cannot operate controls.
- One quiet central task; brief copy, muted blue/ivory, readable dark text,
  visible keyboard focus, 18px base text/optional 20px and still pacing by default.
- Chat, History and Display settings are optional. Save only explicit choices.
- Independent bundled support resources, labeled for the United States and
  territories; verified November 2. External services require their own connection.
- Records describe activity or attributed messages, never inferred emotional state.

The chosen skill, R1–R4/D1–D6 mappings, alternatives, research sources, API contracts
and implementation decisions are in [design-pipeline.md](docs/design-pipeline.md).
The palette is an aesthetic/accessibility choice, not proven anxiety reduction.

```text
frontend/src/
  App.vue                  Views, exercise lifecycle, session outbox, preferences
  breathing.js             Fixed timing rules (no model control)
  api.js                   HTTP, finite deadlines, save confirmation
  components/ChatPanel.vue  Chat, conversation history and retry
  components/SessionHistory.vue  Paginated factual session table
  style.css                Responsive presentation and focus styles
backend/app/
  main.py                  Small FastAPI routes and error envelopes
  models.py / chat_models.py  Typed validation and responses
  controllers.py / chat_controller.py  Business rules and orchestration
  repository.py / chat_repository.py  Parameterized SQLite writes and reads
  retrieval.py             Finite SQL allowlist, ownership, read-only limits
  provider.py              Reviewed prompts, mock and OpenAI adapters
  reply_policy.py          Narrow fixed replies before model use
  config.py                Explicit backend-only configuration
backend/tests/             Temporary fictional data; no working-data reseeding
frontend/tests/            Timing and HTTP contract checks
backend/setup_live.py      Private optional setup; no API call or overwrite
data/app.sqlite3           Ignored runtime records, retained across restart
```

## Repeatable browser evaluation

Use a **separate fictional database**: the browser suite inserts fixtures and
saves sessions. Stop another API on port 8000, then run:

```sh
backend/.venv/bin/python scripts/serve_mock.py --database data/evaluation.sqlite3
```

Start the Vue frontend in a second terminal. In a third:

```sh
EVIDENCE_DIR=../docs/part3/new-evaluation/ node scripts/browser-evaluation.mjs
```

The runner uses installed macOS Google Chrome. Set `BROWSER_EXECUTABLE_PATH` to
another compatible Chromium executable on other platforms. It refuses a live
backend. EVIDENCE_DIR is resolved relative to `scripts/`; the command above writes
to `docs/part3/new-evaluation/`. Without it, the default is `docs/part3/`.
Always use a new output directory to preserve submitted evidence. `SCENARIOS=S17,S18` runs selected checks. `HEADLESS=false`
opens visible Chrome; browser automation did not establish a hidden document in
either mode, so the automated S15 result remains inconclusive. A separate native Chrome
check verified the paused return state; see the final evaluation.

To reproduce the pagination regression on the final version:

```sh
node frontend/node_modules/playwright/cli.js install ffmpeg
node scripts/chat-pagination-check.mjs
```

The `--baseline` option is only for the earlier Part 2 implementation and should
fail its expected-old-behavior assertion on the corrected version. Recordings use
real browser views with clearly labeled editorial captions. `scripts/record-demo.mjs`
requires the fictional live-result conversations to be present in the served demo
database; it is a recording script, not a fresh-install acceptance test.

Optional paid evaluation is explicit:

```sh
backend/.venv/bin/python scripts/evaluate_live.py --allow-live --env-file /private/path/to/.env
```

It uses a separate fictional database, reserves at most 16 calls across reruns,
and never prints credentials. The submitted raw live results are the original
pre-rule observations, preserved unchanged. Do not overwrite them or interpret
fixed-reply regression tests as further live-model success.

## Boundaries

- Narrow phrase rules can miss indirect crisis wording and match quoted/negated
  text. Unknown-pause wording outside the rule can still receive a flawed model
  answer. Independent support is always available; no risk score is produced.
- SQL supports five approved retrieval shapes. Citation-ID validity does not
  establish semantic truth. Live results cover only four inputs repeated twice.
- Unfinished exercise refresh resets without saving, disclosed before Start.
  Pending retries survive same-tab refresh but may be lost on tab closure.
- Single fictional local profile; no accounts, history deletion, clinical
  evaluation, or public support-service deployment.
- Real OS reduced-motion changes, screen-reader speech, native browser zoom,
  and another operating system remain unverified. Native Chrome background-tab
  pausing was verified separately from browser automation.
- Mock versus fixed versus live replies are explicitly labeled. Stored activity
  never establishes feelings or improvement.

Final review: **54 automated tests and production build pass; 17 automated browser
scenarios pass, with S15 verified separately in native Chrome.** All 18 scenarios
have passing observations across those methods. The final visible exercise ran
66.985 seconds, within the 90-second requirement. See [requirement coverage](docs/part3/requirements.md).

[Part 3 report](report.md) · [Final evaluation](docs/part3/evaluation.md) ·
[Recordings](docs/part3/recordings.md) · [Process evidence](docs/evidence.md) ·
[AI disclosure](AI-USE.md) · [Current handoff](handoffs/current.md)

The earlier [published Part 1 design](https://github.com/tmy5235/Mental_Health/tree/f7b91254907a3eb18b22dc7d58b82a89960c63cb)
and [Part 2 submission](https://github.com/tmy5235/Mental_Health/blob/e96469e/report.md)
remain available. No source from the Expedia project was copied.
