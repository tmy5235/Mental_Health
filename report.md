# Assignment 3 — Part 2: Breathing Room

Trevor Michael Yuhaniak · IST 402 · October 26, 2026

## Submission status

**Part 2 implementation and local evidence are complete; publication is pending.**
The Vue/FastAPI/SQLite prototype supports one complete skill, saved conversations
and sessions, scoped SQL RAG, explicit preferences and independent crisis access.
Two real OpenAI exchanges demonstrate the model contribution. One unsupported
pause-history statement is preserved and analyzed below rather than hidden.

- Repository: [Mental_Health](https://github.com/tmy5235/Mental_Health)
- Working branch: `codex/implementation-foundation`
- Submitted implementation commit: **pending reviewed commit and push**.
- Canvas upload: not performed. Separate signed-in rubric/deadline not verified.
- Evidence: screenshots, actual live replies, database comparisons and repeatable
  tests linked below. No video recording is claimed; the supplied overview puts
  the finished-app/process screencasts in Part 3.

Relative links resolve within this repository. Publication checks are recorded
in the verification notes when the implementation is pushed.

## Coherent scope and experience

One skill: six paced-breathing cycles, four counts in and six out. The app opens
on a short instruction and Start breathing. Chat, History and Display settings
are optional. Pause, Stop and clearly labeled Crisis support remain independent
of generated replies. The person never has to type, rate a mood or finish.

The October 26 redesign removes the large preview card, repeated explanatory copy
and decorative motion. A centered layout, muted blue/ivory, dark text, still
pacing by default, and optional larger text reduce simultaneous content. These
are accessibility/design choices, not evidence of anxiety reduction. The
[research rationale and sources](docs/design-pipeline.md#part-2-visual-research-and-selected-design--october-26)
distinguish color-emotion associations from effects on actual feelings.

The prototype is fictional coursework, not therapy, diagnosis, clinical
monitoring or a service to offer to people in crisis. It stores activity and
attributed chat text without inferring mental state or improvement.

## Implementation across the stack

Vue owns the sequence, timing, controls and plain-text display. FastAPI validates
HTTP/JSON requests and coordinates provider and storage operations. Only Python
opens the project-relative SQLite database. Existing demonstration records were
preserved; startup adds schema without reseeding history.

A conversation submission saves its user message with stable conversation,
request and message IDs. First, the provider proposes one of five scoped SQL
SELECT templates from the question and schema. The backend rejects other SQL,
binds ownership, and uses a read-only connection, table/field authorization,
row/time/context limits. Second, the provider receives actual selected records,
field meanings and reviewed skill instructions. The actual reply is committed
before the API confirms a save. Failed requests retain the user message/status;
identical retries never duplicate the exchange. Both live stages count against
a persistent 50-call cap. Mock output and live output have different labels.

Live demonstration used `gpt-4.1-mini` through OpenAI Responses, with two fictional
exchanges/four model calls. The first explained the six 4/6 cycles, 60 active
seconds and exit controls correctly. The second described the latest completed
session as 60 seconds, six cycles and text display, citing the matching SQLite ID.
Actual replies were saved and matched across browser/API/database; identical
retries made no additional model calls. After backend restart and browser refresh,
the live replies remained labeled AI while new requests returned to mock mode.

**Surprising finding and limitation:** the history reply also said “not paused,”
although retrieved session fields contain no pause events. A valid cited ID does
not establish that every sentence is grounded. I strengthened the prompt to
forbid pause-history and stop-reason inference, preserved the original reply,
and did not claim the change fixed live behavior: the approved four-call budget
was exhausted. Broader/repeated live evaluation remains Part 3 work.

[Live reply and record evidence](docs/part2-live-evidence.json) ·
[Saved live replies in current interface](docs/screenshots/part2-submission/10-saved-ai-chat.jpg)

[Architecture, exact contracts and responsibilities](docs/design-pipeline.md) ·
[Run/setup instructions](README.md) · [Source](backend/app/main.py)

## Verified evidence

All observations use fictional records. October 26 results supersede older
implementation-status statements in the historical logs.

| Requirement/check | Observed result | Evidence |
| --- | --- | --- |
| Complete a chosen skill | Browser completed six cycles and saved 60 active seconds. Latest branded run start/end difference **60.003 seconds**, below 90 seconds. No voluntary pause in this run. Separately measured earlier entry: reload-to-ready 2.717 seconds; reload-to-Start return 3.003 seconds. No optional setup or human reading-time claim. | [Completion screenshot](docs/screenshots/part2-submission/05-completed.jpg), session `08e94b53-7233-4f00-a85c-7b4fd5822520` |
| Session persistence | Older rows preserved; newly completed and stopped sessions shown with stable IDs, durations and distinct statuses. | [History screenshot](docs/screenshots/part2-submission/09-history.jpg), [Verification](docs/verification.md), SQLite read-only inspection |
| Live model contribution | Two OpenAI exchanges/four calls saved; correct skill explanation and cited history facts, plus documented unsupported pause claim. | [Actual replies and review](docs/part2-live-evidence.json), [saved AI screenshot](docs/screenshots/part2-submission/10-saved-ai-chat.jpg) |
| Conversation persistence and retrieval | Same conversation/message/source IDs in UI, API and SQLite; original exchange survived refresh and backend restart. | [Chat screenshot](docs/screenshots/part2-submission/10-saved-ai-chat.jpg); live conversation `ee590ec5-eed1-474a-80fc-6424b378f5ad` |
| Request failure and retry | Stopped backend: no false reply/save confirmation. Unconfirmed message survived refresh. After restart, retry produced one user/reply pair. | [Outage screenshot](docs/screenshots/part2-submission/11-request-failure.jpg), verification |
| Leave an exercise | Keyboard Pause/Resume retained focus. Support paused; Return stayed paused. Stop saved a distinct stopped record. | [Paused](docs/screenshots/part2-submission/07-paused.jpg), [stopped](docs/screenshots/part2-submission/08-stopped.jpg); latest stopped session `f076976f-4b14-4f65-815b-a2edbf3bdf02`, 0.483 active seconds |
| Independent crisis route | Bundled support panel opened during backend outage. Regional resources rechecked October 26; no external service contacted. | [Support during failure](docs/screenshots/part2-submission/12-support-during-failure.jpg), verification |
| Low-stimulus presentation | 390px home and larger text had no page-level horizontal overflow. Explicit text choice survived refresh. Revised blue palette: checked text contrast 4.83:1–10.90:1. | [Home](docs/screenshots/part2-submission/01-home.jpg), [mobile](docs/screenshots/part2-submission/03-mobile.jpg), design notes |
| SQL and provider failures | Tests cover empty/selected retrieval; write, scope, comment, function and multi-statement rejection; missing configuration, HTTP failure, malformed/incomplete output, save failure, retry and restart. | [Automated tests](backend/tests/test_chat.py), verification |

**50 automated checks passed** (36 backend, 14 frontend); the production build
passed. Build and test commands/results, exact IDs, selected limitations and inspection
queries are in [verification.md](docs/verification.md). Screenshots are software
evidence, not a recording, participant test or clinical evaluation.

## Screenshot walkthrough

The numbered set shows the current **Breathing Room** branding. Each capture
illustrates one part of the experience; the set collectively covers Part 2.

| Screenshots | What the reviewer can see |
| --- | --- |
| [01 Home](docs/screenshots/part2-submission/01-home.jpg), [02 Preferences](docs/screenshots/part2-submission/02-preferences.jpg), [03 Mobile](docs/screenshots/part2-submission/03-mobile.jpg) | Clear entry, explicit saved choices and readable narrow layout. |
| [04 Active](docs/screenshots/part2-submission/04-active.jpg), [05 Completed](docs/screenshots/part2-submission/05-completed.jpg) | Current instruction/count, Pause/Stop, then six cycles/60 active seconds and confirmed save. |
| [06 Support pauses](docs/screenshots/part2-submission/06-support-pauses.jpg), [07 Paused](docs/screenshots/part2-submission/07-paused.jpg), [08 Stopped](docs/screenshots/part2-submission/08-stopped.jpg) | Support is available during an exercise; Return remains paused; early exit saves as Stopped. |
| [09 Session history](docs/screenshots/part2-submission/09-history.jpg), [10 Saved AI conversation](docs/screenshots/part2-submission/10-saved-ai-chat.jpg) | Durations, outcomes and record IDs; actual saved model replies, model identifier and source ID. |
| [11 Failed request](docs/screenshots/part2-submission/11-request-failure.jpg), [12 Support during failure](docs/screenshots/part2-submission/12-support-during-failure.jpg), [13 Recovered](docs/screenshots/part2-submission/13-recovered.jpg) | Honest unavailable-service state, independent support panel, then successful mock retry after restart. |

Screenshot10 displays previously generated real AI replies while the current
provider is mock; its mode banner is intentional. No additional paid calls were
used to refresh screenshots. The [original live-run capture](docs/screenshots/part2-live-chat.jpg)
preserves the earlier name and live-mode banner. The unsupported pause claim
remains visible and documented. Screenshots alone cannot prove elapsed timing,
SQLite persistence, SQL restrictions or retry idempotence; the measured records,
JSON evidence and repeatable checks above supply that evidence.

## Submission steps

The implementation and Part 2 evidence are prepared. Publish the checked version,
insert its exact commit link above, verify the links, and upload this `report.md`
to Canvas. The app stays on localhost. Student review should include the design
tradeoffs and the live model limitation, not just the screenshots.

## Research grounding and control

R1/D2 led to a fixed six-cycle sequence with one current instruction. R2/D4 led
to the always-visible support control, bundled independently of the model.
R3/R4 led to usable Pause/Stop and optional chat. D1/D3/D5 led to a simple default,
no required self-report, and remembered explicit display preferences with reset.
D6 informed restrained color, brief neutral language and optional motion. The
tradeoff is less automatic personalization and no distress detection; completion
and clicks are activity facts, not evidence of emotional improvement. Full
[R/D mapping and alternatives](docs/design-pipeline.md#research-grounding-and-tradeoffs)
remain in the design notes.

## Limitations and later work

Live generation can be wrong even when schema and cited IDs validate. The finite
SQL grammar restricts questions to recent sessions, current-conversation messages
and preferences; it is not arbitrary analytics. Only two live cases have been
examined; no clinical effectiveness has been established. Mock crisis redirection
is not a validated classifier, and support never depends on it.

Unfinished exercise refresh resets without saving, disclosed before Start. Unsent
retries survive same-tab refresh but can be lost when closing the tab. No account
system, history deletion, interrupted-session recovery or public deployment.
Full screen-reader/zoom/text-spacing/OS-motion checks, true hidden-tab triggering,
clean-checkout setup and broad user testing remain. Figma is optional and unused.
Part 3's full evaluation and final recordings are not claimed complete here.

## Process and AI disclosure

Codex authored and revised code, researched primary color literature and W3C
accessibility guidance, ran automated/browser checks and inspected SQLite. The
[AI-use disclosure](AI-USE.md) records tool/model limits; the
[curated evidence](docs/evidence.md) records decisions and revised approaches.
No source was copied from the prior Expedia app. No real patient data was used.
The student must review and understand generated code and final claims.

The [submitted Part 1 snapshot](https://github.com/tmy5235/Mental_Health/tree/f7b91254907a3eb18b22dc7d58b82a89960c63cb)
remains separately available from this Part 2 implementation.
