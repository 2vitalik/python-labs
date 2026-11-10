<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { games, ruShown, setRuShown } from '../catalog.js'
import { useTaskFilter } from '../taskFilter.js'
import { isUnfolded, unfoldAll } from '../unfold.js'
import { user } from '@core/user.js'

// the search row of /tasks: words in any language, a game, ⭐; every card unfolded or folded at once; the teacher's
// switch for the Russian synonyms on the cards (the search finds by them for everyone)
const { f, set } = useTaskFilter()
const admin = computed(() => user.value?.status === 'admin')
</script>

<template>
  <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
    <input :value="f.q" class="form-control form-control-sm w-auto flex-grow-1" style="max-width: 28rem"
           placeholder="Пошук: назва, інші назви будь-якою мовою, опис…" @input="set({ q: $event.target.value })">
    <button type="button" class="btn btn-sm btn-outline-secondary" @click="unfoldAll('', !isUnfolded())">
      <Icon :name="isUnfolded() ? 'fold' : 'unfold'" /> {{ isUnfolded() ? 'згорнути всі' : 'розгорнути всі' }}
    </button>
    <select :value="f.game" class="form-select form-select-sm w-auto" @change="set({ game: $event.target.value })">
      <option value="">Всі ігри</option>
      <option value="universal">🌍 Універсальні</option>
      <option v-for="g in games" :key="g.slug" :value="g.slug">{{ g.icon }} {{ g.title }}</option>
    </select>
    <div class="form-check mb-0">
      <input id="algo" class="form-check-input" type="checkbox" :checked="f.algo"
             @change="set({ algo: $event.target.checked ? '1' : '' })">
      <label class="form-check-label" for="algo">⭐ алгоритмічні</label>
    </div>
    <div v-if="admin" class="form-check form-switch mb-0" title="Російські синоніми на картках; пошук знаходить за ними завжди">
      <input id="ru-names" class="form-check-input" type="checkbox" role="switch" :checked="ruShown"
             @change="setRuShown($event.target.checked)">
      <label class="form-check-label" for="ru-names">рос. синоніми</label>
    </div>
  </div>
</template>
