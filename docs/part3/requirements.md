# Part 3 — requirement coverage

This matrix maps the supplied Assignment 3 directions to the completed local
submission. Evidence establishes software behavior within the stated fictional
scope; it does not predict a grade or demonstrate clinical effectiveness.

| Requirement | Completed response | Evidence |
| --- | --- | --- |
| Runnable Vue/FastAPI/SQLite application | Local frontend/API, additive schema, separate responsibilities and declared dependencies. | [README](../../README.md), [clean checkout](clean-checkout.md). |
| One intact skill within 90 seconds | Six 4/6 cycles, 60 active seconds; final visible run 66.985s. Entry reported separately; voluntary pauses are not forced closed. | [Timing and S01](evaluation.md), [raw rerun](final-review/browser-results.json). |
| Contextual model interaction and persistent data | Scoped two-stage SQL RAG, actual saved replies, session/conversation history and stable IDs. | [Design/contracts](../design-pipeline.md), [live outputs](live-results.json), [data inspection](final-review/database-check.json). |
| Useful history and personalization | Ordered/paginated history, latest chat reply visible, explicit saved/resettable display choices. | S07/S11/S12 in [evaluation](evaluation.md). |
| User control and low effort | Immediate Start, optional typing/settings, Pause/Resume/Stop, neutral outcomes and independent support. | S01–S05/S18; [design mapping](../design-pipeline.md). |
| Crisis-support route independent of model/detection | Bundled shared panel works through failed/pending requests; recognized chat phrases additionally receive fixed guidance. | B1 and S03–S05/S13/S18 in [evaluation](evaluation.md). |
| Revisit Part 1 decisions and R1–R4/D1–D6 | Final mapping explains retained choices, changed scope and tradeoffs. | [Final design](../design-pipeline.md), [Part 1 disposition](../part1-checklist.md). |
| At least 15 fictional expected/observed scenarios | 18 scenarios, including ordinary use, interruptions, error recovery and layout. | [Scenario matrix](evaluation.md), [native S15 supplement](final-review/native-browser.json). |
| Three explicit cross-case behavior checks | B1 support access, B2 nonblocking exit, B3 application-owned sequence. | [Cross-case matrix](evaluation.md). |
| Repeatable mocked checks and repeated live sample | 54 passing tests; four live inputs repeated twice; variation and three failed criteria retained. | [Verification](../verification.md), [live assessment](evaluation.md). |
| Surprising result, resulting refinement and untested limit | Prompt wording still varied; narrow fixed rules added. Full screen-reader speech remains untested. | [Findings/limits](evaluation.md), [process log](../evidence.md). |
| Bounded live usage with mock fallback | Persistent cap of 50 calls per demonstration counts both stages; Part 3 sample capped at 16. Routine work stays mocked. | [Design](../design-pipeline.md), backend tests and [raw live evidence](live-results.json). |
| Finished demo and process screencast | Full exercise, history, personalization, model contribution, support/recovery; pagination failure, API evidence, correction and source explanation. | [Finished demo](finished-demo.mp4), [process screencast](process-screencast.mp4), [chapters](recordings.md). |
| AI tools/models and curated process evidence | Roles/known identifiers, selected prompts, failed approaches, checks and decisions are disclosed. | [AI-USE](../../AI-USE.md), [evidence log](../evidence.md). |
| Final report and maintained project documents | Report, README, AGENTS, design, verification and evidence agree with the final implementation. | [Report](../../report.md). |
| Repository/version and accessible artifacts | Repository named; relative links work in the local source package. Final GitHub publication is held by explicit instruction. | [Delivery status](../../handoffs/current.md). |

The local deliverables are complete. Publication and assignment-system upload
are separate delivery actions and have not occurred for this final version.
