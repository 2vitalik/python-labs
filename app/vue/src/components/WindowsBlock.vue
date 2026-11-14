<script setup>
import { computed, ref } from 'vue'

import Tip from '@core/components/Tip.vue'
import { useEd } from '../ed.js'
import GameGraph from './GameGraph.vue'
import StableColumns from './StableColumns.vue'
import WindowCard from './WindowCard.vue'
import WindowForm from './WindowForm.vue'

// the body of «Вікна й переходи»: the form of a new window on top, the window cards in stable columns, the map of transitions.
// add(prefill?) opens the form; prefill = { task } — the window type already chosen (the top «＋ Додати» bar)
const ed = useEd()
const adding = ref(null)  // { n, prefill } while the form is open; n remounts it when add() comes again
const orphans = computed(() => ed.menus.filter((m) => !ed.windows.some((w) => w.id === m.window)))
let n = 0
const add = (prefill = {}) => (adding.value = { n: ++n, prefill })
defineExpose({ add })
</script>

<template>
  <div>
    <div v-if="adding" class="card mb-2 editing new">
      <div class="card-body p-2">
        <WindowForm :key="adding.n" :prefill="adding.prefill" @done="adding = null" @cancel="adding = null" />
      </div>
    </div>
    <Tip v-if="!ed.windows.length">
      Вікна — це екрани гри: ігровий екран, головне меню, пауза, налаштування, кінець гри…<br>
      У кожного — тип, скриншот{{ ed.simple ? ' й опис' : ', елементи на ньому, переходи до інших вікон і дії' }}.
    </Tip>
    <StableColumns v-else v-slot="{ item }" :items="ed.windows" scope="windows">
      <WindowCard :part="item" />
    </StableColumns>
    <div v-if="!ed.simple && orphans.length" class="small text-secondary mt-2">
      Меню без вікна: <span v-for="m in orphans" :key="m.id" class="me-2">«{{ m.title }}» ({{ m.items.length }} п.)</span>
      — відкрий вікно й додай пункти там.
    </div>
    <div v-if="!ed.simple && ed.windows.length > 1" id="windows-graph" class="card mt-2">
      <div class="card-body p-2"><GameGraph /></div>
    </div>
  </div>
</template>
