<script setup>
import { ALL_HOW, toAll } from '@core/allkey.js'
import Icon from '@core/components/Icon.vue'
import { cardOwn, isShut, toggleCard } from '../looks.js'

// a card's own fold, beside its pencil (T296 §7): one card folded or opened alone — till the section's switch or the
// page's is pressed again; blue while it differs from its section (T298), ⌥-click — every card of the page.
// `id` — the card, `scope` — its section
defineProps({ id: String, scope: String })
</script>

<template>
  <button type="button" class="iact fold every" :class="{ on: cardOwn(id, scope) }"
          :title="`${isShut(id, scope) ? 'Розгорнути картку' : 'Згорнути картку до заголовка'} · ${ALL_HOW} — усі картки`"
          :data-all="`${isShut(id, scope) ? 'розгорнути' : 'згорнути'} всі картки`"
          :aria-expanded="!isShut(id, scope)" @click="(e) => toggleCard(id, scope, toAll(e))"><Icon :name="isShut(id, scope) ? 'down' : 'up'" /></button>
</template>

<style scoped>
.fold { color: color-mix(in srgb, var(--bs-secondary-color) 70%, transparent); }
.fold:hover { color: var(--bs-body-color); }
.fold.on { background: color-mix(in srgb, var(--bs-link-color) 12%, transparent); color: var(--bs-link-color); }
</style>
