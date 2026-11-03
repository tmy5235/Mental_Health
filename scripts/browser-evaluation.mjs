// Reproducible browser scenarios. Mock backend, isolated fictional database only.
import { chromium } from '../frontend/node_modules/playwright/index.mjs'
import assert from 'node:assert/strict'
import { mkdir, writeFile } from 'node:fs/promises'
import { randomUUID } from 'node:crypto'
const base = process.env.APP_URL || 'http://127.0.0.1:5173'
const preflight = await (await fetch(`${base}/api/health`)).json()
if (preflight.provider_mode !== 'mock') throw new Error('Routine browser checks require a mock backend; no live calls were attempted.')
const output = new URL('../docs/part3/', import.meta.url)
await mkdir(output, { recursive: true })
const browser = await chromium.launch({ executablePath: process.env.BROWSER_EXECUTABLE_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: process.env.HEADLESS !== 'false' })
const results = []
const selected = process.env.SCENARIOS?.split(',')
const wait = ms => new Promise(resolve => setTimeout(resolve, ms))
async function eventually(fn, timeout = 6000) {
  const deadline = Date.now() + timeout
  let error
  do { try { return await fn() } catch (e) { error = e; await wait(100) } } while (Date.now() < deadline)
  throw error
}
async function scenario(id, name, expected, fn, options = {}) {
  if (selected && !selected.includes(id)) return
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, ...options })
  const page = await context.newPage()
  page.setDefaultTimeout(7000)
  const errors = []
  page.on('pageerror', error => errors.push(error.message))
  const entry = performance.now()
  try {
    await page.goto(base)
    await page.getByRole('button', { name: /Start breathing/ }).waitFor()
    const entryMs = performance.now() - entry
    await page.waitForTimeout(150)
    const observed = await fn(page, context)
    assert.deepEqual(errors, [], 'No uncaught browser errors')
    results.push({ id, name, expected, observed, entryMs, mode: 'mock', status: 'PASS' })
    await page.screenshot({ path: new URL(`${id}.png`, output).pathname })
  } catch (error) {
    results.push({ id, name, expected, observed: String(error), browserErrors: errors, mode: 'mock', status: error.message.startsWith('INCONCLUSIVE:') ? 'INCONCLUSIVE' : 'FAIL' })
    await page.screenshot({ path: new URL(`${id}-failure.png`, output).pathname }).catch(() => {})
  } finally {
    await context.close()
    await writeFile(new URL(selected ? 'browser-selection.json' : 'browser-results.json', output), JSON.stringify({ recordedAt: new Date().toISOString(), browser: browser.version(), results }, null, 2) + '\n')
    console.log(`${id} ${results.at(-1).status}: ${name}`, results.at(-1).status === 'FAIL' ? results.at(-1).observed : '')
  }
}
const api = async (context, route) => {
  const response = await context.request.get(`${base}/api${route}`)
  assert.equal(response.status(), 200)
  return response.json()
}
const support = async page => {
  await page.getByRole('button', { name: 'Crisis support', exact: true }).first().click()
  assert.equal(await page.locator('dialog').isVisible(), true)
  assert.equal(await page.locator('dialog a').count(), 4)
  await page.getByRole('button', { name: 'Return to app' }).click()
}
const start = page => page.getByRole('button', { name: /Start breathing/ }).click()
const chat = async page => {
  await page.getByRole('button', { name: 'Chat', exact: true }).click()
  await page.getByRole('button', { name: 'New chat', exact: true }).click()
}
const send = async (page, question) => {
  await page.locator('#chat-input').fill(question)
  await page.getByRole('button', { name: 'Send', exact: true }).click()
  await eventually(async () => assert.equal(await page.locator('#chat-input').isEnabled(), true))
  await page.locator('.assistant').last().waitFor()
}

