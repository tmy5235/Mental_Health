# Part 1 verification

October 15, 2026. This milestone verifies a design package, not application behavior.

## Document checks

The local check uses Python's standard library to inspect repository Markdown
links and required folders, confirm all R1–R4/D1–D6 mappings, and scan for stale
starter placeholders and the superseded retrieval proposal. The publication
review checks the intended file list and excludes credentials, databases,
dependencies, and private source material.

| Check | Expected | Observed |
| --- | --- | --- |
| Starter structure | README, AGENTS, and all six folders exist | Passed: frontend, backend, data, docs, prompts, handoffs. |
| Local Markdown links | Every local destination exists | Passed. Course links may require institutional access. |
| Research mapping | R1–R4 and D1–D6 each have a decision and tradeoff | Passed in design-pipeline.md. |
| Design completeness | Fictional task, three screens, flow, model/data roles, personalization/control, alternatives, and open questions | Present in design-pipeline.md; document inspection only. |
| SQL RAG consistency | README, AGENTS, design, and report specify the two-call workflow | Passed; earlier ordinary-query-only proposal is superseded and recorded as a revision. |
| Timing arithmetic | Six cycles of 4 + 6 seconds | 60 seconds of breathing; proposed total 60–65 seconds, unmeasured. |
| Starter placeholders | Completed design guidelines, no undecided starter fields | Passed in README. Implementation questions remain explicitly listed. |
| Runtime claims | No planned behavior presented as tested | No running app, database, mocked/live-model test, or clinical-effectiveness claim. |

## Access and publication

The separate Canvas Part 1 submission page redirected to Penn State sign-in in
the available browser. No additional page-specific instructions or exact deadline
were verified. Requirements were checked against the supplied course texts, including the user-state ideation activity
and the research-table image. No Canvas upload has been performed.

