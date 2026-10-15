# Assignment 3.1 — Part 1: Paced Breathing

IST 402 · Design milestone · October 15, 2026

**Publication pending:** the design is complete locally, but this report needs the repository URL and accessible document links before upload.

## Project access

Repository URL: **PENDING_REPOSITORY_URL**

Assessed design commit: `58d92cb028d3fe52f3bf452bad1a810253548e20`

- [Design, screen sketches, flow, architecture, and research mapping](docs/design-pipeline.md)
- [Document verification and evidence limits](docs/verification.md)
- [Curated process evidence and revised approaches](docs/evidence.md)
- [Project overview and completed design guidelines](README.md)
- [Coding-agent instructions](AGENTS.md)
- [AI-use disclosure](AI-USE.md)

## Purpose and proposed experience

The proposed application is a localhost coursework prototype using Vue, FastAPI,
and SQLite. It supports one assigned skill: paced breathing, in for four counts
and out for six, repeated for six cycles. Fictional student Alex can start
without describing feelings, pause or stop, and review a saved session later.
It is not therapy, does not diagnose or imply monitoring, and will be tested only
with fictional scenarios.

The main flow is **Welcome → Breathing → neutral completion or early exit**.
Optional chat and history sit outside the guided sequence. The design document
contains a flow diagram and three screen sketches. Pause, exit, and clearly
labeled crisis-support access remain available during the exercise. Support
information is bundled independently of model responses; no classifier gates it.

## Research grounding and tradeoffs

R1 motivates six cycles totaling 60 seconds of breathing. The proposed sequence
budgets roughly 60–65 seconds including transitions, under the 90-second limit;
this is arithmetic and a design budget, not a measured result. Entry/setup time
will be reported separately, and voluntary pauses and support-access time are
excluded. There is no forced timeout or exit.

R2/D4 motivate persistently visible support access. R3/R4 motivate explicit start,
pause, exit, and editable choices. D1–D3 motivate sparse views, a user-selected
simplified presentation, one instruction at a time, and no mandatory disclosure
or feedback. D5 motivates remembering display choices without an onboarding
questionnaire. D6 motivates plain language, readable contrast, restrained motion,
and a text/count alternative. The design maps every R/D code to a decision,
tradeoff, and later check; mention counts do not establish clinical effectiveness.

The selected entry design makes Start prominent and explanation optional. A
conversation-first alternative would provide more context but require more
reading, disclosure, and waiting. Remembered settings reduce repeated effort but
must remain visible and resettable. One skill makes the implementation manageable
while limiting technique choice. Session completion is never treated as evidence
of improvement.

## Model, application control, and data

Optional chat combines reviewed skill information with stored context using the
class's two-call SQL RAG workflow. The model proposes retrieval SQL; FastAPI
validates a scoped, bounded, read-only query. A second call receives retrieved
records with IDs and produces a grounded answer. For example, Alex can ask about
the last session and its display mode. Empty results must be acknowledged rather
than replaced with invented history. Both calls count toward usage limits.

Application code controls timing, steps, navigation, exits, support access, and
parameterized database writes. The model cannot execute SQL directly or change
the exercise. SQLite will save conversations, ordered messages, exercise
sessions, and explicit preferences. History will show times, duration, and neutral
completed/ended/interrupted outcomes without requiring model calls. Failures must
not create fabricated replies, duplicate retries, or false save confirmations.

The crisis-input policy asks the model to avoid counseling and point to the
visible support route, with its unreliability documented. The independent support
panel remains available regardless of model interpretation or failure. Regional
resource content will be verified before implementation.

## Completed work and verification

Completed the project structure, README guidelines, coding-agent instructions,
design specification, sketches/flow, research mapping, proposed architecture/data
model, failure plan, verification plan, AI disclosure, and curated evidence.
The process log records two revisions: removing required preference setup and
replacing the earlier retrieval proposal with class-required SQL RAG.

Part 1 verification covers document links, folder structure, research coverage,
consistent design requirements, and publication status as recorded in the linked
verification notes. No running application, database, model calls, usability
study, or measured exercise timing is claimed. No code has been copied from the
Expedia project; its Vue/FastAPI, persistence, and SQL RAG patterns are candidates
for documented reuse during implementation.

A flow and sketches are the design artifacts for this milestone. No recording or
Figma capture was produced; the supplied Figma activity explicitly adds no new
submission or grading requirement.

## Remaining questions and next milestone

Select the provider/model and exact SQL validation approach; verify support
resource wording; refine reload recovery, keyboard focus, background-tab timing,
and deletion behavior. Then implement one complete flow with mocked checks and
selected live-model verification, comparing SQLite, API, and UI evidence. The
final milestone will include at least 15 fictional scenarios and three explicit
behavior checks. These are future work, not missing claims of implementation for
this design milestone.
