<script setup>
import { reactive } from 'vue'

import TagInput from '@core/components/TagInput.vue'
import { LANGS } from '../taskMeta.js'
import { TIPS } from '../taskTips.js'
import MoreFields from '@core/components/MoreFields.vue'

// a card's other names by language {uk, en, ru}, a one-line field each: the search finds by all of them, the cards show
// the Russian ones to the teacher only. Ukrainian is always there; an empty other language comes by «＋ en» (T291 §4)
const names = defineModel({ type: Object })
const shown = reactive(Object.fromEntries(Object.keys(LANGS).map((k) => [k, k === 'uk' || !!names.value[k]?.length])))
const more = Object.fromEntries(Object.entries(LANGS).filter(([k]) => k !== 'uk'))
</script>

<template>
  <div class="vstack gap-1">
    <template v-for="(label, k) in LANGS" :key="k">
      <div v-if="shown[k]" class="d-flex align-items-baseline gap-2">
        <span class="lang" :class="{ tip: k === 'ru' }" :title="k === 'ru' ? TIPS.ru : null">{{ label }}</span>
        <TagInput v-model="names[k]" :hash="false" placeholder="слово, слово — через кому" class="form-control-sm" />
      </div>
    </template>
    <MoreFields :fields="more" :shown @show="shown[$event] = true" />
  </div>
</template>
