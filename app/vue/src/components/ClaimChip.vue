<script setup>
import { computed, reactive, ref } from 'vue'

import { deleteClaim, judgeClaim, putClaim } from '../api.js'
import { CLAIM_STATUSES, missingParams, paramsText, roleOf, zoneOf } from '../catalog.js'
import CoinBadge from './CoinBadge.vue'
import SlotFields from './SlotFields.vue'

// one claim as a chip in its zone's colour; a click opens the row under it — params, note, link, the anchor to move to,
// and, for the teacher on a passport, the verdict
const props = defineProps({ claim: Object, info: Object, parts: { type: Array, default: () => [] }, editable: Boolean, judge: Boolean, nick: String })
const emit = defineEmits(['changed'])
const open = ref(false)
const error = ref('')
const form = reactive({ params: { ...props.claim.params }, note: props.claim.note, link: props.claim.link, part: props.claim.part })
const verdict = reactive({ status: props.claim.status, verdict: props.claim.verdict })
const ptext = computed(() => paramsText(props.info, props.claim.params))
const missing = computed(() => missingParams(props.info, props.claim.params))
const zone = computed(() => zoneOf(props.info))
const anchors = computed(() => props.parts.filter((p) => p.kind === 'entity' || p.kind === 'window' || p.kind === 'field'))
const anchorName = (p) => (p.kind === 'entity' ? `${roleOf(p.role).icon} ${p.title}` : p.kind === 'window' ? `🪟 ${p.title}` : `🗺️ ${p.title}`)

async function run(fn) {
  error.value = ''
  try {
    await fn()
    open.value = false
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
const save = () => run(() => putClaim(props.claim.id, form))
const remove = () => run(() => deleteClaim(props.claim.id))
const judgeIt = () => run(() => judgeClaim(props.nick, props.claim.id, verdict))
</script>

<template>
  <div class="claim" :class="[claim.status, { open }]">
    <span class="chip badge rounded-pill fw-normal text-body d-inline-flex align-items-center gap-1" :style="{ '--zc': zone.color }"
          :role="editable || judge ? 'button' : null" :title="claim.verdict || claim.note" @click="(editable || judge) && (open = !open)">
      <CoinBadge :coin="info?.coin" :amount="info?.amount" />
      <span>{{ info?.title || claim.task }}</span>
      <span v-if="ptext" class="text-secondary">· {{ ptext }}</span>
      <span v-else-if="missing.length" class="text-warning-emphasis" title="картка чекає параметрів">⚙️?</span>
      <a v-if="claim.link" :href="claim.link" target="_blank" class="text-decoration-none" title="код" @click.stop>🔗</a>
      <span v-if="claim.note" title="нотатка">💬</span>
      <span v-if="claim.status === 'accepted'" class="text-success" title="зараховано">✓</span>
      <span v-else-if="claim.status === 'returned'" class="text-danger" title="повернуто — доробити">↩</span>
    </span>

    <div v-if="open" class="panel border rounded p-2 mt-1 vstack gap-2 small">
      <div v-if="claim.verdict" class="text-secondary">💬 Викладач: {{ claim.verdict }}</div>
      <template v-if="editable">
        <div v-if="info?.slots?.length" class="d-flex flex-wrap gap-1 align-items-center">
          <SlotFields :specs="info.slots" :params="form.params" />
        </div>
        <div class="input-group input-group-sm">
          <input v-model="form.note" class="form-control" placeholder="Нотатка: як саме це зроблено">
          <input v-model="form.link" class="form-control" placeholder="GitHub: файл або коміт (за бажанням)">
        </div>
        <div class="d-flex flex-wrap gap-2 align-items-center">
          <select v-model="form.part" class="form-select form-select-sm w-auto" title="До чого привʼязано">
            <option value="">🎮 гра загалом</option>
            <option v-for="p in anchors" :key="p.id" :value="p.id">{{ anchorName(p) }}</option>
          </select>
          <button class="btn btn-primary btn-sm" @click="save">💾 Зберегти</button>
          <button class="btn btn-outline-danger btn-sm ms-auto" title="Прибрати заявку" @click="remove">✕ прибрати</button>
        </div>
      </template>
      <template v-else-if="judge">
        <div class="d-flex flex-wrap gap-2 align-items-center">
          <div class="btn-group btn-group-sm">
            <button v-for="(label, k) in CLAIM_STATUSES" :key="k" type="button" class="btn"
                    :class="verdict.status === k ? (k === 'accepted' ? 'btn-success' : k === 'returned' ? 'btn-danger' : 'btn-secondary') : 'btn-outline-secondary'"
                    @click="verdict.status = k">{{ label }}</button>
          </div>
          <input v-model="verdict.verdict" class="form-control form-control-sm w-auto flex-grow-1" placeholder="Слово студентові (за бажанням)">
          <button class="btn btn-primary btn-sm" @click="judgeIt">💾</button>
        </div>
        <div v-if="claim.note" class="text-secondary">📝 {{ claim.note }}</div>
      </template>
      <div v-if="error" class="text-danger">{{ error }}</div>
    </div>
  </div>
</template>

<style scoped>
.claim { display: inline-block; max-width: 100%; }
.claim.open { display: block; width: 100%; }
.chip { background: var(--bs-body-bg); border: 1px solid var(--bs-border-color); border-left: 3px solid var(--zc); font-size: .8rem; padding: .3rem .55rem; }
.accepted .chip { border-color: var(--bs-success-border-subtle); border-left-color: var(--bs-success); background: var(--bs-success-bg-subtle); }
.returned .chip { border-color: var(--bs-danger-border-subtle); border-left-color: var(--bs-danger); background: var(--bs-danger-bg-subtle); }
.panel { background: var(--bs-tertiary-bg); }
</style>
