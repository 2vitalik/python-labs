<script setup>
import { computed } from 'vue'

import { ALL_HOW, toAll } from '@core/allkey.js'
import Icon from '@core/components/Icon.vue'
import { setTools, toolsOn } from '../tools.js'

// a card's pencil (T310): no form — it turns the card's tools on and off (tools.js); lit while they are on.
// `id` — the card, `all` — the ids of its section's cards: ⌥-click or a hold switches every one of them
const p = defineProps({ id: String, all: { type: Array, default: () => [] }, what: { type: String, default: 'картці' } })
const on = computed(() => toolsOn(p.id))
const click = (e) => setTools(p.id, !on.value, toAll(e) && p.all.length ? p.all : [p.id])
</script>

<template>
  <button type="button" class="iact tools-btn" :class="{ on, every: all.length > 1 }" :aria-pressed="on"
          :title="`${on ? 'Готово — сховати інструменти' : `Усе, що можна змінити й додати на ${what}`}${all.length > 1 ? ` · ${ALL_HOW} — усі картки` : ''}`"
          :data-all="all.length > 1 ? (on ? 'сховати інструменти всіх карток' : 'інструменти всіх карток') : null" @click="click"><Icon name="pencil" /></button>
</template>

<style scoped>
.tools-btn.on { background: color-mix(in srgb, var(--act-edit) 18%, transparent); color: var(--act-edit); }
</style>
