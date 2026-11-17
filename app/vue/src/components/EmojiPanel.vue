<script setup>
import { computed, nextTick, onMounted, ref, shallowRef, watch } from 'vue'

import { iconOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { loadEmoji } from '../emoji/load.js'
import { fits, remember, sections } from '../emoji/sections.js'
import { stepTo } from '../emoji/walk.js'
import EmojiColors from './EmojiColors.vue'
import EmojiFoot from './EmojiFoot.vue'
import EmojiTabs from './EmojiTabs.vue'

// the emoji picker's panel (T309), inside a Pop: a search over names and words in three languages (emoji/search.js), a
// colour filter, the groups as a strip of signs, the grid and a line that names the icon in hand. Without a query the
// grid starts with the icons offered by `hint` (the entity's name and type) and the last picked ones; with one — the
// found, the best first: the arrows walk them, Enter takes. A text that finds nothing can be taken as it is — any emoji
// or symbol of one's own. An icon another entity of the game wears has a dot. Emits pick(char); '' — back to the type's
// `fallback`. `legend` — for a storyboard's legend: no letters, digits or punctuation
const p = defineProps({ icon: String, fallback: String, hint: String, legend: Boolean })
const emit = defineEmits(['pick'])
const ed = useEd()
const data = shallowRef(null)
const q = ref('')
const color = ref('')
const cursor = ref(-1)  // the cell the keys hold, an index in `flat`
const hover = ref(-1)
const walking = ref(false)  // the arrows have taken the grid: ← → walk it too, until the next letter
const at = ref('')
const input = ref()
const list = ref()

const view = computed(() => (data.value ? sections(data.value, { q: q.value, color: color.value, hint: p.hint, legend: p.legend }) : { list: [], why: new Map() }))
const parts = computed(() => { let n = 0; return view.value.list.map((s) => ({ ...s, start: (n += s.items.length) - s.items.length })) })
const flat = computed(() => view.value.list.flatMap((s) => s.items))
const shown = computed(() => flat.value[hover.value >= 0 ? hover.value : cursor.value])
const own = computed(() => { const t = q.value.trim(); return !flat.value.length && t && [...t].length <= 16 && fits(t, p.legend) ? t : '' })
const live = computed(() => new Set(q.value.trim() ? data.value?.groups.map((g) => g.key) : view.value.list.map((s) => s.key)))
// who else in the game wears an icon: char → that entity's name
const taken = computed(() => new Map((ed?.entities || []).filter((e) => iconOf(e) !== (p.icon || p.fallback)).map((e) => [iconOf(e), e.title])))

watch([q, color], () => {
  cursor.value = q.value.trim() ? 0 : -1
  hover.value = -1
  if (list.value) list.value.scrollTop = 0
})
onMounted(async () => {
  if (!matchMedia('(pointer: coarse)').matches) input.value.focus({ preventScroll: true })  // a phone's keyboard would cover the sheet
  data.value = await loadEmoji()
})

function pick(char) {
  if (char) remember(char)
  emit('pick', char)
}
const cell = (e) => Number(e.target.closest?.('.em')?.dataset.i ?? -1)
function key(e) {
  const step = { ArrowDown: 'down', ArrowUp: 'up', ArrowRight: 1, ArrowLeft: -1 }[e.key]
  if (e.key === 'Enter') {
    e.preventDefault()
    e.stopPropagation()  // not the form's Enter around the picker
    const char = flat.value[cursor.value]?.char || own.value
    if (char) pick(char)
  } else if (step && (typeof step === 'string' || walking.value || !q.value)) {
    e.preventDefault()
    walking.value = true
    const cells = [...list.value.querySelectorAll('.em')]
    cursor.value = stepTo(cells, cursor.value, step)
    hover.value = -1
    cells[cursor.value]?.scrollIntoView({ block: 'nearest' })
  }
}
async function go(key) {
  q.value = ''
  await nextTick()
  list.value.scrollTop = list.value.querySelector(`[data-g="${key}"]`)?.offsetTop || 0
}
function spy() {  // the group in view; the rows above the groups («за назвою», «нещодавні») are the first group's
  const heads = [...list.value.querySelectorAll('[data-g]')].filter((h) => data.value.groups.some((g) => g.key === h.dataset.g))
  at.value = (heads.findLast((h) => h.offsetTop <= list.value.scrollTop + 4) || heads[0])?.dataset.g || ''
}
watch(parts, () => nextTick(spy))
</script>

<template>
  <div class="ep">
    <input ref="input" v-model="q" class="form-control form-control-sm" placeholder="пошук: ключ, wall, серденько, червоний…" autocomplete="off"
           spellcheck="false" aria-label="пошук значка" @keydown="key" @input="walking = false">
    <EmojiColors v-model="color" />
    <EmojiTabs :groups="data?.groups || []" :at :live @go="go" />
    <div ref="list" class="list" @scroll.passive="spy" @mousedown.prevent @click="flat[cell($event)] && pick(flat[cell($event)].char)"
         @mouseover="hover = cell($event)" @mouseleave="hover = -1">
      <div v-if="view.as" class="note">за «{{ q.trim() }}» нічого — показую «{{ view.as }}» (інша розкладка)</div>
      <section v-for="s in parts" :key="s.key" :data-g="s.key">
        <div class="grp">{{ s.title }}</div>
        <div class="cells">
          <button v-for="(it, n) in s.items" :key="it.char" type="button" tabindex="-1" class="em" :data-i="s.start + n" :aria-label="it.uk"
                  :class="{ on: it.char === icon, act: s.start + n === cursor, taken: taken.has(it.char) }">{{ it.char }}</button>
        </div>
      </section>
      <div v-if="!data" class="note">завантажую значки…</div>
      <div v-else-if="own" class="note">Такого в переліку нема. <button type="button" class="own" @click.stop="pick(own)">взяти «{{ own }}» як є</button> — або Enter</div>
      <div v-else-if="!flat.length" class="note">Нічого не знайшлось{{ color ? ' цього кольору' : '' }} — спробуй інше слово.</div>
    </div>
    <EmojiFoot :item="shown" :now="data?.by.get(icon || fallback)" :why="view.why.get(shown)" :taken="shown && taken.get(shown.char)" :q="view.as || q" :icon :fallback @reset="pick('')" />
  </div>
</template>

<style scoped>
.ep { display: flex; flex-direction: column; gap: .35rem; }
.list { position: relative; height: min(15.5rem, 42vh); margin-inline: -.3rem; padding-inline: .3rem; overflow-y: auto; overscroll-behavior: contain; }
.grp { position: sticky; top: 0; z-index: 1; padding: .3rem 0 .1rem; background: var(--bs-body-bg); font-size: .65rem; font-weight: 700; letter-spacing: .04em;
       text-transform: uppercase; color: var(--bs-secondary-color); }
.cells { display: grid; grid-template-columns: repeat(auto-fill, minmax(2rem, 1fr)); }
.em { position: relative; height: 2rem; padding: 0; overflow: hidden; border: 0; border-radius: .3rem; background: none; color: inherit; font-size: 1.3rem; line-height: 1; }
.em:hover { background: var(--bs-tertiary-bg); }
.em.on { background: var(--bs-secondary-bg); }
.em.act { box-shadow: inset 0 0 0 2px color-mix(in srgb, var(--bs-primary) 70%, transparent); }
.em.taken::after { content: ''; position: absolute; top: .12rem; right: .12rem; width: .34rem; height: .34rem; border-radius: 50%; background: var(--bs-warning); }
.note { padding: .5rem .1rem; font-size: .8rem; color: var(--bs-secondary-color); }
.own { padding: 0; border: 0; background: none; color: var(--bs-link-color); text-decoration: underline dotted; }
</style>
