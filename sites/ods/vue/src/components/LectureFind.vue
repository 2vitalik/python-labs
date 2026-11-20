<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import Icon from '@core/components/Icon.vue'

import '../lectureFind.css'
import { hitLink, kept, sectionsOf } from '../lectureFindKinds.js'
import { find, loadTexts } from '../lectureSearch.js'
import LectureHits from './LectureHits.vue'
import LectureKinds from './LectureKinds.vue'

// search over the texts of all lectures (lectureSearch.js): they come on the first keystroke, then every query is local.
// The pills narrow to one kind of match; ↓ ↑ walk the results, Enter opens one, Esc clears, «/» on the page comes here
const NONE = { hits: [], counts: {}, fixed: null }
const router = useRouter()
const input = ref()
const q = ref(kept.q)
const term = computed(() => q.value.trim())
const state = ref('')  // '' → loading → ready · failed
const kind = ref(kept.kind)  // '' — every kind
const res = computed(() => (state.value === 'ready' && term.value.length >= 2 ? find(term.value) : NONE))
const sections = computed(() => sectionsOf(res.value.hits.filter((h) => !kind.value || h.kind === kind.value)))
const rows = computed(() => sections.value.flatMap((s) => s.groups.flatMap((g) => g.rows)))
const active = ref(-1)
watch([term, kind], () => {
  active.value = -1
  Object.assign(kept, { q: q.value, kind: kind.value })
})
watch(() => res.value.counts, (c) => kind.value && !c[kind.value] && (kind.value = ''))  // the narrowed kind has gone

watch(q, async () => {
  if (['loading', 'ready'].includes(state.value) || !term.value) return  // after a failure the next keystroke tries again
  state.value = 'loading'
  try {
    await loadTexts()
    state.value = 'ready'
  } catch {
    state.value = 'failed'
  }
}, { immediate: true })

function keys(e) {
  const n = rows.value.length
  if (['ArrowDown', 'ArrowUp'].includes(e.key) && n) {
    e.preventDefault()
    active.value = e.key === 'ArrowDown' ? (active.value + 1) % n : (active.value <= 0 ? n : active.value) - 1
  } else if (e.key === 'Enter' && n) router.push(hitLink(rows.value[Math.max(0, active.value)]))
  else if (e.key === 'Escape') q.value ? (q.value = '') : input.value.blur()
}
// «/» (its key on any layout: «.» on the Ukrainian one) — unless the reader is typing somewhere
function slash(e) {
  if (!(e.key === '/' || e.code === 'Slash') || e.ctrlKey || e.metaKey || e.altKey) return
  if (e.target.closest?.('input, textarea, select, [contenteditable]')) return
  e.preventDefault()
  input.value.focus()
}
onMounted(() => document.addEventListener('keydown', slash))
onUnmounted(() => document.removeEventListener('keydown', slash))
</script>

<template>
  <div class="find mb-4">
    <div class="position-relative">
      <Icon name="search" class="glass text-secondary" />
      <input ref="input" v-model="q" type="search" class="form-control" placeholder="Пошук у лекціях…" aria-label="Пошук у лекціях"
             @keydown="keys">
      <kbd class="slash" title="Клавіша «/» ставить курсор сюди">/</kbd>
    </div>
    <div v-if="term.length >= 2" class="mt-2">
      <div v-if="state === 'loading'" class="small text-body-tertiary">шукаю…</div>
      <div v-else-if="state === 'failed'" class="small text-danger">Не вдалося завантажити лекції</div>
      <template v-else-if="state === 'ready'">
        <div v-if="res.fixed" class="fixed small">Показано для „<b>{{ res.fixed }}</b>“ · шукали „{{ term }}“</div>
        <LectureKinds v-model="kind" :counts="res.counts" />
        <div v-if="!rows.length" class="none small text-secondary">Нічого не знайдено</div>
        <LectureHits v-else :sections :counts="res.counts" :active />
        <div v-if="rows.length" class="keys small text-body-tertiary">↓ ↑ — вибрати · Enter — відкрити · Esc — очистити</div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.glass { position: absolute; left: .75rem; top: 50%; transform: translateY(-50%); pointer-events: none; }
input { padding-left: 2.25rem; padding-right: 2.25rem; }
/* the key's hint while the box is empty and not in use; a phone has no «/» to press */
.slash { position: absolute; right: .6rem; top: 50%; transform: translateY(-50%); pointer-events: none; padding: 0 .4rem;
         font-size: .75rem; color: var(--bs-tertiary-color); background: none; border: 1px solid var(--bs-border-color); }
input:focus ~ .slash, input:not(:placeholder-shown) ~ .slash { display: none; }
.fixed { color: var(--bs-secondary-color); }
.fixed b { color: var(--bs-body-color); }
.keys { margin-top: .5rem; }
@media (hover: none) { .keys, .slash { display: none; } }
</style>
