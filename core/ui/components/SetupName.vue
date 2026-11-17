<script setup>
import { computed } from 'vue'

import { isRel } from '../tableViews.js'

// a column's name in the setup panels: its short sign, its name, and the lab it is of — «ця» when the view says «this lab»
// (whichever lab it is turned to), «Л2» when it is lab 2 itself
const props = defineProps({ col: { type: Object, required: true } })
const relative = computed(() => !!props.col.lab && isRel(props.col.id || props.col.key))
</script>

<template>
  <span class="sn" :title="col.title">
    <span v-if="col.short !== col.name" class="sn-short">{{ col.short }}</span>
    <span class="sn-name">{{ col.name }}</span>
    <span v-if="col.lab" class="sn-lab" :title="relative ? `ця лаба виду — зараз лаба ${col.lab}` : `саме лаба ${col.lab}`">{{ relative ? 'ця' : `Л${col.lab}` }}</span>
  </span>
</template>

<style scoped>
.sn { display: inline-flex; align-items: baseline; gap: .3rem; min-width: 0; }
.sn-short { flex-shrink: 0; }
.sn-name { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.sn-lab { flex-shrink: 0; padding: 0 .25rem; border-radius: .25rem; background: var(--bs-tertiary-bg); color: var(--bs-secondary-color); font-size: .68rem; }
</style>
