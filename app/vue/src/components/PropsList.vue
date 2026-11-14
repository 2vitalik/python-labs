<script setup>
import { computed } from 'vue'

import { vPeek } from '@core/peek.js'

// properties to read (T270 §8): «Сітка: 🔲 квадратна» in two columns, only the filled ones; `specs` — rows of vocab.field /
// vocab.level; the default slot is what to say when nothing is filled. A chosen option that is a catalog card shows the
// card under the mouse (T291 §6)
const p = defineProps({ props: { type: Object, default: () => ({}) }, specs: { type: Array, default: () => [] } })
// `none` — how v2 stored «no gravity»: now an unset property says the same
const empty = (v) => v == null || v === '' || v === false || v === 'none' || (Array.isArray(v) && !v.length)
// an option the vocab no longer knows is shown as it is stored
const option = (s, v) => {
  const o = s.options?.[v]
  return { text: !o ? v : typeof o === 'string' ? o : [o.icon, o.label].filter(Boolean).join(' '), slug: o?.slug, desc: o?.desc }
}
const values = (s, v) => (s.type === 'bool' ? [{ text: 'так' }] : s.type === 'choice' ? [].concat(v).map((x) => option(s, x))
  : [{ text: Array.isArray(v) ? v.join(' · ') : String(v) }])
const rows = computed(() => p.specs.filter((s) => !empty(p.props?.[s.key]))
  .map((s) => ({ key: s.key, label: s.label.split(/[:(]/)[0].trim(), full: s.label, values: values(s, p.props[s.key]) })))
</script>

<template>
  <div v-if="rows.length || $slots.default" class="plist small">
    <div v-for="r in rows" :key="r.key" class="prop">
      <span class="text-secondary" :title="r.full">{{ r.label }}:</span>
      <template v-for="(o, i) in r.values" :key="i">{{ i ? ' · ' : ' ' }}<span v-peek="o.slug ? { kind: 'task', id: o.slug } : null"
        :title="o.slug ? null : o.desc">{{ o.text }}</span></template>
    </div>
    <slot v-if="!rows.length" />
  </div>
</template>

<style scoped>
.plist { columns: 2 12rem; column-gap: 1.5rem; }
.prop { break-inside: avoid; padding: .05rem 0; }
</style>
