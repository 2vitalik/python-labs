<script setup>
import { computed, reactive, ref, watch } from 'vue'

import SaveCancel from '@core/components/SaveCancel.vue'

import { putLabResult } from '../api.js'
import ReviewHint from './ReviewHint.vue'

// the teacher's word on a work: the hint on top, then the points, the note, the defence taken and the stars — one PUT
// with only what changed; `dirty` — something is not saved yet
const props = defineProps({ n: Number, doc: Object })
const emit = defineEmits(['saved'])
const KEYS = ['points', 'note', 'defended', 'stars']
const DEFENDED = [['', '—'], ['record', 'записом'], ['live', 'наживо']]
const draft = reactive({})
const busy = ref(false)
const error = ref('')
const base = (k) => props.doc[k] ?? { points: null, note: '', defended: '', stars: null }[k]
const reset = () => KEYS.forEach((k) => (draft[k] = base(k)))
watch(() => props.doc, reset, { immediate: true })
const norm = (k, v) => (k === 'points' ? (v === '' || v === null ? null : Number(v)) : v)
const changed = computed(() => KEYS.filter((k) => norm(k, draft[k]) !== base(k)))
const fileStars = computed(() => props.doc.facts?.count?.stars?.[0] ?? 0)
defineExpose({ dirty: () => changed.value.length > 0 })

async function save() {
  busy.value = true
  error.value = ''
  try {
    emit('saved', await putLabResult(props.n, props.doc.vid, Object.fromEntries(changed.value.map((k) => [k, norm(k, draft[k])]))))
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <ReviewHint :grade="doc.grade" @put="draft.points = $event" />
  <div class="group-box mk-form">
    <div class="group-cap">Бали</div>
    <div class="d-flex gap-2">
      <input v-model="draft.points" type="number" min="0" max="20" class="form-control form-control-sm mk-pts" aria-label="Бали">
      <input v-model="draft.note" class="form-control form-control-sm" placeholder="нотатка" aria-label="Нотатка">
    </div>
    <div class="mk-row">
      <span class="mk-lbl">Захист прийнято</span>
      <div class="btn-group btn-group-sm">
        <button v-for="[k, t] in DEFENDED" :key="k" type="button" class="btn btn-outline-secondary" :class="{ active: draft.defended === k }"
                @click="draft.defended = k">{{ t }}</button>
      </div>
    </div>
    <div class="mk-row">
      <span class="mk-lbl">Зірочок</span>
      <div class="btn-group btn-group-sm">
        <button type="button" class="btn btn-outline-secondary" :class="{ active: draft.stars === null }" @click="draft.stars = null">з файла: {{ fileStars }}</button>
        <button v-for="k in 5" :key="k" type="button" class="btn btn-outline-secondary" :class="{ active: draft.stars === k - 1 }"
                @click="draft.stars = k - 1">{{ k - 1 }}</button>
      </div>
    </div>
    <SaveCancel class="mt-1" :class="{ invisible: !changed.length }" :disabled="busy" @save="save" @cancel="reset">
      <span v-if="error" class="small text-danger">{{ error }}</span>
    </SaveCancel>
  </div>
</template>

<style scoped>
.mk-form { display: flex; flex-direction: column; gap: .35rem; }
.mk-pts { width: 4.5rem; flex-shrink: 0; }
.mk-row { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; }
.mk-lbl { min-width: 7.5rem; color: var(--bs-secondary-color); font-size: .8rem; }
</style>
