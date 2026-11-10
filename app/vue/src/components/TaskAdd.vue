<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { postClaim } from '../api.js'
import { kindOf, missingParams, vocab } from '../catalog.js'
import { myGame, reloadInsides } from '../myGame.js'
import { autoNote, landsAt } from '../taskMeta.js'
import SlotFields from './SlotFields.vue'

// the round mark in a card's header for a student with a game: the violet plus «у мою гру» (the params asked in a panel
// at it), the green tick once the card is in, a quiet «?» on the kinds the editor's own forms claim
const props = defineProps({ task: Object, inGame: Boolean })
const kind = computed(() => kindOf(props.task))
const full = computed(() => myGame.value && vocab.value.depth !== 'simple')
const open = ref(false)
const params = ref({})
const busy = ref(false)
const error = ref('')
const ready = computed(() => !missingParams(props.task, params.value).length)

function add() {
  if (!props.task.slots?.length) return send()
  error.value = ''
  open.value = !open.value
}
async function send() {
  busy.value = true
  error.value = ''
  try {
    await postClaim({ task: props.task.slug, params: params.value })
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
  <template v-if="full">
    <RouterLink v-if="inGame" to="/my/game" class="iact round done" title="уже в твоїй грі — відкрити" @click.stop>
      <Icon name="done" />
    </RouterLink>
    <span v-else-if="autoNote(kind)" class="iact round auto" :title="autoNote(kind)"><Icon name="help" /></span>
    <span v-else-if="task.status === 'active'" @click.stop>
      <Pop v-model="open" width="20rem">
        <template #trigger>
          <button type="button" class="iact round add" :disabled="busy" :title="`Додати у мою гру\n${landsAt(kind)}`" @click="add">
            <Icon name="plus" />
          </button>
        </template>
        <template v-if="task.slots?.length">
          <div class="small text-secondary mb-1">Параметри заявки</div>
          <div class="d-flex flex-wrap gap-2 align-items-center mb-2"><SlotFields :specs="task.slots" :params /></div>
          <div class="d-flex gap-2">
            <button type="button" class="btn btn-sm btn-add" :disabled="!ready || busy" @click="send"><Icon name="plus" /> Додати</button>
            <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false">Скасувати</button>
          </div>
        </template>
        <div v-if="error" class="text-danger small" :class="{ 'mt-2': task.slots?.length }">{{ error }}</div>
      </Pop>
    </span>
  </template>
</template>

<style scoped>
/* plus, tick and «?» are one round shape at one spot of the header */
.round { width: 1.5rem; height: 1.5rem; margin: -.05rem -.15rem; border-radius: 50%; font-size: 1.15rem; }
.done { color: var(--bs-success); }
.done:hover { color: var(--bs-success); background: color-mix(in srgb, var(--bs-success) 12%, transparent); }
.auto { opacity: .45; cursor: help; }
.auto:hover { background: none; color: var(--bs-secondary-color); }
</style>
