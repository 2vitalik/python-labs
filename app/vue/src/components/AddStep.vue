<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { postClaim, putPart } from '../api.js'
import { whyOk } from '../asked.js'
import { iconOf, kindOf, missingParams } from '../catalog.js'
import { useEd } from '../ed.js'
import { jump } from '@core/jump.js'
import SlotFields from './SlotFields.vue'
import WhyField from './WhyField.vue'

// the second step of «＋ Додати» for what must belong to someone: a mechanic — to an entity, an element — to a window,
// a parameter — to an entity with its value; and for a card «за запитом» (T319) — its sentence: `why` a string, null — not
// asked (a rule card then opens the rule's form, which claims it). `step` = { task, part, params, why } or { stat, part, value }
const props = defineProps({ step: Object })
const emit = defineEmits(['done'])
const ed = useEd()
const error = ref('')
const s = computed(() => props.step)
const kind = computed(() => s.value.task && kindOf(s.value.task))
const element = computed(() => kind.value === 'element')
const hosted = computed(() => element.value || kind.value === 'mechanic')
const hosts = computed(() => (element.value ? ed.windows : ed.entities))
const asks = computed(() => s.value.why != null)
const ready = computed(() => (s.value.stat ? s.value.part && String(s.value.value).trim()
  : (!s.value.part || !missingParams(s.value.task, s.value.params).length) && (!asks.value || whyOk(s.value.why))))

async function send() {
  error.value = ''
  try {
    if (s.value.task) {
      const why = asks.value ? s.value.why.trim() : ''
      if (kind.value === 'rule') {
        ed.open('rule', { ...s.value.task.rule, card: s.value.task.slug, why })
        return emit('done')
      }
      const part = kind.value === 'field' ? ed.field?.id || '' : s.value.part
      const c = await postClaim({ task: s.value.task.slug, part, params: s.value.params, why })
      jump(`c-${c.id}`)
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
    <span v-if="s.task"><b>{{ s.task.title }}</b><template v-if="hosted"> — {{ element ? 'на яке вікно?' : 'чия це механіка?' }}</template></span>
    <span v-else>Параметр <b>{{ s.stat.icon }} {{ s.stat.label }}</b> — кому?</span>
    <template v-if="hosted || s.stat">
      <div class="d-flex flex-wrap gap-1">
        <button v-for="p in hosts" :key="p.id" type="button" class="btn btn-sm chip" :class="s.part === p.id ? 'btn-secondary' : 'btn-outline-secondary'" @click="s.part = p.id">
          {{ iconOf(p) }} {{ p.title }}
        </button>
        <button v-if="s.task" type="button" class="btn btn-sm chip" :class="s.part === '' ? 'btn-secondary' : 'btn-outline-secondary'" @click="s.part = ''">📥 поки в чернетки</button>
      </div>
      <span v-if="!hosts.length" class="text-secondary">({{ element ? 'вікон' : 'сутностей' }} ще нема{{ s.task ? ' — ляже в чернетки, привʼяжеш потім' : ': спершу додай сутність' }})</span>
    </template>
    <SlotFields v-if="s.task?.slots?.length && kind !== 'rule'" :specs="s.task.slots" :params="s.params" />
    <template v-if="s.stat">
      <input v-model="s.value" class="form-control form-control-sm value" placeholder="значення" @keydown.enter="ready && send()">
      <span v-if="s.stat.unit" class="text-secondary">{{ s.stat.unit }}</span>
    </template>
    <WhyField v-if="asks" v-model="s.why" class="w-100" />
    <button type="button" class="btn btn-sm btn-add" :disabled="!ready" @click="send"><Icon name="plus" /> {{ kind === 'rule' ? 'Далі — правило' : 'Додати' }}</button>
    <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('done')">Скасувати</button>
    <span v-if="error" class="text-danger w-100">{{ error }}</span>
  </div>
</template>

<style scoped>
.step { background: var(--bs-tertiary-bg); }
.value { width: 6rem; }
</style>
