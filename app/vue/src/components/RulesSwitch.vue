<script setup>
import { computed, watchEffect } from 'vue'

import Icon from '@core/components/Icon.vue'
import { useEd } from '../ed.js'
import { isContact, isControl, isTimed, lasts, timedStats } from '../ruleViews.js'

// the switch of the «Правила» views (T274 §6): a view's button shows up only when the view has something to show, with
// the count of its rules; a view left with nothing falls back to the list
const view = defineModel({ type: String, default: 'list' })
const ed = useEd()
const views = computed(() => {
  const time = ed.rules.filter((r) => isTimed(r) || lasts(r)).length
  return [
    { key: 'list', label: 'Список', icon: 'list', n: ed.rules.length, on: true },
    { key: 'contacts', label: 'Контакти', icon: 'table', n: ed.rules.filter(isContact).length },
    { key: 'controls', label: 'Керування', icon: 'keys', n: ed.rules.filter(isControl).length },
    { key: 'time', label: 'Час', icon: 'clock', n: time, on: time || timedStats(ed.entities).length },
  ].filter((v) => v.on || v.n)
})
watchEffect(() => {
  if (!views.value.some((v) => v.key === view.value)) view.value = 'list'
})
</script>

<template>
  <div v-if="views.length > 1" class="views btn-group btn-group-sm" role="group" aria-label="вигляд правил">
    <button v-for="v in views" :key="v.key" type="button" class="btn btn-outline-secondary" :class="{ active: view === v.key }" @click="view = v.key">
      <Icon :name="v.icon" /> {{ v.label }}<span v-if="v.n" class="cnt">{{ v.n }}</span>
    </button>
  </div>
</template>

<style scoped>
.views { flex-wrap: wrap; max-width: 100%; }
.cnt { margin-left: .3rem; font-size: .72rem; opacity: .7; font-variant-numeric: tabular-nums; }
/* four labelled buttons fit a phone once the icons step aside */
@media (max-width: 430px) { .views .icon { display: none; } }
</style>
