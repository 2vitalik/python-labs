<script setup>
import { computed, ref } from 'vue'

import { RULE_GROUP_ORDER, ruleGroup } from '../rules.js'
import RuleRow from './RuleRow.vue'

// the game's rules grouped by what starts them (contact · input and time · state · lifecycle · puzzles)
const props = defineProps({ rules: Array, parts: Array, game: Object, editable: Boolean })
const emit = defineEmits(['changed'])
const adding = ref(false)
defineExpose({ add: () => (adding.value = true) })
const grouped = computed(() => {
  const m = {}
  for (const r of props.rules) (m[ruleGroup(r)] ??= []).push(r)
  return RULE_GROUP_ORDER.filter((g) => m[g]).map((g) => ({ g, list: m[g] }))
})
const done = () => { adding.value = false; emit('changed') }
</script>

<template>
  <div class="vstack gap-2">
    <div v-for="{ g, list } in grouped" :key="g" class="vstack gap-1">
      <div v-if="grouped.length > 1" class="text-uppercase text-secondary group">{{ g }}</div>
      <RuleRow v-for="r in list" :id="`r-${r.id}`" :key="r.id" :rule="r" :parts :game :editable @changed="emit('changed')" />
    </div>
    <RuleRow v-if="adding" :rule="null" :parts :game editable @changed="done" @cancel="adding = false" />
    <p v-else-if="!rules.length" class="text-secondary small mb-0">
      Правило — речення «КОЛИ подія → ЯКЩО умова → ТО ефект»: «КОЛИ гравець × ворог → ТО життя −1»,
      «КОЛИ кожні 20 тіків → ЯКЩО воргів на полі &lt; 4 → ТО спавн ворога».
    </p>
    <div v-if="editable && !adding">
      <button class="btn btn-outline-primary btn-sm" @click="adding = true">＋ правило</button>
    </div>
  </div>
</template>

<style scoped>
.group { font-size: .68rem; font-weight: 600; letter-spacing: .03em; }
</style>
