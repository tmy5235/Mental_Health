<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { request, saveSession } from './api.js'
import { BreathingClock } from './breathing.js'
import SessionHistory from './components/SessionHistory.vue'
import ChatPanel from './components/ChatPanel.vue'
import './style.css'

const view = ref('home')
const connection = ref('Checking session storage…')
const connected = ref(false)
const storageWarning = ref('')
const preferenceKey = 'paced-breathing.preferences.v1'
const outboxKey = 'paced-breathing.outbox.v1'
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
const preferences = ref({ mode: 'text', simple: true, font_size: 'standard' })
const preferenceStatus = ref('Saved on this browser; checking local database…')
let preferenceRevision = 0
let savingPreferences = false
let preferenceDirty = false
const chatOpened = ref(false)
const outbox = ref([])
try {
  const saved = JSON.parse(localStorage.getItem(preferenceKey) || 'null')
  if (saved && ['text', 'motion'].includes(saved.mode) && typeof saved.simple === 'boolean') {
    preferences.value = { ...preferences.value, ...saved }
    if (reducedMotion) preferences.value.mode = 'text'
  }
  const pending = JSON.parse(sessionStorage.getItem(outboxKey) || '[]')
  if (!Array.isArray(pending) || pending.some(item => !item.id || !item.payload)) {
    throw new Error('Invalid pending session data')
  }
  outbox.value = pending.map(item => ({ ...item, state: 'pending', error: '' }))
} catch {
  storageWarning.value = 'Browser storage could not be read. Settings and unsent sessions may not survive refresh.'
}

const clock = new BreathingClock()
const snapshot = ref(clock.snapshot())
const session = ref(null)
const result = ref(null)
const heading = ref(null)
const settingsSummary = ref(null)
const supportDialog = ref(null)
const supportButton = ref(null)
let interval = null
const busy = new Set()
const currentSave = computed(() => result.value?.state || '')
const expansionStyle = computed(() => ({ transform: `scale(${0.68 + snapshot.value.expansion * 0.32})` }))
const remaining = computed(() => Math.ceil((60_000 - snapshot.value.activeMs) / 1_000))

