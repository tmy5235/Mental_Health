<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { request, sendMessage } from '../api.js'

const emit = defineEmits(['support', 'saved'])
const text = ref('')
const messages = ref([])
const conversations = ref([])
const conversationId = ref('')
const busy = ref(false)
const loading = ref(false)
const loadError = ref('')
const sendError = ref('')
const listError = ref('')
const storageNote = ref('')
const pending = ref(null)
const health = ref(null)
const offset = ref(0)
const hasNext = ref(false)
const moreConversations = ref(false)
const budgetFallback = ref(false)
let generation = 0
let alive = true
const pendingKey = 'paced-breathing.chat-pending.v1'
const currentKey = 'paced-breathing.conversation.v1'
const modeLabel = computed(() => !health.value ? 'Chat status unavailable' : health.value.provider_mode === 'mock'
  ? 'Demo replies · no live AI' : !health.value.provider_configured ? 'Live AI not configured'
    : health.value.live_calls_reserved >= 50 ? 'Demo replies · live limit reached' : 'Live AI · OpenAI')
const date = value => new Date(value).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })
function remember() {
  try {
    localStorage.setItem(currentKey, conversationId.value)
    if (pending.value) sessionStorage.setItem(pendingKey, JSON.stringify(pending.value))
    else sessionStorage.removeItem(pendingKey)
  } catch { storageNote.value = 'This browser could not remember the chat. Saved chats remain in history.' }
}
async function refreshHealth() {
  try { const data = await request('/health'); if (alive) health.value = data }
  catch { if (alive) health.value = null }
}
async function loadConversations(more = false) {
  const start = more ? conversations.value.length : 0
  try {
    const data = await request(`/conversations?limit=21&offset=${start}`)
    if (!alive) return
    conversations.value = more ? [...conversations.value, ...data.conversations.slice(0, 20)] : data.conversations.slice(0, 20)
    moreConversations.value = data.conversations.length > 20
    listError.value = ''
  } catch { if (alive) listError.value = 'Saved chats could not be loaded.' }
}
async function load(pageOffset = null) {
  const token = ++generation
  loadError.value = ''
  if (!conversationId.value) { messages.value = []; offset.value = 0; hasNext.value = false; loading.value = false; return }
  loading.value = true
  try {
    const pageQuery = pageOffset === null ? 'latest=true' : `offset=${pageOffset}`
    const data = await request(`/conversations/${conversationId.value}?limit=50&${pageQuery}`)
    if (token !== generation || !alive) return
    messages.value = data.messages.slice(0, 50)
    offset.value = data.offset
    hasNext.value = data.offset + data.messages.length < data.total
    if (pending.value && data.messages.some(m => m.request_id === pending.value.id && m.status === 'completed')) {
      pending.value = null
      sendError.value = ''
      remember()
    }
  } catch (error) {
    if (token !== generation || !alive) return
    if (error.code === 'conversation_missing' && pending.value) messages.value = []
    else loadError.value = error.message
  } finally { if (token === generation && alive) loading.value = false }
}
function choose(id) {
  if (busy.value) return
  conversationId.value = id
  sendError.value = ''
  messages.value = []
  remember()
  void load()
}
function newChat() { choose('') }
async function send(item = null) {
  if (busy.value || (!item && !text.value.trim())) return
  if (!conversationId.value) conversationId.value = crypto.randomUUID()
  const submission = item || { id: crypto.randomUUID(), conversation: conversationId.value, content: text.value.trim() }
  pending.value = submission
  conversationId.value = submission.conversation
  remember()
  busy.value = true
  sendError.value = ''
  try {
    const data = await sendMessage(submission.conversation, submission.id, submission.content)
    if (!alive) return
    budgetFallback.value = data.budget_fallback
    pending.value = null
    text.value = ''
    remember()
    emit('saved')
    await load()
    await loadConversations()
    await refreshHealth()
  } catch (error) {
    if (!alive) return
    sendError.value = error.message
    await load()
    await loadConversations()
  } finally { if (alive) busy.value = false }
}
function retryMessage(message) {
  void send({ id: message.request_id, conversation: message.conversation_id, content: message.content })
}
function discardPending() { pending.value = null; sendError.value = ''; remember() }
onMounted(() => {
  try {
    conversationId.value = localStorage.getItem(currentKey) || ''
    const saved = JSON.parse(sessionStorage.getItem(pendingKey) || 'null')
    if (saved && typeof saved.id === 'string' && typeof saved.content === 'string' && typeof saved.conversation === 'string') {
      pending.value = saved
      conversationId.value = saved.conversation
    }
  } catch { storageNote.value = 'Browser chat memory is unavailable.' }
  void refreshHealth(); void loadConversations(); void load()
})
onBeforeUnmount(() => { alive = false; generation++ })
</script>

