import test from 'node:test'
import assert from 'node:assert/strict'
import { request, saveSession } from '../src/api.js'

test('requests use relative API URLs and a bounded abort signal', async (t) => {
  t.mock.method(globalThis, 'fetch', async (url, options) => {
    assert.equal(url, '/api/health')
    assert.ok(options.signal instanceof AbortSignal)
    return new Response(JSON.stringify({ storage_available: true }))
  })
  assert.deepEqual(await request('/health'), { storage_available: true })
})

test('failed server responses never become successful saves', async (t) => {
  t.mock.method(globalThis, 'fetch', async () => new Response(
    JSON.stringify({ error: { message: 'Storage is unavailable.' } }), { status: 503 },
  ))
  await assert.rejects(saveSession('fictional-id', {}), /Storage is unavailable/)
})

test('successful HTTP status requires explicit matching save confirmation', async (t) => {
  t.mock.method(globalThis, 'fetch', async () => new Response(
    JSON.stringify({ saved: true, session: { id: 'other-session' } }),
  ))
  await assert.rejects(saveSession('fictional-id', {}), /did not confirm/)
})

test('a retry sends the same stable ID and frozen payload', async (t) => {
  const calls = []
  t.mock.method(globalThis, 'fetch', async (url, options) => {
    calls.push([url, options.method, options.body])
    return new Response(JSON.stringify({ saved: true, session: { id: 'fictional-id' } }))
  })
  const payload = Object.freeze({ status: 'stopped', active_duration_seconds: 20 })
  await saveSession('fictional-id', payload)
  await saveSession('fictional-id', payload)
  assert.deepEqual(calls[0], calls[1])
})

test('network, timeout, and unreadable-response failures remain errors', async (t) => {
  const mock = t.mock.method(globalThis, 'fetch', async () => { throw new TypeError('Network') })
  await assert.rejects(request('/health'), /Could not reach/)
  mock.mock.mockImplementation(async () => { throw new DOMException('Aborted', 'AbortError') })
  await assert.rejects(request('/health'), /did not respond in time/)
  mock.mock.mockImplementation(async () => new Response('Proxy failure', { status: 502 }))
  await assert.rejects(request('/health'), /service is unavailable/)
  mock.mock.mockImplementation(async () => new Response('Not JSON'))
  await assert.rejects(request('/health'), /unreadable response/)
})

test('chat retry preserves IDs and checks saved assistant confirmation', async (t) => {
  const { sendMessage } = await import('../src/api.js')
  const calls = []
  const mock = t.mock.method(globalThis, 'fetch', async (url, options) => {
    calls.push([url, options.method, options.body])
    assert.equal(options.timeoutMs, undefined)
    return new Response(JSON.stringify({ saved: true, conversation_id: 'c', request_id: 'r', messages: [{ role: 'assistant' }] }))
  })
  await sendMessage('c', 'r', 'Fictional question')
  await sendMessage('c', 'r', 'Fictional question')
  assert.deepEqual(calls[0], calls[1])
  mock.mock.mockImplementation(async () => new Response(JSON.stringify({ saved: true, conversation_id: 'c', request_id: 'r', messages: [] })))
  await assert.rejects(sendMessage('c', 'r', 'Fictional'), /not confirmed/)
})

test('API errors preserve stable codes for failed chat recovery', async (t) => {
  t.mock.method(globalThis, 'fetch', async () => new Response(JSON.stringify({ error: { code: 'provider_failed', message: 'Reply failed.' } }), { status: 503 }))
  await assert.rejects(request('/conversations/c'), error => error.code === 'provider_failed')
})
