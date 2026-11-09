<script setup>
import { computed, nextTick, ref } from 'vue'

import Toc from '@core/components/Toc.vue'
import { applyTemplate, postPart } from '../api.js'
import { COIN_ORDER, COINS, games, taskIndex, templates } from '../catalog.js'
import { hints as makeHints } from '../hints.js'
import { anchorKind } from '../myGame.js'
import AddBar from './AddBar.vue'
import ClaimZones from './ClaimZones.vue'
import EntityCard from './EntityCard.vue'
import FieldCard from './FieldCard.vue'
import GameGraph from './GameGraph.vue'
import Hints from './Hints.vue'
import RulesBlock from './RulesBlock.vue'
import WindowCard from './WindowCard.vue'

// the description of a game — the same body for the owner's editor (`editable`) and a student's passport
// (read-only; `judge` lets the teacher accept or return claims). Sections: поле · сутності · правила · вікна · гра загалом
const props = defineProps({ game: Object, parts: Array, claims: Array, rules: Array, tasks: Object, editable: Boolean, judge: Boolean, nick: String })
const emit = defineEmits(['changed'])
const error = ref('')
const rulesBlock = ref()
const info = (slug) => props.tasks[slug] || taskIndex.value[slug]
const field = computed(() => props.parts.find((p) => p.kind === 'field'))
const entities = computed(() => props.parts.filter((p) => p.kind === 'entity'))
const windows = computed(() => props.parts.filter((p) => p.kind === 'window'))
const menus = computed(() => props.parts.filter((p) => p.kind === 'menu'))
const menusOf = (id) => menus.value.filter((m) => m.window === id)
const orphanMenus = computed(() => menus.value.filter((m) => !windows.value.some((w) => w.id === m.window)))
const claimsOf = (id) => props.claims.filter((c) => c.part === id)
const gameClaims = computed(() => props.claims.filter((c) => !c.part))
const drafts = computed(() => gameClaims.value.filter((c) => anchorKind(info(c.task)) !== 'game'))
const base = computed(() => games.value.find((g) => g.slug === props.game.base_game))
const template = computed(() => templates.value[props.game.base_game])
const coins = computed(() => {
  const n = { claimed: {}, accepted: {} }
  for (const c of props.claims) {
    const t = info(c.task)
    if (!t?.coin) continue
    n.claimed[t.coin] = (n.claimed[t.coin] || 0) + (t.amount || 1)
    if (c.status === 'accepted') n.accepted[t.coin] = (n.accepted[t.coin] || 0) + (t.amount || 1)
  }
  const row = (m) => COIN_ORDER.filter((k) => m[k]).map((k) => `${COINS[k]}×${m[k]}`).join(' ')
  return { claimed: row(n.claimed), accepted: row(n.accepted) }
})
const hints = computed(() => (props.editable ? makeHints({ ...props, tasks: new Proxy({}, { get: (_, k) => info(k) }), base: base.value }) : []))
const toc = computed(() => [
  ...(drafts.value.length ? [{ id: 'drafts', text: `📥 Чернетки (${drafts.value.length})`, depth: 2 }] : []),
  { id: 'field', text: '🗺️ Поле', depth: 2 },
  { id: 'entities', text: `👾 Сутності (${entities.value.length})`, depth: 2 },
  { id: 'rules', text: `📜 Правила (${props.rules.length})`, depth: 2 },
  { id: 'windows', text: `🪟 Вікна й меню (${windows.value.length})`, depth: 2 },
  { id: 'game', text: `🎮 Гра загалом (${gameClaims.value.length - drafts.value.length})`, depth: 2 },
])

const changed = () => { error.value = ''; emit('changed') }
async function go(id) {
  await nextTick()
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'center' })
}
async function fromTemplate() {
  error.value = ''
  try {
    const r = await applyTemplate()
    emit('changed')
    if (r.skipped.length) error.value = `Пропущено: ${r.skipped.slice(0, 5).join('; ')}`
  } catch (e) {
    error.value = e.message
  }
}
async function newField() {
  try {
    await postPart({ kind: 'field', title: 'Поле' })
    emit('changed')
    go('field')
  } catch (e) {
    error.value = e.message
  }
}
const empty = computed(() => !props.parts.length && !props.rules.length && !props.claims.length)
</script>

