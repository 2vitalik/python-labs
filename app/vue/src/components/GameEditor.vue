<script setup>
import { computed, nextTick, reactive, ref, toRef } from 'vue'

import Icon from '@core/components/Icon.vue'
import Lightbox from '@core/components/Lightbox.vue'
import Toc from '@core/components/Toc.vue'
import { user } from '@core/user.js'
import { applyTemplate } from '../api.js'
import { COIN_ORDER, COINS, games, kindOf, taskIndex, templates, vocab } from '../catalog.js'
import { provideEd } from '../ed.js'
import { hints as makeHints } from '../hints.js'
import { jump } from '../jump.js'
import { isDraft } from '../myGame.js'
import AddBar from './AddBar.vue'
import ClaimRow from './ClaimRow.vue'
import ClaimsTable from './ClaimsTable.vue'
import EntitiesBlock from './EntitiesBlock.vue'
import FieldCard from './FieldCard.vue'
import Hints from './Hints.vue'
import LevelsBlock from './LevelsBlock.vue'
import RulesBlock from './RulesBlock.vue'
import SectionHead from './SectionHead.vue'
import WindowsBlock from './WindowsBlock.vue'
import ZoneSection from './ZoneSection.vue'

// the description of a game — the same body for the owner's editor (`editable`) and a student's passport (read-only;
// `judge` lets the teacher accept or return claims). It fills the editor context (ed.js) every piece below reads.
// `full` — always the whole description, whatever depth the viewer's own editor has (a base game's reference description);
// `reload` — the page's way to fetch the game again: `ed.changed()` awaits it, so a form closes onto fresh data
const props = defineProps({ game: Object, parts: Array, claims: Array, rules: Array, tasks: Object, coins: Object, editable: Boolean, judge: Boolean, nick: String, full: Boolean, reload: Function })
const error = ref('')
const view = ref('desc')  // desc — the sections · cards — everything claimed as a tree (T270 §11)
const simpleLook = ref(false)  // the teacher's preview of what a student sees in the short form
const blocks = { entity: ref(), window: ref(), level: ref(), rule: ref() }
const admin = computed(() => user.value?.status === 'admin')
const cards = computed(() => Object.fromEntries(Object.entries(props.tasks || {}).map(([slug, t]) => [slug, { slug, ...taskIndex.value[slug], ...t }])))
const ofKind = (kind) => computed(() => props.parts.filter((p) => p.kind === kind))

const ed = reactive({
  game: toRef(props, 'game'), parts: toRef(props, 'parts'), claims: toRef(props, 'claims'), rules: toRef(props, 'rules'),
  editable: toRef(props, 'editable'), judge: toRef(props, 'judge'), nick: toRef(props, 'nick'),
  field: computed(() => props.parts.find((p) => p.kind === 'field')),
  entities: ofKind('entity'), windows: ofKind('window'), levels: ofKind('level'), menus: ofKind('menu'),
  simple: computed(() => !props.full && (simpleLook.value || vocab.value.depth === 'simple')), showRules: false,
  info: (slug) => cards.value[slug] || taskIndex.value[slug],
  claimsOf: (id) => props.claims.filter((c) => c.part === id),
  ruleClaims: (id) => props.claims.filter((c) => c.rule === id),
  changed: () => { error.value = ''; return props.reload?.() },
  open: (block, prefill) => open(block, prefill),
  fail: (text) => (error.value = text),
})
provideEd(ed)

const ZONES = [
  { id: 'zone-game-logic', icon: '🎲', title: 'Логіка гри', zones: ['game-logic', 'entities', 'field', 'levels'], hint: 'Що гра вміє загалом, а правилом не скажеш: збереження, суперник-ШІ, скасування ходу, магазин, складність, чіти.' },
  { id: 'zone-interface', icon: '🕹️', title: 'Інтерфейс, графіка, звук', zones: ['interface'], hint: 'Те, що не привʼязане до одного вікна: анімації, ефекти, звук і музика, рекорди й статистика.' },
  { id: 'zone-code', icon: '💻', title: 'Код', zones: ['code'], hint: 'Архітектура, типи, тести, git, запуск — з посиланням на файл чи коміт у нотатці картки.' },
  { id: 'zone-support', icon: '📣', title: 'Супровід', zones: ['support'], hint: 'Відео-демки, сторінка гри, інструкція гравця, журнал розробки.' },
]
const loose = computed(() => props.claims.filter((c) => !c.part && !c.rule && !c.auto))
const drafts = computed(() => loose.value.filter((c) => isDraft(c, ed.info(c.task))))
const inZone = (z) => loose.value.filter((c) => kindOf(ed.info(c.task)) === 'game' && z.zones.includes(ed.info(c.task)?.zone)).length
const own = computed(() => props.claims.filter((c) => !c.auto).length)
const base = computed(() => games.value.find((g) => g.slug === props.game.base_game))
const template = computed(() => templates.value[props.game.base_game])
const empty = computed(() => !props.parts.length && !props.rules.length && !props.claims.length)
const row = (m) => COIN_ORDER.filter((k) => m?.[k]).map((k) => `${COINS[k]}×${m[k]}`).join(' ')
const hints = computed(() => (props.editable ? makeHints({ game: props.game, parts: props.parts, rules: props.rules, claims: props.claims, info: ed.info, base: base.value, simple: ed.simple }) : []))
const toc = computed(() => (view.value === 'cards' ? [] : [
  ...(drafts.value.length && !ed.simple ? [['drafts', `📥 Чернетки (${drafts.value.length})`]] : []),
  ...(ed.simple ? [] : [['field', '🗺️ Поле'], ['levels', `🪜 Рівні (${ed.levels.length})`]]),
  ['entities', `👾 Сутності (${ed.entities.length})`],
  ...(ed.simple ? [] : [['rules', `📜 Правила (${props.rules.length})`]]),
  ['windows', `🪟 Вікна (${ed.windows.length})`],
  ...(ed.simple ? [] : ZONES.map((z) => [z.id, `${z.icon} ${z.title} (${inZone(z)})`])),
].map(([id, text]) => ({ id, text, depth: 2 }))))

