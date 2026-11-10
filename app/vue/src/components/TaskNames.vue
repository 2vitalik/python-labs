<script setup>
import TagInput from '@core/components/TagInput.vue'

import { LANGS } from '../taskMeta.js'

// a card's synonyms by language {uk, en, ru}: the search finds by all of them, the cards show the Russian ones on demand
const names = defineModel({ type: Object })
</script>

<template>
  <div class="vstack gap-1">
    <div class="hint">Синоніми — інші назви, за якими картку знаходить пошук</div>
    <div v-for="(label, k) in LANGS" :key="k" class="d-flex align-items-center gap-2">
      <span class="lang">{{ label }}</span>
      <TagInput v-model="names[k]" :hash="false" placeholder="слово і Enter" class="form-control-sm" />
    </div>
  </div>
</template>
