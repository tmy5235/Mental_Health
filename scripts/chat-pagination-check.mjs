// Real browser + real mock API. Run only against an isolated fictional database.
import { chromium } from '../frontend/node_modules/playwright/index.mjs'
import { mkdir, writeFile, readFile } from 'node:fs/promises'
import { randomUUID } from 'node:crypto'
const root = new URL('../docs/part3/', import.meta.url)
await mkdir(root, { recursive: true })
const baseline = process.argv.includes('--baseline')
const label = baseline ? 'pagination-before' : 'pagination-after'
const browser = await chromium.launch({ executablePath: process.env.BROWSER_EXECUTABLE_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true })
const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, recordVideo: { dir: root.pathname, size: { width: 1280, height: 900 } } })
const page = await context.newPage()
const base = process.env.APP_URL || 'http://127.0.0.1:5173'
const preflight = await (await fetch(`${base}/api/health`)).json()
if (preflight.provider_mode !== 'mock') throw new Error('Routine browser checks require a mock backend; no live calls were attempted.')
const conversation = randomUUID()
for (let i = 1; i <= 26; i++) {
  const response = await context.request.put(`${base}/api/conversations/${conversation}/messages/${randomUUID()}`, { data: { content: `Fictional pagination fixture ${i}: how does breathing work?` } })
  if (!response.ok()) throw new Error(`Fixture failed: ${response.status()}`)
}
await page.goto(base)
await page.evaluate(id => localStorage.setItem('paced-breathing.conversation.v1', id), conversation)
await page.getByRole('button', { name: 'Chat', exact: true }).click()
await page.locator('.message').first().waitFor()
if (!baseline) {
  await page.getByRole('button', { name: 'Earlier messages' }).click()
  await page.waitForFunction(() => document.querySelectorAll('.message').length === 50)
}
const caption = async text => {
  await page.evaluate(text => {
    let el = document.querySelector('#recording-caption')
    if (!el) { el = document.createElement('div'); el.id = 'recording-caption'; document.body.append(el) }
    el.style.cssText = 'position:fixed;bottom:0;left:0;right:0;z-index:99999;padding:20px 32px;background:#182331;color:white;font:20px/1.5 sans-serif;pointer-events:none;white-space:pre-wrap'
    el.textContent = 'RECORDING COMMENTARY · FICTIONAL TEST\n' + text
  }, text)
}
await caption('Failure investigation: this chat contains 52 saved messages. The first page displays only the first 50. We will send one more message from this page.')
await page.waitForTimeout(7000)
await page.locator('#chat-input').fill('Fictional newest message: explain the breathing counts.')
await page.getByRole('button', { name: 'Send', exact: true }).click()
await page.getByRole('button', { name: 'Send', exact: true }).waitFor()
await page.waitForTimeout(1000)
const response = await context.request.get(`${base}/api/conversations/${conversation}?limit=100`)
const saved = (await response.json()).messages
const latest = saved.at(-1)
const visible = await page.locator('.record-details').allTextContents()
const latestVisible = visible.some(value => value.includes(latest.id))
await caption(`Evidence: API has ${saved.length} messages, including the new saved reply.\nThe new reply is ${latestVisible ? 'VISIBLE' : 'MISSING'} on the current page. ${baseline ? 'The save succeeded; pagination kept showing the old page.' : 'The corrected view opens the page containing the new reply.'}`)
await page.screenshot({ path: new URL(`${label}.png`, root).pathname, fullPage: false })
await page.waitForTimeout(10000)
await caption('Code decision: after a successful send, fetch the latest page. The API supplies total message count; the view computes floor((total - 1) / 50) * 50. Manual Earlier/Later navigation remains available. This changes presentation, not saved records.')
await page.waitForTimeout(11000)
if (!baseline) {
  const source = await readFile(new URL('../backend/app/main.py', import.meta.url), 'utf8')
  const excerpt = source.slice(source.indexOf('    def messages('), source.indexOf('    @app.get("/api/preferences"'))
  const escape = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
  await page.setContent(`<html><body style="margin:48px;background:#f7f4ef;color:#303744;font:22px/1.6 sans-serif"><p>PROCESS SCREENCAST · SOURCE EXPLANATION</p><h1>Why the new reply was hidden</h1><p>The old view reloaded its current offset after Send. Saving was correct, but the new reply could be on a later page.</p><pre style="font:16px/1.6 monospace;white-space:pre-wrap;background:#e8edf4;padding:24px">${escape(excerpt)}</pre><p>For 54 messages and pages of 50, floor((54 − 1) / 50) × 50 = 50. Fetching offset 50 displays messages 51–54. Subtracting one also handles exactly full pages correctly.</p><p>The UI requests <code>latest=true</code> after Send. Earlier/Later navigation passes an explicit offset. Regression tests cover 52 messages and the exact 100-message boundary.</p><p>This generated code controls navigation only. It neither fabricates a reply nor changes stored history.</p></body></html>`)
  await page.waitForTimeout(22000)
}
await writeFile(new URL(`${label}.json`, root), JSON.stringify({ baseline, conversation, total: saved.length, latest_message_id: latest.id, latestVisible, expected: !baseline, pass: latestVisible === !baseline }, null, 2) + '\n')
const video = page.video()
await context.close()
await video.saveAs(new URL(`${label}.webm`, root).pathname)
await video.delete()
await browser.close()
console.log(JSON.stringify({ label, latestVisible, messages: saved.length }))
if (latestVisible !== !baseline) process.exitCode = 1