function focusHeading() {
  nextTick(() => { heading.value?.focus({ preventScroll: true }); window.scrollTo(0, 0) })
}
function navigate(target) {
  if (target === 'chat') chatOpened.value = true
  view.value = target
  if (target !== 'result') void checkConnection()
  focusHeading()
}
function storePreferences() {
  preferenceRevision++
  preferenceDirty = true
  try { localStorage.setItem(preferenceKey, JSON.stringify(preferences.value)) }
  catch { storageWarning.value = 'Your display choice works now, but could not be remembered on this browser.' }
  void savePreferences()
}
async function savePreferences() {
  if (savingPreferences) return
  savingPreferences = true
  while (preferenceDirty) {
    preferenceDirty = false
    preferenceStatus.value = 'Saving display choice…'
    try {
      await request('/preferences', { method: 'PUT', body: JSON.stringify(preferences.value) })
      preferenceStatus.value = 'Display choices saved on this computer.'
    } catch { preferenceStatus.value = 'Database save failed. Your current display still works.' }
  }
  savingPreferences = false
}
async function loadPreferences() {
  const revision = preferenceRevision
  try {
    const data = await request('/preferences')
    if (preferenceRevision !== revision) return
    if (data.saved) {
      preferences.value = data.preferences
      if (reducedMotion) preferences.value.mode = 'text'
    }
    preferenceStatus.value = data.saved ? 'Display choices saved on this computer.' : 'Choices are saved when you change them.'
  } catch { preferenceStatus.value = 'Database unavailable. Browser display choices still work.' }
}
function setMode(mode) {
  preferences.value.mode = mode
  storePreferences()
}
function onSettingsToggle(event) {
  const simple = !event.target.open
  if (preferences.value.simple !== simple) {
    preferences.value.simple = simple
    storePreferences()
  }
}
function resetPreferences() {
  preferences.value = { mode: 'text', simple: true, font_size: 'standard' }
  storePreferences()
  nextTick(() => settingsSummary.value?.focus({ preventScroll: true }))
}
function collapseSettings() {
  preferences.value.simple = true
  storePreferences()
  nextTick(() => settingsSummary.value?.focus({ preventScroll: true }))
}
function persistOutbox() {
  try {
    sessionStorage.setItem(outboxKey, JSON.stringify(outbox.value.map(({ id, payload }) => ({ id, payload }))))
  } catch {
    storageWarning.value = 'Unconfirmed saves are held only in memory. Keep this page open to retry them.'
  }
}
async function checkConnection() {
  try {
    const health = await request('/health')
    connected.value = health.storage_available === true
    connection.value = connected.value ? 'Local storage connected' : 'Session storage unavailable'
  } catch {
    connected.value = false
    connection.value = 'Session storage unavailable · exercise still works'
  }
}
function clearTimer() {
  clearInterval(interval)
  interval = null
}
function tick() {
  snapshot.value = clock.snapshot()
  if (snapshot.value.state === 'completed') finish()
}
function start() {
  clearTimer()
  result.value = null
  session.value = { id: crypto.randomUUID(), startedAt: Date.now() }
  snapshot.value = clock.start()
  view.value = 'exercise'
  focusHeading()
  interval = setInterval(tick, 50)
}
function pause() {
  snapshot.value = clock.pause()
  clearTimer()
  if (snapshot.value.state === 'completed') finish()
}
function resume() {
  if (supportDialog.value?.open || document.hidden) return
  snapshot.value = clock.resume()
  if (snapshot.value.state === 'running') {
    clearTimer()
    interval = setInterval(tick, 50)
  }
}
function stop() {
  snapshot.value = clock.stop()
  finish()
}
function finish() {
  if (view.value !== 'exercise') return
  clearTimer()
  const item = {
    id: session.value.id,
    payload: clock.outcome(session.value.startedAt, preferences.value.mode),
    state: 'pending', error: '',
  }
  outbox.value.push(item)
  result.value = outbox.value.at(-1)
  persistOutbox()
  navigate('result')
  void submit(result.value)
}
async function submit(item) {
  if (busy.has(item.id)) return
  busy.add(item.id)
  item.state = 'saving'
  item.error = ''
  try {
    await saveSession(item.id, item.payload)
    item.state = 'saved'
    outbox.value = outbox.value.filter(candidate => candidate.id !== item.id)
    connected.value = true
    connection.value = 'Local storage connected'
    persistOutbox()
  } catch (error) {
    item.state = 'failed'
    item.error = error.message
    connected.value = false
    connection.value = 'Latest session save not confirmed'
  } finally {
    busy.delete(item.id)
  }
}
function openSupport() {
  if (view.value === 'exercise') pause()
  supportDialog.value.showModal()
}
function closeSupport() {
  supportDialog.value.close()
}
function restoreSupportFocus() {
  supportButton.value?.focus()
}
function onVisibility() {
  if (document.hidden && view.value === 'exercise') pause()
}
onMounted(() => {
  void checkConnection()
  void loadPreferences()
  document.addEventListener('visibilitychange', onVisibility)
})
onBeforeUnmount(() => {
  clearTimer()
  document.removeEventListener('visibilitychange', onVisibility)
})
</script>

