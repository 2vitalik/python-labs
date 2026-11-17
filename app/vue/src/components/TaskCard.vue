<script setup>
import { computed, ref, watch } from 'vue'

import InlineText from '@core/components/InlineText.vue'
import { COINS, kidsOf, STATUSES } from '../catalog.js'
import { useGameCtx } from '../gameCtx.js'
import { hl, norm, useTaskQuery } from '../taskFilter.js'
import { saveTask } from '../taskForm.js'
import { addable } from '../taskMeta.js'
import { covers, isUnfolded, order } from '../unfold.js'
import { user } from '@core/user.js'
import TaskAdd from './TaskAdd.vue'
import TaskBody from './TaskBody.vue'
import TaskCoinPick from './TaskCoinPick.vue'
import TaskEdit from './TaskEdit.vue'
import TaskKidsMark from './TaskKidsMark.vue'
import TierBadge from './TierBadge.vue'

// a card of the catalog: a click on the header unfolds it. Unfolded, the teacher changes the title and the price where they
// read (T306) — elsewhere on the header a click folds it back; the pencil turns it into its form in place and back
const props = defineProps({ task: Object })
const ctx = useGameCtx()
const admin = computed(() => user.value?.status === 'admin')
const q = useTaskQuery()
const kids = computed(() => kidsOf.value[props.task.slug] || [])
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
const inGame = computed(() => ctx.slugs.value.has(props.task.slug) && addable(props.task))
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
  <div v-else class="border rounded mb-1 task" :class="{ stack: kids.length, ['st-' + task.status]: true, 'in-game': inGame }">
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
      <TaskCard v-for="k in kids" :key="k.id" :task="k" />
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
.st-archived > div > .title { text-decoration: line-through; }
</style>
