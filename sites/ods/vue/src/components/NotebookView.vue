<script setup>
import { computed, ref } from 'vue'

import Lightbox from '@core/components/Lightbox.vue'
import { showShot } from '@core/lightbox.js'

import NotebookCell from './NotebookCell.vue'

// a notebook as if it had just been run (T354 §6). `cells` — NOTEBOOK.cells; `mode` (the parent's switch): all ·
// own — the template's cells hidden, a task keeps the question right before it · notes — conclusions, report, ai and
// notes, each under its task; `other` — hashes of another version: a cell not among them is marked changed;
// `tasks` — FACTS.tasks, the words a note is put under
const props = defineProps({ cells: { type: Array, default: () => [] }, mode: { type: String, default: 'all' }, other: Set,
                            tasks: { type: Array, default: () => [] } })
const NOTES = { conclusion: 'висновок', report: 'рапорт', ai: 'ШІ', note: 'нотатка' }
const EMPTY = { all: 'У ноутбуці нема клітинок.', own: 'Своїх клітинок нема — лише шаблон.', notes: 'Висновків у ноутбуці нема.' }
const root = ref()

function headOf(c) {
  const key = c.key || c.task
  const t = key && props.tasks.find((x) => x.key === key)
  return [key, t?.case, t?.title].filter(Boolean).join(' · ') || NOTES[c.role]
}
const shown = computed(() => {
  const cs = props.cells
  if (props.mode === 'own') return cs.filter((c, i) => !c.given || (c.kind === 'markdown' && cs[i + 1] && !cs[i + 1].given))
  if (props.mode !== 'notes') return cs
  let last = ''
  return cs.filter((c) => NOTES[c.role]).map((c) => {
    const head = headOf(c)
    return { ...c, head: head !== last ? (last = head) : '' }
  })
})

function zoom(e) {
  if (!e.target.matches('img.nb-img')) return
  const all = [...root.value.querySelectorAll('img.nb-img')]
  showShot(all.map((i) => i.src), all.indexOf(e.target))
}
</script>

<template>
  <div ref="root" class="nb" @click="zoom">
    <template v-for="c in shown" :key="c.i">
      <div v-if="c.head" class="nb-head">{{ c.head }}</div>
      <NotebookCell :c :changed="!!other && !other.has(c.h)" />
    </template>
    <p v-if="!shown.length" class="text-secondary">{{ EMPTY[mode] }}</p>
    <Lightbox />
  </div>
</template>

<style scoped>
.nb { display: flex; flex-direction: column; gap: .15rem; }
.nb-head { margin: .75rem 0 0 3.8rem; color: var(--bs-secondary-color); font-size: .78rem; font-weight: 600; }
</style>
