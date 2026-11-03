# AI-use disclosure

## Tools, identifiers and roles

| Tool or model | Role and disclosure |
| --- | --- |
| OpenAI Codex desktop coding assistant | Interpreted supplied requirements; proposed/revised design; generated application code, tests and documentation; debugged failures; operated browser checks; inspected SQLite; produced captioned recordings and packaged deliverables. The supplied assistant context identifies a GPT-6-based agent; the exact runtime model/build was not exposed and is not invented here. |
| OpenAI Responses API, configured alias gpt-4.1-mini | Proposed scoped SQL and generated replies from reviewed skill context and selected fictional records. Two exchanges/four calls in Part 2 and eight exchanges/16 calls in Part 3: 20 calls across those recorded evaluations. The exact returned model snapshot was not captured. |
| demo-v1 | Deterministic mock adapter for routine tests and demonstration. It is application logic, not a live AI model. |
| reviewed-rules-v1 | Narrow application-owned fixed replies for recognized crisis phrases and past-pause questions. No provider call, retrieval or usage reservation; not a clinical detector. |
| Python unittest, Node node:test, FastAPI, SQLite, shell/Git | Regression checks, application execution, read-only data inspection, versioning and local packaging. |
| Playwright 1.64.1 and Chrome 156.0.8078.80 | Fictional browser evaluation, screenshots and actual browser recordings. Native computer-use controls supplemented the background-tab check during the final review. |
| Playwright FFmpeg and isolated imageio-ffmpeg utility | Converted/joined actual captures and added written explanatory captions. The recordings contain no spoken narration and do not establish independent human testing. |

No sub-agents, Figma, image generation, clinical participant evaluation, external
conversation dataset import or model training were used. No Expedia source code
or private conversation history was copied. Familiar architecture patterns and
an authorized private credential configuration were reused; credentials remain
outside source, logs and deliverables.

## Inputs and assistance boundaries

Inputs included the supplied assignment overview, R1–R4/D1–D6 research table,
user-state ideation material, explicit design preferences and local project files.
Earlier research review used official accessibility/provider documentation and
the palette sources cited in [the design](docs/design-pipeline.md). Regional
support details were checked through the available helpline lookup. Sources and
assistant suggestions informed design; they are not evidence of clinical benefit.

Codex authored substantial code and prose, including the final explanations and
recording captions. The [curated process log](docs/evidence.md) connects selected
instructions to implementation changes, verification and retained tradeoffs.
The source explanation in the process recording describes the generated pagination
code; it is not a recording of an independently performed human explanation.

## Evaluation and revised approaches

The original live outputs are preserved in [Part 2 evidence](docs/part2-live-evidence.json)
and [Part 3 raw results](docs/part3/live-results.json). Part 2 exposed an unsupported
pause inference. A stronger prompt was followed by repeated Part 3 tests; one pause
answer remained ambiguous and both crisis-input replies lacked direct redirection.
Five of eight Part 3 replies met the criteria; three motivated narrow fixed rules.
Mocked regression tests prove those rules' application behavior, not new live-model
success or broad safety. No further paid calls were made for final review or videos.

Another failure involved saved replies hidden by pagination. The before/after
recordings, API IDs and boundary tests establish the correction. The final audit
reran 54 automated tests, the production build and 18 browser scenarios. Automation
could not hide the tab; a separate native Chrome observation verified the paused
return state. Both observations remain recorded rather than rewriting the earlier
inconclusive result. See [evaluation](docs/part3/evaluation.md).

All evaluation inputs are fictional. No real person in distress was recruited,
no external support service was contacted, and no clinical effectiveness, monitoring
or therapeutic suitability is claimed. Raw evidence is retained with its original
wording; final prose consolidates earlier milestone notes into the completed design.