<template>
  <div class="app-shell" :class="{ 'large-text': preferences.font_size === 'large' }">
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="header">
      <div class="brand"><svg class="brand-icon" viewBox="0 0 40 40" fill="none" aria-hidden="true" focusable="false"><path d="M5 14h20c7 0 7-9 1-9-3 0-4 2-4 3M5 20h28M5 26h15c8 0 8 9 2 9-3 0-4-2-4-3" /></svg><span>Breathing Room</span></div>
      <button ref="supportButton" class="support-button" @click="openSupport"><svg class="help-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9" /><path d="M12 8v8M8 12h8" /></svg>Crisis support</button>
    </header>
    <nav v-if="view !== 'exercise'" class="main-nav" aria-label="Main navigation">
      <button :aria-current="view === 'home' || view === 'result' ? 'page' : undefined" @click="navigate('home')">Breathe</button>
      <button :aria-current="view === 'chat' ? 'page' : undefined" @click="navigate('chat')">Chat</button>
      <button :aria-current="view === 'history' ? 'page' : undefined" @click="navigate('history')">History</button>
    </nav>
    <main id="main-content" tabindex="-1">
      <section v-if="view === 'home'" class="home-section" aria-labelledby="home-title">
        <div class="practice-mark" aria-hidden="true"><span></span></div>
        <p class="eyebrow">One minute, at your pace</p>
        <h1 id="home-title" ref="heading" tabindex="-1">A moment to breathe.</h1>
        <p class="lead">Four counts in. Six counts out.</p>
        <p class="home-note">Six cycles. Pause or stop anytime.</p>
        <button class="primary start-button" @click="start">Start breathing <span aria-hidden="true">→</span></button>
        <p class="small-note refresh-note">Stop or finish to save. Refresh leaves without saving.</p>
        <details class="display-settings" :open="!preferences.simple" @toggle="onSettingsToggle">
          <summary ref="settingsSummary">Display settings</summary>
          <div class="settings-content">
            <div class="setting-row"><span>Pacing</span><div class="display-controls" role="group" aria-label="Pacing display"><button :aria-pressed="preferences.mode === 'text'" @click="setMode('text')">Still text</button><button :aria-pressed="preferences.mode === 'motion'" @click="setMode('motion')">Moving circle</button></div></div>
            <div class="setting-row"><span>Text size</span><div class="display-controls" role="group" aria-label="Text size"><button :aria-pressed="preferences.font_size === 'standard'" @click="preferences.font_size = 'standard'; storePreferences()">Standard</button><button :aria-pressed="preferences.font_size === 'large'" @click="preferences.font_size = 'large'; storePreferences()">Larger</button></div></div>
            <p class="small-note" role="status">{{ preferenceStatus }}</p>
            <div><button class="text-button" @click="resetPreferences">Reset display</button><button class="text-button" @click="collapseSettings">Show fewer options</button><button v-if="preferenceStatus.includes('failed')" class="text-button" @click="storePreferences">Retry save</button></div>
          </div>
        </details>
      </section>

      <section v-if="view === 'exercise'" class="exercise-card" aria-labelledby="exercise-title">
        <div class="exercise-top"><span>Cycle {{ snapshot.cycle }} / 6</span><span>{{ remaining }}s left</span></div>
        <h1 id="exercise-title" ref="heading" tabindex="-1" class="phase-title" aria-live="polite">{{ snapshot.phase }}</h1>
        <div class="pacing-area" :class="{ 'text-mode': preferences.mode === 'text' }">
          <div v-if="preferences.mode === 'motion'" class="pacing-orbit" aria-hidden="true"><div class="pacing-circle" :style="expansionStyle"></div></div>
          <div class="count"><span>{{ snapshot.count }}</span></div>
        </div>
        <p class="pause-message" role="status">{{ snapshot.state === 'paused' ? 'Paused. Take your time.' : 'You can stop anytime.' }}</p>
        <div class="exercise-actions"><button class="primary" @click="snapshot.state === 'running' ? pause() : resume()">{{ snapshot.state === 'running' ? 'Pause' : 'Resume' }}</button><button class="secondary" @click="stop">Stop</button></div>
        <button class="text-button mode-toggle" @click="setMode(preferences.mode === 'motion' ? 'text' : 'motion')">{{ preferences.mode === 'motion' ? 'Use still text' : 'Use moving circle' }}</button>
      </section>

      <section v-if="view === 'result' && result" class="result-card" aria-labelledby="result-title">
        <p class="eyebrow">Your session</p><h1 id="result-title" ref="heading" tabindex="-1">{{ result.payload.status === 'completed' ? 'Finished.' : 'Stopped.' }}</h1>
        <p class="lead">{{ result.payload.active_duration_seconds.toFixed(1) }} seconds · {{ result.payload.cycles_completed }} / 6 cycles</p>
        <p class="save-status" role="status">{{ currentSave === 'saved' ? 'Saved on this computer.' : currentSave === 'saving' ? 'Saving… You can leave this screen.' : 'Save not confirmed.' }}</p>
        <p v-if="result.error" class="error-text">{{ result.error }}</p>
        <button v-if="['failed', 'pending'].includes(currentSave)" class="secondary" @click="submit(result)">Retry save</button>
        <div class="result-actions"><button class="primary" @click="navigate('home')">Back to breathing</button><button class="text-button" @click="navigate('history')">View history</button></div>
      </section>

      <section v-if="view === 'history'" aria-labelledby="history-title" class="history-section">
        <p class="eyebrow">Saved on this computer</p><h1 id="history-title" ref="heading" tabindex="-1">Your sessions</h1>
        <p class="history-intro">Fictional activity. These records do not measure how you feel.</p>
        <SessionHistory />
      </section>
      <section v-if="chatOpened" v-show="view === 'chat'" aria-labelledby="chat-title" class="chat-section">
        <h1 id="chat-title" :ref="el => { if (view === 'chat') heading = el }" tabindex="-1">A little guidance.</h1>
        <ChatPanel @support="openSupport" @saved="checkConnection" />
      </section>
      <aside v-if="outbox.length && view !== 'exercise' && view !== 'result'" class="pending-panel" aria-label="Unconfirmed session saves">
        <h2>{{ outbox.length }} unsaved {{ outbox.length === 1 ? 'session' : 'sessions' }}</h2><p class="small-note">Retry before closing this tab.</p>
        <div v-for="item in outbox" :key="item.id" class="pending-row"><span>{{ item.payload.status }} · {{ item.payload.active_duration_seconds }}s <span v-if="item.error">— {{ item.error }}</span></span><button class="secondary" :disabled="item.state === 'saving'" @click="submit(item)">{{ item.state === 'saving' ? 'Saving…' : 'Retry save' }}</button></div>
      </aside>
      <p v-if="storageWarning" role="alert" class="error-text">{{ storageWarning }}</p>
    </main>
    <footer class="footer"><p>Coursework prototype · Fictional use only</p><p>Not therapy. No one is monitoring this app.</p><p v-if="!connected" class="small-note" role="status">{{ connection }}</p></footer>
    <dialog ref="supportDialog" class="support-dialog" aria-labelledby="support-title" @close="restoreSupportFocus">
      <div class="dialog-inner"><p class="eyebrow">EXTERNAL SUPPORT</p><h2 id="support-title">Crisis support</h2><p class="lead">United States and territories</p><p>The 988 Suicide &amp; Crisis Lifeline offers support for suicidal crisis or emotional distress.</p>
        <div class="support-links"><a href="tel:988?oai_link_source=model_response_hotline">988</a><span>Call</span><a href="sms:988?oai_link_source=model_response_hotline">988</a><span>Text</span><a href="https://988lifeline.org/chat/?oai_link_source=model_response_hotline" target="_blank" rel="noopener noreferrer">https://988lifeline.org/chat/</a><span>Online chat</span></div>
        <p class="small-note">Links open external services. This app is not monitored. These resources are for the U.S.; service availability elsewhere differs.</p><p class="small-note"><a href="https://988lifeline.org?oai_link_source=model_response_hotline" target="_blank" rel="noopener noreferrer">https://988lifeline.org</a> · Verified November 2, 2026.</p>
        <p v-if="view === 'exercise'" class="pause-message">The exercise is paused. Returning will not resume it.</p>
        <div class="dialog-actions"><button class="primary" autofocus @click="closeSupport">Return to app</button><button v-if="view === 'exercise'" class="secondary" @click="stop">Stop exercise</button></div>
      </div>
    </dialog>
  </div>
</template>
