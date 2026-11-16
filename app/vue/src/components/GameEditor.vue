<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, toRef, watch } from 'vue'
import { useRoute } from 'vue-router'

import { ALL_KEY } from '@core/allkey.js'
import Clamp from '@core/components/Clamp.vue'
import Icon from '@core/components/Icon.vue'
import Lightbox from '@core/components/Lightbox.vue'
import PeekHost from '@core/components/PeekHost.vue'
import Tip from '@core/components/Tip.vue'
import Toc from '@core/components/Toc.vue'
import { user } from '@core/user.js'
import { wideOf } from '@core/wide.js'
import { applyTemplate } from '../api.js'
import { games, kindOf, taskIndex, templates, vocab } from '../catalog.js'
import { provideEd } from '../ed.js'
import { savers } from '../edSave.js'
import { allMode, isFolded, isOwn, isShort, setAll, setFold, setShort } from '../fold.js'
import { hints as makeHints } from '../hints.js'
import { jump, target } from '../jump.js'
import { canCols, colsMode, edWidth } from '../layout.js'
import { cards as cardLooks, CARDS, ROWS, rows } from '../looks.js'
import '../peeks.js'
import { sandbox } from '../sandbox.js'
import { foldKey, HEADS, sectionOf, SECTIONS, SIMPLE, ZONES } from '../sections.js'
import { editing } from '../teacher.js'
import AddBar from './AddBar.vue'
import ClaimsTable from './ClaimsTable.vue'
import ColsSwitch from './ColsSwitch.vue'
import DraftStrip from './DraftStrip.vue'
import EntitiesBlock from './EntitiesBlock.vue'
import EtalonGap from './EtalonGap.vue'
import FieldCard from './FieldCard.vue'
import GameTotals from './GameTotals.vue'
import GroupsFold from './GroupsFold.vue'
import Hints from './Hints.vue'
import LevelsBlock from './LevelsBlock.vue'
import LookSwitch from './LookSwitch.vue'
import MomentsBlock from './MomentsBlock.vue'
import RulesBlock from './RulesBlock.vue'
import SectionHead from './SectionHead.vue'
import WideSwitch from './WideSwitch.vue'
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
  sandbox: computed(() => !!sandbox.value && props.editable),  // the sample's scratch copy (T274 §7): no screenshots there
  teacher: computed(() => !!editing.value && props.editable),  // the teacher edits a student's game (T282): no owner's aids
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
ed.save = savers(ed)
provideEd(ed)

const loose = computed(() => props.claims.filter((c) => !c.part && !c.rule && !c.auto))
const inZone = (z) => loose.value.filter((c) => kindOf(ed.info(c.task)) === 'game' && z.zones.includes(ed.info(c.task)?.zone)).length
const own = computed(() => props.claims.filter((c) => !c.auto).length)
const base = computed(() => games.value.find((g) => g.slug === props.game.base_game))
const template = computed(() => templates.value[props.game.base_game])
const empty = computed(() => !props.parts.length && !props.rules.length && !props.claims.length)
const hints = computed(() => (props.editable ? makeHints({ game: props.game, parts: props.parts, rules: props.rules, claims: props.claims, info: ed.info, base: base.value, simple: ed.simple, shots: !ed.sandbox }) : []))
// the sections in the catalog's order (T278 §9): their headings and the contents say the same
const shown = computed(() => (ed.simple ? SIMPLE : SECTIONS))
const counts = computed(() => ({ entities: ed.entities.length, rules: props.rules.length, levels: ed.levels.length, windows: ed.windows.length,
  ...Object.fromEntries(ZONES.map((z) => [z.id, inZone(z)])) }))
