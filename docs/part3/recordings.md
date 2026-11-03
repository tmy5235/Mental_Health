# Recordings — finished app and process

These are screen captures of the actual running local app, using fictional data,
with clearly labeled written commentary. They have no spoken narration. Playback
is at normal speed, including the full breathing sequence. They were produced with coding-agent assistance, disclosed in [AI-USE.md](../../AI-USE.md).
They demonstrate actual application behavior and a written source explanation;
no independent human participant evaluation or spoken narration is claimed.

## Finished application — 2 minutes 12 seconds

[Play/download the finished-app demonstration](finished-demo.mp4)

| Approximate time | Section |
| --- | --- |
| 0:00 | 1 · Purpose and choice |
| 0:06 | 2 · Explicit personalization |
| 0:12 | 3 · Full exercise — real time |
| 1:12 | 4 · Completion and persistence |
| 1:18 | 5 · Useful saved history |
| 1:24 | 6 · Independent support and exit |
| 1:30 | 7 · User control |
| 1:35 | 8 · Saved live-model contribution |
| 1:44 | 9 · Refined model boundary |
| 1:52 | 10 · Failure is visible |
| 1:58 | 11 · Support survives failure |
| 2:04 | 12 · Recovery and limits |

The saved live reply at 1:35 is an actual response from the bounded evaluation,
shown while the server is back in mock mode. The recording makes no new live
calls. Failure injection blocks API requests in the browser and is explicitly
identified in the commentary. External support links are never activated.

## Process screencast — 1 minute 42 seconds

[Play/download the failure, evidence, fix and code explanation](process-screencast.mp4)

- 0:00–0:38: original pagination failure, observed before changing the behavior.
  A new reply is saved in a 54-message conversation but absent from the visible page.
- Approximately 0:39–1:19: repeat the same scenario after the correction; API
  count and saved message ID establish that the latest reply is now visible.
- Approximately 1:20–1:42: show and explain the actual generated API code,
  including the latest-page calculation and exact-page-boundary regression test.

The two real captures are joined in sequence; the source explanation is an
explicitly labeled explanatory screen. [Before JSON](pagination-before.json),
[after JSON](pagination-after.json), [source runner](../../scripts/chat-pagination-check.mjs).

## Verification and reproducibility

MP4/H.264, 25 fps; demo 1280×960, process 1280×900. [Media metadata](video-metadata.json).
Representative frames showing the exercise, actual AI reply and source explanation
were decoded and visually reviewed. A first demo capture timed out before completing;
it is excluded from deliverables and was replaced by a successful full capture.
The failed recording is not treated as a failed application test; its cause was
not established. The separate final timed browser check is the timing evidence.

Scripts use Playwright video capture. `record-demo.mjs` needs the fictional live
conversation records in its served demo database; normal app startup does not.
MP4 conversion/joining used an isolated FFmpeg utility, with no timing changes.