// «＋» anywhere: the section's own form of a new thing, in view and lit
async function open(block, prefill) {
  view.value = 'desc'
  await nextTick()
  blocks[block].value?.add(prefill)
  jump({ entity: 'entities', window: 'windows', level: 'levels', rule: 'rule-new' }[block])
}
async function fromTemplate() {
  error.value = ''
  try {
    const r = await applyTemplate()
    await ed.changed()
    if (r.skipped.length) error.value = `Пропущено: ${r.skipped.slice(0, 5).join('; ')}`
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="editor">
    <div class="d-flex flex-wrap align-items-center gap-2 small text-secondary mb-2">
      <span>{{ ed.entities.length }} сут. · {{ ed.windows.length }} вікон<template v-if="!ed.simple"> · {{ rules.length }} правил · {{ ed.levels.length }} рівнів · {{ own }} карток</template></span>
      <span v-if="row(coins?.claimed)" title="заявлено монеток: картка рахується не більше разів, ніж дозволяє">· {{ row(coins.claimed) }}</span>
      <span v-if="row(coins?.accepted)" class="text-success" title="зараховано">· ✓ {{ row(coins.accepted) }}</span>
      <label v-if="admin && !full" class="form-check form-switch m-0 ms-auto" title="Як бачить студент, поки відкрито лише простий опис">
        <input v-model="simpleLook" type="checkbox" class="form-check-input"> простий вигляд
      </label>
      <div v-if="!ed.simple" class="btn-group btn-group-sm" :class="{ 'ms-auto': !admin || full }">
        <button type="button" class="btn" :class="view === 'desc' ? 'btn-secondary' : 'btn-outline-secondary'" @click="view = 'desc'"><Icon name="list" /> Опис</button>
        <button type="button" class="btn" :class="view === 'cards' ? 'btn-secondary' : 'btn-outline-secondary'" title="Усе заявлене деревом: зона → картка → де вона" @click="view = 'cards'"><Icon name="table" /> Картки</button>
      </div>
    </div>

    <template v-if="editable">
      <AddBar class="mb-2" @open="open" />
      <div v-if="empty && template && !ed.simple" class="alert alert-light border d-flex flex-wrap align-items-center gap-2 py-2 small">
        <span>Порожньо. Почати з еталона <b>{{ base?.icon }} {{ base?.title }}</b> — {{ template.entities }} сутностей, {{ template.rules }} правил, {{ template.windows }} вікон, {{ template.claims }} карток — і далі викреслювати й додавати своє?</span>
        <button type="button" class="btn btn-sm btn-add ms-auto" @click="fromTemplate"><Icon name="plus" /> Почати з еталона</button>
      </div>
      <Hints :items="hints" class="mb-3" />
    </template>
    <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>

    <ClaimsTable v-if="view === 'cards' && !ed.simple" />
    <template v-else>
      <section v-if="drafts.length && !ed.simple" id="drafts" class="mb-4">
        <SectionHead icon="📥" title="Чернетки" :count="drafts.length" note="картки без місця — натисни на картку, далі «Перемістити»" />
        <ClaimRow v-for="c in drafts" :key="c.id" :claim="c" />
      </section>
      <template v-if="!ed.simple">
        <section id="field" class="mb-4"><SectionHead icon="🗺️" title="Поле" /><FieldCard /></section>
        <section id="levels" class="mb-4">
          <SectionHead icon="🪜" title="Рівні" :count="ed.levels.length">
            <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('level')"><Icon name="plus" /> рівень</button>
          </SectionHead>
          <LevelsBlock :ref="blocks.level" />
        </section>
      </template>
      <section id="entities" class="mb-4">
        <SectionHead icon="👾" title="Сутності" :count="ed.entities.length">
          <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('entity')"><Icon name="plus" /> сутність</button>
        </SectionHead>
        <EntitiesBlock :ref="blocks.entity" />
      </section>
      <section v-if="!ed.simple" id="rules" class="mb-4">
        <SectionHead icon="📜" title="Правила" :count="rules.length">
          <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('rule')"><Icon name="plus" /> правило</button>
        </SectionHead>
        <RulesBlock :ref="blocks.rule" />
      </section>
      <section id="windows" class="mb-4">
        <SectionHead icon="🪟" :title="ed.simple ? 'Вікна' : 'Вікна й меню'" :count="ed.windows.length">
          <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('window')"><Icon name="plus" /> вікно</button>
        </SectionHead>
        <WindowsBlock :ref="blocks.window" />
      </section>
      <template v-if="!ed.simple">
        <section v-for="z in ZONES" :id="z.id" :key="z.id" class="mb-4">
          <SectionHead :icon="z.icon" :title="z.title" :count="inZone(z)" />
          <ZoneSection :zones="z.zones" :hint="z.hint" />
        </section>
      </template>
    </template>

    <Toc :items="toc" />
    <Lightbox />
  </div>
</template>

<style scoped>
section { scroll-margin-top: 1rem; }
</style>
