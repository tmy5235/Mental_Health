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
