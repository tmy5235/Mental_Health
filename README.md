# Mental Health Skills App — Paced Breathing

IST 402 · Assignment 3.1 · Design milestone · October 15, 2026

## Purpose and status

Design a local application that guides a short assigned skill, allows stopping at any time, and makes saved conversations and exercise history useful. The Part 1 design is documented; there is no running application yet.

This is a coursework prototype tested only with fictional scenarios. It does not diagnose, provide therapy, imply human monitoring, or establish clinical effectiveness. Do not deploy or offer it as a real mental health support service.

## Design guidelines

- **Skill and fictional task:** paced breathing, in for four counts and out for six, for six cycles. Fictional student Alex starts without disclosing feelings, may pause or leave, and later reviews a saved session.
- **Main flow:** Welcome → Breathing → neutral completion or early exit. Chat, history, and presentation options are optional supporting views. Keep pause, exit, and clearly labeled crisis access available during the exercise.
- **Timing and effort:** 60 seconds of breathing plus measured application overhead; no more than 90 seconds from first instruction to final planned step. Report entry/setup separately; exclude voluntary pauses and crisis-access time. Show one primary instruction at a time; require no typing, mood survey, or feedback (R1, D2, D3).
- **Presentation:** use plain, nonjudgmental language, readable contrast, visible keyboard focus, a narrow-screen layout, and a phase/count alternative to motion. Keep crisis access visible through errors and overlays (R2, D4, D6).
- **Personalization and control:** remember explicitly chosen display settings, with change/reset controls. Offer a user-controlled simplified view. Do not infer distress or diagnosis from clicks or automatically start an exercise (R3, R4, D1, D5).
- **Model and stored context:** optional chat uses reviewed skill material and scoped saved records through the class's two-call SQL RAG workflow. Application code controls timing, sequence, navigation, and writes. History browsing needs no model call.
- **Selected alternative:** immediate start with optional explanation rather than a conversation or settings questionnaire first. This reduces reading and configuration cost but provides less initial context (D3, D5). Supporting one skill limits technique choice; this is an acknowledged scope tradeoff (R4).

See [design-pipeline.md](docs/design-pipeline.md) for the sketches, flow, all ten R/D mappings, data model, alternatives, failure behavior, and unresolved implementation questions.

## Technology and boundaries

- Vue with JavaScript, HTML, and CSS presents the interface and calls FastAPI through HTTP/JSON. Node.js provides future frontend tooling.
- Python/FastAPI owns request validation, controllers, model-provider calls, and database operations. Plan a project-local `backend/.venv`.
- SQLite at `data/app.sqlite3` stores conversations, ordered messages, sessions, and preferences. Only the backend opens it; resolve its path from the project location.
- Keep keys in ignored `backend/.env`, explicitly loaded by backend code. Add a safe `.env.example` during implementation. Never expose keys to Vue, logs, submitted evidence, or Figma.

For RAG, the model first proposes retrieval SQL from a question and approved schema. The backend validates a single scoped, bounded, read-only query; a second call receives selected records and reviewed skill content. Save only actual replies through parameterized backend writes. Count both calls toward usage limits. Reject unsafe SQL; do not rely only on a SELECT prefix. Distinguish empty results, failed calls, and failed saves. Use finite timeouts, stable IDs, and bounded retries.

The fixed breathing sequence and bundled crisis information work independently of model requests. A model cannot control exits or determine whether support information is accessible. Later verification will compare SQLite rows, API responses, and displayed history across refresh/restart with fictional data.

## Repository map

```text
mental_health/
├── README.md
├── AGENTS.md
├── AI-USE.md
├── report.md
├── .gitignore
├── frontend/                 Vue implementation later
├── backend/                  FastAPI implementation later
├── data/                     Ignored runtime database; fictional fixtures later
├── docs/
│   ├── design-pipeline.md     Maintained design and architecture
│   ├── design.md              Compatibility link to the maintained design
│   ├── evidence.md            Curated decisions and revisions
│   ├── verification.md        Actual Part 1 document checks and limitations
│   └── part1-checklist.md      Submission checklist
├── prompts/                  Reusable instructions as needed
└── handoffs/
    └── current.md            Current state and next steps
```

Placeholder `.gitkeep` files preserve otherwise empty folders in a checkout. No dependencies, environment files, application code, or database have been created.

## Review this milestone

Read [report.md](report.md), [the design](docs/design-pipeline.md), [verification](docs/verification.md), [process evidence](docs/evidence.md), and [AI disclosure](AI-USE.md). Markdown can be read directly in the repository; no installation or launch command is required for this design-only milestone.

The startup folders and initial design guidelines are complete. Figma is an available later exploration method, not an additional Part 1 submission requirement. No Figma capture, live model run, application test, or clinical evaluation is claimed.

## Reuse and later work

The earlier Expedia project supplies candidate Vue/FastAPI, persistence, and two-call SQL RAG patterns. No source has been copied or audited for reuse here; identify exact files and adaptations when that occurs. Choose the provider/model, verify regional support-resource content, define endpoints and SQL validation, then implement and verify one complete flow. Add actual install/run/stop/test commands only after checking them. Use mocks for routine checks and fictional scenarios for every test.
