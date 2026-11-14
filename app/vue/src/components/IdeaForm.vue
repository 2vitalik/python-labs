<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import Icon from '@core/components/Icon.vue'
import { postRef, putRef } from '../api.js'
import { taskIndex } from '../catalog.js'
import { KINDS, refKind, zonePath } from '../ideas.js'
import ZonePick from './ZonePick.vue'

// one form for every record of /ideas (T274 §4): what came as a prop is not asked but shown as «про що»;
// `parent` — an idea under that find; `edit` — an existing record, saved in place; `note` — the text a new one starts with
const props = defineProps({ kind: String, zone: String, subzone: String, task: String, parent: String, compact: Boolean, edit: Object, note: String })
const emit = defineEmits(['done', 'cancel'])
const e = props.edit || {}
const form = reactive({ kind: props.kind || (props.edit ? refKind(e) : 'link'), title: e.title || '', note: e.note || props.note || '',
                        url: e.url || '', zone: e.zone || '', subzone: e.subzone || '' })
const task = props.task || e.task || ''
const card = computed(() => taskIndex.value[task])
const fixed = computed(() => (props.zone ? [props.zone, props.subzone || ''] : card.value ? [card.value.zone, card.value.subzone] : null))
const about = computed(() => [fixed.value && zonePath(...fixed.value), task && `«${card.value?.title || task}»`].filter(Boolean).join(' · '))
const hint = computed(() => KINDS[form.kind])
const ready = computed(() => (form.kind === 'link' ? form.url.trim() : form.title.trim() || form.note.trim()))
const fc = computed(() => ['form-control', { 'form-control-sm': props.compact }])
const root = ref()
const busy = ref(false)
const sent = ref(false)
const error = ref('')
onMounted(() => root.value.querySelector('input, textarea')?.focus())

async function send() {
  if (!ready.value || busy.value) return
  const [zone, subzone] = fixed.value || (form.kind === 'site' ? ['', ''] : [form.zone, form.subzone])
  const data = { kind: form.kind, url: form.url.trim(), title: form.title.trim(), note: form.note.trim(), zone, subzone, task,
                 parent: props.parent || e.parent || '' }
  error.value = ''
  busy.value = true
  try {
    const r = props.edit ? await putRef(e.id, data) : await postRef(data)
    if (props.edit) return emit('done', r)
    sent.value = true
    setTimeout(() => emit('done', r), 1000)
  } catch (err) {
    error.value = err.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div ref="root" class="vstack gap-2" @keydown.enter="(ev) => (ev.metaKey || ev.ctrlKey) && send()">
    <div v-if="sent" class="text-success">Надіслано ✓ — дякую</div>
    <template v-else>
      <div v-if="!kind" class="d-flex flex-wrap gap-1">
        <button v-for="(m, k) in KINDS" :key="k" type="button" class="btn btn-sm chip"
                :class="form.kind === k ? 'btn-secondary' : 'btn-outline-secondary'" @click="form.kind = k">{{ m.icon }} {{ m.one }}</button>
      </div>
      <div v-if="about" class="about">про що: {{ about }}</div>
      <input v-if="form.kind === 'link'" v-model="form.url" :class="fc" inputmode="url" placeholder="https://… — посилання">
      <input v-model="form.title" :class="fc" :placeholder="hint.title">
      <GrowArea v-model="form.note" :class="fc" :placeholder="hint.note" />
      <input v-if="form.kind !== 'link'" v-model="form.url" :class="fc" inputmode="url" placeholder="посилання — за бажанням">
      <ZonePick v-if="!fixed && form.kind !== 'site'" v-model:zone="form.zone" v-model:subzone="form.subzone" :small="compact" />
      <div class="d-flex gap-2">
        <button v-if="edit" type="button" class="btn btn-sm btn-success" :disabled="!ready || busy" title="⌘/Ctrl+Enter" @click="send">
          <Icon name="check" /> Зберегти</button>
        <button v-else type="button" class="btn btn-sm btn-add" :disabled="!ready || busy" title="⌘/Ctrl+Enter" @click="send">
          <Icon name="plus" /> Надіслати</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
      </div>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </template>
  </div>
</template>

<style scoped>
.about { font-size: .8rem; color: var(--bs-secondary-color); }
</style>
