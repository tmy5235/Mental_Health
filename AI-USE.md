# AI-use disclosure

## Part 1 design, October 13, 2026

- Tool: OpenAI Codex desktop application.
- Model: the assistant is identified as based on GPT-6 in its supplied context; the exact runtime model identifier and desktop build were not exposed in the tools used for this work. Verify against the app if available before submission.
- Roles: interpret the student-supplied assignment and research table; discuss scope and screen flow; propose research-to-design mappings, model boundaries, data storage, and verification plans; draft project documentation.
- Supporting tools: local file inspection/editing and read-only retrieval of prior assignment chat context to identify possible reuse patterns.
- Sources: student-provided assignment overview and research-table image. No external clinical dataset was used.
- Current limits: no application implementation, clinical assessment, usability study, live-model evaluation, or database verification has occurred in this project.
- Student responsibility: review the draft, correct it where needed, understand the decisions, and record substantive changes or additional tools used.

See [the curated evidence log](docs/evidence.md) for selected prompts, decisions, and a revised approach. Extend this file during Parts 2 and 3 with the application provider/model identifiers and their roles.

## Part 1 finalization, October 15, 2026

Codex incorporated the supplied startup and Figma activity instructions, filled
the design guidelines from the preceding discussion, added a fictional task and
screen sketches, and revised the retrieval design to the class's two-call SQL
RAG pattern. It organized the submission documents and checked local links,
research-code coverage, and repository contents. Browser access to the separate
Canvas submission page reached sign-in; no additional instructions or submission
were verified. No Figma tools, clinical datasets, app-provider calls, or generated
application code were used. The model identifier disclosure above remains the
available information; no more specific version is invented.

Publication used local Git commands and anonymous HTTP checks to publish the
student-specified repository and verify report-document access. No Canvas upload
was performed. Publication evidence is stored in docs/publication-links.json.

## User-state ideation revision, October 15, 2026

Codex used the newly supplied ideation activity to draft comparisons and rationale
for explicit presentation controls, distinguish self-report/observations/inference,
and add proposed fictional cases. It updated the design, report, and project notes.
It did not independently read the referenced research papers or inspect/download
questionnaires, datasets, models, or videos, and did not run participant or model
tests. Research statements in this revision are attributed to the course activity.

## Backend foundation, October 20, 2026

Codex inspected local project files/tools and authored a session API contract,
Python/FastAPI source, SQLite persistence, and tests. No Expedia source was
copied. Seven standard-library tests passed against temporary fictional records.
HTTP tests were authored but not run because dependencies are absent. No provider,
RAG, browser, Figma, or clinical testing occurred. Model identification remains
limited to the supplied GPT-6 context. Installation approval is pending.

## Backend installation and verification, October 20, 2026

Following explicit student approval, Codex used pip in backend/.venv to install
backend dependencies, recorded their resolved versions, and ran automated and
real-process localhost checks. It corrected test SQLite cleanup and the restart
exit-code assumption, and aligned the health OpenAPI error schema with actual
responses. Fifteen tests passed; the affected seven API tests passed again after
the schema correction. Local sqlite3 read-only inspection checked fictional rows
and relationships. A browser attempt via computer-use tools returned
ERR_BLOCKED_BY_CLIENT, so no browser result is claimed. No application provider
or model calls, frontend code, Figma work, or clinical evaluation occurred.

## Running Vue prototype, October 20, 2026

Codex authored the Vue app, fixed timing controller, HTTP client, history view,
styles, and Node built-in tests. Installed Vue/Vite/plugin dependencies only after
explicit student approval. Used the available helpline lookup for the labeled
U.S. support resources. Browser tools operated Chrome Guest and the Codex browser
for fictional scenarios; local Python inspected SQLite read-only and compared
IDs with API/UI records. Corrected focus handling and failure wording based on
observations. No Figma, image-generation service, prior-project source copying,
provider/model API calls, real patient data, or clinical evaluation was used.
A screenshot and detailed observed/unverified checks are retained in docs.

## Part 2 build, research and verification — October 26, 2026

Codex authored the conversation/retrieval/provider/preferences code, simplified
Vue layout/styles, tests, private setup helper and Part 2 report updates. The
coding assistant's exact runtime model identifier remains unavailable; it is
identified as GPT-6-based in supplied context. No subagents were used.