<template>
  <div class="chat-panel">
    <p class="mode-label">{{ modeLabel }}</p>
    <p class="small-note">Fictional messages only. Saved on this computer.<template v-if="health?.provider_mode === 'openai'"> Live chat sends your question and selected records to OpenAI.</template></p>
    <details class="saved-chats">
      <summary>Saved chats</summary>
      <p v-if="listError" role="alert">{{ listError }} <button class="text-button" @click="loadConversations()">Retry</button></p>
      <p v-else-if="!conversations.length" class="small-note">No saved chats yet.</p>
      <button v-for="chat in conversations" :key="chat.id" class="chat-link" :disabled="busy" :aria-current="conversationId === chat.id ? 'true' : undefined" @click="choose(chat.id)">{{ chat.title }}<time :datetime="chat.updated_at">{{ date(chat.updated_at) }}</time></button>
      <button v-if="moreConversations" class="text-button" @click="loadConversations(true)">Older chats</button>
    </details>
    <div class="chat-toolbar"><button class="text-button" :disabled="busy || loading" @click="newChat">New chat</button><button class="text-button" :disabled="busy || loading" @click="load(offset); refreshHealth()">Refresh chat</button></div>
    <p v-if="loading" role="status">Loading messages…</p>
    <p v-if="loadError && loadError !== sendError" role="alert" class="error-text">{{ loadError }}</p>
    <div v-if="!messages.length && !loading && !loadError" class="chat-empty">
      <p>Ask about breathing or saved activity.</p>
      <button class="suggestion" :disabled="busy || !!pending" @click="text = 'What happened in my last session?'">What happened in my last session?</button>
    </div>
    <ol class="messages" aria-label="Saved messages, oldest first">
      <li v-for="message in messages" :key="message.id" :class="['message', message.role]">
        <div class="message-label">{{ message.role === 'user' ? 'You · fictional' : message.provider_mode === 'local' ? 'App reply · fixed guidance' : message.provider_mode === 'mock' ? 'Demo reply · not live AI' : 'AI reply' }}</div>
        <p class="message-content">{{ message.content }}</p>
        <div class="message-meta"><time :datetime="message.created_at">{{ date(message.created_at) }}</time><span>Saved</span></div>
        <p v-if="message.role === 'user' && message.status !== 'completed'" class="small-note">{{ message.status === 'pending' ? 'Reply pending.' : 'Reply failed.' }}</p>
        <button v-if="message.role === 'user' && message.status === 'failed' && !pending" class="text-button" :disabled="busy" @click="retryMessage(message)">Retry reply</button>
        <details class="record-details"><summary>Record details</summary><p>Message <code>{{ message.id }}</code></p><p>Conversation <code>{{ message.conversation_id }}</code></p><p>Request <code>{{ message.request_id }}</code> · {{ message.status }}</p><p v-if="message.error_code">{{ message.error_code }}</p><p v-if="message.role === 'assistant'">{{ message.model }} · {{ message.retrieval_status === 'not_requested' ? 'Fixed app response · no retrieval' : message.retrieval_status === 'empty' ? 'No matching records' : 'History retrieved' }}</p><p v-if="message.record_ids.length">Sources: <code v-for="id in message.record_ids" :key="id">{{ id }} </code></p></details>
      </li>
    </ol>
    <div v-if="offset || hasNext" class="pagination"><button :disabled="!offset || loading || busy" @click="load(Math.max(0, offset - 50))">Earlier messages</button><button :disabled="!hasNext || loading || busy" @click="load(offset + 50)">Later messages</button></div>
    <p v-if="busy" role="status">Waiting for a reply… You can still use Breathing or Crisis support.</p>
    <p v-if="sendError" role="alert" class="error-text">{{ sendError }}</p>
    <div v-if="pending && !busy" class="pending-chat"><p>Reply not confirmed. Retry the same message.</p><p class="small-note">{{ pending.content }}</p><button class="secondary" @click="send(pending)">Retry reply</button><button class="text-button" @click="discardPending">Dismiss retry</button></div>
    <p v-if="budgetFallback" class="small-note" role="status">Live call limit reached. This reply used the demo.</p>
    <form class="chat-form" @submit.prevent="send()"><label for="chat-input">Your message</label><textarea id="chat-input" v-model="text" rows="2" maxlength="1000" :disabled="busy || !!pending" placeholder="Ask a question…"></textarea><button class="primary" :disabled="busy || !!pending || !text.trim()">{{ busy ? 'Waiting…' : 'Send' }}</button></form>
    <p class="small-note">Not therapy or crisis care. <button class="inline-button" @click="emit('support')">Crisis support</button></p>
    <p v-if="storageNote" role="status" class="small-note">{{ storageNote }}</p>
  </div>
</template>
