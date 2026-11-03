# Final verification

Final review: November 2, 2026, America/New_York. Raw timestamps use UTC and can
fall on November 3. Evaluation used fictional data and mock mode unless explicitly
identified as the earlier bounded live sample. No working database was reseeded.

## Commands and results

From the project root:

```sh
backend/.venv/bin/python -m pip check
backend/.venv/bin/python -W error::ResourceWarning -m unittest discover -s backend/tests -t backend -v
npm test --prefix frontend
npm run build --prefix frontend
```

All **40 backend and 14 frontend tests pass**, dependency checking reports no broken
requirements, and the production build passes. Backend tests cover validation,
idempotent/conflicting saves, transactions/restart, scoped SQL rejection, provider
failure/caps, preferences, pagination boundaries and fixed-rule replay without a
provider. Frontend tests cover the clock, delayed callbacks, pause/stop and HTTP
failure contracts. Provider responses in automated tests are mocked.

Latest logs: [backend](part3/final-review/backend.txt),
[frontend](part3/final-review/frontend.txt), [build](part3/final-review/build.txt).
The known Starlette HTTPX TestClient deprecation warning remains visible; it did
not fail the suite and was not hidden by changing warning policy.

## Browser and data checks

The final review served the production frontend build at localhost port 5174,
proxied to a separate mock API on port 8004 with an isolated fictional database.
The normal working app/database/configuration were preserved. Browser command:

```sh
APP_URL=http://127.0.0.1:5174 EVIDENCE_DIR=../docs/part3/final-review/ node scripts/browser-evaluation.mjs
```

The runner verified 17 scenarios and recorded one inconclusive automation result
because it could not hide the tab. A separate native Chrome tab switch verified
that S15 returns paused without automatic resumption. All 18 scenarios therefore
have passing observations across automated and native checks; the original
inconclusive JSON is preserved. The [matrix](part3/evaluation.md) lists expected
and actual behavior, three cross-case checks and limitations.

The final visible sequence measured **66.985 seconds** from first observed instruction
to visible Finished, including observer/scheduling delay. Saved timestamps span
60.003 seconds with 60 active seconds/six cycles. Start-to-instruction was 47.5ms;
scripted page entry was 71.2ms. These are separate measurements, not human setup
time. The original run measured 60.321 seconds. Both meet the supplied 90-second
boundary; neither included voluntary pauses/support visits.

Read-only SQLite checks compare the completed-session ID/fields against browser
observations, validate integrity and foreign keys, and check duplicate request/role
pairs. [Final database results](part3/final-review/database-check.json) supplement
the [original inspection](part3/database-check.json). The restart integration test
independently verifies retained records and successful retry replay.

## Reproducibility, model sample and recordings

The [clean-checkout check](part3/clean-checkout.md) installed declared dependencies
from tracked source, started both services without a private key or existing database,
and verified empty history, mock chat, reload, support and saving. Application source
and dependency locks remain unchanged by this documentation audit; the evaluation
runner now accepts EVIDENCE_DIR to preserve earlier artifacts.

Four live inputs were each repeated twice using gpt-4.1-mini: eight exchanges/16
calls. Five replies met the criteria; three motivated fixed-rule refinements.
[Raw outputs](part3/live-results.json) remain unchanged. No paid calls were needed
for this final review. The deterministic fixes are not reported as additional
successful live-model tests.

Both normal-speed [recordings](part3/recordings.md) were checked through metadata
and representative decoded frames. Written captions explain the actual browser
behavior and generated source. No independent human participant study is claimed.

## Document review and boundaries

All maintained Markdown files were reconciled with the implementation and supplied
requirements; stale startup plans and contradictory current claims were removed.
Local links and referenced artifacts are checked before packaging. Historical
JSON, logs and recordings retain their original wording and results.

Full screen-reader speech, native browser zoom, real OS reduced-motion settings,
another operating system and live credential entry on a new machine remain
untested. Browser emulation does not establish those outcomes. No clinical benefit
or comprehensive accessibility conformance is claimed. The final branch has been
pushed to the existing GitHub repository with explicit authorization. Publication
link checks are a separate delivery check from application testing; the final
report identifies the published checkpoint and linked evidence.
