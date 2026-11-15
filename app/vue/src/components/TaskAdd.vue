<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { postClaim } from '../api.js'
import { myPlaces } from '../claimPlace.js'
import { addPart, addsMore, addStat, plusOf } from '../gameAdd.js'
import { myClaims, myGame, reloadInsides } from '../myGame.js'
import { addable, addsTo, drawn } from '../taskMeta.js'
import { factorOf, factorText, roomFor } from '../tiers.js'
import TaskAddParams from './TaskAddParams.vue'
import TaskAddPart from './TaskAddPart.vue'
import TaskAddStat from './TaskAddStat.vue'

// the round mark in a card's header for a student with a game: the violet plus «у мою гру», the green tick once the card is
// in (an entity type keeps a small plus beside it — «ще одну»; so does a card with repeats while one more still counts,
// T291 §13). What the plus does depends on the card's kind (gameAdd.js); a question it asks first — in a panel at it
const props = defineProps({ task: Object, inGame: Boolean })
const count = computed(() => myClaims.value.filter((c) => c.task === props.task.slug).length)
const canAdd = computed(() => props.task.status === 'active' && !drawn(props.task) && (!props.inGame || addsMore(props.task) || roomFor(props.task, count.value)))
const moreTitle = computed(() => {
  if (addsMore(props.task)) return 'Ще одну сутність цього типу'
  const price = factorText(factorOf(props.task, count.value + 1))
  return `Ще раз — повтор (${count.value + 1}-й)${price ? `\nза ${price} ціни` : ''}`
})
const shown = computed(() => !!myGame.value && addable(props.task) && (props.inGame || canAdd.value))
const places = computed(() => (props.inGame ? myPlaces(props.task.slug) : []))
const where = ref(false)
const open = ref(false)
const plus = ref({})
const busy = ref(false)
const error = ref('')

function add() {
  error.value = ''
  plus.value = plusOf(props.task)
  if (plus.value.ask) open.value = !open.value
  else write(plus.value.run)
}
async function write(run) {
  busy.value = true
  error.value = ''
  try {
    await run()
    await reloadInsides()
    open.value = false
  } catch (e) {
    error.value = e.message
    open.value = true
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <span v-if="shown" class="marks" @click.stop>
    <Pop v-if="canAdd" v-model="open" width="20rem">
      <template #trigger>
        <button type="button" class="iact round add" :class="{ more: inGame }" :disabled="busy" @click="add"
                :title="inGame ? moreTitle : `Додати у мою гру\n${addsTo(task)}`">
          <Icon name="plus" />
        </button>
      </template>
      <TaskAddPart v-if="plus.ask === 'part'" :task :busy @send="(form) => write(() => addPart(task, form))" @cancel="open = false" />
      <TaskAddStat v-else-if="plus.ask === 'stat'" :task :busy @send="(parts, value) => write(() => addStat(task, parts, value))"
                   @cancel="open = false" />
      <TaskAddParams v-else-if="plus.ask === 'params'" :task :busy @send="(params) => write(() => postClaim({ task: task.slug, params }))"
                     @cancel="open = false" />
      <template v-else-if="plus.ask === 'replace'">
        <div class="small mb-2">Зараз: «{{ plus.opt.now }}». Замінити на «{{ plus.opt.name }}»?</div>
        <div class="d-flex gap-2">
          <button type="button" class="btn btn-sm btn-success" :disabled="busy" @click="write(plus.run)"><Icon name="check" /> Замінити</button>
          <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false">Скасувати</button>
        </div>
      </template>
      <div v-if="error" class="text-danger small" :class="{ 'mt-2': plus.ask }">{{ error }}</div>
    </Pop>
    <!-- the tick leads to the card's place in the game; a card that sits in several — to a list of them -->
    <Pop v-if="inGame && places.length > 1" v-model="where" width="17rem">
      <template #trigger>
        <button type="button" class="iact round done many" :title="`уже в твоїй грі — у ${places.length} місцях: показати де`" @click="where = !where">
          <Icon name="done" /><sup>{{ places.length }}</sup>
        </button>
      </template>
      <div class="cap">у твоїй грі</div>
      <RouterLink v-for="p in places" :key="p.id" :to="{ path: '/my/game', hash: `#${p.id}` }" class="place"><span>{{ p.text }}</span><Icon name="arrow" /></RouterLink>
    </Pop>
    <RouterLink v-else-if="inGame" :to="{ path: '/my/game', hash: places[0] ? `#${places[0].id}` : '' }" class="iact round done"
                :title="`уже в твоїй грі${places[0] ? `: ${places[0].text}` : ''} — показати там`"><Icon name="done" /></RouterLink>
  </span>
</template>

<style scoped>
.marks { display: inline-flex; align-items: center; gap: .3rem; }
.marks :deep(.pop) { display: flex; }  /* no line box around the small plus: it centres on the tick */
/* plus and tick are one round shape at one spot of the header */
.round { width: 1.5rem; height: 1.5rem; margin: -.05rem -.15rem; border-radius: 50%; font-size: 1.15rem; }
.round.more { width: 1.1rem; height: 1.1rem; font-size: .85rem; }
.done { color: var(--bs-success); }
.done:hover { color: var(--bs-success); background: color-mix(in srgb, var(--bs-success) 12%, transparent); }
/* the count hangs on the tick's shoulder, and the tick keeps a step from the coin after it (T296 §5) */
.many { position: relative; margin-right: .25rem; }
.many sup { position: absolute; top: -.05rem; right: -.2rem; font-size: .6rem; font-weight: 700; line-height: 1; }
.cap { margin-bottom: .2rem; font-size: .7rem; color: var(--bs-secondary-color); }
.place { display: flex; align-items: center; justify-content: space-between; gap: .5rem; padding: .2rem .35rem; border-radius: .3rem; color: inherit;
         font-size: .85rem; text-decoration: none; }
.place:hover { background: var(--bs-tertiary-bg); }
.place .icon { color: var(--bs-secondary-color); }
</style>
