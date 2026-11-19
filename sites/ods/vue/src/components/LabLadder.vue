<script setup>
import { vHint } from '@core/hint.js'

import { WAYS } from '../labText.js'

// the levels of a lab (T228, GRADE.steps): each level, the form of defence it asks, and what the work has of it —
// ✅ there · ⬜ not yet · ? the file does not tell (no file, marimo without outputs)
defineProps({ steps: { type: Array, default: () => [] } })
const mark = (ok) => (ok === true ? '✅' : ok === false ? '⬜' : '?')
</script>

<template>
  <ol class="ladder-l list-unstyled mb-0">
    <li v-for="s in steps" :key="s.level" class="ladder-s" :class="{ ok: s.ok }">
      <div class="ladder-h">
        <span class="ladder-n">{{ s.level }}</span>
        <span>{{ s.title }}</span>
        <span v-if="WAYS[s.way] && s.way !== 'none'" class="ladder-w">{{ WAYS[s.way] }}</span>
      </div>
      <ul class="list-unstyled mb-0 ladder-needs">
        <li v-for="nd in s.needs" :key="nd.key">
          <span v-if="nd.ok === null" v-hint="'з файла не видно'" class="ladder-q">?</span><span v-else>{{ mark(nd.ok) }}</span>
          {{ nd.text }}
        </li>
      </ul>
    </li>
  </ol>
</template>

<style scoped>
.ladder-l { display: flex; flex-direction: column; gap: .4rem; font-size: .85rem; }
.ladder-h { display: flex; align-items: baseline; gap: .4rem; }
.ladder-n { min-width: 1.9rem; padding: 0 .3rem; border-radius: .25rem; background: var(--bs-tertiary-bg); color: var(--bs-secondary-color);
            font-weight: 700; text-align: center; font-variant-numeric: tabular-nums; }
.ladder-s.ok .ladder-n { background: var(--bs-success-bg-subtle); color: var(--bs-success-text-emphasis); }
.ladder-w { color: var(--bs-secondary-color); font-size: .78rem; }
.ladder-needs { margin-left: 2.3rem; color: var(--bs-secondary-color); font-size: .8rem; }
.ladder-s.ok .ladder-needs { color: inherit; }
.ladder-q { display: inline-block; width: 1.1em; text-align: center; color: var(--bs-secondary-color); font-weight: 700; cursor: help; }
</style>
