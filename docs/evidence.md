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
