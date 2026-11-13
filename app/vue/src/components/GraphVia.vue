<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { viaWords } from '../graphTree.js'

// what makes a transition on the map of windows: «☰ items» of «Переходи й дії», «⚡ reasons» of the rules — each of its colour
const props = defineProps({ via: Array })
const w = computed(() => viaWords(props.via || []))
</script>

<template>
  <span class="gvia">
    <span v-if="w.item" class="by-item"><Icon name="menu" /> {{ w.item }}</span>
    <span v-if="w.rule" class="by-rule">⚡&#xFE0E; {{ w.rule }}</span>
  </span>
</template>

<style scoped>
.gvia { font-size: .7rem; font-weight: 500; }
.by-item { color: var(--gg-item); }
.by-rule { color: var(--gg-rule); }
.by-item + .by-rule { margin-left: .4em; }
</style>
