<script setup>
import { vHint } from '@core/hint.js'

import { MODES } from '../labNb.js'

// the three ways to look at a notebook: усе · лише своє · висновки
const mode = defineModel({ type: String, default: 'all' })
const TIPS = { all: 'увесь ноутбук, як у студента', own: 'лише клітинки студента; питання завдання лишається над відповіддю',
               notes: 'висновки, рапорт, ШІ й нотатки — кожне під своїм завданням' }
</script>

<template>
  <div class="btn-group btn-group-sm" role="group" aria-label="Що показати з ноутбука">
    <button v-for="[k, t] in MODES" :key="k" type="button" class="btn btn-outline-secondary" :class="{ active: mode === k }"
            v-hint="TIPS[k]" @click="mode = k">{{ t }}</button>
  </div>
</template>
