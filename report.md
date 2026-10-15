# Assignment 3.1 — Part 1: Paced Breathing

IST 402 · Design milestone · October 15, 2026

The design and supporting evidence are published. Repository and report-document links were verified accessible without signing in.

## Project access

Repository URL: [Mental_Health](https://github.com/tmy5235/Mental_Health).

Published branch: `codex/assignment3-part1`.

Assessed design commit: [`58d92cb028d3fe52f3bf452bad1a810253548e20`](https://github.com/tmy5235/Mental_Health/commit/58d92cb028d3fe52f3bf452bad1a810253548e20).

Document links below use publication-evidence snapshot `802bafa`; the assessed design is unchanged from `58d92cb`.

- [Design, screen sketches, flow, architecture, and research mapping](https://github.com/tmy5235/Mental_Health/blob/802bafa2cf4e503ccfc174d52661a5bfa26b19cc/docs/design-pipeline.md)
- [Document verification and evidence limits](https://github.com/tmy5235/Mental_Health/blob/802bafa2cf4e503ccfc174d52661a5bfa26b19cc/docs/verification.md)
- [Curated process evidence and revised approaches](https://github.com/tmy5235/Mental_Health/blob/802bafa2cf4e503ccfc174d52661a5bfa26b19cc/docs/evidence.md)
- [Project overview and completed design guidelines](https://github.com/tmy5235/Mental_Health/blob/802bafa2cf4e503ccfc174d52661a5bfa26b19cc/README.md)
- [Coding-agent instructions](https://github.com/tmy5235/Mental_Health/blob/802bafa2cf4e503ccfc174d52661a5bfa26b19cc/AGENTS.md)
- [AI-use disclosure](https://github.com/tmy5235/Mental_Health/blob/802bafa2cf4e503ccfc174d52661a5bfa26b19cc/AI-USE.md)

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

## User-state ideation

The supplied **Understanding User State: Questionnaires and Clicking Behavior**
activity informed a comparison of a full questionnaire, an optional brief check-in,
interaction measurements, and explicit display choices. We selected **Show fewer
options / Show more options**, keeping Start, optional-feature access, and crisis
information reachable. This supports D1, D3, D5, and R4 without claiming to detect
distress. The current scope excludes questionnaires, pointing tasks, click-speed
tracking, and anxiety scores; the tradeoff is less structured reflection and no
automated state estimate.

Self-reported chat content remains attributed to the user; session events are
observations, not explanations of feelings. If no signal exists, the normal flow
still works. If Alex reports feeling calm but pauses repeatedly, the app must not
infer anxiety or change the layout automatically. The activity's mouse-study
summary does not validate browser clicks as an anxiety measure, and its DBT-app
summary concerns experience/usefulness rather than established treatment outcomes.
The detailed design records these limits and future fictional checks. The original
papers, STAI form, datasets, and video were not independently inspected; no clinical
instrument or dataset was adopted. The activity describes ideation possibilities,
not new Assignment 3 requirements.

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
The process log records revisions including: removing required preference setup and
replacing the earlier retrieval proposal with class-required SQL RAG. The new
ideation notes also make the limits of state inference and the rationale for
explicit presentation controls concrete.

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
