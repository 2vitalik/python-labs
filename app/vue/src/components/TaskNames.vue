<script setup>
import TagInput from '@core/components/TagInput.vue'

import { LANGS } from '../taskMeta.js'
import { TIPS } from '../taskTips.js'

// a card's other names by language {uk, en, ru}, a one-line field each: the search finds by all of them, the cards show
// the Russian ones to the teacher only
const names = defineModel({ type: Object })
</script>

<template>
  <div class="vstack gap-1">
    <div v-for="(label, k) in LANGS" :key="k" class="d-flex align-items-baseline gap-2">
      <span class="lang" :class="{ tip: k === 'ru' }" :title="k === 'ru' ? TIPS.ru : null">{{ label }}</span>
      <TagInput v-model="names[k]" :hash="false" placeholder="слово, слово — через кому" class="form-control-sm" />
    </div>
  </div>
</template>
