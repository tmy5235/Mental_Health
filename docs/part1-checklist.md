# Part 1 decisions — final disposition

The original design is preserved in the [published Part 1 snapshot](https://github.com/tmy5235/Mental_Health/tree/f7b91254907a3eb18b22dc7d58b82a89960c63cb).
This document records how those decisions were resolved in the final implementation.

| Design commitment | Final disposition |
| --- | --- |
| One intact skill and fictional task | Six 4/6 cycles; immediate Start; fictional Alex; no mandatory disclosure. |
| Screens, flow and research mapping | Implemented home/exercise/result plus optional chat/history; all R1–R4/D1–D6 mapped in the final design. |
| Model and data responsibilities | Two-call scoped SQL RAG; separate application writes and fixed exercise/support control. |
| Personalization and state boundaries | Explicit saved display choices; no questionnaire, click tracking or inferred state. |
| User control and crisis access | Pause/Resume/Stop, neutral outcomes, unconditional bundled support. |
| Timing and persistence questions | Measured visible sequence below 90s; inspected saved IDs; restart/retry checks pass. |
| Active recovery and simplified-screen proposals | Unfinished refresh disclosed as unsaved; only display settings collapse. These scope changes are explained in the design. |
| Evaluation and process record | 18 fictional scenarios, three cross-case checks, repeated live sample, failures/refinements, two recordings and AI disclosure. |

The [final design](design-pipeline.md) gives reasons and tradeoffs;
[Part 3 coverage](part3/requirements.md) maps the final deliverables to the supplied
assignment. Figma was an optional workflow and was not used or claimed.
