<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { postClaim, putPart } from '../api.js'
import { iconOf, kindOf, missingParams } from '../catalog.js'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import SlotFields from './SlotFields.vue'

// the second step of «＋ Додати» for what must belong to someone: a mechanic — to an entity, an element — to a window,
// a parameter — to an entity with its value. `step` = { task, part, params } or { stat, part, value }
const props = defineProps({ step: Object })
const emit = defineEmits(['done'])
const ed = useEd()
const error = ref('')
const s = computed(() => props.step)
const element = computed(() => s.value.task && kindOf(s.value.task) === 'element')
const hosts = computed(() => (element.value ? ed.windows : ed.entities))
const ready = computed(() => (s.value.stat ? s.value.part && String(s.value.value).trim() : !s.value.part || !missingParams(s.value.task, s.value.params).length))

async function send() {
  error.value = ''
  try {
    if (s.value.task) {
      const c = await postClaim({ task: s.value.task.slug, part: s.value.part, params: s.value.params })
      jump(s.value.part ? `c-${c.id}` : 'drafts')
    } else {
      const p = ed.entities.find((e) => e.id === s.value.part), st = s.value.stat
      const stats = [...p.stats, { key: st.key, label: st.label, value: String(s.value.value).trim(), unit: st.unit }]
      await putPart(p.id, { title: p.title, icon: p.icon, role: p.role, description: p.description, stats, states: p.states, order: p.order })
      jump(`p-${p.id}`)
    }
    ed.changed()
    emit('done')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="border rounded p-2 d-flex flex-wrap gap-2 align-items-center small step">
    <span v-if="s.task"><b>{{ s.task.title }}</b> — {{ element ? 'на яке вікно?' : 'чия це механіка?' }}</span>
    <span v-else>Параметр <b>{{ s.stat.icon }} {{ s.stat.label }}</b> — кому?</span>
    <div class="d-flex flex-wrap gap-1">
      <button v-for="p in hosts" :key="p.id" type="button" class="btn btn-sm chip" :class="s.part === p.id ? 'btn-secondary' : 'btn-outline-secondary'" @click="s.part = p.id">
        {{ iconOf(p) }} {{ p.title }}
      </button>
      <button v-if="s.task" type="button" class="btn btn-sm chip" :class="s.part === '' ? 'btn-secondary' : 'btn-outline-secondary'" @click="s.part = ''">📥 поки в чернетки</button>
    </div>
    <span v-if="!hosts.length" class="text-secondary">({{ element ? 'вікон' : 'сутностей' }} ще нема{{ s.task ? ' — ляже в чернетки, привʼяжеш потім' : ': спершу додай сутність' }})</span>
    <SlotFields v-if="s.task?.slots?.length" :specs="s.task.slots" :params="s.params" />
    <template v-if="s.stat">
      <input v-model="s.value" class="form-control form-control-sm value" placeholder="значення" @keydown.enter="ready && send()">
      <span v-if="s.stat.unit" class="text-secondary">{{ s.stat.unit }}</span>
    </template>
    <button type="button" class="btn btn-sm btn-add" :disabled="!ready" @click="send"><Icon name="plus" /> Додати</button>
    <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('done')">Скасувати</button>
    <span v-if="error" class="text-danger w-100">{{ error }}</span>
  </div>
</template>

<style scoped>
.step { background: var(--bs-tertiary-bg); }
.value { width: 6rem; }
</style>
