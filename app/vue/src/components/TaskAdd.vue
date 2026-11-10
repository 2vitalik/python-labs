<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { postClaim } from '../api.js'
import { addStat, plusOf } from '../gameAdd.js'
import { myGame, reloadInsides } from '../myGame.js'
import { addable, addsTo } from '../taskMeta.js'
import TaskAddParams from './TaskAddParams.vue'
import TaskAddStat from './TaskAddStat.vue'

// the round mark in a card's header for a student with a game: the violet plus «у мою гру», the green tick once the card is
// in. What the plus does depends on the card's kind (gameAdd.js); a question it asks first — in a panel at it
const props = defineProps({ task: Object, inGame: Boolean })
const shown = computed(() => !!myGame.value && addable(props.task))
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
  <template v-if="shown">
    <RouterLink v-if="inGame" to="/my/game" class="iact round done" title="уже в твоїй грі — відкрити" @click.stop>
      <Icon name="done" />
    </RouterLink>
    <span v-else-if="task.status === 'active'" @click.stop>
      <Pop v-model="open" width="20rem">
        <template #trigger>
          <button type="button" class="iact round add" :disabled="busy" :title="`Додати у мою гру\n${addsTo(task)}`" @click="add">
            <Icon name="plus" />
          </button>
        </template>
        <TaskAddStat v-if="plus.ask === 'stat'" :task :busy @send="(parts, value) => write(() => addStat(task, parts, value))"
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
    </span>
  </template>
</template>

<style scoped>
/* plus and tick are one round shape at one spot of the header */
.round { width: 1.5rem; height: 1.5rem; margin: -.05rem -.15rem; border-radius: 50%; font-size: 1.15rem; }
.done { color: var(--bs-success); }
.done:hover { color: var(--bs-success); background: color-mix(in srgb, var(--bs-success) 12%, transparent); }
</style>
