<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { postClaim } from '../api.js'
import { COINS, kidsOf, missingParams, STATUSES } from '../catalog.js'
import { claimedSlugs, myGame, reloadInsides } from '../myGame.js'
import { hl, norm } from '../taskFilter.js'
import { user } from '@core/user.js'
import CoinBadge from './CoinBadge.vue'
import Md from './Md.vue'
import SlotFields from './SlotFields.vue'

const props = defineProps({ task: Object })
const open = ref(false)
const route = useRoute()
const q = computed(() => route.query.q || '')
const kids = computed(() => kidsOf.value[props.task.slug] || [])
// family shows the min‥max range of its children's coins instead of the card's reference coin
const range = computed(() => {
  const present = Object.keys(COINS).filter((c) => kids.value.some((k) => k.coin === c))
  if (!present.length) return []
  return present.length === 1 || present[0] === present.at(-1) ? [present[0]] : [present[0], present.at(-1)]
})
// the search hit is somewhere inside (description, aliases, children): open so it is visible
watch(q, (v) => { if (v && !norm(props.task.title).includes(norm(v))) open.value = true }, { immediate: true })

// «＋ у гру»: a student with a game adds the card to it from here — to the game level or the drafts, params first if required
const canAdd = computed(() => myGame.value && !kids.value.length && !props.task.tags.includes('window') && props.task.status === 'active')
const inGame = computed(() => claimedSlugs.value.has(props.task.slug))
const asking = ref(false)
const params = ref({})
const busy = ref(false)
const error = ref('')
const ready = computed(() => !missingParams(props.task, params.value).length)
async function add() {
  if (props.task.slots?.length && !asking.value) { asking.value = true; open.value = true; return }
  busy.value = true
  error.value = ''
  try {
    await postClaim({ task: props.task.slug, params: params.value })
    await reloadInsides()
    asking.value = false
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="border rounded mb-1 task" :class="{ stack: kids.length, ['st-' + task.status]: true, 'in-game': inGame }">
    <div class="d-flex align-items-start gap-2 px-2 py-1" role="button" @click="open = !open">
      <span class="title me-auto">
        <span v-html="hl(task.title, q)"></span>
        <span v-if="task.tags.includes('algo')" class="ms-1" title="алгоритмічне — золото">⭐</span>
        <span v-if="task.max_count !== 1" class="ms-1" title="можна зараховувати кілька разів">🔁</span>
        <span v-if="user?.status === 'admin' && task.status !== 'active'"
              class="badge text-bg-light border text-secondary fw-normal ms-1">{{ STATUSES[task.status] }}</span>
      </span>
      <template v-if="canAdd">
        <RouterLink v-if="inGame" to="/my/game" class="add text-success text-decoration-none" title="уже в твоїй грі — відкрити «Мою гру»" @click.stop>✓</RouterLink>
        <button v-else type="button" class="add btn btn-sm py-0 px-1 btn-outline-primary" :disabled="busy" title="＋ у мою гру" @click.stop="add">＋</button>
      </template>
      <span v-if="kids.length" class="badge fam" title="сімʼя: кілька варіантів, кожен зі своєю ціною">×{{ kids.length }}</span>
      <span v-if="kids.length" class="text-nowrap" title="діапазон цін варіантів">
        <template v-for="(c, i) in range" :key="c"><span v-if="i" class="text-secondary">‥</span>{{ COINS[c] }}</template>
      </span>
      <CoinBadge v-else :coin="task.coin" :amount="task.amount" />
    </div>

    <div v-if="open" class="px-2 py-2 border-top rounded-bottom" :class="kids.length ? 'bg-body' : 'bg-body-tertiary'">
      <div v-if="asking" class="d-flex flex-wrap gap-1 align-items-center small mb-2">
        <span class="text-secondary">параметри:</span>
        <SlotFields :specs="task.slots" :params="params" />
        <button class="btn btn-primary btn-sm" :disabled="!ready || busy" @click="add">＋ у гру</button>
        <button class="btn btn-outline-secondary btn-sm" @click="asking = false">✕</button>
        <span v-if="error" class="text-danger">{{ error }}</span>
      </div>
      <div v-else-if="error" class="small text-danger mb-2">{{ error }}</div>
      <div v-if="task.description || user?.status === 'admin'" class="d-flex align-items-start gap-2 mb-2">
        <Md v-if="task.description" :text="task.description" :q="q" class="small flex-grow-1" />
        <RouterLink v-if="user?.status === 'admin'" :to="`/tasks/${task.slug}/edit`"
                    class="ms-auto text-decoration-none" title="Редагувати">✏️</RouterLink>
      </div>
      <div v-if="task.slots?.length" class="small text-secondary mb-2" title="параметри, які вказуються в заявці">
        ⚙️ {{ task.slots.map((s) => s.label + (s.unit ? ` (${s.unit})` : '')).join(' · ') }}
      </div>
      <div v-if="task.aliases?.length" class="small text-secondary mb-2" title="інші назви, за якими картку знаходить пошук">
        🔎 <span v-html="task.aliases.map((a) => hl(a, q)).join(' · ')"></span>
      </div>
      <TaskCard v-for="k in kids" :key="k.id" :task="k" />
      <div v-if="task.max_count !== 1 || task.games.length"
           class="d-flex gap-2 flex-wrap align-items-center small mt-2">
        <span v-if="task.max_count === 0" class="text-secondary">без ліміту повторів</span>
        <span v-else-if="task.max_count > 1" class="text-secondary">до {{ task.max_count }} разів</span>
        <RouterLink v-for="g in task.games" :key="g" :to="`/games/${g}`"
                    class="badge text-bg-light border fw-normal text-decoration-none game-tag">{{ g }}</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.task { background: var(--bs-body-bg); }
/* family looks like a small stack of cards */
.stack { box-shadow: 3px 3px 0 -1px var(--bs-body-bg), 3px 3px 0 0 var(--bs-border-color); }
.fam { background: var(--bs-tertiary-bg); color: var(--bs-secondary-color); border: 1px solid var(--bs-border-color); }
.game-tag { color: var(--bs-link-color); }
.add { line-height: 1.2; font-size: .9rem; }
.in-game { border-color: var(--bs-success-border-subtle); }
/* drafts fade into the background instead of shouting */
.st-draft { border-style: dashed; }
.st-draft > div > .title { color: var(--bs-secondary-color); }
.st-archived { opacity: .5; }
.st-archived > div > .title { text-decoration: line-through; }
</style>
