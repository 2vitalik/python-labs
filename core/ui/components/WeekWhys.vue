<script setup>
import { computed } from 'vue'

import { was } from '../weekIf.js'
import { CATS, cats } from '../weekWhy.js'

// why people can't, as chips with how many say so (T186). Hover — only those marks stay bright on the strips; a click counts
// the reason as «незручно» everywhere: what if the teacher talked people out of it. `laid` — lay() of weekSum.js
const props = defineProps({ laid: { type: Array, required: true } })
const soft = defineModel('soft', { type: Set, required: true })
const lit = defineModel('lit', { type: Number })
const counts = computed(() => CATS.map((_, c) => props.laid.filter(({ s }) => s.week.marks.some((m) => was(m) === 'no' && cats(m.why).includes(c))).length))
function toggle(c) {
  const next = new Set(soft.value)
  next.has(c) ? next.delete(c) : next.add(c)
  soft.value = next
}
</script>

<template>
  <div v-if="counts.some(Boolean)" class="d-flex flex-wrap align-items-center gap-1 mb-2 small">
    <span class="text-secondary me-1">Чому не можуть:</span>
    <template v-for="(title, c) in CATS" :key="c">
      <button v-if="counts[c]" type="button" class="btn btn-sm chip btn-outline-secondary" :class="{ soft: soft.has(c) }"
              :title="soft.has(c) ? 'Рахується як «незручно». Клік — знову «не можуть»' : 'Клік — рахувати як «незручно»'"
              @pointerenter="lit = c" @pointerleave="lit = null" @click="toggle(c)">{{ title }} <span class="count">{{ counts[c] }}</span></button>
    </template>
    <a v-if="soft.size" href="#" class="text-secondary ms-1" @click.prevent="soft = new Set()">скинути</a>
    <span class="hint text-secondary ms-1">наведи — підсвітити, клік — рахувати як «незручно»</span>
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; font-size: .85em; }
@media (hover: none) { .hint { display: none; } }  /* a finger has no hover; the chips' titles say the rest */
/* counted as «незручно»: struck out and hatched like its marks on the strips */
.soft { text-decoration: line-through;
        background-image: repeating-linear-gradient(135deg, transparent 0 4px, color-mix(in srgb, var(--strip-meh) 70%, transparent) 4px 7px); }
</style>