Tools: local shell/apply_patch/Git inspection; Python unittest/SQLite read-only
inspection; Node tests and Vite build; web research of original publications,
W3C guidance and official OpenAI documentation; browser computer-use and screenshot
tools; helpline lookup to reverify regional resources. Applied Sites' local-only
workflow and OpenAI Docs guidance. No public hosting, Figma, image generation,
new package installation, copied prior-app source, private messages or real patient
data were used. See design-pipeline.md for citations and evidence.md for revisions.

Application provider: default deterministic `demo-v1` mock logic, clearly labeled
in UI and stored reply metadata. Prepared OpenAI Responses API with configurable
model (setup suggestion `gpt-4.1-mini`) for scoped SQL selection and concise grounded
answers. **No real model API calls have been made**; provider HTTP tests are mocked.
Mock crisis branches are demonstration behavior, not a validated risk classifier.

The student must review generated code, understand the SQL allowlist, request
transactions and timer boundaries, verify a small live sample, and finalize the
submission. Research-informed aesthetics and passing software tests do not show
clinical effectiveness or establish a universally calming palette.


Palette follow-up: Codex researched the student's request to replace green,
reviewed Wilms & Oberfeld (2018) and Jonauskaite & Mohr (2025), changed CSS to
muted blue/ivory, calculated contrast, built the frontend and inspected desktop
and mobile in the real browser. Exact colors are design judgments, not a proven
anxiety intervention. No new dependency, generated image or model API call.


## Live model contribution — October 26, 2026

The student approved reusing a private key locally and four paid calls. OpenAI
Responses with configured alias `gpt-4.1-mini` performed SQL-template selection
and answer generation for two fictional browser exchanges. The exact returned
model snapshot was not captured. Replies and cited IDs were saved and inspected;
see docs/part2-live-evidence.json. Only the key configuration was reused from the
prior Expedia app, not source code or private conversation records.

A live reply inferred that a completed session was not paused; that was not
established by retrieved fields. Codex strengthened the prompt, preserved the
original output and documented that no live retest was performed after the change.
Four calls total; identical retries added none. Routine app mode was reset to mock.
Earlier “no live calls” entries describe their historical checkpoints only.


Branding/screenshots follow-up: Codex renamed the prototype Breathing Room and
authored small inline SVG airflow/help icons in Vue, adjusted responsive header
styles and updated the browser title. No image generator or new dependency used.
Recaptured real interface states for Part 2 coverage; no screenshots fabricated
and no stored live answer edited. No additional paid model calls.


## Part 3 — November 2, 2026

- **Codex coding assistant:** audited the assignment/repository, generated and
  revised code/tests, operated local browser checks, inspected SQLite, drafted
  documentation, created captioned recordings, and prepared the submission.
  The exact assistant model identifier was not exposed by this session and is
  not inferred from the app brand. No sub-agents were used.
- **OpenAI API:** configured alias `gpt-4.1-mini`, eight fictional exchanges and
  16 calls (SQL proposal plus answer generation), before the final fixed-rule
  refinement. Exact provider snapshot was not recorded. Raw answers and human-
  readable assessments are preserved, including three failing/ambiguous results.
- **Mock/fixed modes:** `demo-v1` for routine tests; `reviewed-rules-v1` for narrow
  application responses. Neither is represented as live AI. No further paid calls
  were needed for screenshots, video or policy regression tests.
- **Tools:** Python unittest, Node node:test, FastAPI/SQLite, Playwright 1.64.1,
  installed Chrome 156.0.8078.80, shell/Git, and read-only SQLite inspection.
  Playwright's FFmpeg and an isolated imageio-ffmpeg utility encode recordings;
  these tools do not generate app behavior. No Figma or image generation was used.
- **Recordings:** agent-produced screen captures of the actual browser with
  clearly labeled written commentary, including the code explanation. They do
  not represent the student's voice or independently establish the student's
  understanding. The student should review both the code and recordings before
  submitting. The report does not claim that a human peer performed the tests.

The curated prompts, failures, changes and checks are summarized in
[process evidence](docs/evidence.md) and [evaluation](docs/part3/evaluation.md).
Credentials, private environment files and runtime databases are excluded from Git.
