# Assignment 3 — Part 3: Breathing Room

Trevor Michael Yuhaniak · IST 402 · November 2, 2026

## Submitted version

Repository: https://github.com/tmy5235/Mental_Health
Branch: `codex/part3-final`
Submitted commit: 9e3819006d56ae63379ceafe24ca677406d2c646 (application source; final evidence commit recorded after publication)

This final submission implements one complete paced-breathing skill in Vue,
FastAPI and SQLite, with optional model assistance, saved conversations/sessions,
useful history, explicit saved preferences and independent crisis-support access.
It remains a localhost-only coursework prototype tested with fictional scenarios.
It does not diagnose, provide therapy, imply monitoring, or establish effectiveness.

## What is complete and what changed

The exercise provides six cycles of four counts in/six counts out, with optional
motion, still text, Pause, Resume and Stop. Preferences are remembered but remain
changeable/resettable; starting does not require setup, chat or disclosure. History
shows actual saved outcomes/durations, ordered messages and record IDs. Model calls
use reviewed skill context and bounded, scoped, read-only SQL retrieval. Application
code owns sequence, exits, persistence and the support panel.

Part 3 testing changed two behaviors. First, a long chat could successfully save
new replies while leaving them offscreen. The final view opens the latest message
page after Send, with manual earlier/later navigation retained. Second, repeated
live tests still produced ambiguous pause-history language and generic crisis
responses. Narrow fixed application replies now handle recognized past-pause
questions and clear crisis phrases before any model call, accurately labeled
App reply. Their phrase-matching limitations are explicit; support never depends
on detection. See [final design and Part 1 changes](docs/design-pipeline.md).

R1/D2 motivated the short fixed sequence; R2/D4 independent visible support;
R3/R4 voluntary exits and choice; D1/D3/D5 explicit low-effort personalization;
D6 restrained presentation and neutral wording. Saving choices reduces repeated
configuration but supplies no reliable distress estimate. We retained one skill
and disclosed unfinished-refresh behavior instead of expanding scope into a
questionnaire, automatic diagnosis/adaptation or additional techniques.

## Verification evidence

- **54 automated tests pass:** 40 backend, 14 frontend; production build passes.
  [Backend results](docs/part3/backend-final.txt), [frontend results](docs/part3/frontend-final.txt),
  [build](docs/part3/build-final.txt).
- **18 fictional browser scenarios:** 17 pass; actual background-tab behavior is
  inconclusive because automation did not hide the document. The [evaluation matrix](docs/part3/evaluation.md)
  records expected/observed results and **three explicit cross-case checks** for
  support access, nonblocking exits, and application-controlled sequence.
  [Raw observations](docs/part3/browser-results.json).
- **Timing:** 60.321 seconds from first observed exercise instruction to visible
  Finished; saved timestamps span 60.003 seconds, with 60 active seconds/six cycles.
  Entry and Start-to-instruction overhead are reported separately in the matrix.
  This run had no required typing, voluntary pauses or support visits.
- **Persistence:** read-only SQLite inspection matches browser/API IDs and timing;
  integrity is `ok`, with no foreign-key errors or duplicate request/role pairs.
  [Database evidence](docs/part3/database-check.json). Restart tests verify retained
  records and idempotent retries.
- **Repeated live evaluation:** four inputs repeated twice, eight exchanges/16
  calls using `gpt-4.1-mini`. [Raw live replies](docs/part3/live-results.json) and
  [assessments/variation](docs/part3/evaluation.md) are separate from mocked checks.
  Five replies met the criteria; three motivated the final fixed-rule refinement.
- **Clean checkout:** fresh project-local installation, both servers, empty-database
  startup, mock conversation, reload, support and session saving verified using
  the README. [Setup evidence](docs/part3/clean-checkout.md), [browser observations](docs/part3/clean-browser.json),
  [run instructions](README.md).

Routine and peer tests use mocks. The browser runner refuses a live backend.
The application enforces a persistent maximum of 50 live calls per demo session,
counting both RAG stages, then switches to labeled mock replies. This evaluation
used a stricter 16-call cap and made no additional paid calls for recordings.

## Demonstration and process screencast

- [Finished application demonstration — 2:12](docs/part3/finished-demo.mp4): full
  exercise at normal speed, personalization, persistence, saved real-model reply,
  fixed guidance, independent support, failure and recovery.
- [Process screencast — 1:42](docs/part3/process-screencast.mp4): a real pagination
  failure, API evidence, resulting correction and explanation of generated code.
- [Recording chapters and method](docs/part3/recordings.md).

The agent produced these real browser recordings with written explanatory captions,
not spoken student narration. AI assistance is disclosed; the student should review
and understand the code and recordings before submission.

## Surprising finding and limits

Even an explicit no-pause-inference prompt produced ambiguous wording, and a crisis
prompt produced general app descriptions. The final narrow rules guarantee their
own wording, not broad crisis detection or clinical safety. Tests show fixed replies
work with a failing provider, use no calls, and save/replay correctly. These are
application checks, not additional live-model success claims.

Untested limitations include native hidden-tab behavior, full screen-reader speech,
actual OS reduced-motion changes, browser zoom and another operating system.
Phrase rules can miss indirect language and match quoted/negated text. Other model
answers may remain unsupported despite valid record IDs. Unfinished refresh is
unsaved by design and disclosed before Start; closing a tab can lose unsent retries.
No real person in distress was tested and no support service was contacted.

## Process and AI disclosure

[AI-USE.md](AI-USE.md) names tools/model identifiers and their roles.
[Curated evidence log](docs/evidence.md) connects selected instructions, changes,
failed/revised approaches, tests and decisions. Credentials, private environment
files and runtime databases are excluded. No code was copied from the earlier
Expedia project; familiar architecture and development practices were reused.

Upload this `report.md` after reviewing the code, evidence and captioned recordings.
This report addresses the supplied assignment overview; no Canvas submission has
been made by the agent.
