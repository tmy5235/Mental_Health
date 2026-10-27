# Curated process evidence

## 2026-10-13 — Scope and first design

- Student request: explain the assignment and how to begin Part 1; later, “Okay now lets get started on the assignment. What do I need to do for part 1”.
- Inputs: assignment overview pasted by the student and the student-supplied research-table image containing R1–R4 and D1–D6.
- Decision: propose one complete paced-breathing flow with optional chat, SQLite history, and editable display preferences. Student continued with this scope after discussing the three screens.
- Result: created README, agent instructions, design notes with flow and research mapping, this evidence log, AI disclosure, submission checklist, and a draft report. No application code or previous-project source was copied.

## Revised approach — optional preferences rather than required setup

- Earlier proposal: Welcome → choose preferences → start exercise.
- Evidence prompting revision: D3 identifies the emotional effort of disclosure/performance; D5 describes adaptation without configuration burden.
- Revision: Start works immediately. Display preferences are optional, remembered after explicit changes, and resettable. Optional chat is not a prerequisite.
- Tradeoff: fewer initial customization choices and less subjective information, in exchange for less work before the exercise.
- Verification status: design reasoning only; no usability observations or clinical claims.

## Design verification status

- Source review: the supplied overview explicitly says a working application is not expected for Part 1 and requests a sketch or flow, model/data roles, research grounding, personalization/control, and unresolved questions.
- Timing arithmetic: 6 × (4 + 6) = 60 seconds of breathing. Actual rendering, interruption behavior, and total timing are unmeasured.
- The proposed checks in design.md have not run. There are no browser screenshots, database observations, mock-model runs, or live-model results yet.
- Publication status is maintained in report.md and handoffs/current.md; the design checks here do not establish external accessibility.

Only curated coursework prompts and design decisions are included. No credentials, real patient conversations, participant records, or private third-party content are included.

## 2026-10-15 — Startup activity and revised retrieval design

- New evidence: the supplied startup activity explicitly requires a model-proposed SQL query, backend validation/read-only retrieval, and a second answer-generation call.
- Earlier approach: ordinary backend queries alone would retrieve context. That was simpler but did not satisfy the new class instructions.
- Revision: adopted two-call SQL RAG with scoped retrieval, limits, separate parameterized writes, record-grounded answers, and explicit failure states. Both calls count toward the usage budget. This adds validation complexity and cost; it never gates the breathing exercise or crisis information.
- Startup work: created missing folders and replaced abbreviated root instructions with the supplied baseline after showing the differences; preserved earlier supporting documents.

## 2026-10-15 — Part 1 finalization

- Student request: “Yes can we finish the part one submission”.
- Completed the README guidelines using the previously discussed paced-breathing direction. Organized the maintained design in design-pipeline.md, retained design.md as a compatibility link, added fictional Alex's task, screen sketches, and a conversation-first versus start-first comparison.
- Retained unresolved provider, SQL-validator, resource-content, and interaction details as implementation questions; did not present them as working features.
- The supplied Figma activity explicitly adds no new submission/grading requirement. Used sketches and a flow diagram for Part 1; no Figma capture or working prototype was claimed.
- Tried the separate Canvas Part 1 page; the available browser redirected to Penn State sign-in. Requirements were checked against supplied materials, not a verified signed-in page.
- Document and publication checks are recorded in verification.md. No live application/model results are claimed.

## 2026-10-15 — Repository publication

- Student supplied `https://github.com/tmy5235/Mental_Health.git` as the destination.
- Checked the remote before writing; it had no advertised refs. Connected it as origin and pushed `codex/assignment3-part1` without overwriting existing history.
- Assessed design checkpoint: `58d92cb028d3fe52f3bf452bad1a810253548e20`.
- Anonymous HTTP checks returned 200 for the repository, assessed commit, and all six report-document links. See [publication results](publication-links.json).
- Replaced report placeholders with accessible URLs. Publication metadata does not add application code or change the assessed design. No Canvas submission was performed.

## 2026-10-15 — User-state ideation incorporated

