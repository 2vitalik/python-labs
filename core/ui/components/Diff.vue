<script setup>
import { computed, ref } from 'vue'

import { diffLines, fold } from '../diff.js'

// line diff of one guide save: red −, green +, unchanged runs folded until clicked
const props = defineProps({ old: String, new: String })
const all = ref(false)
const diff = computed(() => diffLines(props.old || '', props.new || ''))
const rows = computed(() => (all.value ? diff.value : fold(diff.value)))
</script>

<template>
  <div class="diff font-monospace">
    <template v-for="(r, i) in rows" :key="i">
      <a v-if="r.t === '…'" href="#" class="d-block text-decoration-none text-body-tertiary" @click.prevent="all = true">
        ··· ще {{ r.n }} рядків без змін ···
      </a>
      <div v-else :class="{ add: r.t === '+', del: r.t === '-' }">{{ r.t }} {{ r.s }}</div>
    </template>
  </div>
</template>

<style scoped>
.diff { font-size: .8rem; white-space: pre-wrap; overflow-wrap: anywhere; }
.add { background: var(--bs-success-bg-subtle); }
.del { background: var(--bs-danger-bg-subtle); }
</style>
