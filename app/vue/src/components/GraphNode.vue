<script setup>
import Icon from '@core/components/Icon.vue'
import { vPeek } from '@core/peek.js'

// a window on the map (T284 §1): its sign — filled when the window has a screenshot — and its name, in the colour of
// its type (GameGraph's .gg-w). The mouse over it brings the window's card, a click keeps the card
defineProps({ id: String, title: String, shot: Boolean, tone: String, lit: Boolean })
</script>

<template>
  <button v-peek.pin="{ kind: 'window', id }" type="button" class="gnode gg-w" :class="[tone && `tone-${tone}`, { lit, shot }]">
    <Icon :name="shot ? 'winshot' : 'win'" class="sign" /><span class="ttl">{{ title }}</span>
  </button>
</template>

<style scoped>
.gnode { display: inline-flex; align-items: center; gap: .35rem; max-width: 100%; padding: 0 .55rem 0 .45rem; border: 1px solid var(--w-line); border-radius: 6px;
         background: var(--w-bg); color: var(--bs-body-color); font-size: .8rem; line-height: 1.2; text-align: start; }
.gnode:hover { border-color: var(--w-ink); }
.gnode.lit { background: var(--bs-warning-bg-subtle); border-color: var(--bs-warning-border-subtle); }
.sign { color: var(--w-ink); font-size: .85rem; }
.ttl { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>
