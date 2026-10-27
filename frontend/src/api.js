export async function request(path, options = {}) {
  const { timeoutMs = 5000, ...fetchOptions } = options
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), timeoutMs)
  try {
    const response = await fetch(`/api${path}`, {
      ...fetchOptions,
      headers: { 'Content-Type': 'application/json', ...options.headers },
      signal: controller.signal,
    })
    let data
    try {
      data = await response.json()
    } catch {
      throw new Error(response.ok
        ? 'The local service returned an unreadable response.'
        : 'The local service is unavailable.')
    }
    if (!response.ok) {
      const error = new Error(data.error?.message || 'The local service is unavailable.')
      error.code = data.error?.code
      throw error
    }
    return data
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('The local service did not respond in time.')
    if (error instanceof TypeError) throw new Error('Could not reach the local service.')
    throw error
  } finally {
    clearTimeout(timeout)
  }
}

export async function sendMessage(conversationId, requestId, content) {
  const data = await request(`/conversations/${encodeURIComponent(conversationId)}/messages/${encodeURIComponent(requestId)}`, {
    method: 'PUT', body: JSON.stringify({ content }), timeoutMs: 50000,
  })
  if (data.saved !== true || data.request_id !== requestId || data.conversation_id !== conversationId
      || !data.messages?.some(message => message.role === 'assistant')) {
    throw new Error('The reply save was not confirmed. Refresh chat before retrying.')
  }
  return data
}

export async function saveSession(id, payload) {
  const response = await request(`/sessions/${encodeURIComponent(id)}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
  if (response.saved !== true || response.session?.id !== id) {
    throw new Error('The service did not confirm this session was saved.')
  }
  return response.session
}
