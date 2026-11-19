<script setup>
import { computed } from 'vue'

import { fmtWhen } from '@core/labs.js'
import { vHint } from '@core/hint.js'

import { fmtSize, numbered } from '../labText.js'

// the versions of a notebook as pills, newest first: «#3 · 19 лист., 14:02»; `to(f)` — a link for each, else a click
// picks one (`pick`); `current` — the one shown
const props = defineProps({ files: { type: Array, default: () => [] }, current: String, to: Function })
defineEmits(['pick'])
const list = computed(() => numbered(props.files).reverse())
const tip = (f) => `${f.name} · ${fmtSize(f.size)}${f.line ? ' · з рядком відповідей' : ''}`
</script>

<template>
  <div class="vers d-flex flex-wrap gap-1">
    <template v-for="f in list" :key="f.id">
      <RouterLink v-if="to" v-hint="tip(f)" :to="to(f)" class="vers-p" :class="{ on: f.id === current }">
        #{{ f.k }} · {{ fmtWhen(f.at) }}<template v-if="f.line"> · рядок</template>
      </RouterLink>
      <button v-else v-hint="tip(f)" type="button" class="vers-p" :class="{ on: f.id === current }" @click="$emit('pick', f.id)">
        #{{ f.k }} · {{ fmtWhen(f.at) }}<template v-if="f.line"> · рядок</template>
      </button>
    </template>
  </div>
</template>

<style scoped>
.vers-p { padding: .05rem .55rem; border: 1px solid var(--bs-border-color); border-radius: 1rem; background: none; color: var(--bs-body-color);
          font-size: .8rem; text-decoration: none; white-space: nowrap; }
.vers-p:hover { background: var(--bs-tertiary-bg); }
.vers-p.on { border-color: var(--bs-primary); background: var(--bs-primary-bg-subtle); color: var(--bs-primary-text-emphasis); }
</style>
