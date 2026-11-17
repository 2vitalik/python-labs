<script setup>
import { computed, nextTick, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { useEd } from '../ed.js'
import { BASE, FEATURES, GROUPS } from '../features.js'
import FeatureRow from './FeatureRow.vue'

// «Можливості» (T319): what the game page holds beyond its base — all at once («Усе»), back to the base, or one by one.
// Turning off takes away only the empty: what has data stays, so nothing filled is ever hidden. The owner's only (GameEditor).
// Everything is in sight at once (T344): the names in two columns, a row each; what a row adds reads at the panel's foot
// while the mouse is on it — nothing to scroll, nothing moves
const ed = useEd()
const open = ref(false)
const busy = ref(false)
const hint = ref(null)  // the row under the mouse: { icon, title, text }
const TITLE = Object.fromEntries(GROUPS)
const COLS = [['entities', 'rules', 'windows', 'page'], ['sections']]  // the long group stands alone: the columns come out even
const cols = COLS.map((ids) => ids.map((id) => ({ id, title: TITLE[id], list: FEATURES.filter((f) => f.group === id) })))
const count = computed(() => FEATURES.filter((f) => ed.has(f.id)).length)
const ids = (fn) => FEATURES.filter(fn).map((f) => f.id)
const more = computed(() => ids((f) => !ed.has(f.id) && ed.offers(f.id)))
const less = computed(() => ids((f) => ed.has(f.id) && !ed.filled(f.id)))
const button = ref()
// a tile above may come or go with a feature (T348): the page scrolls by as much, and the panel stays under the mouse
async function run(fn) {
  busy.value = true
  const was = button.value.getBoundingClientRect().top
  await fn()
  await nextTick()
  const shift = button.value.getBoundingClientRect().top - was
  if (shift) scrollBy({ top: shift, behavior: 'instant' })
  busy.value = false
}
</script>

<template>
  <Pop v-model="open" width="35rem">
    <template #trigger="{ toggle }">
      <button ref="button" type="button" class="btn btn-sm btn-outline-secondary" :aria-expanded="open" title="Що ще описати в грі: усе одразу чи галочками" @click="toggle">
        <Icon name="layers" /> Можливості <span class="cnt">{{ count ? `основа + ${count}` : 'основа' }}</span>
      </button>
    </template>
    <div class="fp vstack gap-2" @mouseleave="hint = null">
      <div class="d-flex flex-wrap gap-2">
        <button type="button" class="btn btn-sm btn-add py-0" :disabled="busy || !more.length" title="Увімкнути все, що відкрито"
                @click="run(() => ed.turn(more, true))"><Icon name="plus" /> Усе</button>
        <button type="button" class="btn btn-sm btn-outline-secondary py-0" :disabled="busy || !less.length" title="Прибрати все порожнє — заповнене лишається"
                @click="run(() => ed.turn(ids((f) => !ed.filled(f.id)), false))">Лише основа</button>
      </div>
      <div class="base">
        <span class="group-cap">Основа — є завжди</span>
        <span v-for="[title, text] in BASE" :key="title" class="b" @mouseenter="hint = { title, text }">{{ title }}</span>
      </div>
      <div class="cols">
        <div v-for="(col, i) in cols" :key="i" class="vstack gap-2">
          <div v-for="g in col" :key="g.id">
            <div class="group-cap">{{ g.title }}</div>
            <FeatureRow v-for="f in g.list" :key="f.id" :f :busy :run @mouseenter="hint = f" @focusin="hint = f" />
          </div>
        </div>
      </div>
      <div class="foot" aria-live="polite">
        <template v-if="hint"><b>{{ hint.icon }} {{ hint.title }}</b> — {{ hint.text }}</template>
        <template v-else>Наведи на рядок — тут буде, що він додає. Вимкнути можна лише порожнє: заповнене лишається на сторінці.</template>
      </div>
    </div>
  </Pop>
</template>

<style scoped>
.cnt { font-size: .75rem; opacity: .7; }
.fp { font-size: .82rem; }
.base { display: flex; flex-wrap: wrap; align-items: center; gap: .1rem .6rem; padding: .25rem .5rem; border-radius: .375rem; background: var(--bs-tertiary-bg); font-size: .78rem; }
.b { font-weight: 600; white-space: nowrap; cursor: default; }
.cols { display: grid; grid-template-columns: 1fr 1fr; column-gap: 1.25rem; }
/* two lines tall whatever it says: the panel keeps its height while the mouse goes down the rows */
.foot { min-height: 2.6rem; padding-top: .35rem; border-top: 1px dashed var(--bs-border-color); color: var(--bs-secondary-color); font-size: .76rem; line-height: 1.35; }
.foot b { font-weight: 600; color: var(--bs-body-color); }
/* a phone has one column, and its sheet (Pop) scrolls */
@media (max-width: 575px) { .cols { grid-template-columns: 1fr; row-gap: .5rem; } }
</style>
