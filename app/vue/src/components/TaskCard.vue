<script setup>
import { computed, ref, watch } from 'vue'

import InlineText from '@core/components/InlineText.vue'
import { asked } from '../asked.js'
import { COINS, kidsOf, STATUSES } from '../catalog.js'
import { isMore } from '../coreMode.js'
import { useGameCtx } from '../gameCtx.js'
import { hl, norm, useCardsMode, useTaskQuery } from '../taskFilter.js'
import { saveTask } from '../taskForm.js'
import { addable, closedHome } from '../taskMeta.js'
import { covers, isUnfolded, order } from '../unfold.js'
import { user } from '@core/user.js'
import TaskAdd from './TaskAdd.vue'
import TaskBody from './TaskBody.vue'
import TaskCoinPick from './TaskCoinPick.vue'
import TaskEdit from './TaskEdit.vue'
import TaskKidsMark from './TaskKidsMark.vue'
import TaskMoreRow from './TaskMoreRow.vue'
import TierBadge from './TierBadge.vue'

// a card of the catalog: a click on the header unfolds it. Unfolded, the teacher changes the title and the price where they
// read (T306) — elsewhere on the header a click folds it back; the pencil turns it into its form in place and back.
// A card «за запитом» (T319) is pale in a dashed frame; in a family that is partly in the core its variants «за запитом»
// wait behind a row under «Основа», as a subcategory's do
const props = defineProps({ task: Object })
const ctx = useGameCtx()
const admin = computed(() => user.value?.status === 'admin')
const q = useTaskQuery()
const kids = computed(() => kidsOf.value[props.task.slug] || [])
const isAsked = computed(() => asked(props.task))
const { s: mode, coreOnly } = useCardsMode()
const kidsMore = computed(() => (coreOnly.value && !isAsked.value ? kids.value.filter(asked).length : 0))
const kidsShown = computed(() => (kidsMore.value && !isMore(mode, props.task.slug) ? kids.value.filter((k) => !asked(k)) : kids.value))
const scope = computed(() => `${props.task.zone}/${props.task.subzone}`)
const open = ref(isUnfolded(scope.value))
const editing = ref(false)
// a click in the coin's panel, which hangs from the header, is not a click on the header — nor is one begun there: a save
// greys the panel and lets the mouse through, so the release lands beside it
let pressed = null
const press = (e) => (pressed = e.target)
function fold(e) {
  if (![pressed, e.target].some((el) => el?.closest('.pop-panel'))) open.value = !open.value
  pressed = null
}
// a card of a closed feature that is in the game still has its tick: what is filled stays seen (T319)
const inGame = computed(() => ctx.slugs.value.has(props.task.slug) && (addable(props.task) || closedHome(props.task)))
// family shows the min‥max range of its children's coins instead of the card's reference coin
const range = computed(() => {
  const present = Object.keys(COINS).filter((c) => kids.value.some((k) => k.coin === c))
  if (!present.length) return []
  return present.length === 1 || present[0] === present.at(-1) ? [present[0]] : [present[0], present.at(-1)]
})
// the search hit is somewhere inside (description, aliases, children): open so it is visible
watch(q, (v) => { if (v && !norm(props.task.title).includes(norm(v))) open.value = true }, { immediate: true })
watch(order, (o) => { if (covers(scope.value)) open.value = o.open })
</script>

<template>
  <TaskEdit v-if="editing" :task class="mb-1" @done="editing = false" />
  <div v-else class="border rounded mb-1 task" :class="{ stack: kids.length, ['st-' + task.status]: true, 'in-game': inGame, asked: isAsked }">
    <div class="d-flex align-items-start gap-2 px-2 py-1" role="button" @mousedown="press" @click="fold">
      <span class="title me-auto">
        <span v-if="task.icon" class="me-1">{{ task.icon }}</span>
        <InlineText :value="task.title" :can="admin && open" required placeholder="Назва" :save="(title) => saveTask(task, { title })">
          <span v-html="hl(task.title, q)"></span>
        </InlineText>
        <span v-if="task.tags.includes('algo')" class="ms-1" title="алгоритмічне — золото">⭐</span>
        <TierBadge :task class="ms-1" />
        <span v-if="admin && task.status !== 'active'"
              class="badge text-bg-light border text-secondary fw-normal ms-1">{{ STATUSES[task.status] }}</span>
        <span v-if="isAsked" class="ask-tag ms-1"
              title="Цієї картки ще нема в основі курсу: додати можна з одним реченням, монетка — коли викладач відкриє картку">за запитом</span>
      </span>
      <TaskAdd v-if="!kids.length" :task :in-game="inGame" />
      <TaskKidsMark v-else :task />
      <span v-if="kids.length" class="badge fam" title="сімʼя: кілька карток усередині, кожна зі своєю ціною">×{{ kids.length }}</span>
      <span v-if="kids.length" class="text-nowrap" title="діапазон цін варіантів">
        <template v-for="(c, i) in range" :key="c"><span v-if="i" class="text-secondary">‥</span>{{ COINS[c] }}</template>
      </span>
      <TaskCoinPick v-else :task :can="admin && open && !!task.coin" />
    </div>
    <TaskBody v-if="open" :task :family="kids.length > 0" :q @edit="editing = true">
      <TaskCard v-for="k in kidsShown" :key="k.id" :task="k" />
      <TaskMoreRow :scope="task.slug" :n="kidsMore" class="mb-1" />
    </TaskBody>
  </div>
</template>

<style scoped>
.task { background: var(--bs-body-bg); }
/* family looks like a small stack of cards */
.stack { box-shadow: 3px 3px 0 -1px var(--bs-body-bg), 3px 3px 0 0 var(--bs-border-color); }
.fam { background: var(--bs-tertiary-bg); color: var(--bs-secondary-color); border: 1px solid var(--bs-border-color); }
/* already in the student's game: the tick's green, faintly, over the whole card */
.in-game { border-color: color-mix(in srgb, var(--bs-success) 50%, var(--bs-body-bg));
           background: color-mix(in srgb, var(--bs-success) 7%, var(--bs-body-bg)); }
/* drafts fade into the background instead of shouting */
.st-draft { border-style: dashed; }
.st-draft > div > .title { color: var(--bs-secondary-color); }
.st-archived { opacity: .5; }
/* «за запитом» (T319): pale in a dashed frame, a quiet word by the title */
.asked { border-style: dashed; }
.asked > div > .title { opacity: .72; }
.ask-tag { padding: 0 .3rem; border: 1px dashed var(--bs-border-color); border-radius: .25rem; color: var(--bs-secondary-color);
           font-size: .68rem; font-weight: 400; white-space: nowrap; cursor: help; }
.st-archived > div > .title { text-decoration: line-through; }
</style>
