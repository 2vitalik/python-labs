<script setup>
import { computed, onBeforeUnmount, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import Icon from '@core/components/Icon.vue'
import { vHint } from '@core/hint.js'

// whose work this is, and the way to the neighbours of the table: ← → and the keys [ ] when no field has the focus;
// `prev` / `next` — a vid, or {vid, name}
const props = defineProps({ n: Number, doc: Object })
const router = useRouter()
const side = (x) => (x && typeof x === 'object' ? x : x ? { vid: x } : null)
const prev = computed(() => side(props.doc.prev))
const next = computed(() => side(props.doc.next))
const to = (x) => `/labs/${props.n}/results/${x.vid}`
const tip = (x, key) => `${x.name || x.vid} · клавіша ${key}`

function key(e) {
  if (e.metaKey || e.ctrlKey || e.altKey || e.target.closest?.('input, textarea, select, [contenteditable]')) return
  const x = { '[': prev.value, ']': next.value }[e.key]
  if (x) router.push(to(x))
}
onMounted(() => addEventListener('keydown', key))
onBeforeUnmount(() => removeEventListener('keydown', key))
</script>

<template>
  <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
    <RouterLink v-if="prev" v-hint="tip(prev, '[')" :to="to(prev)" class="btn btn-sm btn-outline-secondary" aria-label="Попередня робота"><Icon name="left" /></RouterLink>
    <span v-else class="btn btn-sm btn-outline-secondary disabled" aria-hidden="true"><Icon name="left" /></span>
    <RouterLink v-if="next" v-hint="tip(next, ']')" :to="to(next)" class="btn btn-sm btn-outline-secondary" aria-label="Наступна робота"><Icon name="right" /></RouterLink>
    <span v-else class="btn btn-sm btn-outline-secondary disabled" aria-hidden="true"><Icon name="right" /></span>
    <h1 class="h4 mb-0">{{ doc.who?.name || doc.student || 'Картка вільна' }}</h1>
    <span class="text-secondary">
      <code>{{ doc.vid }}</code> · {{ doc.group }}<template v-if="doc.who?.nick"> · {{ doc.who.nick }}</template>
    </span>
    <RouterLink :to="`/labs/${n}/results`" class="small ms-auto">усі результати лаби</RouterLink>
  </div>
</template>
