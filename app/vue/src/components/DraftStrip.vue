<script setup>
import { computed } from 'vue'

import { kindOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { isDraft } from '../myGame.js'
import ClaimRow from './ClaimRow.vue'

// the claims of `kinds` still waiting for their place (T274 §3): added to the game, not yet tied to an entity, a window,
// a rule or the field — a red-edged strip under the heading of the section they belong to
const props = defineProps({ kinds: Array, hint: String })
const ed = useEd()
const list = computed(() => ed.claims.filter((c) => {
  const t = ed.info(c.task)
  return isDraft(c, t) && props.kinds.includes(kindOf(t))
}))
</script>

<template>
  <div v-if="list.length" class="strip vstack gap-1 mb-2">
    <div class="small"><span class="title">Ще без місця · {{ list.length }}</span><span v-if="ed.editable && hint" class="hint"> — {{ hint }}</span></div>
    <ClaimRow v-for="c in list" :key="c.id" :claim="c" />
  </div>
</template>

<style scoped>
.strip { padding: .3rem 0 .3rem .6rem; border-left: 3px solid var(--bs-danger); }
.title { font-weight: 600; color: var(--bs-danger-text-emphasis); }
.hint { color: var(--bs-secondary-color); }
</style>
