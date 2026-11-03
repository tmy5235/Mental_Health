# Curated process evidence

This log records selected instructions, decisions and observed revisions, rather
than a full conversation transcript. Inputs and tests are fictional; credentials,
private records and unrelated conversations are excluded. Historical checkpoints
remain in Git. [AI-USE.md](../AI-USE.md) identifies tools and assistance roles.

| Selected instruction or evidence | Change and reason | Check and final decision |
| --- | --- | --- |
| Request to begin Part 1 using the supplied overview and R1–R4/D1–D6 table | Selected one complete paced-breathing skill with optional chat, history and preferences. | Arithmetic established a 60-active-second plan; later S01 measured the rendered sequence. No efficacy inference. |
| Earlier proposal required preferences before Start | Replaced mandatory setup with immediate Start and optional remembered choices to reduce effort. | S01/S07 verify no setup requirement and reversible preferences. |
| Supplied retrieval specification required model-proposed SQL and a second answer call | Revised ordinary backend retrieval to finite, scoped two-stage SQL RAG. | Allowlist/read-only/scope/limit tests, mocked provider contracts and small real-provider samples. Complexity/cost accepted to meet architecture. |
| User-state ideation requested comparison of questionnaires and clicking behavior | Selected explicit presentation choice; separated self-report, interaction facts and unsupported interpretation. | No questionnaire, click-speed telemetry, score, inferred profile or imported dataset. Current controls and storage reflect this boundary. |
| Request to begin implementation | Added typed session contracts, parameterized persistence and stable-ID retries before integrating Vue. | Storage/API/restart checks established saved IDs, conflict behavior and retained records. |
| Browser observations exposed focus/recovery wording issues | Corrected keyboard focus handling and distinct unsaved/retry states. | Keyboard, failed-save and failed-chat scenarios pass; screen-reader speech remains untested. |
| Request for a quieter interface and replacement of green | Selected sparse blue/ivory presentation, optional motion, readable type and visible focus. | Contrast calculation, narrow viewport and spacing checks; exact palette is a preference, not a proven intervention. |
| Part 2 live reply inferred no pauses from completion | Strengthened the prompt while preserving the actual reply. | Part 3 repeated the question; one answer still ambiguous. Prompt-only correction was insufficient. |
| Part 3 request: “Okay do what needs done and let me know if you need anything” | Added bounded repeated live evaluation, scenario evidence, refinements and recordings. | Eight exchanges/16 calls, five criteria met and three failures/ambiguities; no evidence was rewritten to hide failures. |
| Repeated live pause/crisis findings | Added narrow fixed replies before provider selection and reservations. | Provider-failure/replay tests and S13/S17 verify explicit wording, labels, zero calls and persistence. Indirect/negated-language limits remain. |
| A 52-message chat saved new replies outside the visible first page | Load the latest page after opening/sending; preserve Earlier/Later. | Before: 54 messages saved, newest absent. After: latest reply visible; 52/100-message tests and S12 pass. |
| First demo recording timed out | Replaced the incomplete capture with a successful full normal-speed recording. | Metadata and representative decoded frames checked; the failed capture is not an application failure claim. Separate S01 provides timing evidence. |
| Automated tab switch did not actually hide the document | Preserved S15 as inconclusive; supplemented with a native Chrome tab switch. | Native return showed Paused, Resume, cycle 1/6, 58s left and count 2; another observation showed the same values. No synthetic visibility event counted. |
| Final request to check functionality/documents and use final-submission language | Consolidated stale milestone notes into final rationale, contracts, evidence and requirement coverage; retained required prototype and AI disclosures. | 54 tests and build pass again; 17 automated scenario passes plus the native S15 observation. The final rendered timing was 66.985s, below 90s. |
| Explicit instruction “dont push yet” | Kept final review and deliverables local. | No push, deployment or submission is part of this review. |

The most consequential changes solve different problems: the pagination correction
makes already-saved information findable; the fixed replies prevent two recognized
input classes from relying on wording that varied in the live sample. Neither
change establishes clinical safety or general model reliability.

## Direct evidence

- [Before pagination](part3/pagination-before.json) and [after pagination](part3/pagination-after.json).
- [Process screencast and source explanation](part3/process-screencast.mp4).
- [Original repeated live outputs](part3/live-results.json) and [criteria/assessments](part3/evaluation.md).
- [Final browser rerun](part3/final-review/browser-results.json) and [native observation](part3/final-review/native-browser.json).
- [Final verification](verification.md), [clean checkout](part3/clean-checkout.md) and [requirement coverage](part3/requirements.md).

Unresolved limits are explicit: phrase matching is incomplete, other generated
claims can be unsupported, unfinished refresh is unsaved, tab closure can lose
pending retries, and full assistive-technology/other-OS testing has not occurred.
