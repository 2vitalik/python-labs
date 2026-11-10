<script setup>
import { computed, nextTick, reactive, ref, toRef, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import Lightbox from '@core/components/Lightbox.vue'
import Toc from '@core/components/Toc.vue'
import { user } from '@core/user.js'
import { applyTemplate } from '../api.js'
import { COIN_ORDER, COINS, games, kindOf, taskIndex, templates, vocab } from '../catalog.js'
import { provideEd } from '../ed.js'
import { foldAll, isFolded, setFold } from '../fold.js'
import { hints as makeHints } from '../hints.js'
import { jump, target } from '../jump.js'
import { sandbox } from '../sandbox.js'
import { foldKey, sectionOf, SECTIONS, ZONES } from '../sections.js'
import AddBar from './AddBar.vue'
import ClaimsTable from './ClaimsTable.vue'
import DraftStrip from './DraftStrip.vue'
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
  sandbox: computed(() => !!sandbox.value && props.editable),  // the sample's scratch copy (T274 §7): no screenshots there
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

const loose = computed(() => props.claims.filter((c) => !c.part && !c.rule && !c.auto))
const inZone = (z) => loose.value.filter((c) => kindOf(ed.info(c.task)) === 'game' && z.zones.includes(ed.info(c.task)?.zone)).length
const own = computed(() => props.claims.filter((c) => !c.auto).length)
const base = computed(() => games.value.find((g) => g.slug === props.game.base_game))
const template = computed(() => templates.value[props.game.base_game])
const empty = computed(() => !props.parts.length && !props.rules.length && !props.claims.length)
const row = (m) => COIN_ORDER.filter((k) => m?.[k]).map((k) => `${COINS[k]}×${m[k]}`).join(' ')
const hints = computed(() => (props.editable ? makeHints({ game: props.game, parts: props.parts, rules: props.rules, claims: props.claims, info: ed.info, base: base.value, simple: ed.simple, shots: !ed.sandbox }) : []))
const toc = computed(() => (view.value === 'cards' ? [] : [
  ...(ed.simple ? [] : [['field', '🗺️ Поле'], ['levels', `🪜 Рівні (${ed.levels.length})`]]),
  ['entities', `👾 Сутності (${ed.entities.length})`],
  ...(ed.simple ? [] : [['rules', `⚡ Правила (${props.rules.length})`]]),
  ['windows', `🪟 Вікна (${ed.windows.length})`],
  ...(ed.simple ? [] : ZONES.map((z) => [z.id, `${z.icon} ${z.title} (${inZone(z)})`])),
].map(([id, text]) => ({ id, text, depth: 2 }))))

// folding (T274 §8): each section by its heading, all at once by the button beside «Опис | Картки»
const shown = computed(() => (ed.simple ? ['entities', 'windows'] : SECTIONS))
const folded = (id) => isFolded(foldKey(id))
const allFolded = computed(() => shown.value.every(folded))
const foldEvery = () => foldAll(shown.value.map(foldKey), !allFolded.value)
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
  <div class="editor">
    <div class="d-flex flex-wrap align-items-center gap-2 small text-secondary mb-2">
      <span>{{ ed.entities.length }} сут. · {{ ed.windows.length }} вікон<template v-if="!ed.simple"> · {{ rules.length }} правил · {{ ed.levels.length }} рівнів · {{ own }} карток</template></span>
      <span v-if="row(coins?.claimed)" title="заявлено монеток: картка рахується не більше разів, ніж дозволяє">· {{ row(coins.claimed) }}</span>
      <span v-if="row(coins?.accepted)" class="text-success" title="зараховано">· ✓ {{ row(coins.accepted) }}</span>
      <label v-if="admin && !full" class="form-check form-switch m-0 ms-auto" title="Як бачить студент, поки відкрито лише простий опис">
        <input v-model="simpleLook" type="checkbox" class="form-check-input"> простий вигляд
      </label>
      <span class="d-flex gap-2" :class="{ 'ms-auto': !admin || full }">
        <span v-if="!ed.simple" class="btn-group btn-group-sm">
          <button type="button" class="btn" :class="view === 'desc' ? 'btn-secondary' : 'btn-outline-secondary'" @click="view = 'desc'"><Icon name="list" /> Опис</button>
          <button type="button" class="btn" :class="view === 'cards' ? 'btn-secondary' : 'btn-outline-secondary'" title="Усе заявлене деревом: категорія → картка → де вона" @click="view = 'cards'"><Icon name="table" /> Картки</button>
        </span>
        <button type="button" class="btn btn-sm btn-outline-secondary" :disabled="view === 'cards'" :title="allFolded ? 'Розгорнути всі секції' : 'Згорнути всі секції'"
                @click="foldEvery"><Icon :name="allFolded ? 'unfold' : 'fold'" /></button>
      </span>
    </div>

    <template v-if="editable">
      <AddBar class="mb-2" @open="open" />
      <div v-if="empty && template && !ed.simple && !ed.sandbox" class="alert alert-light border d-flex flex-wrap align-items-center gap-2 py-2 small">
        <span>Порожньо. Почати з еталона <b>{{ base?.icon }} {{ base?.title }}</b> — {{ template.entities }} сутностей, {{ template.rules }} правил, {{ template.windows }} вікон, {{ template.claims }} карток — і далі викреслювати й додавати своє?</span>
        <button type="button" class="btn btn-sm btn-add ms-auto" @click="fromTemplate"><Icon name="plus" /> Почати з еталона</button>
      </div>
      <Hints :items="hints" class="mb-3" />
    </template>
    <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>

    <ClaimsTable v-if="view === 'cards' && !ed.simple" />
    <!-- folded bodies stay mounted (v-show): «＋» still opens their forms, «show me where» still finds what is inside -->
    <template v-else>
      <template v-if="!ed.simple">
        <section id="field" class="mb-4">
          <SectionHead icon="🗺️" title="Поле" :fold="foldKey('field')" />
          <div v-show="!folded('field')">
            <DraftStrip :kinds="['field']" hint="сядуть на поле самі, щойно його опишеш" />
            <FieldCard />
          </div>
        </section>
        <section id="levels" class="mb-4">
          <SectionHead icon="🪜" title="Рівні" :count="ed.levels.length" :fold="foldKey('levels')">
            <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('level')"><Icon name="plus" /> рівень</button>
          </SectionHead>
          <LevelsBlock v-show="!folded('levels')" :ref="blocks.level" />
        </section>
      </template>
      <section id="entities" class="mb-4">
        <SectionHead icon="👾" title="Сутності" :count="ed.entities.length" :fold="foldKey('entities')">
          <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('entity')"><Icon name="plus" /> сутність</button>
        </SectionHead>
        <div v-show="!folded('entities')">
          <DraftStrip :kinds="['mechanic']" hint="привʼяжи до сутності: натисни на картку → «Перемістити»" />
          <EntitiesBlock :ref="blocks.entity" />
        </div>
      </section>
      <section v-if="!ed.simple" id="rules" class="mb-4">
        <SectionHead icon="⚡" title="Правила" :count="rules.length" :fold="foldKey('rules')">
          <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('rule')"><Icon name="plus" /> правило</button>
        </SectionHead>
        <div v-show="!folded('rules')">
          <DraftStrip :kinds="['rule']" hint="натисни на картку → «нове правило з цієї картки» або привʼяжи до наявного" />
          <RulesBlock :ref="blocks.rule" />
        </div>
      </section>
      <section id="windows" class="mb-4">
        <SectionHead icon="🪟" :title="ed.simple ? 'Вікна' : 'Вікна й меню'" :count="ed.windows.length" :fold="foldKey('windows')">
          <button v-if="editable" type="button" class="btn btn-sm btn-add" @click="open('window')"><Icon name="plus" /> вікно</button>
        </SectionHead>
        <div v-show="!folded('windows')">
          <DraftStrip :kinds="['element']" hint="привʼяжи до вікна: натисни на картку → «Перемістити»" />
          <WindowsBlock :ref="blocks.window" />
        </div>
      </section>
      <template v-if="!ed.simple">
        <section v-for="z in ZONES" :id="z.id" :key="z.id" class="mb-4">
          <SectionHead :icon="z.icon" :title="z.title" :count="inZone(z)" :fold="foldKey(z.id)" />
          <ZoneSection v-show="!folded(z.id)" :zones="z.zones" :hint="z.hint" />
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
