# Assignment 3 — Part 3: Breathing Room

Trevor Michael Yuhaniak · IST 402 · November 2, 2026

Repository: [Mental_Health](https://github.com/tmy5235/Mental_Health)

Final branch: `codex/part3-final`

Submitted source/evidence commit: [743d3825220a754adbf9d12dd5e5fe1d1f5bdc29](https://github.com/tmy5235/Mental_Health/commit/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29)

This checkpoint contains the evaluated application, final design, test evidence
and recordings. The report and publication checks add no application changes.

## Completed solution

Breathing Room implements one complete paced-breathing skill in Vue, FastAPI and
SQLite, with optional contextual model interaction, saved conversations/sessions,
useful history, explicit preferences and independent crisis-support access. It is
a localhost assignment prototype for fictional evaluation, not therapy, diagnosis,
monitoring or a public support service.

The central design problem was to provide a usable short sequence without adding
mandatory disclosure, configuration or model waiting. Start immediately begins six
cycles of four counts in and six counts out. Pause, Resume and Stop preserve user
control; still-text pacing, optional motion and larger text are remembered and
resettable. History presents actual activity and attributed messages, with stable
IDs and ordered pagination. It does not infer feelings or improvement.

The model explains reviewed skill material and uses bounded, scoped, read-only SQL
retrieval to answer factual history questions. Application code owns sequence,
exits, writes and bundled support. Neither a classifier nor a successful model
response is required to open Crisis support.

## Problems resolved and design decisions

Part 3 resolved two observed failures. A long conversation saved a new reply while
leaving it offscreen; the corrected interface opens the latest page after Send/open
and retains Earlier/Later navigation. Separately, repeated live responses still
used ambiguous pause-history language and generic descriptions for crisis-related
input. Narrow application-owned replies now handle recognized past-pause questions
and clear crisis phrases before any provider call, labeled App reply. These rules
do not establish comprehensive detection; unconditional support remains essential.

The [final design](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/design-pipeline.md) revisits Part 1 and maps every R1–R4 and
D1–D6 finding to an implemented choice and tradeoff. R1/D2 informed the short fixed
sequence; R2/D4 independent visible support; R3/R4 voluntary exits and choice;
D1/D3/D5 low-effort explicit personalization; D6 restrained presentation and neutral
language. Mandatory setup and inferred-state tracking were rejected. Display settings
collapse while navigation remains visible. Unfinished refresh is explicitly unsaved,
rather than inventing an interrupted/completed outcome. One skill and a single
fictional profile keep the implementation bounded.

## Verification and what it establishes

- **54 automated tests pass:** 40 backend, 14 frontend; production build passes.
  [Final verification and logs](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/verification.md).
- **18 fictional scenarios have passing observations:** 17 automated passes plus
  a separate native Chrome background-tab check. The automated S15 result remains
  inconclusive in the raw evidence. [Expected/observed matrix](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/part3/evaluation.md)
  includes three explicit cross-case checks: independent support, nonblocking exit
  and application-owned sequence.
- **Visible duration meets 90 seconds:** the final run measured 66.985 seconds
  from first instruction to visible Finished, including observed delay. Saved
  records show 60 active seconds/six cycles. Start-to-instruction was 47.5ms;
  scripted entry was 71.2ms, reported separately. No voluntary pauses or support
  visits occurred. The original visible run was 60.321 seconds.
- **Persistence is inspectable:** final SQLite/API/browser IDs and activity fields
  match; integrity is `ok`, with no foreign-key violations or duplicate request/role
  pairs. Restart and retry tests retain records without duplicating successful
  exchanges. [Database evidence](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/part3/final-review/database-check.json).
- **Clean setup works:** a fresh tracked-file checkout installed declared dependencies,
  started without a key or existing database, and passed mock-chat, reload, support
  and session-save checks. [Clean-checkout evidence](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/part3/clean-checkout.md).
- **Repeated live sample exposes variation:** four fictional inputs repeated twice,
  eight exchanges/16 calls using `gpt-4.1-mini`; five met criteria and three motivated
  refinement. [Original replies](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/part3/live-results.json) and
  [assessments](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/part3/evaluation.md) are separate from mocked regression checks.

Routine evaluation uses mocks. Both live RAG stages count toward a persistent
50-call demonstration cap, followed by labeled mock fallback. The Part 3 sample
used a stricter 16-call cap; final review and recordings added no paid calls.
The [requirement coverage matrix](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/part3/requirements.md) connects the supplied
directions to implementation and evidence.

## Demonstration and process evidence

- [Finished application demonstration — 2:12](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/part3/finished-demo.mp4): full
  normal-speed sequence, personalization, history, saved live-model contribution,
  fixed guidance, support, failure and recovery.
- [Process screencast — 1:42](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/part3/process-screencast.mp4): observed pagination
  failure, API evidence, corrected behavior and generated-source explanation.
- [Chapters and recording method](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/part3/recordings.md),
  [curated process log](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/docs/evidence.md) and [AI-use disclosure](https://github.com/tmy5235/Mental_Health/blob/743d3825220a754adbf9d12dd5e5fe1d1f5bdc29/AI-USE.md).

These actual browser captures use agent-authored written captions and source
explanation, with no spoken narration or independent human participant test.

## Surprising finding and remaining limits

An explicit prompt against pause inference still produced ambiguous wording, and
both crisis-input repeats led with general app descriptions. The fixed rules address
those recognized cases deterministically; they do not make arbitrary model answers
reliable. Tests verify that fixed replies work with a failing provider, use zero
calls and save/replay correctly. This is application evidence, not another successful
live-model sample. Valid record IDs do not establish semantic truth.

Phrase rules can miss indirect language and match quoted/negated text. Full
screen-reader speech, native zoom, actual OS reduced-motion changes and another
operating system remain untested. Unfinished exercise refresh is unsaved; closing
a tab can lose pending retries. No real person in distress was tested, no external
support service was contacted and no clinical effectiveness is claimed.

## Submission artifacts

The source, design, verification evidence and both recordings are published in the
repository. All linked artifacts were verified accessible without signing in.
The linked checkpoint preserves the evaluated implementation and its evidence. This report is the standalone assignment deliverable; the application
remains a localhost prototype, and no assignment-system upload is claimed.