<template>
  <div class="editor">
    <div class="d-flex flex-wrap align-items-center gap-2 small text-secondary mb-2">
      <span>{{ entities.length }} сут. · {{ rules.length }} правил · {{ windows.length }} вікон · {{ claims.length }} заявок</span>
      <span v-if="coins.claimed" title="заявлено монеток — довідково">· {{ coins.claimed }}</span>
      <span v-if="coins.accepted" class="text-success" title="зараховано">· ✓ {{ coins.accepted }}</span>
    </div>

    <template v-if="editable">
      <AddBar :parts :claims class="mb-2" @changed="changed" @rule="rulesBlock?.add(); go('rules')" @field="newField" />
      <div v-if="empty && template" class="alert alert-light border d-flex flex-wrap align-items-center gap-2 py-2 small">
        <span>Порожньо. Почати з еталона <b>{{ base?.icon }} {{ base?.title }}</b> — {{ template.entities }} сутностей, {{ template.rules }} правил, {{ template.windows }} вікон, {{ template.claims }} карток — і далі викреслювати й додавати своє?</span>
        <button class="btn btn-primary btn-sm ms-auto" @click="fromTemplate">Почати з еталона</button>
      </div>
      <Hints :items="hints" class="mb-3" @go="go" />
    </template>
    <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>

    <section v-if="drafts.length" id="drafts" class="mb-4">
      <h2 class="h6 head">📥 Чернетки <span class="count">({{ drafts.length }})</span>
        <span class="text-secondary fw-normal small ms-2">картки без господаря — відкрий чіп і привʼяжи до сутності чи вікна</span></h2>
      <ClaimZones :claims :parts :info :editable :judge :nick drafts @changed="changed" @error="error = $event" />
    </section>

    <section id="field" class="mb-4">
      <h2 class="h6 head">🗺️ Поле</h2>
      <FieldCard :part="field" :claims="field ? claimsOf(field.id) : []" :info :parts :editable :judge :nick @changed="changed" />
    </section>

    <section id="entities" class="mb-4">
      <h2 class="h6 head">👾 Сутності <span class="count">({{ entities.length }})</span></h2>
      <p v-if="!entities.length" class="text-secondary small">Мешканці поля: гравець, вороги, предмети, стіни, підлога. У кожної — роль, параметри (HP, швидкість…), стани, механіки з каталогу і правила. Додай через «＋ Додати» словом «гравець», «ворог», «бонус»…</p>
      <div class="masonry">
        <EntityCard v-for="p in entities" :id="`p-${p.id}`" :key="p.id" :part="p" :claims="claimsOf(p.id)" :rules :parts :info :editable :judge :nick @changed="changed" @go="go" />
      </div>
    </section>

    <section id="rules" class="mb-4">
      <h2 class="h6 head">📜 Правила <span class="count">({{ rules.length }})</span></h2>
      <RulesBlock ref="rulesBlock" :rules :parts :game :editable @changed="changed" />
    </section>

    <section id="windows" class="mb-4">
      <h2 class="h6 head">🪟 Вікна й меню <span class="count">({{ windows.length }})</span></h2>
      <p v-if="!windows.length" class="text-secondary small">Екрани гри: ігровий екран, головне меню, пауза, налаштування, кінець гри… Кожне — тип з каталогу, скриншот, елементи на ньому і пункти меню. Додай через «＋ Додати» словом «меню», «пауза», «налаштування»…</p>
      <div class="masonry">
        <WindowCard v-for="p in windows" :key="p.id" :part="p" :menus="menusOf(p.id)" :windows :claims="claimsOf(p.id)" :game-claims="gameClaims" :parts :info :editable :judge :nick @changed="changed" />
      </div>
      <div v-if="orphanMenus.length" class="small text-secondary mt-2">
        Меню без вікна: <span v-for="m in orphanMenus" :key="m.id" class="me-2">«{{ m.title }}» ({{ m.items.length }} п.)</span> — відкрий вікно й додай пункти там.
      </div>
      <div v-if="windows.length > 1" class="card mt-2">
        <div class="card-body p-2"><GameGraph :windows :menus @pick="(id) => go(`p-${id}`)" /></div>
      </div>
    </section>

    <section id="game" class="mb-4">
      <h2 class="h6 head">🎮 Гра загалом <span class="count">({{ gameClaims.length - drafts.length }})</span></h2>
      <ClaimZones :claims :parts :info :editable :judge :nick @changed="changed" @error="error = $event" />
    </section>

    <Toc :items="toc" />
  </div>
</template>

<style scoped>
.head { font-weight: 700; margin-bottom: .5rem; padding-bottom: .25rem; border-bottom: 1px solid var(--bs-border-color); }
.count { font-weight: 400; opacity: .55; }
section { scroll-margin-top: 1rem; }
/* cards of different heights pack without the gaps a row grid leaves */
.masonry { columns: 2 18rem; column-gap: .5rem; }
.masonry > * { break-inside: avoid; margin-bottom: .5rem; }
.masonry > :deep(.card) { height: auto !important; }
</style>
