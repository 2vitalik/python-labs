<script setup>
import { computed } from 'vue'

import { pages } from '@core/guide.js'

import { shortTitle } from '../lectures.js'
import ChangeOpen from './ChangeOpen.vue'
import ChangeRow from './ChangeRow.vue'

// the changes the filters left, lecture by lecture and slide by slide, a portion at a time: thousands of rows at once
// would hold the page up. The open one unfolds under its row
const props = defineProps({ list: Array, items: Array, limit: Number, open: String, cur: String })
const emit = defineEmits(['toggle', 'more', 'ready'])
const STEP = 200
const shown = computed(() => props.list.slice(0, props.limit))
const perLec = computed(() => props.list.reduce((n, it) => ((n[it.lec] = (n[it.lec] || 0) + 1), n), {}))
const rows = computed(() => shown.value.map((it, i) => {
  const p = shown.value[i - 1]
  return { it, lec: !p || p.lec !== it.lec, first: !p || p.lec !== it.lec || p.slide !== it.slide }
}))
const title = (it) => shortTitle(pages.value[it.slug]?.title || '')
const left = computed(() => props.list.length - shown.value.length)
</script>

<template>
  <div class="chg-list">
    <template v-for="r in rows" :key="r.it.id">
      <h2 v-if="r.lec" class="chg-lec">
        <span>Лекція {{ r.it.lec }}</span><span v-if="title(r.it)" class="t">{{ title(r.it) }}</span><span class="n">{{ perLec[r.it.lec] }}</span>
      </h2>
      <ChangeRow :it="r.it" :open="open === r.it.id" :cur="cur === r.it.id" :first="r.first" @click="emit('toggle', r.it.id)" />
      <ChangeOpen v-if="open === r.it.id" :it="r.it" :items @ready="emit('ready')" />
    </template>
    <p v-if="left > 0" class="chg-more">
      <span class="quiet">показано {{ shown.length }} з {{ list.length }}</span>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('more', STEP)">показати ще {{ Math.min(STEP, left) }}</button>
      <button v-if="left > STEP" type="button" class="dot small" @click="emit('more', left)">усі {{ list.length }}</button>
    </p>
  </div>
</template>