Published the assessed design to [Mental_Health](https://github.com/tmy5235/Mental_Health)
on branch `codex/assignment3-part1`. The initial, now superseded design checkpoint was:
`58d92cb028d3fe52f3bf452bad1a810253548e20`.

Ran `python3 /tmp/check_mental_health_links.py` using concurrent anonymous
`curl -q --location --max-time 25` checks, without cookies or authorization
headers. The repository, assessed commit, and six linked documents all returned
HTTP 200. [Recorded results](publication-links.json) contain the checked URLs
and statuses. This establishes public document access at check time, not Canvas
submission or application behavior. The user-state ideation revision changes the design and supersedes that initial
checkpoint. The current assessed commit is identified in report.md. Link evidence
is refreshed after publication; earlier access checks do not prove access to a
new snapshot.

## Later checks — not executed

Exercise timing, pause/exit behavior, reduced motion, keyboard/narrow-screen use,
late model responses, crisis access after failure, SQLite persistence/restart,
scoped retrieval, rejected SQL, empty results, and duplicate prevention all need
implementation and observed results. The fictional cases in the design document
are a test plan. They are not passed tests.

## User-state ideation document review

Checked that README and design-pipeline.md consistently select explicit display
controls, exclude questionnaires/click-based state inference from the current
scope, distinguish self-report from interaction records and interpretation, and
specify missing/conflicting-information behavior. The report summarizes the
tradeoff. Source notes attribute study claims to the supplied activity and do not
claim direct reading, dataset inspection, or completion of a separate graded
activity. Local Markdown links and all ten R/D mappings were rechecked. These
are document checks only; the new fictional scenarios remain unexecuted.

## Revised publication verified

The user-state ideation design is published at
`f7b91254907a3eb18b22dc7d58b82a89960c63cb`, superseding the earlier design checkpoint.
Ran `python3 /tmp/verify_mental_health_report.py` to extract and check every exact
URL in the revised report. The repository, new assessed commit, and six pinned
documents all returned HTTP 200 without authentication. The recorded JSON now
contains these updated results. This confirms accessibility, not Canvas upload.

## October 20, 2026 — initial backend source

Environment: Python 3.14.7, Node v24.18.1, npm 11.16.0. Module discovery found no
FastAPI, Uvicorn, HTTPX, or Pydantic in the current interpreter. No packages were
installed. Created `codex/implementation-foundation` from clean `6a0fc60` on
`codex/assignment3-part1`. No commit or push performed.

| Command/check | Expected | Observed |
| --- | --- | --- |
| `python3 -m unittest tests.test_repository -v` from `backend/` | Seven storage checks pass | Passed 7/7: empty startup, retry/reopen, conflict preservation, concurrent retries, order/pagination, rollback, project-relative path. |
| Read-only SQLite inspection within retry/reopen test | Matching row and valid relationships | One fictional stopped record, 20 active seconds, expected UUID/profile; no foreign-key violations. |
| `python3 -m compileall -q backend/app backend/tests` from root | Source parses | Passed; does not verify third-party imports. |
| `git diff --check` | No whitespace errors | Passed. |
| `git check-ignore backend/.env backend/.venv/pyvenv.cfg data/app.sqlite3` | All paths ignored | Passed. |

Tests use temporary SQLite files removed afterward; no working database exists.
Reopening the repository is storage persistence evidence, not a server restart.
The HTTP suite is authored but unexecuted. It covers health, validation,
completion, UTC normalization, retries, conflicts, app lifecycle restart, and
unavailable storage. Install dependencies after approval, verify versions/imports,
and run the full suite before recording any HTTP success.

No browser, live server restart, frontend-to-backend, exercise timing, crisis
resource, RAG, mock-provider, or live-provider checks have occurred.

## October 20, 2026 — approved installation and backend verification

This section supersedes the pending installation/HTTP status above. The user
explicitly approved installing backend dependencies and continuing tests.

Setup actually run from the project root:

```sh
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements-dev.txt
```

The initial pip attempt failed because the sandbox could not resolve pypi.org.
The approved network-enabled retry used:

```sh
backend/.venv/bin/python -m pip install --no-cache-dir -r backend/requirements-dev.txt
```

It succeeded. Imports and interpreter prefix confirmed project-local installation:
Python 3.14.7; SQLite 3.50.4; FastAPI 0.156.0; Uvicorn 0.54.0; HTTPX 0.28.1;
Pydantic 2.14.1; Starlette 1.9.0. Pinned direct manifests and captured all 17
resolved dependencies with `backend/.venv/bin/python -m pip freeze` into
`backend/requirements-lock.txt`. Checked that lock against the installed set with
`backend/.venv/bin/python -m pip install --no-index --no-cache-dir -r backend/requirements-lock.txt`;
all requirements were already satisfied. `backend/.venv/bin/python -m pip --no-cache-dir check`
reported no broken requirements. No second clean-environment install was run.

### Observed tests and corrections

From backend, ran:

```sh
.venv/bin/python -W error::ResourceWarning -m unittest discover -s tests -t . -v
```

Final full-suite result: **15 passed** (7 repository, 7 API, 1 real-process HTTP).
Localhost binding needed sandbox escalation; the initial restricted execution
failed with PermissionError before the live-server check could run.

The initial 14-test run passed but exposed an unclosed SQLite connection in test
inspection code. Added explicit contextlib.closing around those test connections.
No ResourceWarning appeared in subsequent runs. The new restart check initially
failed because it expected exit code zero after SIGTERM. Inspection of installed
Uvicorn server.py confirmed it restores/re-raises the signal after shutdown.
The test now accepts that signal exit and requires `Application shutdown complete.`
for both server stops. This corrected the test assumption, not app persistence.

| Check | Expected | Observed |
| --- | --- | --- |
| Health/empty history | Healthy status, provider not implemented, no seeded sessions | Passed in TestClient and actual localhost HTTP. |
| Valid stopped/completed saves | Exact status, duration, cycles, normalized UTC times | Passed. Real-process rows: stopped UUID 11111111-1111-4111-8111-111111111111 at 20 seconds; completed UUID 22222222-2222-4222-8222-222222222222 at 60 seconds. |
| Identical and concurrent retries | One record per stable ID | Passed; no duplicates. |
| Changed payload with existing ID | 409, preserve original | Passed. |
| Invalid fields, duration, cycles, timezone, URL, pagination | 422; no invalid rows | Passed. |
| Unavailable database | 503 without save confirmation or path disclosure | Passed. Health uses its documented health body. |
| Process restart | Same ordered history and stable IDs after shutdown/new process | Passed using two actual Uvicorn processes and real loopback HTTP. |
| SQLite/API comparison | Matching IDs/status/duration, valid relationships | Passed using read-only SQLite; integrity_check was ok, foreign_key_check returned no violations. |
| Health OpenAPI error contract | 503 schema references Health | Corrected the route's response documentation; all 7 API tests passed again afterward. Runtime behavior unchanged. |

### Default command, storage, browser, and shutdown

Ran the following from the project root:

```sh
backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Actual HTTP GETs (urllib.request with a proxy-free opener) to /api/health,
/api/sessions, and /openapi.json returned 200. Read-only inspection of the actual
`data/app.sqlite3` found demo_profiles and sessions, zero rows in both, the
sessions.profile_id foreign key, and `PRAGMA integrity_check` = ok. No fixture
records were inserted into this working database; test records lived in temporary
files and were removed by the tests. The default database and environment match
Git ignore rules.

Attempted browser navigation with cua.createBrowserTab to
http://127.0.0.1:8000/api/health. The browser returned ERR_BLOCKED_BY_CLIENT;
no successful browser rendering or refresh is claimed. Direct HTTP checks do
not replace that evidence. Ctrl+C stopped the default server; logs confirmed
application shutdown complete. No server remains running from this check.

Remaining warning: Starlette 1.9.0 deprecates its HTTPX TestClient adapter and
suggests HTTPX2. Tests pass with the authorized HTTPX dependency; no additional
package was installed or warning suppressed. Revisit during future dependency
updates. Browser/UI, exercise timing, support content, conversations, RAG,
preferences, and provider integration remain untested/unimplemented. Zero model
calls were made. Backend checks are not clinical or usability evaluation.

## October 20, 2026 — running Vue app and end-to-end evidence

User requested a running app and explicitly approved Vue 3, Vite 7, and the
Vue plugin installation. Ran from the project root:

```sh
npm install --prefix frontend --cache /private/tmp/mental-health-npm-cache
npm run dev --prefix frontend
npm run build --prefix frontend
npm test --prefix frontend
npm ls --prefix frontend --depth=0
```

Installed Vue 3.5.44, Vite 7.3.7, @vitejs/plugin-vue 6.0.10. npm added 34 packages,
audited 35, and reported zero known vulnerabilities at that check. A pending
esbuild postinstall-script notice appeared; no additional scripts were approved.
The dev server and production build work with the installed package binaries.
package-lock.json records resolution. No frontend test framework was installed;
node:test runs the timing and HTTP-helper tests.

**Automated results:** 12 frontend tests pass and Vite builds. All 15 backend
tests passed again, using the already documented command with localhost socket
permission. Total: 27. The Starlette HTTPX deprecation warning remains.

### Real browser and database observations

Used Chrome Guest via computer-use tools for the initial health round trip and
full-duration run, then the Codex in-app browser for subsequent checks. Raw JSON
navigation was previously blocked in Codex, but the Vue HTML URL works. No model
calls were made. All exercise records are labeled fictional. External support
links were displayed and inspected, not called or submitted to.

| Check | Expected | Observed |
| --- | --- | --- |
| Initial Vue/FastAPI round trip | Vue renders health result from HTTP JSON | “Local session storage is connected” appeared in Chrome before exercise UI expansion. |
| Six-cycle completion | Fixed 4/6 cycle, 60 active seconds, under 90 seconds including overhead | Completed UI showed 60.0 seconds/6 cycles and confirmed save. Stored timestamps differ by 60.004 seconds; completion was observed within 65.6 seconds of Start. |
| UI/API/SQLite identity | Same saved ID/status/duration | `ee246f94-1082-4126-9316-a110542df822`: completed, 60.0 seconds, 6 cycles, motion. UI record details, API JSON, and read-only SQLite matched. |
| Text-only display and support | Text pacing; support pauses; Return does not resume | Observed text/count display, “1 PAUSED”, explicit Resume, and independent support dialog. |
| Stop inside support | Exit immediately and save stopped status | `12b6a9c9-f181-4e3d-a506-8c5fb00bd941`: stopped, 8.063 seconds, zero completed cycles, text. Saved confirmation shown. |
| Backend outage | Exercise/support remain usable; no false successful save | Stopped FastAPI, started exercise and opened support, then stopped. UI showed Save not confirmed and Retry save. |
| Refresh and retry | Pending terminal payload survives refresh; one row after retry | Same-tab refresh retained the 3.698-second pending payload. Restarted FastAPI and retried; `77cc6a00-ca78-48cd-be55-a70119443f8b` appeared once in history/SQLite. |
| Server restart/history | Prior sessions remain intact | History after restart included previous completed/stopped records with stable IDs. |
| Keyboard controls | Visible focus; Pause/Resume retain focus | Tab then Enter paused; Enter resumed; focused control stayed on Resume/Pause with visible focus outline. |
| Refresh while unfinished | Reset to home, no fabricated completed record | Home returned; database count remained four after the unsaved exercise. |
| Explicit preferences | Choice survives refresh; can reveal options | Text selection and Show fewer options survived reload; Show more options restored controls. |
| Narrow viewport | Usable controls, no page-wide overflow | At 390×844, Start, support, text pacing, Pause/Resume, and Stop visible/usable. document scrollWidth and clientWidth both 390. |
| Color contrast calculation | Readable checked text pairs | Body 10.30:1, secondary 5.48:1, primary button 9.44:1, error text 6.92:1. Not a complete accessibility audit. |

Read-only SQLite at the verification checkpoint contained four unique IDs/four
rows: two completed motion sessions and two stopped text sessions. A second
completed session was created while the user was trying the app; preserved it,
without treating it as an independently measured agent test. No rows were deleted
or reseeded. PRAGMA integrity_check returned ok; foreign_key_check returned no
violations. Live demonstration records remain in the ignored working database.

### Corrections and limits

- Replaced separate conditional Pause/Resume buttons with one persistent button
  after noticing focus loss. Retested with keyboard; focus remained visible.
- Reworded non-JSON proxy failures as service unavailable and changed the footer
  to Latest session save not confirmed after save errors. Reran all frontend
  tests and build. The full outage/retry observation preceded these wording fixes.
- Added a sticky header so support stays available while scrolling. Inspected
  narrow-screen layout again after the change.
- A Codex tab-switch attempt left document.visibilityState = visible, so it did
  not exercise the hidden-tab handler. Hidden-tab pause is implemented but its
  real visibility-event trigger remains unverified in a native browser.
- Text mode was verified manually. Default detection of the OS reduced-motion
  setting, assistive-technology behavior, multi-page history pagination, and a
  clean npm install on another machine are not yet observed browser checks.
- No conversation/RAG/provider, backend preferences, interrupted-session recovery,
  Figma capture, clinical efficacy, or complete coursework evaluation is claimed.

Screenshot: [running app](screenshots/running-app.jpg). Temporary viewport override
was reset. Both local services are left running: frontend http://127.0.0.1:5173/,
backend http://127.0.0.1:8000. The Codex app tab was marked as a deliverable.

## Part 2 implementation and redesign — October 26, 2026

All data below is fictional. Local date is October 26 (stored UTC timestamps cross
into October 27). No live model call was made; all provider tests use deterministic
adapters or HTTPX MockTransport. This section supersedes older “not implemented”
status statements above, which remain historical records.

### Environment and automated checks actually run

- `node --version`: v24.18.1. Python 3.14.7; FastAPI 0.156.0; HTTPX 0.28.1 imports verified.
- `git check-ignore backend/.env`: ignored. No real `.env` file or key was added.
- `backend/.venv/bin/python -m pip check`: no broken requirements. Existing pip-cache
  permission warning only; no packages installed. HTTPX moved into runtime manifest.
- `npm test --prefix frontend`: **14 passed**, including stable chat IDs, confirmed
  replies, error codes and the fixed clock boundaries.
- `npm run build --prefix frontend`: passed; Vue/Vite production bundle generated.
- From backend, `.venv/bin/python -W error::ResourceWarning -m unittest discover -s tests -t . -v`:
  **36 passed**. Includes a real temporary Uvicorn process, two sessions and a chat
  exchange, shutdown/restart, same-ID retry and read-only SQLite comparison.
- `backend/.venv/bin/python backend/setup_live.py` without a terminal: correctly
  refused noninteractive key input without creating `.env`. Real credential entry
  and live provider access remain unverified. The helper does not make API calls.
- Known Starlette HTTPX TestClient deprecation warning remains; tests pass. No
  installation of an unapproved replacement package was attempted.

The 50 passing automated tests are software checks, not a completed Part 3 live
scenario evaluation. Provider coverage includes selected/empty retrieval, missing
configuration, failure at either stage, 401/timeouts/malformed/oversized/incomplete
responses, no invented reply, rejected citations, failed user/reply saves, duplicate
and conflicting retries, interrupted attempts, ordered history, scoped reads,
preferences, and persistent two-call budgeting with mock fallback at 50.

Unsafe query tests include DELETE, changed ownership, removed conversation scope,
extra statements, comments, excessive limit, PRAGMA, load_extension, CTE and UNION.
Rejected SQL never reaches execution or the answer call. Approved reads use a
read-only URI, query-only connection, restrictive SQLite authorizer and progress
handler. This intentionally supports a finite language, not a general SQL parser.

### Real browser observations

Used the existing Codex in-app browser at http://127.0.0.1:5173/. Interacted with
actual Vue controls and inspected rendered state; only fictional messages were
submitted. No external support links were activated.

| Check | Expected | Observed |
| --- | --- | --- |
| Simplified home | One prominent start, optional settings, no decorative motion | Centered brief instructions; Breathe/Chat/History; collapsed Display settings; visible Crisis support. |
| Full sequence | Six fixed 4/6 cycles; <90 seconds from start to final step | Finished UI showed 60.0 seconds/6 cycles and Saved. Session `6f38bdd8-9e16-4fbf-beac-e959f95795fe` has UTC start `2026-10-27T02:55:28.546000+00:00`, end `02:56:28.548000+00:00`: **60.002 seconds**, text display. |
| Entry/setup timing | Report separately from guided duration | User-paced navigation/setup excluded; not separately timed. No pause/support time in the full completion run. |
| Keyboard Pause/Resume | Focus retained; explicit resume | Enter toggled the same button; active element remained Resume. Enter resumed. |
| Support interruption | Pause; Return does not auto-resume | Opened support, returned to Paused, reopened and stopped from the dialog. |
| Early exit | Distinct stopped row; no forced completion | `cde9caa4-84e9-42b5-b67f-53fe37b996b2`: stopped, 0.752 active seconds, zero cycles, text. |
| Persisted conversation | Real HTTP/JSON and SQLite writes | Sent “What happened in my last session?”; labeled demo reply cited the existing stopped record, 3.698s/text. UI/API/SQLite IDs matched below. |
| Refresh and restart | Original ordered exchange remains | Refreshed browser and restarted real backend; same original two messages remained, with no reseed. |
| Chat service outage | Error, no invented reply, retry possible | Stopped FastAPI; submitted “How does the breathing exercise work?”; visible unavailable/Reply not confirmed state. |
| Independent support during failure | Bundled panel works without backend | Opened Crisis support while FastAPI was stopped. Region and external links rendered. |
| Refresh unconfirmed request | Retain same request for retry | Reloaded; pending text and Retry reply persisted. |
| Recovery | One exchange after retry | Restarted FastAPI; Retry reply saved one user/assistant pair under the original request ID. Read-only SQLite confirmed no duplicate request-role pairs. |
| Narrow home | No horizontal page overflow | At 390×844, clientWidth=scrollWidth=390; start/support and short text visible. |
| Larger text | Explicit, remembered, no overflow | Selected Larger; reload retained it and computed app font-size 20px. Widths remained 390. Reset returned to standard/still/collapsed. |
| Narrow chat | Wrapped messages without page overflow | clientWidth=scrollWidth=390, with saved messages and input usable. |
| Resource content | Region-specific verified information | Rechecked support resources with helpline lookup October 26; updated verification date; did not contact services. |

The completion measurement comes from start/end values captured by application
code around the monotonic-clock run and compared in SQLite; it is not an external
physiological measurement or a clinical benefit claim. The browser visibly rendered
Finished. Earlier October 20 timing evidence is retained separately above.

### Browser/API/SQLite identity and inspection

Conversation: `a2a98e89-10c0-49c3-86a4-a866c8efe3ae`.
First request: `82544a28-ccb0-4391-aeff-7d8006d5bdfa`.
User message: `36afcf74-904b-4eb2-8b0d-b5fe608d683c`.
Assistant message: `697b132d-675b-4022-a4d2-5953d4c4f239`.
Supporting session: `77cc6a00-ca78-48cd-be55-a70119443f8b`.
The exact factual reply, IDs and completed status matched the browser's expanded
Record details, GET `/api/conversations/{id}`, and a read-only SQLite join.

Outage/retry request: `4d391db0-7f15-48c1-b165-12b9cce57163`.
Saved user: `fd4ce1bb-8c68-473b-bd18-4ccd0c3ea83b`;
reply: `00f638f2-4626-418a-9b0a-ea4afa456ff2`.
The working DB at this checkpoint has six sessions (three completed/three stopped),
one conversation, four messages/two completed requests, and one preference row.
The original four sessions remain. No provider-usage rows/live calls were created.

Inspection used Python's standard `sqlite3` with
`sqlite3.connect(Path('data/app.sqlite3').resolve().as_uri() + '?mode=ro', uri=True)`
and `contextlib.closing`, not an installed database viewer. Representative queries:

```sql
SELECT name, sql FROM sqlite_master WHERE type = 'table';
SELECT id, status, active_duration_seconds, display_mode
  FROM sessions ORDER BY started_at DESC;
SELECT m.id, m.conversation_id, m.request_id, m.role, m.content,
       m.record_ids, r.status
  FROM messages m JOIN chat_requests r ON r.id = m.request_id
  ORDER BY m.sequence;
SELECT request_id, role, count(*) FROM messages
  GROUP BY request_id, role HAVING count(*) > 1;
PRAGMA integrity_check;
PRAGMA foreign_key_check;
```

Observed: duplicate query empty; integrity `ok`; foreign-key check empty.
The API comparison used `curl --silent --fail` against localhost only. Test code
uses temporary fictional databases and never removes/reseeds working records.

### Contrast and presentation checks

Calculated from CSS sRGB values using WCAG relative luminance:

| Pair | Ratio |
| --- | --- |
| Body #293f38 / ivory #f5f5ef | 10.30:1 |
| Secondary #56665f / ivory | 5.54:1 |
| Button #fffef9 / #365c4e | 7.43:1 |
| Message #293f38 / sage #e4ebe2 | 9.28:1 |
| Message metadata #56665f / sage | 4.99:1 |
| Error #873e32 / ivory | 6.94:1 |
| Focus #765b31 / ivory | 5.80:1 |
| Control outline #788a7f / ivory | 3.34:1 |

These are checked pairs, not a full WCAG audit. Sources and the limit of
color-emotion research are in the design document. No image generation, clinical
color-effect testing, participant testing or Figma capture was performed.

Screenshots, saved and visually inspected:
[home](screenshots/part2-home.jpg), [mobile](screenshots/part2-mobile.jpg),
[completed](screenshots/part2-completed.jpg), [chat](screenshots/part2-chat.jpg),
[outage before the final duplicate-error wording cleanup](screenshots/part2-chat-failure.jpg).

### Findings, corrections and outstanding checks

- A browser outage exposed a stale footer after chat recovered. Added a connection
  recheck after successful chat saves/navigation and verified the recovered
  screen no longer showed unavailable storage. Repeated unavailable messages are
  now collapsed to one when chat-load and submit errors are identical.
- Closing settings initially left focus on the body. Reset/fewer-options now
  explicitly return focus to the settings disclosure; browser activeElement confirmed
  Display settings after Reset. The keyboard exercise
  Pause/Resume behavior is separately observed above.
- Navigation initially retained a scroll position that clipped the nav beneath
  the sticky header. Navigation now resets scroll and focuses the heading without
  scrolling it behind the header; inspected the normal-size home again.
- Live OpenAI requests, actual credential validity, generated crisis redirection,
  and semantic grounding remain **unverified**. HTTP MockTransport is not a live
  provider check. Prompt rules and valid source IDs cannot guarantee answer truth.
- Long-history pagination has API tests but not a multi-page browser walkthrough.
  Real OS reduced-motion triggering, screen reader, 200% zoom, text-spacing
  overrides, hidden-tab triggering and clean-checkout setup remain unverified.
- No finished recording, reviewed implementation commit/push, verified public
  Part 2 links or Canvas submission yet. The report explicitly states this.


## Blue palette revision — October 26, 2026

CSS-only replacement following the student's dislike of green. Ran
`npm run build --prefix frontend` (passed, 14 modules) and `git diff --check`
(passed). No dependencies installed or provider calls made. The prior 50-test
run remains historical; behavioral suites were not rerun for color-only edits.

Calculated WCAG relative-luminance ratios from the actual CSS hex values:

| Pair | Ratio |
| --- | --- |
| Slate #303744 / ivory #f7f4ef | 10.90:1 |
| Secondary #606775 / ivory | 5.18:1 |
| Button text #fdfbf8 / blue #526783 | 5.61:1 |
| Message metadata #606775 / pale blue #e8edf4 | 4.83:1 |
| Control outline #7d8798 / ivory | 3.31:1 |
| Focus #765b31 / ivory | 5.78:1 |
| Count #303744 / circle #d4deed | 8.81:1 |

Observed the real running home and saved chat views in the Codex browser;
blue actions, blue selected navigation, pale blue message background and slate
text rendered. At 390×844, home clientWidth and scrollWidth both equaled390;
Start and Crisis support remained visible. Saved
[revised home](screenshots/part2-blue-home.jpg) and
[revised mobile](screenshots/part2-blue-mobile.jpg), then reset the viewport.
Earlier completion/chat/outage screenshots show the previous green palette and
remain evidence of behavior at the time. No claim of clinical benefit or a full
accessibility audit follows from these checks.


## Final Part 2 live demonstration — October 26, 2026

User explicitly approved reuse of the existing private Expedia OpenAI key and
at most four model calls. Created ignored/untracked backend/.env with mode0600
without overwriting any file or printing credentials. No previous-project source
copied. Key validity was established by two successful browser exchanges using
configured model alias `gpt-4.1-mini`, two RAG stages each. See
[redacted fictional evidence](part2-live-evidence.json) and
[live screenshot](screenshots/part2-live-chat.jpg). Exact provider snapshot was
not captured; the configured alias is the model identifier recorded by this app.

Conversation: `ee590ec5-eed1-474a-80fc-6424b378f5ad`.
Request1: `2591ef2a-1457-49d2-a6b0-d750d5ffaec9`.
Request2: `a85a2b59-22bc-4b45-8cb2-b54fab2c5190`.
History assistant message: `92fb3f84-9c84-4b6f-880d-386843a67c47`.
Supporting session: `6f38bdd8-9e16-4fbf-beac-e959f95795fe`.

Expected exercise answer: six 4/6 cycles, 60 active seconds, app-owned controls.
Observed: correct, three sentences. Expected history answer: factual latest
completed status/duration/display plus valid record ID, without unsupported
inference. Observed: correct 60 seconds/six cycles/text and correct source ID,
**but an unsupported claim that it was not paused**. Retrieved fields do not
include pause events. Tightened ANSWER_RULES to prohibit pause-history/stop-reason
inferences. Did not edit stored replies or make more paid calls. Prompt change
is unverified against the live model; ID checks alone do not guarantee grounding.

Read-only SQLite inspection and GET conversation response matched all four live
message IDs/content/source IDs. PUT replay of both identical requests returned
saved exchanges without additional calls; provider_usage remained4. At this
checkpoint: six sessions, two conversations, eight messages/four completed
requests; integrity_check=ok, foreign_key_check empty, duplicate request/role
query empty. Returned backend/.env to mock mode, restarted backend, refreshed
browser: both real replies remained visible as AI replies while mode label
correctly read Demo replies. No key is included in submitted evidence.

Verification commands this session: `npm test --prefix frontend` (14 passed),
`npm run build --prefix frontend` (passed), backend full unittest suite (36 passed).
Initial sandbox run blocked only the localhost bind in the real-server test;
reran with port permission and passed. After the prompt refinement ran
`.venv/bin/python -W error::ResourceWarning -m unittest tests.test_chat -v`
(21 passed, mocked providers). Known Starlette HTTPX deprecation warning remains.
These tests do not validate the revised prompt's semantic effectiveness.


Final timing repeat: scripted navigation/reload began2026-10-27T03:15:58.169Z;
ready state returned after2.717s; Start action returned after3.003s. This measures
scripted entry with no optional setup, not a person's reading/decision time.
Session `4424d3d6-d8cf-466c-b30f-154cd361d6f0` started03:16:00.943Z and ended
03:17:00.948Z: **60.005s wall duration**,60 active seconds,6cycles,completed,text.
No pauses/support visits in this run. Browser showed Finished and Saved.
[Current completion screenshot](screenshots/part2-final-completed.jpg).
Working database now7sessions; prior sessions preserved. Previous live evidence
JSON accurately reflects its earlier six-session checkpoint.


## Breathing Room branding and screenshot audit — October 26, 2026

Changed only visible brand, inline SVG marks, header styling, document title/theme
and documentation. Production Vite build passed (14modules); git diff --check
passed. Retained descriptive Crisis support accessible name; SVGs aria-hidden
and unfocusable. Header includes both icons at390px and320px with clientWidth=
scrollWidth at both widths. Temporary viewport overrides reset. Initial mobile
capture targeted a different tab (1280px); detected via dimensions and replaced
with a verified390px capture. No false mobile result retained.

Numbered current set: screenshots/part2-submission/01-home.jpg through
13-recovered.jpg, mapped individually in report.md. Actual browser captures,
not mockups. Earlier named captures remain historical. Saved AI replies were
recaptured from SQLite history with IDs/model details, current mock label intact.
No paid calls; provider_usage remains4 for part2-local.

New scripted full exercise:08e94b53-7233-4f00-a85c-7b4fd5822520,
03:25:40.456Z to03:26:40.459Z,60.003wall seconds,60active seconds,6cycles,text.
Support opened during a second exercise and paused it; Return left it paused,
then Stop saved f076976f-4b14-4f65-815b-a2edbf3bdf02,0.483active seconds,0cycles.
Both IDs, durations and outcomes matched the visible history and read-only SQLite.
An additional circle-mode session was present from the user's separate tab;
retained it without attributing it to the scripted timing check.

Stopped the real backend briefly, submitted a fictional question and observed
unavailable-service/no confirmed reply. Opened the independent support panel
while the backend remained stopped (screenshots11/12). Reverified bundled regional
resources using hotline lookup; did not activate external links. Restarted backend
and retried the same pending message, producing one user/one mock reply (13).
Conversation932c75c4-3fe0-4025-9842-ab8e0b544461,
requestf30d38a9-b6d0-4678-8c24-d463c7f0f91b,
assistant3da18260-d6c9-458b-99c0-28aeea84cdeb. SQLite query confirmed the pair;
integrity_check=ok and foreign_key_check empty. Backend remains running in mock.


## Final Part 2 requirement audit — October 26, 2026

Re-read the student-supplied Assignment3 overview and Part2 passage. Coverage:
chosen skill completes through Vue; live model contribution recorded; conversation
and session persistence inspected in SQLite/API/browser;60.003s measured exercise
and separate entry timing; independent support visible during exercise/failure;
stopped outcome and failed-request/retry shown; coherent one-skill scope and
unfinished work explained; R/D rationale and explicit personalization/control;
fictional-only testing; README/AGENTS/design notes; AI-USE and curated revised
approach. Report maps each claim to actual evidence and13 current screenshots.
No screenshot is treated as proof of SQL storage or elapsed time on its own.

The supplied overview places15scenario evaluation, clean-checkout verification,
finished-app demo and process screencast in Part3. Attempted the exact Part2
Canvas submission URL through the browser; it redirected to Penn State sign-in.
Separate authenticated rubric and deadline remain unverified, not assumed absent.
No Canvas upload or clinical/public-service deployment performed.

Final pre-publication commands: frontend npm test(14passed), npm run build(passed),
backend unittest discover with ResourceWarning errors(36passed including real
localhost restart). Known Starlette HTTPX deprecation warning only. No new live
calls. All report/README local links resolve;74 candidate repository files checked
for credential patterns and the configured private key, with zero matches.
backend/.env and data/app.sqlite3 are ignored/untracked; neither will be published.
User explicitly authorized commit/push of the reviewed Part2 milestone.
