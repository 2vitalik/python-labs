<script setup>
import { COLORS } from '../emoji/search.js'

// the picker's colour filter (T309): a row of drawn dots, one may be on; a click on it again takes the filter off
const color = defineModel({ type: String, default: '' })
</script>

<template>
  <div class="colors">
    <span class="lbl">колір</span>
    <button v-for="[key, name, paint] in COLORS" :key type="button" class="dot qtip" :class="{ on: color === key }" :style="{ '--c': paint }"
            :data-tip="name" :aria-label="name" :aria-pressed="color === key" @click="color = color === key ? '' : key" />
    <button v-if="color" type="button" class="off" @click="color = ''">будь-який</button>
  </div>
</template>

<style scoped>
.colors { display: flex; align-items: center; gap: .32rem; height: 1.5rem; }
.lbl { margin-right: .15rem; font-size: .65rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); }
.dot { width: 1.05rem; height: 1.05rem; padding: 0; border: 1px solid color-mix(in srgb, var(--bs-body-color) 28%, transparent); border-radius: 50%; background: var(--c); }
.dot:hover { transform: scale(1.15); }
.dot.on { box-shadow: 0 0 0 2px var(--bs-body-bg), 0 0 0 4px var(--bs-primary); }
.off { margin-left: auto; padding: 0; border: 0; background: none; font-size: .75rem; color: var(--bs-secondary-color); text-decoration: underline dotted; }
</style>