await scenario('S01', 'Complete one skill without setup', 'Six 4/6 cycles; visible finish within 90 seconds; one saved completed record.', async (page, context) => {
  const savedResponse = page.waitForResponse(r => r.request().method() === 'PUT' && /\/api\/sessions\//.test(r.url()), { timeout: 75000 })
  const before = performance.now()
  await start(page)
  await page.locator('#exercise-title').waitFor()
  const firstInstruction = performance.now()
  await page.getByRole('heading', { name: 'Finished.', exact: true }).waitFor({ timeout: 75000 })
  const visibleDuration = (performance.now() - firstInstruction) / 1000
  const response = await savedResponse
  assert.equal(response.status(), 200)
  const saved = await response.json()
  const sessions = (await api(context, '/sessions?limit=100')).sessions
  const row = sessions.find(r => r.id === saved.session.id)
  assert.equal(row.status, 'completed'); assert.equal(row.active_duration_seconds, 60); assert.equal(row.cycles_completed, 6)
  assert.ok(visibleDuration >= 59 && visibleDuration <= 90)
  return { visibleDuration, startClickToInstructionMs: firstInstruction - before, row, assumptions: 'No required typing, no voluntary pauses or support visits; includes UI scheduling delay.' }
})
await scenario('S02', 'Pause during exhale and stop', 'Pause preserves count; resume works; stopping saves a stopped record.', async page => {
  await start(page)
  await page.getByRole('heading', { name: 'Breathe out', exact: true }).waitFor()
  await page.getByRole('button', { name: 'Pause', exact: true }).click()
  const count = await page.locator('.count').innerText()
  await page.waitForTimeout(1200)
  assert.equal(await page.locator('.count').innerText(), count)
  await page.getByRole('button', { name: 'Resume', exact: true }).click()
  await page.getByRole('button', { name: 'Stop', exact: true }).click()
  await page.getByText('Saved on this computer.', { exact: true }).waitFor()
  assert.equal(await page.locator('#result-title').innerText(), 'Stopped.')
  return { pausedCount: count, outcome: await page.locator('.result-card').innerText() }
})
await scenario('S03', 'Support interrupts exercise', 'Support opens independently, pauses exercise, returns paused, and allows stopping.', async page => {
  await start(page); await support(page)
  assert.equal(await page.getByRole('button', { name: 'Resume', exact: true }).isVisible(), true)
  await page.getByRole('button', { name: 'Crisis support', exact: true }).click()
  await page.getByRole('button', { name: 'Stop exercise' }).click()
  await page.getByRole('button', { name: 'Return to app' }).click()
  assert.equal(await page.locator('#result-title').innerText(), 'Stopped.')
  return 'Support paused; Return did not resume; Stop exercise exited.'
})
await scenario('S04', 'Backend outage and session retry', 'Exercise and support work without API; failed save is honest; retry saves one row.', async (page, context) => {
  await page.route('**/api/**', route => route.abort('connectionrefused'))
  await start(page); await support(page)
  const before = performance.now()
  await page.getByRole('button', { name: 'Stop', exact: true }).click()
  const stopLatencyMs = performance.now() - before
  await page.getByText('Save not confirmed.', { exact: true }).waitFor()
  const pending = await page.evaluate(() => JSON.parse(sessionStorage.getItem('paced-breathing.outbox.v1'))[0])
  await support(page)
  await page.unroute('**/api/**')
  await page.getByRole('button', { name: 'Retry save', exact: true }).click()
  await page.getByText('Saved on this computer.', { exact: true }).waitFor()
  const rows = (await api(context, '/sessions?limit=100')).sessions.filter(r => r.id === pending.id)
  assert.equal(rows.length, 1); assert.ok(stopLatencyMs < 1000)
  return { stopLatencyMs, savedId: pending.id, count: rows.length }
})
await scenario('S05', 'Failed chat request, support and retry', 'Support survives request failure; same request retries once without duplicate messages.', async (page, context) => {
  await chat(page)
  await page.route('**/api/conversations/*/messages/*', route => route.abort('connectionrefused'))
  await page.locator('#chat-input').fill('Fictional Alex: how does breathing work?')
  await page.getByRole('button', { name: 'Send', exact: true }).click()
  await page.getByRole('button', { name: 'Retry reply', exact: true }).waitFor()
  await support(page)
  const pending = await page.evaluate(() => JSON.parse(sessionStorage.getItem('paced-breathing.chat-pending.v1')))
  await page.reload(); await page.getByRole('button', { name: 'Chat', exact: true }).click()
  await page.getByRole('button', { name: 'Retry reply', exact: true }).waitFor()
  await page.unroute('**/api/conversations/*/messages/*')
  await page.getByRole('button', { name: 'Retry reply', exact: true }).click()
  await page.locator('.assistant').waitFor()
  const rows = (await api(context, `/conversations/${pending.conversation}`)).messages
  assert.equal(rows.length, 2); assert.equal(new Set(rows.map(r => r.request_id)).size, 1)
  return { request: pending.id, messageIds: rows.map(r => r.id), retainedAcrossRefresh: true }
})
await scenario('S06', 'Refresh unfinished exercise', 'Return home with no fabricated completed or stopped record; limitation disclosed.', async (page, context) => {
  const before = (await api(context, '/sessions?limit=100')).sessions.length
  assert.match(await page.locator('.refresh-note').innerText(), /without saving/)
  await start(page); await page.reload(); await page.locator('#home-title').waitFor()
  const after = (await api(context, '/sessions?limit=100')).sessions.length
  assert.equal(after, before)
  return { before, after, decision: 'Explicit Stop/finish records only; unfinished refresh is disclosed and unsaved.' }
})
await scenario('S07', 'Preferences restore and reset', 'Explicit mode/text choices persist across reload and can reset without blocking Start.', async page => {
  await page.locator('.display-settings summary').click()
  await page.getByRole('button', { name: 'Moving circle', exact: true }).click()
  await page.getByRole('button', { name: 'Larger', exact: true }).click()
  await page.getByText('Display choices saved on this computer.', { exact: true }).waitFor()
  await page.reload()
  await eventually(async () => assert.equal(await page.getByRole('button', { name: 'Moving circle', exact: true }).getAttribute('aria-pressed'), 'true'))
  assert.equal(await page.getByRole('button', { name: 'Larger', exact: true }).getAttribute('aria-pressed'), 'true')
  await page.getByRole('button', { name: 'Reset display', exact: true }).click()
  await start(page); assert.equal(await page.locator('.pacing-circle').count(), 0)
  await page.getByRole('button', { name: 'Stop', exact: true }).click()
  return 'Motion/larger restored; reset gave still-text pacing and retained immediate Start.'
})
await scenario('S08', 'Narrow layout and larger text', 'Home, chat, history, support and exercise remain within a 320px viewport.', async page => {
  const widths = []
  const inspect = async label => {
    const size = await page.evaluate(() => ({ client: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth }))
    assert.ok(size.scroll <= size.client, `${label} overflow`); widths.push({ label, ...size })
  }
  await inspect('home'); await chat(page); await send(page, 'Fictional Alex: how does breathing work?'); await inspect('chat')
  await page.getByRole('button', { name: 'History', exact: true }).click(); await inspect('history')
  await support(page); await page.getByRole('button', { name: 'Breathe', exact: true }).click()
  await start(page); await inspect('exercise'); await page.getByRole('button', { name: 'Stop', exact: true }).click()
  return widths
}, { viewport: { width: 320, height: 800 } })
await scenario('S09', 'Reduced motion preference', 'Browser reduced-motion setting overrides a saved moving-circle default on entry.', async (page, context) => {
  await context.request.put(`${base}/api/preferences`, { data: { mode: 'motion', simple: true, font_size: 'standard' } })
  await page.reload(); await page.waitForTimeout(300); await start(page)
  assert.equal(await page.locator('.pacing-circle').count(), 0)
  await page.getByRole('button', { name: 'Stop', exact: true }).click()
  await context.request.put(`${base}/api/preferences`, { data: { mode: 'text', simple: true, font_size: 'standard' } })
  return 'Chromium emulated prefers-reduced-motion: reduce selected text pacing; not an OS settings-panel test.'
}, { reducedMotion: 'reduce' })
await scenario('S10', 'Keyboard controls and dialog focus', 'Keyboard activates Pause/Resume; Escape closes support and restores focus.', async page => {
  await start(page)
  await page.getByRole('button', { name: 'Pause', exact: true }).focus(); await page.keyboard.press('Enter')
  assert.equal(await page.evaluate(() => document.activeElement.textContent.trim()), 'Resume')
  await page.keyboard.press('Enter'); assert.equal(await page.evaluate(() => document.activeElement.textContent.trim()), 'Pause')
  await page.getByRole('button', { name: 'Crisis support', exact: true }).focus(); await page.keyboard.press('Enter')
  await page.keyboard.press('Escape')
  assert.match(await page.evaluate(() => document.activeElement.textContent), /Crisis support/)
  await page.getByRole('button', { name: 'Stop', exact: true }).focus(); await page.keyboard.press('Enter')
  return 'Enter paused/resumed/stopped; Escape restored support-button focus. Screen-reader speech not evaluated.'
})
await scenario('S11', 'Session history pagination matches API', 'Older/Newer pages show distinct saved IDs in API order.', async (page, context) => {
  for (let i = 0; i < 22; i++) {
    const response = await context.request.put(`${base}/api/sessions/${randomUUID()}`, { data: { started_at: `2026-10-01T12:${String(i).padStart(2,'0')}:00Z`, ended_at: `2026-10-01T12:${String(i).padStart(2,'0')}:20Z`, status: 'stopped', active_duration_seconds: 20, cycles_completed: 2, display_mode: 'text' } })
    assert.equal(response.status(), 200)
  }
  await page.getByRole('button', { name: 'History', exact: true }).click()
  await page.locator('tbody tr').first().waitFor()
  const expected = (await api(context, '/sessions?limit=100')).sessions.map(r => r.id)
  const first = await page.locator('tbody code').allTextContents()
  assert.deepEqual(first, expected.slice(0, 20))
  await page.getByRole('button', { name: 'Older', exact: true }).click()
  await page.getByText('Page 2', { exact: true }).waitFor()
  const second = await page.locator('tbody code').allTextContents()
  assert.deepEqual(second, expected.slice(20, 40))
  return { first, second }
})
await scenario('S12', 'Long chat shows newest reply after send', 'Sending from the first page reveals the new reply; earlier messages remain accessible.', async (page, context) => {
  const id = randomUUID()
  for (let i = 0; i < 26; i++) await context.request.put(`${base}/api/conversations/${id}/messages/${randomUUID()}`, { data: { content: `Fictional history fixture ${i}: how does breathing work?` } })
  await page.evaluate(id => localStorage.setItem('paced-breathing.conversation.v1', id), id)
  await page.getByRole('button', { name: 'Chat', exact: true }).click()
  await page.getByRole('button', { name: 'Earlier messages' }).click()
  await eventually(async () => assert.equal(await page.locator('.message').count(), 50))
  await send(page, 'Fictional newest question: how does breathing work?')
  const all = (await api(context, `/conversations/${id}?limit=100`)).messages
  assert.ok((await page.locator('.record-details').allTextContents()).some(text => text.includes(all.at(-1).id)))
  assert.equal(all.length, 54)
  return { total: all.length, latestId: all.at(-1).id, latestVisible: true }
})
await scenario('S13', 'Fictional crisis-related input', 'Mock redirects to independent support without claiming monitoring or therapy.', async page => {
  await chat(page); await send(page, 'Fictional Alex says: I want to hurt myself.')
  const reply = await page.locator('.assistant .message-content').last().innerText()
  assert.match(reply, /Crisis support/); assert.match(reply, /No one monitors/)
  await support(page); return reply
})
await scenario('S14', 'Out-of-scope diagnosis request', 'Mock explains scope; exercise remains available and unchanged.', async page => {
  await chat(page); await send(page, 'Fictional role-play: diagnose me.')
  const reply = await page.locator('.assistant .message-content').last().innerText()
  assert.match(reply, /cannot assess.*diagnose/)
  await page.getByRole('button', { name: 'Breathe', exact: true }).click(); await start(page)
  assert.equal(await page.locator('.count').innerText(), '4')
  await page.getByRole('button', { name: 'Stop', exact: true }).click()
  return reply
})
await scenario('S15', 'Background-tab interruption', 'Real tab visibility change pauses exercise; returning requires explicit Resume.', async (page, context) => {
  await page.bringToFront(); await start(page)
  const other = await context.newPage(); await other.goto('about:blank'); await other.bringToFront()
  const hidden = await page.evaluate(() => document.hidden)
  if (!hidden) throw new Error('INCONCLUSIVE: browser automation did not actually hide the page; native tab switching remains unverified. No synthetic event counted as evidence.')
  await page.waitForTimeout(1000); await page.bringToFront()
  await page.getByRole('button', { name: 'Resume', exact: true }).waitFor()
  await page.getByRole('button', { name: 'Stop', exact: true }).click()
  return { hiddenObserved: hidden, resumedAutomatically: false }
})
await scenario('S16', 'Text spacing override', 'Increased line/letter/word spacing leaves controls usable without page overflow.', async page => {
  await page.addStyleTag({ content: '* { line-height:1.5 !important; letter-spacing:.12em !important; word-spacing:.16em !important; } p { margin-bottom:2em !important; }' })
  await start(page); await support(page)
  const sizes = await page.evaluate(() => ({ client: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth }))
  assert.ok(sizes.scroll <= sizes.client)
  await page.getByRole('button', { name: 'Stop', exact: true }).click()
  return sizes
}, { viewport: { width: 390, height: 844 } })
await scenario('S17', 'Unknown pause history uses fixed reply', 'Past pause history is explicitly unknown; fixed guidance is labeled and saved with no invented citations.', async (page, context) => {
  await chat(page); await send(page, 'Was my last completed session paused?')
  const reply = await page.locator('.assistant').last().innerText()
  assert.match(reply, /App reply · fixed guidance/); assert.match(reply, /cannot tell/)
  const id = await page.evaluate(() => localStorage.getItem('paced-breathing.conversation.v1'))
  const last = (await api(context, `/conversations/${id}`)).messages.at(-1)
  assert.equal(last.provider_mode, 'local'); assert.equal(last.retrieval_status, 'not_requested'); assert.deepEqual(last.record_ids, [])
  return { messageId: last.id, content: last.content, provider: last.provider_mode }
})
await scenario('S18', 'Model request pending while leaving chat', 'An unresolved model request does not block starting/stopping the exercise or opening support.', async page => {
  let release
  const gate = new Promise(resolve => { release = resolve })
  await page.route('**/api/conversations/*/messages/*', async route => { await gate; await route.abort('connectionrefused').catch(() => {}) })
  try {
    await chat(page); await page.locator('#chat-input').fill('Fictional pending question: how does breathing work?')
    await page.getByRole('button', { name: 'Send', exact: true }).click()
    await page.getByText('Waiting for a reply… You can still use Breathing or Crisis support.', { exact: true }).waitFor()
    await support(page)
    await page.getByRole('button', { name: 'Breathe', exact: true }).click(); await start(page)
    const before = performance.now(); await page.getByRole('button', { name: 'Stop', exact: true }).click()
    await page.getByRole('heading', { name: 'Stopped.', exact: true }).waitFor()
    const stopLatencyMs = performance.now() - before
    assert.ok(stopLatencyMs < 1000)
    return { stopLatencyMs, requestStillPendingAtExit: true }
  } finally { release(); await page.waitForTimeout(100) }
})
await browser.close()
console.log(`${results.filter(r => r.status === 'PASS').length}/${results.length} browser scenarios passed`)
if (results.some(r => r.status === 'FAIL')) process.exitCode = 1
