<script setup>
import { computed, reactive, ref } from 'vue'

import TagInput from '@core/components/TagInput.vue'
import { deletePart, postClaim, postPart, putPart } from '../api.js'
import { vocab } from '../catalog.js'
import CardPicker from './CardPicker.vue'
import ClaimChip from './ClaimChip.vue'
import ShotStrip from './ShotStrip.vue'

// the field — one per game: its properties as a row of chips, the render / camera cards claimed on it, a screenshot
const props = defineProps({ part: Object, claims: Array, info: Function, parts: Array, editable: Boolean, judge: Boolean, nick: String })
const emit = defineEmits(['changed'])
const edit = ref(false)
const error = ref('')
const form = reactive({ props: {}, description: '' })
const specs = computed(() => vocab.value.field)
const chips = computed(() => specs.value.flatMap((s) => {
  const v = props.part?.props?.[s.key]
  if (v === undefined || v === '' || v === false || (Array.isArray(v) && !v.length)) return []
  if (s.type === 'bool') return [s.label.split(' (')[0]]
  if (s.type === 'choice') return [s.options[v] || v]
  if (s.type === 'tags') return [`шари: ${v.join(' · ')}`]
  return [v]
}))

async function run(fn) {
  error.value = ''
  try {
    await fn()
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
function start() {
  form.props = { ...(props.part?.props || {}) }
  form.description = props.part?.description || ''
  edit.value = true
}
const save = () => run(async () => {
  if (props.part) await putPart(props.part.id, { title: 'Поле', ...form })
  else await postPart({ kind: 'field', title: 'Поле', ...form })
  edit.value = false
})
const remove = () => run(() => deletePart(props.part.id))
const addClaim = (task, params) => run(() => postClaim({ task, part: props.part.id, params }))
</script>

<template>
  <div class="card">
    <div class="card-body p-2 vstack gap-2">
      <div v-if="!edit" class="d-flex flex-wrap align-items-center gap-1">
        <span class="me-1">🗺️</span>
        <template v-if="chips.length">
          <span v-for="c in chips" :key="c" class="badge rounded-pill text-bg-light border fw-normal text-body">{{ c }}</span>
        </template>
        <span v-else class="text-secondary small">{{ part ? 'Поле без властивостей — додай розмір, сітку, час' : 'Поле ще не описане: розмір, сітка, тор, час, керування, шари клітини' }}</span>
        <template v-if="editable">
          <button class="btn btn-sm ms-auto" :class="part ? 'btn-link text-decoration-none py-0' : 'btn-outline-primary'" @click="start">{{ part ? '✏️' : 'Описати поле' }}</button>
          <span v-if="part" class="text-secondary act" role="button" title="Прибрати поле" @click="remove">🗑️</span>
        </template>
      </div>
      <div v-else class="row g-2 align-items-end">
        <div v-for="s in specs" :key="s.key" :class="s.type === 'tags' ? 'col-12' : 'col-6 col-md-3'">
          <label class="form-label small mb-0 text-secondary">{{ s.label }}</label>
          <input v-if="s.type === 'text'" v-model="form.props[s.key]" class="form-control form-control-sm" :placeholder="s.hint">
          <select v-else-if="s.type === 'choice'" v-model="form.props[s.key]" class="form-select form-select-sm">
            <option value="">—</option>
            <option v-for="(label, v) in s.options" :key="v" :value="v">{{ label }}</option>
          </select>
          <div v-else-if="s.type === 'bool'" class="form-check mb-1"><input v-model="form.props[s.key]" class="form-check-input" type="checkbox"> <span class="small">так</span></div>
          <TagInput v-else v-model="form.props[s.key]" :hash="false" :known="['підлога', 'обʼєкти', 'розмітка', 'туман', 'предмети']" />
        </div>
        <div class="col-12">
          <input v-model="form.description" class="form-control form-control-sm" placeholder="Коротко про поле: як генерується, чи є рівні, камера…">
        </div>
        <div class="col-12 d-flex gap-2">
          <button class="btn btn-primary btn-sm" @click="save">💾 Зберегти</button>
          <button class="btn btn-outline-secondary btn-sm" @click="edit = false">✕</button>
        </div>
      </div>
      <div v-if="part?.description && !edit" class="text-secondary small">{{ part.description }}</div>
      <template v-if="part">
        <ShotStrip v-if="editable || part.screenshots.length" :part :editable @changed="emit('changed')" />
        <div v-if="claims.length" class="d-flex flex-wrap gap-1 align-items-start">
          <ClaimChip v-for="c in claims" :key="c.id" :claim="c" :info="info(c.task)" :parts :editable :judge :nick @changed="emit('changed')" />
        </div>
        <CardPicker v-if="editable" placeholder="＋ картка про поле: рендер, камера, масштаб, генерація…"
                    :claimed="new Set(claims.map((c) => c.task))" @pick="addClaim" />
      </template>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
  </div>
</template>

<style scoped>
.act { opacity: .6; }
.act:hover { opacity: 1; }
</style>
