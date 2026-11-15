<script setup>
import Icon from '@core/components/Icon.vue'
import { zoneOf } from '../catalog.js'

// what a claim is — a card of the catalog (T296 §14): one drawing wherever a card is mentioned, as ⚡ is a rule's and the
// window's frame is a window's; its colour is the card's category. `task` — the card (its info)
defineProps({ task: Object })
</script>

<template>
  <Icon name="card" class="csign" :style="{ color: zoneOf(task).color }" />
</template>

<style scoped>
.csign { stroke-width: 1.4; }
</style>
