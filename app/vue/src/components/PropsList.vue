<script setup>
import { computed } from 'vue'

// properties to read (T270 §8): «Сітка: 🔲 квадратна» in two columns, only the filled ones; `specs` — rows of vocab.field /
// vocab.level; the default slot is what to say when nothing is filled
const p = defineProps({ props: { type: Object, default: () => ({}) }, specs: { type: Array, default: () => [] } })
// `none` — how v2 stored «no gravity»: now an unset property says the same
const empty = (v) => v == null || v === '' || v === false || v === 'none' || (Array.isArray(v) && !v.length)
// an option the vocab no longer knows is shown as it is stored
const option = (s, v) => {
  const o = s.options?.[v]
  return !o ? v : typeof o === 'string' ? o : [o.icon, o.label].filter(Boolean).join(' ')
}
const text = (s, v) => (s.type === 'bool' ? 'так' : s.type === 'choice' ? [].concat(v).map((x) => option(s, x)).join(' · ')
  : Array.isArray(v) ? v.join(' · ') : String(v))
const rows = computed(() => p.specs.filter((s) => !empty(p.props?.[s.key]))
  .map((s) => ({ key: s.key, label: s.label.split(/[:(]/)[0].trim(), full: s.label, value: text(s, p.props[s.key]) })))
</script>

<template>
  <div v-if="rows.length || $slots.default" class="plist small">
    <div v-for="r in rows" :key="r.key" class="prop"><span class="text-secondary" :title="r.full">{{ r.label }}:</span> {{ r.value }}</div>
    <slot v-if="!rows.length" />
  </div>
</template>

<style scoped>
.plist { columns: 2 12rem; column-gap: 1.5rem; }
.prop { break-inside: avoid; padding: .05rem 0; }
</style>
