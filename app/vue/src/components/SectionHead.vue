<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { ALL_HOW, toAll } from '@core/allkey.js'
import HashLink from '@core/components/HashLink.vue'
import Icon from '@core/components/Icon.vue'
import { vToStart } from '@core/toStart.js'
import { zones } from '../catalog.js'
import { useEd } from '../ed.js'
import { allMode, isFolded, isShort, ownShort, toggleFold, toggleShort } from '@core/fold.js'
import { canCols, modeOf } from '../layout.js'
import { cards, CARDS, ROWS, rows } from '../looks.js'
import ColsSwitch from './ColsSwitch.vue'
import LookSwitch from './LookSwitch.vue'
import WideSwitch from './WideSwitch.vue'

// a section's heading in the editor: icon and title, a count, a muted note, and the section's own actions on the right;
// with `fold` (the key it is remembered by, fold.js) a chevron leads the title and a click on either folds the section,
// and a quiet button at the end shows the section in short or in full (T284 §3) — its icon says which it is now;
// `zone` — the catalog category the section belongs to: a bar of its colour before the title (T278 §9);
// the page's width is switched from every heading, and `layout` — the section lays cards in columns — adds the switch of
// its own columns (T291 §1, T294 §1–2); `anchor` — the section's id: a link to it by the title (T291 §11), the key of its
// own columns and of its rows (T296 §6); `cardFold` — its cards fold to their heads, the switch of that too (T296 §7).
// A switch is blue while its section differs from the top row — the default (T298); ⌥-click on any of them, the chevron
// too, or a long press on it, does the same in every section (allkey.js); held ⌥ rings them all under the mouse.
// An explanation put away inside the section leaves its icon by the title (`tip-dock`, Tip.vue).
// The heading sticks under the menu while its section is on screen: the reader sees where they are and can fold it away;
// a click on its empty space while it is stuck goes back to the section's start (T306, toStart.js).
// `catalog` — the catalog's cards the section is about (sections.js catalogOf, T318): a quiet sign opens them in a window
// over the page; it is a link too — ⌘-click takes the same category to «Таски» in a new tab
const props = defineProps({ icon: String, title: String, count: [Number, String], note: String, fold: String, zone: String, layout: Boolean, anchor: String, cardFold: Boolean,
                            catalog: Object })
const ed = useEd()
const router = useRouter()
const looks = computed(() => !ed?.has || ed.has('looks'))  // the reader's switches wait for «Налаштування вигляду» (T319): the base keeps a heading calm
const tasksHref = computed(() => (props.catalog ? router.resolve(props.catalog.to).href : ''))
const el = ref()
const WORD = { open: 'повністю', short: 'коротко', folded: 'згорнуто' }
const shortTip = (key) => `${isShort(key) ? 'Зараз коротко: видно початок секції — показати всю' : 'Зараз уся секція — показати коротко, лише початок'}`
  + `${ownShort(key) ? ` (угорі — ${WORD[allMode(key.split(':')[0])]})` : ''} · ${ALL_HOW} — у всіх секціях`

// a change made from the heading — folding, short, other columns, another width — moves everything around it; the reader
// stays at this section: a stuck heading keeps its section right under the menu, a heading in the flow keeps its place
// in the window. The layout settles over a few frames (columns are dealt again), so the place is held through them
async function keep(change) {
  const sec = el.value.closest('section')
  const nav = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 0
  const stuck = sec.getBoundingClientRect().top < nav - 1
  const y = el.value.getBoundingClientRect().top
  change()
  for (let i = 0; i < 12 && el.value; i++) {
    await new Promise(requestAnimationFrame)
    const off = stuck ? sec.getBoundingClientRect().top - nav : el.value.getBoundingClientRect().top - y
    if (Math.abs(off) > 1) scrollBy({ top: off, behavior: 'instant' })
  }
}
</script>

