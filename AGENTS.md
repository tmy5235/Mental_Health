# Project operating instructions

Breathing Room is a completed Assignment 3 prototype for fictional localhost
evaluation. Read README.md, docs/design-pipeline.md, docs/verification.md and
handoffs/current.md before changing it. Inspect the branch and local changes;
preserve existing work, configuration and records.

## Architecture and behavior

- Vue owns presentation and explicit interaction; FastAPI owns validation,
  orchestration and provider calls; only Python opens SQLite. Keep routes small,
  writes parameterized and related message/request changes transactional.
- Application code owns six four-second inhales/six-second exhales, Pause,
  Resume, Stop and independent support. A model cannot operate these controls.
- Start requires no chat, questionnaire or setup. Keep support accessible during
  failures, pauses and pending requests. Never gate it on phrase detection.
- Remember only explicit display choices; permit changing/resetting them. Do not
  infer distress, improvement or a diagnosis from clicks, duration or completion.
- Preserve neutral outcomes, visible focus, narrow layouts, still-text pacing,
  honest save states and the fictional-use/non-therapy/non-monitoring disclosure.

## Data and model boundaries

Use stable UUIDs and idempotent saves. Startup may add schema but must not seed,
replace or erase working records. Use separate temporary fictional databases for
tests. Keep raw historical model replies unchanged, including failed examples.

SQL RAG proposes one of five exact read-only queries, validates it, binds profile
and conversation scope, reads at most five records within execution/context
limits, then generates a grounded answer. Provider SQL is untrusted; never relax
the allowlist to a SELECT-prefix check. Writes remain application-owned.

Recognized crisis phrases and past-pause questions use narrow fixed replies before
provider selection or usage reservation. Label these App replies, preserve their
false-positive/false-negative disclosure, and never call them a distress detector.
Mock, fixed and live reply labels must match actual execution and saved metadata.

Keep credentials backend-only in ignored backend/.env; never print, commit or
overwrite them. Health may expose configuration presence, never secret values.
Preserve finite deadlines and the persistent 50-call demonstration cap, counting
both RAG calls and conservatively reserved failures. The completed Part 3 live
sample used 16 calls; routine work uses mocks and requires no further paid calls.

## Verification and documentation

Use the README commands and project-local declared dependencies. For browser
evaluation, use scripts/serve_mock.py with a separate database and EVIDENCE_DIR
pointing to a new results directory. Do not overwrite submitted observations.
Check UI, API and SQLite identities, failure recovery, restart persistence and
the full visible sequence when behavior changes. Never claim that a build alone
establishes functionality, or that mocked tests establish live-model reliability.

Keep requirements, decisions, observed results and untested limitations distinct.
README holds setup; design-pipeline holds the final rationale/contracts;
verification and part3/evaluation hold evidence; evidence.md holds selected
prompt/change/check/decision records; AI-USE.md discloses assistance. Historical
milestones remain in Git and raw evidence, not as contradictory current promises.

## Delivery boundary

The user explicitly directed **do not push yet**. Keep this work local; do not
push, publish, deploy or submit it without a later instruction. Figma, additional
skills, accounts, clinical studies and public hosting are outside this scope.
Update the handoff and final report after relevant changes. Stage only intended
files; never include runtime databases, credentials or dependency directories.
