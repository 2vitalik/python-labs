<script setup>
import { computed, nextTick } from 'vue'

import { flash } from '@core/anchors.js'
import { vHint } from '@core/hint.js'
import { fmtWhen } from '@core/labs.js'

import { keyWord } from '../labText.js'
import NotebookModes from './NotebookModes.vue'
import NotebookView from './NotebookView.vue'

// the left side of the review desk: the notebook with its tasks as pills — a click goes to the task's cell (in «усе»
// when the current way of looking hides it); `tasks` — LabShape's, done or not from FACTS; `mode` is the page's
const props = defineProps({ nb: Object, tasks: { type: Array, default: () => [] }, other: Set, loading: Boolean, colab: String })
const mode = defineModel('mode', { type: String, default: 'all' })
const cellOf = (key) => props.nb?.cells.find((c) => c.key === key) || props.nb?.cells.find((c) => c.task === key)
const pills = computed(() => props.tasks.map((t) => ({ ...t, cell: cellOf(t.key) })))
// done · not done (a star is a choice, not a debt) · null — the file cannot tell
const look = (t) => (t.done ? 'done' : t.done === false && t.role !== 'star' ? 'miss' : '')
const tip = (t) => [t.case, t.title].filter(Boolean).join(' · ') + (t.done ? '' : t.done === false ? ' — не зроблено' : ' — з файла не видно')

async function go(t) {
  if (!t.cell) return
  if (!document.getElementById(`cell-${t.cell.i}`)) {
    mode.value = 'all'
    await nextTick()
  }
  flash(`cell-${t.cell.i}`)
}
</script>

<template>
  <div>
    <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
      <NotebookModes v-model="mode" />
      <span v-if="nb?.file" class="small text-secondary">{{ nb.file.name }} · {{ fmtWhen(nb.file.at) }}<template v-if="loading"> · завантажую…</template></span>
    </div>
    <div v-if="nb && pills.length" class="d-flex flex-wrap gap-1 mb-2">
      <button v-for="t in pills" :key="t.key" v-hint="tip(t)" type="button" class="tk" :class="look(t)" :disabled="!t.cell" @click="go(t)">
        {{ keyWord(t.key, t.role) }}</button>
    </div>
    <NotebookView v-if="nb" :cells="nb.cells" :mode :other :tasks="nb.facts?.tasks" />
    <p v-else-if="loading" class="text-secondary">Завантажую ноутбук…</p>
    <div v-else class="text-secondary py-4">
      <p class="mb-1">Файла ще нема — позначки на панелі праворуч ідуть лише з рядка відповідей.</p>
      <a v-if="colab" :href="colab" target="_blank" rel="noopener">Ноутбук у Colab ↗</a>
    </div>
  </div>
</template>

<style scoped>
.tk { min-width: 2.2rem; padding: 0 .45rem; border: 1px solid var(--bs-border-color); border-radius: 1rem; background: none; color: var(--bs-secondary-color);
      font-size: .78rem; font-variant-numeric: tabular-nums; }
.tk:hover:not(:disabled) { background: var(--bs-tertiary-bg); color: var(--bs-body-color); }
.tk.done { border-color: var(--bs-success-border-subtle); background: var(--bs-success-bg-subtle); color: var(--bs-success-text-emphasis); }
.tk.miss { border-color: color-mix(in srgb, var(--act-miss) 45%, transparent); color: var(--act-miss); }
.tk:disabled { opacity: .5; }
</style>
