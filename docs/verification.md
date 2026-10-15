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
were verified. Requirements were checked against the three supplied course texts
and the research-table image. No Canvas upload has been performed.

Repository publication and anonymous link checks are not established by local
file checks. The final report identifies the assessed commit and records the
publication result when it is verified. Until then, publication is pending.

## Later checks — not executed

Exercise timing, pause/exit behavior, reduced motion, keyboard/narrow-screen use,
late model responses, crisis access after failure, SQLite persistence/restart,
scoped retrieval, rejected SQL, empty results, and duplicate prevention all need
implementation and observed results. The fictional cases in the design document
are a test plan. They are not passed tests.
