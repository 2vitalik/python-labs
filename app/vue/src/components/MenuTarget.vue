<script setup>
import { computed, ref } from 'vue'

import Pop from '@core/components/Pop.vue'
import { useEd } from '../ed.js'
import { cardItems } from '../items.js'
import Picker from './Picker.vue'

// «веде до» of a menu item (T270 §10.1): nowhere, another window of the game, or a card — an action that opens no window.
// v-model:window (a window part id) and v-model:task (a card slug), one of them or none; `host` — the menu's own window
const props = defineProps({ host: String })
const win = defineModel('window', { type: String, default: '' })
const task = defineModel('task', { type: String, default: '' })
const ed = useEd()
const open = ref(false)
const ACTIONS = ['element', 'game', 'level', 'rule', 'mechanic', 'field']
const items = computed(() => [
  { key: '', title: 'нікуди — просто пункт', icon: '·' },
  ...ed.windows.filter((w) => w.id !== props.host)
    .map((w) => ({ key: `w:${w.id}`, title: w.title, icon: '🪟', desc: w.description, group: 'Вікна', taken: w.id === win.value })),
  ...cardItems(ACTIONS).map((it) => ({ ...it, key: `t:${it.key}`, group: 'Дія — картка каталогу', taken: it.key === task.value })),
])
const winTitle = computed(() => ed.windows.find((w) => w.id === win.value)?.title || '?')

function pick(it) {
  win.value = it.key.startsWith('w:') ? it.key.slice(2) : ''
  task.value = it.key.startsWith('t:') ? it.key.slice(2) : ''
  open.value = false
}
</script>

<template>
  <Pop v-model="open" width="24rem" class="target">
    <template #trigger="{ toggle }">
      <button type="button" class="form-select form-select-sm text-start text-truncate" title="Куди веде пункт" @click="toggle">
        <template v-if="win">🪟 {{ winTitle }}</template>
        <template v-else-if="task">⚙ {{ ed.info(task)?.title || task }}</template>
        <span v-else class="text-secondary">нікуди</span>
      </button>
    </template>
    <Picker inline autofocus :items placeholder="вікно або картка…" @pick="pick" />
  </Pop>
</template>

<style scoped>
.target { flex: 1 1 9rem; min-width: 0; }
</style>
