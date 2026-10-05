<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { DAYS } from '../week.js'

// a day's page of /week (T186): the other days a click or ←/→ away; the view in the address goes along
const props = defineProps({ day: { type: Number, required: true }, days: { type: Number, required: true } })
const route = useRoute()
const router = useRouter()
const to = (d) => ({ path: `/week/${d + 1}`, query: route.query })
function key(e) {
  if (e.altKey || e.ctrlKey || e.metaKey || e.target.closest?.('input, textarea, select, [contenteditable]')) return
  const d = props.day + ({ ArrowLeft: -1, ArrowRight: 1 }[e.key] || 0)
  if (d !== props.day && d >= 0 && d < props.days) router.push(to(d))
}
onMounted(() => addEventListener('keydown', key))
onUnmounted(() => removeEventListener('keydown', key))
</script>

<template>
  <div class="btn-group btn-group-sm" title="Інший день — ще й стрілками ← →">
    <RouterLink v-for="d in days" :key="d" :to="to(d - 1)" class="btn" :class="d - 1 === day ? 'btn-secondary' : 'btn-outline-secondary'">{{ DAYS[d - 1] }}</RouterLink>
  </div>
</template>
