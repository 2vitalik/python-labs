<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

import { toTop } from '@core/anchors.js'
import Icon from '@core/components/Icon.vue'
import LabTabs from '@core/components/LabTabs.vue'
import { loadGuide, pages } from '@core/guide.js'
import { user } from '@core/user.js'
import { wideOf } from '@core/wide.js'

import '../labColors.css'
import { gates, loadGates } from '../labGates.js'
import { labsWithCards, loadLabPages } from '../labPages.js'
import { rowGone } from '../labRow.js'
import { LABS } from '../site.js'
import LabStrip from './LabStrip.vue'

// a lab's bar on the shelf under the menu (App.vue), on every page of the lab: the numbers of the labs, the lab's pages
// (LabStrip), «Моя лаба» and the teacher's «Результати» — one row on any screen. A link to the page open now, or the
// bar's empty space once the page is scrolled, goes to the top. Its height stands before its data: nothing under it moves.
// `row` — the page lays the pills in a row of its own (LabRow): the bar shows them only once that row has gone under the
// shelf, in the room kept for them all along (T381). The open lab's number is filled with its colour (labColors.css)
const props = defineProps({ row: Boolean })
const pills = computed(() => !props.row || rowGone.value)
const route = useRoute()
const about = computed(() => !!route.meta.about)
const n = computed(() => (about.value ? 0 : Number(route.params.n)))
const at = computed(() => (about.value ? '' : ['my', 'results'].find((k) => route.path.split('/')[3] === k) || ''))
const admin = computed(() => user.value?.status === 'admin')
const wide = computed(() => !!wideOf(route.meta.wide)?.on.value)  // as App.vue's <main>
const held = ref([])
const ready = ref(false)
Promise.all([loadGuide(), loadGates(), labsWithCards().then((l) => (held.value = l)), loadLabPages().catch(() => null)])
  .then(() => (ready.value = true))
const cards = (k) => held.value.some((l) => l.n === k)
// a student has no page of a hidden lab, the teacher has; from «Моя лаба» or «Результати» a number leads to the same
// page of that lab while it has cards
const labs = computed(() => LABS.filter((l) => pages.value[l.slug])
  .map((l) => ({ ...l, path: at.value && cards(l.n) ? `${l.path}/${at.value}` : l.path })))
// at the right end: the address · the word · its drawing · the colour. The teacher's two are drawings with the word under
// the mouse: in words they push a lab's seven pages out of the page column; a student's one button keeps its word
const ends = computed(() => [['my', 'Моя лаба', 'card', 'btn-outline-primary'], ...(admin.value ? [['results', 'Результати', 'table', 'btn-outline-secondary']] : [])])

const free = ref(false)
const isFree = (e) => scrollY > 0 && !e.target.closest('a, button')
function click(e) {
  const a = e.target.closest('a')
  if (a ? a.pathname === location.pathname : isFree(e)) toTop()
}
</script>

<template>
  <Teleport defer to="#top-shelf">
    <nav class="lab-bar" :class="[{ free }, n ? `lab-c${n}` : '']" :title="free ? 'Нагору' : null" aria-label="Лаба"
         @click="click" @mousemove="free = isFree($event)" @mouseleave="free = false">
      <div class="in" :class="wide ? 'container-fluid px-4' : 'page'">
        <template v-if="ready">
          <!-- a LabTabs a number: a lab hidden from students is pale -->
          <span class="nums" :class="{ bare: admin }"><LabTabs v-for="(l, i) in labs" :key="l.n" :labs="[l]" :n :class="[`lab-c${l.n}`, { more: i, shut: gates[l.n] === 'hidden' }]" /></span>
          <LabStrip :n :class="{ away: !pills }" />
          <span v-if="cards(n)" class="ends btn-group btn-group-sm" :class="{ two: admin }">
            <RouterLink v-for="[k, word, pic, look] in ends" :key="k" :to="`/labs/${n}/${k}`" class="btn" :class="[look, { active: at === k }]"
                        :aria-label="word" :title="admin ? word : null"><Icon :name="pic" /><span>{{ word }}</span></RouterLink>
          </span>
        </template>
      </div>
    </nav>
  </Teleport>
</template>

<style scoped>
.lab-bar { border-bottom: 1px solid var(--bs-border-color); background: var(--bs-body-bg); }
.lab-bar.free { cursor: pointer; }
.in { display: flex; align-items: center; gap: .75rem; height: 2.5rem; }
.nums { display: flex; flex: none; align-items: center; gap: .2rem; }
.more :deep(.cap), .bare :deep(.cap) { display: none; }  /* the teacher's five numbers leave the caption's room to the pages */
.shut { opacity: .45; }
/* only the open lab wears its colour, filled: which one is pressed reads at once. Another lab's colour shows under the
   mouse, pale — where it leads (over LabTabs' own blue) */
.nums :deep(.tab.on) { border-color: var(--lab); background: var(--lab); }
.nums :deep(.tab:not(.on):hover) { border-color: color-mix(in srgb, var(--lab) 45%, var(--bs-border-color));
                                   background: color-mix(in srgb, var(--lab) var(--lab-pale), var(--bs-body-bg)); }
.ends { flex: none; }
.btn { white-space: nowrap; }
.btn .icon { display: none; }
.two .btn { padding-inline: .6rem; }
.two .icon { display: inline-block; }
.two .btn span { display: none; }
@media (max-width: 575.98px) {
  .in { gap: .5rem; }
  .nums :deep(.cap) { display: none; }
}
@media (pointer: coarse) { .nums :deep(.tab) { min-width: 1.75rem; line-height: 1.75rem; } }  /* a finger: taller to tap */
@media print { .lab-bar { display: none; } }
</style>
