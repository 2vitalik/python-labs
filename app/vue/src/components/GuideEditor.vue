<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'

import { putGuidePage } from '../api.js'
import { section, sliceSection, spliceSection } from '../headings.js'
import GuideText from './GuideText.vue'

// inline editor for one section (`id` = heading id in the page's own text) or the whole page (id '');
// lands under the heading via Teleport into the slot renderMd emits, or in place for the whole page
const props = defineProps({ page: Object, id: { type: String, default: '' }, prefix: { type: String, default: '' } })
const emit = defineEmits(['saved', 'close'])
const LEAVE = 'Є незбережені зміни. Піти без збереження?'

const sec = computed(() => (props.id ? section(props.page.body, props.id) : null))
const start = props.id ? sliceSection(props.page.body, props.id) : props.page.body
const draft = ref(start)
const title = ref(props.page.title)
const note = ref('')
const error = ref('')
const busy = ref(false)
const area = ref()
const dirty = computed(() => draft.value !== start || title.value !== props.page.title)
const rows = computed(() => Math.min(Math.max(draft.value.split('\n').length + 1, 6), 40))
const to = computed(() => (props.id ? `#${props.prefix ? props.prefix + '-' : ''}${props.id}-slot` : null))

async function save() {
  if (!dirty.value || busy.value) return
  busy.value = true
  error.value = ''
  const body = props.id ? spliceSection(props.page.body, props.id, draft.value) : draft.value
  try {
    const data = { title: title.value, body, rev: props.page.rev, note: note.value, section: sec.value?.title || '' }
    emit('saved', await putGuidePage(props.page.slug, data))
  } catch (e) {
    error.value = e.message
  }
  busy.value = false
}
const cancel = () => (!dirty.value || confirm(LEAVE)) && emit('close')
function keys(e) {
  if (e.key === 'Escape') cancel()
  else if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) save()
}

onBeforeRouteLeave(() => !dirty.value || confirm(LEAVE))
const unload = (e) => dirty.value && e.preventDefault()
onMounted(() => {
  window.addEventListener('beforeunload', unload)
  area.value.setSelectionRange(0, 0)  // Chrome would put the caret, and the scroll, at the end
  area.value.focus()
})
onUnmounted(() => window.removeEventListener('beforeunload', unload))
defineExpose({ dirty })
</script>

<template>
  <Teleport :to="to || 'body'" :disabled="!to">
    <div class="editor border rounded p-2 my-2" @keydown="keys" @click.stop>
      <div class="d-flex align-items-center gap-2 small text-secondary mb-2">
        <span>✏️ {{ sec ? sec.title : 'Уся сторінка' }}</span>
        <span class="ms-auto d-none d-md-inline">⌘/Ctrl+Enter — зберегти · Esc — скасувати</span>
      </div>
      <input v-if="!id" v-model="title" class="form-control form-control-sm mb-2" placeholder="Назва сторінки">
      <div class="split">
        <textarea ref="area" v-model="draft" class="form-control font-monospace" :rows="rows" spellcheck="false"></textarea>
        <div class="preview border rounded px-3 py-2"><GuideText :text="draft" :prefix /></div>
      </div>
      <div class="d-flex flex-wrap align-items-center gap-2 mt-2">
        <input v-model="note" class="form-control form-control-sm flex-grow-1 w-auto"
               placeholder="Що змінив — рядок у чернетку «Що змінилось» (необовʼязково)">
        <button type="button" class="btn btn-primary btn-sm" :disabled="!dirty || busy" @click="save">Зберегти</button>
        <button type="button" class="btn btn-outline-secondary btn-sm" @click="cancel">Скасувати</button>
      </div>
      <div v-if="error" class="text-danger small mt-1">{{ error }}</div>
    </div>
  </Teleport>
</template>

<style scoped>
/* inside a heading's section the h2/h3 styles must not leak in; the preview is the page's own renderer */
.editor { background: var(--bs-tertiary-bg); font-size: 1rem; font-weight: 400; }
.split { display: grid; gap: .75rem; }
@media (min-width: 62rem) { .split { grid-template-columns: 1fr 1fr; } }
textarea { font-size: .85rem; line-height: 1.4; resize: vertical; }
.preview { background: var(--bs-body-bg); overflow: auto; max-height: 70vh; font-size: .9rem; }
.preview :deep(.guide > :first-child) { margin-top: 0; }
</style>
