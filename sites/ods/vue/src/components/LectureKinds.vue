<script setup>
import { computed } from 'vue'

import { KINDS } from '../lectureFindKinds.js'

// how many matches of each kind (the engine's counts, before it cut each kind); a pill narrows the results to its kind,
// the pressed one lets go. A kind with none stays in its place, grey: the row does not jump from query to query
const props = defineProps({ counts: { type: Object, default: () => ({}) } })
const kind = defineModel({ type: String, default: '' })
const pills = computed(() => [
  { key: '', name: 'усі', n: KINDS.reduce((s, k) => s + (props.counts[k.key] || 0), 0) },
  ...KINDS.map((k) => ({ ...k, n: props.counts[k.key] || 0 })),
])
</script>

<template>
  <div class="kinds" role="group" aria-label="Види збігів">
    <button v-for="p in pills" :key="p.key" type="button" class="pill" :class="[p.key && `k-${p.key}`, { on: kind === p.key }]"
            :disabled="!p.n && kind !== p.key" :aria-pressed="kind === p.key" @click="kind = kind === p.key ? '' : p.key">
      <span v-if="p.key" class="kdot" />{{ p.name }}<span class="n">{{ p.n }}</span>
    </button>
  </div>
</template>

<style scoped>
.kinds { display: flex; flex-wrap: wrap; gap: .35rem; margin: .5rem 0 .25rem; }
.pill { display: inline-flex; align-items: center; gap: .35rem; padding: .1rem .6rem; font-size: .8rem; line-height: 1.5;
        color: var(--bs-secondary-color); background: none; border: 1px solid var(--bs-border-color); border-radius: 1rem; }
.pill:hover:not(:disabled) { color: var(--bs-body-color); border-color: var(--bs-secondary-color); }
.pill.on { color: var(--bs-body-color); border-color: var(--k, var(--bs-body-color));
           background: color-mix(in srgb, var(--k, var(--bs-body-color)) 14%, transparent); }
.pill:disabled { opacity: .45; }
.pill:disabled .kdot { background: var(--bs-border-color); }
.n { font-variant-numeric: tabular-nums; color: var(--bs-tertiary-color); }
.pill.on .n, .pill:hover:not(:disabled) .n { color: var(--bs-secondary-color); }
</style>
