<script setup>
import { computed, reactive, ref } from 'vue'

import { putStudentLab } from '../api.js'
import { STATES, VERDICTS, fmtWhen, fromInput, labName, toInput } from '../labs.js'
import LabReport from './LabReport.vue'

// the teacher's word on one student × one lab: 🙋 they asked, an extension (a date, «поки невідомо», none), a verdict, a note — one save;
// below, the agent's review with the full report on demand
const props = defineProps({ nick: { type: String, required: true }, lab: { type: [Number, String], required: true }, cell: { type: Object, required: true } })
const emit = defineEmits(['saved', 'close'])
const m = props.cell.mark || {}
const form = reactive({ asked: !!m.asked, asked_for: m.asked_for || '', until: toInput(m.until), open: !!m.open, reason: m.reason || '',
  met: m.met ?? null, note: m.note || '' })
const saving = ref(false)
const error = ref('')
const showReport = ref(false)
const st = computed(() => STATES[props.cell.state])
const f = computed(() => props.cell.facts)
const WORDS = [[null, 'як рахує сайт'], [true, '✅ вклався'], [false, '❌ не вклався']]

async function save() {
  saving.value = true
  error.value = ''
  try {
    emit('saved', await putStudentLab(props.nick, props.lab, { ...form, until: fromInput(form.until) }))
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}
function drop() {
  Object.assign(form, { until: '', open: false, reason: '' })
  save()
}
</script>

<template>
  <div class="edit rounded p-3">
    <div class="d-flex flex-wrap align-items-baseline gap-2 mb-2">
      <b>{{ labName(lab) }}</b> <span>{{ st.emoji }} {{ st.text }}</span>
      <span class="text-secondary small">
        <template v-if="cell.due">дедлайн {{ fmtWhen(cell.due) }}<template v-if="cell.mark?.until"> · базовий {{ fmtWhen(cell.base) }}</template></template>
        <template v-else>дедлайн не заданий</template>
        · комітів до: {{ f.before }}<template v-if="f.window !== f.before"> (у вікні {{ f.window }})</template>, після: {{ f.after }}<template v-if="f.last"> · останній до дедлайну {{ fmtWhen(f.last) }}</template>
      </span>
      <button type="button" class="btn-close btn-sm ms-auto" title="Згорнути" @click="emit('close')"></button>
    </div>
    <div class="row g-2 align-items-end">
      <div class="col-auto">
        <div class="form-check mb-1"><input id="asked" v-model="form.asked" class="form-check-input" type="checkbox"><label class="form-check-label small" for="asked">🙋 просив подовжити</label></div>
      </div>
      <div class="col-sm">
        <input v-model="form.asked_for" class="form-control form-control-sm" placeholder="на скільки, його словами: на тиждень, до 5.11…" :disabled="!form.asked">
      </div>
    </div>
    <div class="row g-2 align-items-end mt-1">
      <div class="col-sm-4 col-md-3">
        <label class="form-label small mb-0">Подовжити до</label>
        <input v-model="form.until" type="datetime-local" class="form-control form-control-sm" :disabled="form.open">
      </div>
      <div class="col-auto">
        <div class="form-check mb-1"><input id="open" v-model="form.open" class="form-check-input" type="checkbox"><label class="form-check-label small" for="open">поки невідомо</label></div>
      </div>
      <div class="col-sm">
        <label class="form-label small mb-0">Причина</label>
        <input v-model="form.reason" class="form-control form-control-sm" placeholder="хворів, поїздка…">
      </div>
      <div class="col-auto">
        <button v-if="cell.mark?.until || cell.mark?.open" type="button" class="btn btn-outline-secondary btn-sm" :disabled="saving" @click="drop">Зняти подовження</button>
      </div>
    </div>
    <div class="row g-2 align-items-end mt-1">
      <div class="col-auto">
        <div class="btn-group btn-group-sm">
          <button v-for="[v, text] in WORDS" :key="String(v)" type="button" class="btn" :class="form.met === v ? 'btn-secondary' : 'btn-outline-secondary'" @click="form.met = v">{{ text }}</button>
        </div>
      </div>
      <div class="col-sm">
        <input v-model="form.note" class="form-control form-control-sm" placeholder="нотатка для себе">
      </div>
      <div class="col-auto">
        <button type="button" class="btn btn-primary btn-sm" :disabled="saving" @click="save">Зберегти</button>
      </div>
    </div>
    <div v-if="error" class="text-danger small mt-2">{{ error }}</div>
    <div class="small mt-3">
      <template v-if="cell.review">
        🤖 звіт: <b>{{ VERDICTS[cell.review.verdict] }}</b> на зрізі <code>{{ cell.review.commit }}</code><template v-if="cell.review.head"> · HEAD — {{ VERDICTS[cell.review.head_verdict] || '?' }}</template>
        <span v-if="cell.review.stale" class="text-warning"> · зріз уже інший</span> · {{ cell.review.by }}, {{ fmtWhen(cell.review.at) }}
        <span v-if="cell.review.summary"> — {{ cell.review.summary }}</span>
        <a href="#" class="ms-2" @click.prevent="showReport = !showReport">{{ showReport ? 'сховати звіт' : 'весь звіт' }}</a>
        <LabReport v-if="showReport" :nick :lab />
      </template>
      <span v-else class="text-secondary">🤖 звіту агента ще нема — <code>bin/repos cut {{ lab }}</code>, ревʼю, <code>bin/repos reviews</code></span>
    </div>
  </div>
</template>

<style scoped>
.edit { background: var(--bs-tertiary-bg); }
</style>
