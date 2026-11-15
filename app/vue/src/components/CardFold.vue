<script setup>
import Icon from '@core/components/Icon.vue'
import { isShut, toggleCard } from '../looks.js'

// a card's own fold, beside its pencil (T296 §7): one card folded or opened alone — till the section's switch or the
// page's is pressed again. `id` — the card, `scope` — its section
defineProps({ id: String, scope: String })
</script>

<template>
  <button type="button" class="iact fold" :title="isShut(id, scope) ? 'Розгорнути картку' : 'Згорнути картку до заголовка'"
          :aria-expanded="!isShut(id, scope)" @click="toggleCard(id, scope)"><Icon :name="isShut(id, scope) ? 'down' : 'up'" /></button>
</template>

<style scoped>
.fold { color: color-mix(in srgb, var(--bs-secondary-color) 70%, transparent); }
.fold:hover { color: var(--bs-body-color); }
</style>