- Student supplied **[Ideation] Understanding User State: Questionnaires and Clicking Behavior** and requested including it in Part 1.
- Compared questionnaire/check-in, behavioral measurement, and explicit presentation-choice alternatives. Selected the existing simplified-view direction with a concrete Show fewer options / Show more options control.
- Added a distinction between attributed self-report, factual session behavior, and unsupported emotional-state interpretation. Specified behavior for missing or apparently conflicting information and added fictional expected checks (not executed).
- Kept questionnaires, click-speed monitoring, pointing tasks, anxiety scores, dataset imports, and specialized-model adoption outside scope. This reduces input burden while giving up automatic state estimation and structured reflection.
- Attributed study summaries to the supplied activity; no original papers, questionnaire items, model examples, datasets, or video were independently reviewed. Did not claim to complete the separately referenced graded group activity.
- This changes the design rationale and requires a new assessed design checkpoint and updated report links; the earlier `58d92cb` snapshot does not include this activity.

## 2026-10-20 — implementation started

- Student request: “Can you start implementation”.
- Inspected project, design, handoff, and installed tools; created feature branch
  `codex/implementation-foundation` from `6a0fc60`.
- Defined the session API contract and worked example before adding backend
  models, repository, controller, and routes. Chose one backend operation before
  the interface, following the project's incremental-development instruction.
- Identical stable-ID retries preserve one row; conflicting retries cannot alter
  history. Startup creates schema without seeding fictional sessions.
- Seven standard-library storage tests passed, including concurrent retries,
  rollback, and read-only row/relationship inspection. HTTP tests remain pending.
- Dependencies are declared but not installed. AGENTS.md requires installation
  approval. No provider calls, credentials, frontend, or Figma work occurred.

## 2026-10-20 — approved dependency installation and testing

- Student explicitly approved backend installation and testing. Created local venv
  and installed declared packages; used network escalation after sandbox DNS
  failure. Pinned direct versions and recorded the complete resolved package set.
- Ran 14 existing tests; corrected a test-only unclosed SQLite connection warning.
- Added a repeatable real-process HTTP test with temporary fictional records,
  shutdown/restart, duplicate/conflict/validation checks, and SQLite comparison.
  Corrected its exit-code assumption after inspecting Uvicorn's signal behavior.
- Final suite: 15 passed. Corrected health OpenAPI 503 schema to match actual
  output, then reran all seven API tests successfully.
- Verified default localhost startup, API health/history/schema, empty working
  database, and Ctrl+C shutdown. Browser navigation was blocked by the client;
  recorded this limitation without claiming browser success.
- No frontend dependencies, provider calls, credentials, Figma, commit, or push.

## 2026-10-20 — running app

- Student asked for a running app, then approved the three frontend dependencies
  through the installation prompt. Prepared Vue scaffold and verified its health
  request before expanding the interface.
- Implemented the selected fixed paced-breathing sequence, text alternative,
  explicit browser-local display controls, support dialog, session saving, and
  paginated history. No model/provider dependency was introduced.
- Verified U.S./territories support links with the helpline lookup; region is
  labeled in the interface. No external support service was contacted.
- Real browser testing caught Pause/Resume focus loss and a stale connection
  status after failed saving; corrected these. A full exercise, stopped outcome,
  support pause/Stop, refresh, server outage/retry, and SQLite/API identity were
  checked. Records were preserved, including the user's demonstration session.
- Twelve frontend and fifteen backend tests pass. Production build passes.
  Browser timing for the measured completed session was 60.004 seconds.
- Screenshot saved in docs/screenshots. Source and data limits are explicit:
  unfinished reloads are unsaved, preferences are browser-local, SQL RAG/chat
  remain later work. Visibility-change triggering needs a native-browser check.

## 2026-10-26 — Part 2 implementation and quieter interface

- Student asked to build the remaining assignment, simplify layout/copy, research
  color and typography, and progress toward submission. Explained that the model
  supplies optional chat, while the exercise never needs it. No key was provided.
