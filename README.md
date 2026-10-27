# Breathing Room — paced breathing

IST 402 · Local Part 2 coursework prototype · October 26, 2026

A simple Vue interface guides six cycles: four counts in, six out. Pause, Stop,
still-text pacing and an independent crisis-support panel remain available.
FastAPI and SQLite save sessions, conversations, actual replies, request status
and explicit display preferences. Optional chat retrieves scoped records through
a two-stage SQL RAG pipeline.

**Default/current mode: labeled mock replies.** Two live OpenAI exchanges were
verified on October 26 using `gpt-4.1-mini` (four model calls), then the app was
returned to mock mode for routine testing. Saved live replies keep their AI labels.
The history answer included an unsupported pause claim; the prompt was tightened,
but that change has not been live-retested. See [report.md](report.md).

This is a fictional coursework prototype, not therapy, diagnosis, monitoring or
a public support service. Only fictional content belongs in its local database.

## Run

From the project root, use two terminals:

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
calls count conservatively. Four live calls were used in the Part 2 demonstration; replaying saved IDs added none.

For repeatable peer testing, use `PROVIDER_MODE=mock` and restart. The mock adapter
is fixed demonstration logic (`demo-v1`), not an AI or a clinical classifier.
Live requests send the question and selected fictional records to OpenAI.

## Verified environment and installation

Existing dependencies were installed with prior user approval. October 26 work
installed no additional packages. HTTPX was moved from the dev manifest to runtime
because the provider adapter now uses the already-installed library.

- Python 3.14.7, SQLite 3.50.4, FastAPI 0.156.0, Uvicorn 0.54.0,
  HTTPX 0.28.1, Pydantic 2.14.1.
- Node 24.18.1, npm 11.16.0, Vue 3.5.44, Vite 7.3.7,
  @vitejs/plugin-vue 6.0.10.

For a fresh environment, these are the installation commands used for this
project. A separate clean-checkout installation is still unverified; follow
AGENTS.md's installation-approval rule when acting as an agent.

```sh
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements-lock.txt
npm install --prefix frontend --cache /private/tmp/mental-health-npm-cache
```

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
  territories; verified October 26. External services require their own connection.
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
  config.py                Explicit backend-only configuration
backend/tests/             Temporary fictional data; no working-data reseeding
frontend/tests/            Timing and HTTP contract checks
backend/setup_live.py      Private optional setup; no API call or overwrite
data/app.sqlite3           Ignored runtime records, retained across restart
```

## Boundaries and remaining work

- Two live cases establish working integration, not reliable grounding across cases.
  The revised pause-history instruction needs live evaluation in Part 3.
- Unfinished exercise reloads reset without saving; Stop/finish records save normally.
  Unconfirmed session/chat retries survive same-tab refresh through sessionStorage;
  closing the tab can lose unsent content. Saved records remain in SQLite.
- SQL supports five approved retrieval shapes, not arbitrary analytics. At most
  five records/12,000 context characters reach answer generation. Answers can
  still be inaccurate; citation validation does not prove semantic correctness.
- Single fictional local profile, no accounts or production security/deployment.
- Screen reader, OS reduced-motion changes, browser zoom/text-spacing overrides,
  true hidden-tab triggering and clean checkout need further verification.
- Figma, extra skills, history deletion and clinical evaluation are outside this increment.
- Report publication requires a reviewed commit and push; Canvas upload remains manual.

[Part 2 report](report.md) · [Verification](docs/verification.md) ·
[Process evidence](docs/evidence.md) · [AI disclosure](AI-USE.md) ·
[Current handoff](handoffs/current.md)

The earlier [published Part 1 design](https://github.com/tmy5235/Mental_Health/tree/f7b91254907a3eb18b22dc7d58b82a89960c63cb)
is preserved. No source from the previous Expedia project was copied.
