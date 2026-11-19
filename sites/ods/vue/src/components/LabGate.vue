<script setup>
import { vHint } from '@core/hint.js'

import { GATES, gates, setGate } from '../labGates.js'

// the teacher's switch on a lab's row: how open the lab is to students; three words in one place, the one in force is filled
defineProps({ n: Number })
</script>

<template>
  <span class="btn-group btn-group-sm" role="group" :aria-label="`Лаба ${n} студентам`">
    <button v-for="[state, word, hint] in GATES" :key="state" v-hint="hint" type="button" class="btn"
            :class="gates?.[n] === state ? 'btn-secondary' : 'btn-outline-secondary'" :aria-pressed="gates?.[n] === state"
            @click="setGate(n, state)">{{ word }}</button>
  </span>
</template>

<style scoped>
/* a word not in force stays light under the mouse: only the one in force is filled */
.btn-outline-secondary { --bs-btn-hover-bg: var(--bs-tertiary-bg); --bs-btn-hover-color: var(--bs-body-color);
                         --bs-btn-active-bg: var(--bs-secondary-bg); --bs-btn-active-color: var(--bs-body-color); }
</style>
