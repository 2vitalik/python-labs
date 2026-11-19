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