- Used Sites' local-only workflow and OpenAI Docs guidance; retained Vue/FastAPI/
  SQLite and the existing checkout. No hosting, Figma, image generation, copied
  Expedia code, new dependencies or clinical dataset.
- Research: primary systematic color review and W3C cognitive/WCAG guidance.
  Revised the premise from a universally calming color combination to a measured
  contrast/presentation choice. Association with low arousal does not establish
  an anxiety-reducing interface. Sources and tradeoffs are in design-pipeline.md.
- Removed the large preview card, duplicate introductory copy and default motion;
  adopted one main action, optional settings, 18/20px text and muted sage/ivory.
- Implemented conversation/request/message persistence, stable retry IDs, five
  tightly allowlisted SQL retrieval shapes, bounded OpenAI adapter, labeled mock
  responses, explicit preferences and a restart-resistant 50-call budget.
- Rejected free-form generated SQL in favor of a small exact template language.
  Tradeoff: narrower questions, but an inspectable scope boundary with no extra
  SQL parser/framework dependency. Stored text cannot invoke app actions.
- Browser tests found navigation scroll/focus and stale recovery-status issues;
  corrected them and checked rendered results. Full exercise measured 60.002s.
  Outage/retry retained the request and saved one pair; SQLite/API/UI IDs matched.
- All 50 automated checks passed (36 backend/14 frontend) and the bundle builds.
  Provider transport tests are mocks. No live model, actual key setup or clinical
  benefit is claimed. API setup helper refuses noninteractive key entry.
- Rewrote report.md for Part 2 with actual evidence, preserved published Part 1
  links, and left live demonstration/commit/publication/Canvas fields honest.


### Palette feedback revision — October 26

Student rejected green. Reviewed Wilms & Oberfeld's controlled color study and
revisited the systematic review; selected muted blue/ivory with slate text.
Changed CSS colors only, built successfully, calculated contrast and inspected
home/chat/mobile. New blue screenshots preserve the previous evidence separately.
See design-pipeline.md for research limits and verification.md for measured ratios.


### Part 2 completion and live finding — October 26

- Student requested finishing the assignment and approved reusing the prior
  project's key locally for two fictional exchanges/four paid model calls.
- Configured the ignored owner-only .env; no key printed or committed. Used
  OpenAI Docs guidance and the existing Responses adapter; no dependency install.
- Both live exchanges saved and matched SQLite/API/browser. Stable-ID replays
  added neither replies nor usage; four calls total. Returned app to mock mode.
- Failed assumption: schema-valid output and valid record IDs would imply a fully
  grounded answer. Live history reply added “not paused,” unsupported by available
  fields. Revised the prompt to prohibit that inference, preserved the reply and
  documented that the change is not yet live-validated. This is a model limitation,
  not a claim that the clinical safety of the app has been established.
- Re-ran 50 automated checks/build; after prompt change,21 chat checks passed.
  The initial server test needed localhost permission; the authorized rerun passed.


### Breathing Room and submission captures — October 26

Student requested a breathing-related name/logo, clearer help icon and screenshots
covering assignment requirements. Authored inline SVG airflow and outlined plus
icons, retained Crisis support text, and updated responsive branding. Captured13
real states covering entry/preferences/mobile, active/completed/stopped exercise,
support pause, saved records/AI replies, unavailable service/support and recovery.
Mapped each to Part 2 in report.md. Reused actual saved AI replies without paying
for new calls. Detected an incorrect viewport target from dimensions and replaced
that capture with verified390px evidence. Timing/storage claims use actual records,
not screenshots alone; no video recording claimed.


### Authorized Part2 publication — October26

Student asked to publish and double-check all Part2 requirements. Re-read supplied
assignment and matched requirements against report evidence. Exact Canvas Part2
URL required Penn State sign-in, so no authenticated rubric verification claimed.
Re-ran50automated checks and build successfully. Checked source/evidence for the
actual local key and credential patterns without printing it; no matches.
Publish the implementation branch, then finalize standalone report links to its
immutable assessed commit. Canvas upload remains the student's action.