const LAID = ['entities', 'rules', 'levels', 'windows', ...ZONES.map((z) => z.id)]  // the sections that lay cards in columns
const SHUT = ['entities', 'windows', 'levels']  // the sections whose cards fold to their heads (looks.js)
const head = (id) => {
  const { icon, title, short, zone } = HEADS[id]
  return { icon, title: (ed.simple && short) || title, zone, count: counts.value[id], fold: foldKey(id), anchor: id, layout: LAID.includes(id),
           cardFold: SHUT.includes(id) }
}
const zone = (id) => ZONES.find((z) => z.id === id)
const cardsToc = ref([])  // «Картки» names its own contents: the categories on screen
// the places inside a section a link may lead to (#rules-phases…): the section opens whole first; of them only the map of
// windows is worth a line in the contents (T291 §3, T294 §10) — a sub-item, a step right of its section's title
const partHome = { 'rules-phases': 'rules', 'levels-general': 'levels', 'windows-graph': 'windows' }
const parts = computed(() => (ed.simple ? {} : { windows: ed.windows.length > 1 ? [['windows-graph', '🔀 Схема вікон']] : [] }))
const toc = computed(() => (view.value === 'cards' ? cardsToc.value : shown.value.flatMap((id) => {
  const h = head(id)
  return [{ id, text: `${h.icon} ${h.title}${h.count === undefined ? '' : ` (${h.count})`}`, depth: 2 },
    ...(parts.value[id] || []).map(([pid, text]) => ({ id: pid, text, depth: 4 }))]
})))

// the page on the whole window (T287): the reader's choice where the page allows it (router: meta.wide 'game'); the top
// of the editor keeps the page column, the sections take the width — and more columns of cards with it
const route = useRoute()
const wide = computed(() => route.meta.wide === 'game' && wideOf('game').on.value)
// the editor's own width is what the columns switch decides by (layout.js)
const root = ref()
const sized = new ResizeObserver(() => (edWidth.value = root.value.offsetWidth))
onMounted(() => sized.observe(root.value))
onBeforeUnmount(() => sized.disconnect())

// folding (T274 §8, T284 §3): a section is open, short (its beginning) or folded — each by its own heading, all at once
// by the three buttons beside «Опис | Картки»: the one pressed is the default, a heading differing from it is blue (T298)
const folded = (id) => isFolded(foldKey(id))
const short = (id) => isShort(foldKey(id))
const unclamp = (id) => setShort(foldKey(id), false)
const ownFolds = computed(() => shown.value.map(foldKey).filter(isOwn).length)
const pointer = matchMedia('(hover: hover)').matches  // a phone has no ⌥: it only holds
const MODES = [['open', 'unfold', 'усе', 'Усі секції повністю'], ['short', 'short', 'коротко', 'Усі секції коротко: початок кожної і «Показати все»'], ['folded', 'fold', 'згорнуто', 'Згорнути всі секції до заголовків']]
const totals = computed(() => ({ ...counts.value, cards: own.value }))
const go = (k) => (k === 'cards' ? (view.value = 'cards') : jump(k))
// «show me where» lands in the description: back from «Картки», the section holding the place unfolded. A claim just
// added is jumped to before the reload brings it, so its section is looked for again as the data comes
let landed = ''  // its section is open: a later reload must not unfold it again
watch([target, () => props.claims, () => props.parts], ([id], [was]) => {
  if (!id) landed = ''
  if (!id || id === landed) return
  if (id !== was) view.value = 'desc'
  const s = sectionOf(id, { parts: props.parts, claims: props.claims, info: ed.info })
  if (s) {
    setFold(foldKey(s), false)
    landed = id
  }
})

// a link to a place in the description (#p-…, #r-…, #c-…, a section — the tick of /tasks leads so): unfold what holds
// it and show it, on arrival and later
watch(() => route.hash, (h) => {
  const id = decodeURIComponent(h.slice(1))
  const home = partHome[id]  // a part of a section: the section opens whole first
  if (home) setFold(foldKey(home), false)
  if (home) setShort(foldKey(home), false)
  if (home || /^[prc]-/.test(id) || SECTIONS.includes(id)) jump(id)
}, { immediate: true })

