<script setup>
import { computed, ref } from 'vue'

import { postClaim, postPart, putPart } from '../api.js'
import { COINS, missingParams, roleOf, subzoneTitle } from '../catalog.js'
import { anchorKind } from '../myGame.js'
import { searchAll } from '../search.js'
import SlotFields from './SlotFields.vue'

// one «＋ Додати…» for the whole description: type what you built — a card (by any of its names), a role («ворог»),
// a window type, «поле», «правило» — then say where it goes
const props = defineProps({ parts: Array, claims: Array })
const emit = defineEmits(['changed', 'rule', 'field'])
const q = ref('')
const open = ref(false)
const cursor = ref(0)
const step = ref(null)  // { kind: 'card', task, part, params } | { kind: 'entity'|'window', role?, task?, title }
const error = ref('')
const found = computed(() => (q.value.trim().length < 2 ? [] : searchAll(q.value)))
const entities = computed(() => props.parts.filter((p) => p.kind === 'entity'))
const windows = computed(() => props.parts.filter((p) => p.kind === 'window'))
const claimedHere = (slug, part) => props.claims.some((c) => c.task === slug && c.part === part)
const wants = computed(() => step.value?.kind === 'card' && anchorKind(step.value.task))
const anchors = computed(() => (wants.value === 'window' ? windows.value : wants.value === 'entity' ? entities.value : []))
const ready = computed(() => step.value?.kind === 'stat' ? step.value.part && step.value.value.trim()
  : step.value?.kind !== 'card' || step.value.part === '' || !missingParams(step.value.task, step.value.params).length)