<template>
  <h2 ref="el" v-to-start="'секції'" class="h6 head d-flex flex-wrap align-items-center gap-2" data-all-host>
    <span v-if="zones[zone]" class="bar" :style="{ background: zones[zone].color }" :title="`категорія каталогу: ${zones[zone].title}`" />
    <component :is="fold ? 'button' : 'span'" :type="fold ? 'button' : null" class="name" :class="{ 'fold every every-start': fold }"
               :aria-expanded="fold ? !isFolded(fold) : null" :title="fold ? `${isFolded(fold) ? 'Розгорнути' : 'Згорнути'} секцію · ${ALL_HOW} — усі секції` : null"
               :data-all="fold ? `${isFolded(fold) ? 'розгорнути' : 'згорнути'} всі секції` : null"
               @click="(e) => fold && keep(() => toggleFold(fold, toAll(e)))">
      <Icon v-if="fold" :name="isFolded(fold) ? 'right' : 'down'" class="chev" />
      {{ icon }} {{ title }} <span v-if="count !== undefined" class="count">({{ count }})</span>
    </component>
    <HashLink v-if="anchor" :id="anchor" class="hash" />
    <span class="tip-dock" />
    <span v-if="note" class="note">{{ note }}</span>
    <span class="ms-auto d-flex align-items-center gap-1">
      <slot :keep />
      <template v-if="!(fold && isFolded(fold))">
        <a v-if="catalog && ed" :href="tasksHref" target="_blank" rel="noopener" class="iact dim"
           title="Картки каталогу для цієї секції — у вікні над сторінкою&#10;⌘- чи Ctrl-клік — та сама категорія на «Тасках», у новій вкладці"
           @click.exact.prevent="ed.catalog(catalog)"><Icon name="puzzle" /></a>
        <template v-if="looks">
        <ColsSwitch v-if="layout" quiet :scope="anchor" :around="keep" />
        <LookSwitch v-if="layout && canCols" quiet :look="rows" :modes="ROWS" label="Розкладка" :scope="anchor" :around="keep"
                    :off="modeOf(anchor) === 'one' ? 'Один стовпець — рядами нема чого вирівнювати' : ''" />
        <LookSwitch v-if="cardFold" quiet :look="cards" :modes="CARDS" label="Картки" :scope="anchor" :around="keep" />
        <WideSwitch quiet :around="keep" />
        </template>
      </template>
      <button v-if="looks && fold && !isFolded(fold)" type="button" class="iact every" :class="ownShort(fold) ? 'on' : 'dim'" :aria-pressed="isShort(fold)"
              :title="shortTip(fold)" :data-all="`у всіх секціях: ${isShort(fold) ? 'повністю' : 'коротко'}`"
              @click="(e) => keep(() => toggleShort(fold, toAll(e)))">
        <Icon :name="isShort(fold) ? 'short' : 'lines'" />
      </button>
    </span>
  </h2>
</template>

<style scoped>
/* stuck under the menu, over the section's own content; wider than the column by its padding, so nothing shows beside it */
.head { position: sticky; top: var(--nav-h, 0px); z-index: 20; min-height: var(--stick-h, 2.6rem); margin: 0 -.5rem .5rem; padding: .25rem .5rem; border-bottom: 1px solid var(--bs-border-color);
        background: var(--bs-body-bg); font-weight: 700; }
.bar { width: 4px; height: 1.2em; margin-right: -.2rem; border-radius: 2px; }
.name.fold { padding: 0; border: 0; background: none; color: inherit; font: inherit; text-align: start; }
.chev { font-size: .85em; opacity: .55; }
.name.fold:hover .chev { opacity: 1; }
.count { font-weight: 400; opacity: .55; }
.note { font-size: .8rem; font-weight: 400; color: var(--bs-secondary-color); }
/* the link to the section waits for the mouse over the heading; a finger has no hover — there it is pale, not absent */
.hash { margin-left: -.3rem; }
@media (hover: hover) { .head:not(:hover) .hash:not(.done) { opacity: 0; } }
/* a switch at rest is a pale grey drawing (T291 §2) — the same drawing wears colour when its section differs from the
   top row (T298): short — the two lines that are shown take the colour of «Показати все», the two cut ones fade (Icon `short`) */
.head :deep(.iact.dim) { color: color-mix(in srgb, var(--bs-secondary-color) 60%, transparent); }
.head :deep(.iact.dim:hover) { color: var(--bs-body-color); }
.head :deep(.iact.on) { background: color-mix(in srgb, var(--bs-link-color) 12%, transparent); color: var(--bs-link-color); }
</style>
