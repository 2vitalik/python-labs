<script setup>
import { computed } from 'vue'

import TagInput from '@core/components/TagInput.vue'
import { vocab } from '../catalog.js'
import OptionCards from './OptionCards.vue'

// the field's properties to fill (T270 §8): options as tiles, a checkbox, a short text, words; `only` — the keys to show
// (a level's form takes just the ones a level may override)
const model = defineModel({ type: Object, default: () => ({}) })
const p = defineProps({ only: Array })
const specs = computed(() => vocab.value.field.filter((s) => !p.only || p.only.includes(s.key)))
const set = (key, v) => (model.value = { ...model.value, [key]: v })
</script>

<template>
  <div class="vstack gap-2">
    <div v-for="s in specs" :key="s.key">
      <label v-if="s.type === 'bool'" class="form-check small mb-0">
        <input class="form-check-input" type="checkbox" :checked="!!model[s.key]" @change="set(s.key, $event.target.checked)">
        {{ s.label }}
      </label>
      <template v-else>
        <div class="small text-secondary mb-1">{{ s.label }}</div>
        <OptionCards v-if="s.type === 'choice'" :model-value="model[s.key]" :options="s.options" :multi="s.multi"
                     @update:model-value="set(s.key, $event)" />
        <input v-else-if="s.type === 'text'" :value="model[s.key] || ''" class="form-control form-control-sm text" :placeholder="s.hint"
               @input="set(s.key, $event.target.value)">
        <template v-else>
          <TagInput :model-value="model[s.key] || []" :hash="false" placeholder="слова через кому" @update:model-value="set(s.key, $event)" />
          <div v-if="s.hint" class="form-text mt-1">{{ s.hint }}</div>
        </template>
      </template>
    </div>
  </div>
</template>

<style scoped>
.text { max-width: 26rem; }
</style>
