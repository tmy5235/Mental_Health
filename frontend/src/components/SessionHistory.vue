<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { request } from '../api.js'
const sessions = ref([])
const status = ref('loading')
const error = ref('')
const offset = ref(0)
const hasNext = ref(false)
let generation = 0
async function load(nextOffset = offset.value) {
  const token = ++generation
  status.value = 'loading'
  error.value = ''
  try {
    const data = await request(`/sessions?limit=21&offset=${nextOffset}`)
    if (token !== generation) return
    if (!Array.isArray(data.sessions)) throw new Error('History could not be read.')
    sessions.value = data.sessions.slice(0, 20)
    hasNext.value = data.sessions.length > 20
    offset.value = nextOffset
    status.value = 'ready'
  } catch (failure) {
    if (token !== generation) return
    error.value = failure.message
    status.value = 'failed'
  }
}
const date = (value) => new Date(value).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })
onMounted(() => load())
onBeforeUnmount(() => generation++)
</script>

<template>
  <div class="history-toolbar"><span>Saved session records</span><button class="text-button" :disabled="status === 'loading'" @click="load()">Refresh history</button></div>
  <p v-if="status === 'loading'" role="status" class="empty-state">Loading local history…</p>
  <div v-else-if="status === 'failed'" role="alert" class="empty-state"><h2>History is unavailable</h2><p>{{ error }}</p><button class="secondary" @click="load()">Try again</button></div>
  <div v-else-if="!sessions.length" class="empty-state"><span class="empty-symbol" aria-hidden="true">◷</span><h2>No sessions saved yet</h2><p>A completed or stopped practice will appear here after its save is confirmed.</p></div>
  <div v-else class="history-table-wrap"><table><caption class="sr-only">Fictional paced-breathing sessions, newest first</caption><thead><tr><th scope="col">Session</th><th scope="col">Active time</th><th scope="col">Outcome</th><th scope="col">Final display</th></tr></thead><tbody><tr v-for="item in sessions" :key="item.id"><th scope="row"><time :datetime="item.started_at">{{ date(item.started_at) }}</time><details><summary>Record details</summary><code>{{ item.id }}</code><span class="record-meta">{{ item.cycles_completed }} of 6 cycles · Fictional record</span></details></th><td>{{ item.active_duration_seconds.toFixed(1) }}s</td><td><span class="outcome-pill">{{ item.status === 'completed' ? 'Completed' : 'Stopped' }}</span></td><td>{{ item.display_mode === 'text' ? 'Text' : 'Circle' }}</td></tr></tbody></table></div>
  <div v-if="status === 'ready' && (offset > 0 || hasNext)" class="pagination"><button class="secondary" :disabled="offset === 0" @click="load(Math.max(0, offset - 20))">Newer</button><span>Page {{ offset / 20 + 1 }}</span><button class="secondary" :disabled="!hasNext" @click="load(offset + 20)">Older</button></div>
</template>