// «＋» anywhere: the section's own form of a new thing, in view and lit
async function open(block, prefill) {
  view.value = 'desc'
  setFold(foldKey({ entity: 'entities', window: 'windows', level: 'levels', rule: 'rules' }[block]), false)
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
  <div ref="root" class="editor">
    <div :class="{ 'in-column': wide }">
    <GameTotals :counts="totals" :coins :simple="ed.simple" class="mb-3" @go="go">
      <!-- the tiles, then the look and the folding, then the layout — a line each, a word of what it does (T294 §3) -->
      <div class="d-flex flex-wrap align-items-center gap-2 small text-secondary">
        <span v-if="!ed.simple" class="btn-group btn-group-sm">
          <button type="button" class="btn" :class="view === 'desc' ? 'btn-secondary' : 'btn-outline-secondary'" @click="view = 'desc'"><Icon name="list" /> Опис</button>
          <button type="button" class="btn" :class="view === 'cards' ? 'btn-secondary' : 'btn-outline-secondary'" title="Усе заявлене деревом: категорія → картка → де вона" @click="view = 'cards'"><Icon name="table" /> Картки</button>
        </span>
        <span class="btn-group btn-group-sm" role="group" aria-label="секції">
          <button v-for="[m, icon, word, tip] in MODES" :key="m" type="button" class="btn btn-outline-secondary" :class="{ active: view === 'desc' && allMode('ed') === m }"
                  :disabled="view === 'cards'" :title="`${tip}${ownFolds ? ` · свої на заголовках: ${ownFolds}, клік їх скине` : ''}`" @click="setAll('ed', m)"><Icon :name="icon" /><span class="d-none d-sm-inline"> {{ word }}</span></button>
        </span>
        <label v-if="admin && !full" class="form-check form-switch m-0" title="Як бачить студент, поки відкрито лише простий опис">
          <input v-model="simpleLook" type="checkbox" class="form-check-input"> простий вигляд
        </label>
      </div>
      <!-- the reader's look of the sections as one framed group (T301 §3): its explanation, put away, leaves its icon at the
           caption's right end — right of the switches, left of the wallet — not a row of its own -->
      <div v-if="view === 'desc'" class="looks group-box vstack gap-1 align-items-start" data-dock>
        <div class="group-cap">Вигляд<span class="tip-dock ms-auto" /></div>
        <ColsSwitch wordy />
        <LookSwitch wordy :look="rows" :modes="ROWS" label="Розкладка"
                    :off="!canCols ? 'вікно вузьке — один стовпець, вирівнювати нема чого' : colsMode === 'one' ? 'один стовпець — вирівнювати нема чого' : ''" />
        <LookSwitch wordy :look="cardLooks" :modes="CARDS" label="Картки сутностей, рівнів і вікон" />
        <WideSwitch wordy />
        <Tip id="all-key">Угорі — як за замовчуванням для всіх секцій; кнопка на заголовку синя, поки секція інакша.
          {{ pointer ? `${ALL_KEY}-клік чи утримати кнопку на заголовку` : 'Утримай кнопку на заголовку' }} — те саме одразу в усіх секціях</Tip>
      </div>
    </GameTotals>

    <template v-if="editable">
      <AddBar class="mb-2" @open="open" />
      <div v-if="empty && template && !ed.simple && !ed.sandbox && !ed.teacher" class="alert alert-light border d-flex flex-wrap align-items-center gap-2 py-2 small">
        <span>Порожньо. Почати з еталона <b>{{ base?.icon }} {{ base?.title }}</b> — {{ template.entities }} сутностей, {{ template.rules }} правил, {{ template.windows }} вікон, {{ template.claims }} карток — і далі викреслювати й додавати своє?</span>
        <button type="button" class="btn btn-sm btn-add ms-auto" @click="fromTemplate"><Icon name="plus" /> Почати з еталона</button>
      </div>
      <Hints v-if="!ed.teacher" :items="hints" class="mb-3" />
      <EtalonGap v-if="!ed.simple && !ed.sandbox && !ed.teacher && game.base_game" class="mb-3" />
    </template>
    <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>
    </div>

    <ClaimsTable v-if="view === 'cards' && !ed.simple" :class="{ 'in-column': wide }" @toc="cardsToc = $event" />
    <!-- in SECTIONS' order (sections.js); folded bodies stay mounted (v-show): «＋» still opens their forms, «show me where»
         still finds what is inside -->
    <template v-else>
      <section v-if="!ed.simple" id="field" class="mb-4">
        <SectionHead v-bind="head('field')" />
        <Clamp v-show="!folded('field')" :on="short('field')" @open="unclamp('field')">
          <DraftStrip :kinds="['field']" hint="сядуть на поле самі, щойно його опишеш" />
          <FieldCard />
        </Clamp>
      </section>
      <section id="entities" class="mb-4">
        <SectionHead v-bind="head('entities')">
          <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('entity')"><Icon name="plus" /> сутність</button>
        </SectionHead>
        <Clamp v-show="!folded('entities')" :on="short('entities')" @open="unclamp('entities')">
          <DraftStrip :kinds="['mechanic']" hint="привʼяжи до сутності: натисни на картку → «Перемістити»" />
          <EntitiesBlock :ref="blocks.entity" />
        </Clamp>
      </section>
      <section v-if="!ed.simple" id="rules" class="mb-4">
        <SectionHead v-bind="head('rules')">
          <template #default="{ keep }">
            <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('rule')"><Icon name="plus" /> правило</button>
            <GroupsFold v-if="!folded('rules')" :around="keep" />
          </template>
        </SectionHead>
        <Clamp v-show="!folded('rules')" :on="short('rules')" @open="unclamp('rules')">
          <DraftStrip :kinds="['rule']" hint="натисни на картку → «нове правило з цієї картки» або «привʼязати до наявного»" />
          <RulesBlock :ref="blocks.rule" />
        </Clamp>
      </section>
      <ZoneSection v-if="!ed.simple" :z="zone('zone-game-logic')" :head="head('zone-game-logic')" />
      <section v-if="!ed.simple" id="levels" class="mb-4">
        <SectionHead v-bind="head('levels')">
          <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('level')"><Icon name="plus" /> рівень</button>
        </SectionHead>
        <Clamp v-show="!folded('levels')" :on="short('levels')" @open="unclamp('levels')"><LevelsBlock :ref="blocks.level" /></Clamp>
      </section>
      <section v-if="!ed.simple" id="moments" class="mb-4">
        <SectionHead v-bind="head('moments')" />
        <Clamp v-show="!folded('moments')" :on="short('moments')" @open="unclamp('moments')"><MomentsBlock /></Clamp>
      </section>
      <section id="windows" class="mb-4">
        <SectionHead v-bind="head('windows')">
          <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('window')"><Icon name="plus" /> вікно</button>
        </SectionHead>
        <Clamp v-show="!folded('windows')" :on="short('windows')" @open="unclamp('windows')">
          <DraftStrip :kinds="['element']" hint="привʼяжи до вікна: натисни на картку → «Перемістити»" />
          <WindowsBlock :ref="blocks.window" />
        </Clamp>
      </section>
      <template v-if="!ed.simple">
        <ZoneSection v-for="id in ['zone-interface', 'zone-code', 'zone-support']" :key="id" :z="zone(id)" :head="head(id)" />
      </template>
    </template>

    <Toc :items="toc" :side="!wide" :bar="view === 'cards'" />
    <Lightbox />
    <PeekHost />
  </div>
</template>

<style>
/* a section's heading sticks under the menu (SectionHead): what is scrolled to on this page lands below both; a card's head
   and a group of rules stick right under it (partCard.css) — so the heading keeps this height, buttons and all */
html:has(.editor) { --stick-h: 2.6rem; }
/* a section reads as a block of its own (T287): its content stands in from the heading's line on both sides, and the
   next heading comes after a wider gap */
.editor > section { margin-bottom: 2.5rem !important; scroll-margin-top: 1rem; }
@media (min-width: 576px) { .editor > section > .clamp { padding-inline: .75rem; } }  /* a phone has no width to give away */
/* the frame is as wide as its switches: the explanation wraps inside it instead of widening it */
.editor .looks { align-self: flex-start; max-width: 100%; }
.editor .looks > .group-cap { align-self: stretch; }
.editor .looks > .tipbox { width: 0; min-width: 100%; }
</style>