function pick(r) {
  q.value = ''
  open.value = false
  error.value = ''
  if (r.kind === 'rule') return emit('rule')
  if (r.kind === 'field') return emit('field')
  if (r.kind === 'card') {
    const kind = anchorKind(r.task)
    const only = kind === 'entity' && entities.value.length === 1 ? entities.value[0].id : kind === 'window' && windows.value.length === 1 ? windows.value[0].id : ''
    step.value = { kind: 'card', task: r.task, part: only, params: {} }
  } else if (r.kind === 'stat') {
    step.value = { kind: 'stat', stat: r.stat, part: entities.value.length === 1 ? entities.value[0].id : '', value: '' }
  } else {
    step.value = { kind: r.kind, role: r.role, task: r.task, title: r.kind === 'window' ? r.task.title : '' }
  }
}
async function send() {
  error.value = ''
  try {
    const s = step.value
    if (s.kind === 'card') await postClaim({ task: s.task.slug, part: s.part, params: s.params })
    else if (s.kind === 'entity') await postPart({ kind: 'entity', role: s.role, title: s.title })
    else if (s.kind === 'stat') {
      const p = entities.value.find((e) => e.id === s.part)
      const stats = [...p.stats.filter((x) => x.key !== s.stat.key), { key: s.stat.key, label: s.stat.label, value: s.value, unit: s.stat.unit }]
      await putPart(p.id, { title: p.title, role: p.role, description: p.description, stats, states: p.states, order: p.order })
    } else await postPart({ kind: 'window', task: s.task.slug, title: s.title })
    step.value = null
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
function key(e) {
  if (e.key === 'ArrowDown') { cursor.value = Math.min(cursor.value + 1, found.value.length - 1); e.preventDefault() }
  else if (e.key === 'ArrowUp') { cursor.value = Math.max(cursor.value - 1, 0); e.preventDefault() }
  else if (e.key === 'Enter' && found.value[cursor.value]) { pick(found.value[cursor.value]); e.preventDefault() }
  else if (e.key === 'Escape') open.value = false
}
const KIND = { card: '', entity: 'нова сутність', window: 'нове вікно', rule: 'форма', field: 'форма' }
</script>

<template>
  <div class="addbar">
    <div v-if="!step" class="position-relative">
      <input v-model="q" class="form-control" placeholder="＋ Додати: що є в грі — «ворог», «життя», «пауза», «телепорт», «правило»…"
             @focus="open = true" @blur="open = false" @input="cursor = 0" @keydown="key">
      <div v-if="open && found.length" class="list-group position-absolute w-100 shadow results">
        <button v-for="(r, i) in found" :key="r.kind + (r.task?.slug || r.role || r.label)" type="button"
                class="list-group-item list-group-item-action py-1 small d-flex gap-2 align-items-center" :class="{ active: i === cursor }"
                @mousedown.prevent="pick(r)" @mousemove="cursor = i">
          <span v-if="r.kind === 'card'">{{ COINS[r.task.coin] || '·' }}</span>
          <span v-else-if="r.kind === 'window'">🪟</span>
          <span v-else-if="r.kind === 'entity'">👾</span>
          <span v-else-if="r.kind === 'stat'">#</span>
          <span v-else>📝</span>
          <span class="me-auto">{{ r.label }} <span v-if="r.kind === 'card' && claimedHere(r.task.slug, '')" title="уже в грі">✓</span></span>
          <span class="text-secondary text-nowrap">{{ r.kind === 'card' ? subzoneTitle(r.task) : r.hint || KIND[r.kind] }}</span>
        </button>
      </div>
      <div v-else-if="open && q.trim().length >= 2" class="list-group position-absolute w-100 shadow results">
        <div class="list-group-item py-1 small text-secondary">Нічого не знайшлось. Спробуй інше слово — або <RouterLink to="/ideas">запропонуй нову картку</RouterLink>.</div>
      </div>
    </div>

    <div v-else class="border rounded p-2 d-flex flex-wrap gap-2 align-items-center small step">
      <template v-if="step.kind === 'card'">
        <span><b>{{ COINS[step.task.coin] }} {{ step.task.title }}</b> — куди?</span>
        <div class="d-flex flex-wrap gap-1">
          <button type="button" class="btn btn-sm chip" :class="step.part === '' ? 'btn-primary' : 'btn-outline-secondary'" @click="step.part = ''">
            {{ wants === 'game' ? '🎮 гра загалом' : '📥 поки в чернетки' }}
          </button>
          <button v-for="p in anchors" :key="p.id" type="button" class="btn btn-sm chip" :class="step.part === p.id ? 'btn-primary' : 'btn-outline-secondary'" @click="step.part = p.id">
            {{ p.kind === 'entity' ? roleOf(p.role).icon : '🪟' }} {{ p.title }}
          </button>
        </div>
        <span v-if="wants !== 'game' && !anchors.length" class="text-secondary">(сутностей чи вікон ще нема — ляже в чернетки, привʼяжеш пізніше)</span>
        <template v-if="step.task.slots?.length">
          <span class="text-secondary">параметри:</span>
          <SlotFields :specs="step.task.slots" :params="step.params" />
        </template>
      </template>
      <template v-else-if="step.kind === 'stat'">
        <span>Параметр <b>{{ step.stat.icon }} {{ step.stat.label }}</b> — кому?</span>
        <div class="d-flex flex-wrap gap-1">
          <button v-for="p in entities" :key="p.id" type="button" class="btn btn-sm chip" :class="step.part === p.id ? 'btn-primary' : 'btn-outline-secondary'" @click="step.part = p.id">
            {{ roleOf(p.role).icon }} {{ p.title }}
          </button>
        </div>
        <span v-if="!entities.length" class="text-secondary">(спершу додай сутність)</span>
        <input v-model="step.value" class="form-control form-control-sm w-auto" style="width: 6rem" placeholder="значення" @keydown.enter="ready && send()">
        <span v-if="step.stat.unit" class="text-secondary">{{ step.stat.unit }}</span>
      </template>
      <template v-else>
        <span>{{ step.kind === 'entity' ? `Нова сутність · ${roleOf(step.role).icon} ${roleOf(step.role).label}` : `Нове вікно · ${step.task.title}` }}:</span>
        <input v-model="step.title" class="form-control form-control-sm w-auto" :placeholder="step.kind === 'entity' ? 'назва у твоїй грі' : 'назва вікна'" autofocus @keydown.enter="step.title.trim() && send()">
      </template>
      <button class="btn btn-primary btn-sm" :disabled="!ready || (step.kind !== 'card' && step.kind !== 'stat' && !step.title.trim())" @click="send">Додати</button>
      <button class="btn btn-outline-secondary btn-sm" @click="step = null">✕</button>
      <span v-if="error" class="text-danger">{{ error }}</span>
    </div>
  </div>
</template>

<style scoped>
.results { z-index: 20; max-height: 22rem; overflow-y: auto; }
.step { background: var(--bs-tertiary-bg); }
</style>
