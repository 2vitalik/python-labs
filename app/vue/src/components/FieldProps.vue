<script setup>
import { computed } from 'vue'

import TagInput from '@core/components/TagInput.vue'
import Tip from '@core/components/Tip.vue'
import { vocab } from '../catalog.js'
import OptionCards from './OptionCards.vue'

// the field's properties to fill (T270 §8): options as tiles, a checkbox, a short text, words — each caption in a left gutter,
// so a property costs no row of its own (T291 §4); `only` — the keys to show (a level's form takes just the ones a level
// may override)
const model = defineModel({ type: Object, default: () => ({}) })
const p = defineProps({ only: Array })
const specs = computed(() => vocab.value.field.filter((s) => !p.only || p.only.includes(s.key)))
const set = (key, v) => (model.value = { ...model.value, [key]: v })
</script>

<template>
  <div class="props">
    <template v-for="s in specs" :key="s.key">
      <label v-if="s.type === 'bool'" class="form-check small mb-0 whole">
        <input class="form-check-input" type="checkbox" :checked="!!model[s.key]" @change="set(s.key, $event.target.checked)">
        {{ s.label }}
      </label>
      <template v-else>
        <span class="cap">{{ s.label }}</span>
        <OptionCards v-if="s.type === 'choice'" :model-value="model[s.key]" :options="s.options" :multi="s.multi"
                     @update:model-value="set(s.key, $event)" />
        <input v-else-if="s.type === 'text'" :value="model[s.key] || ''" class="form-control form-control-sm text" :placeholder="s.hint"
               @input="set(s.key, $event.target.value)">
        <div v-else class="vstack gap-1">
          <TagInput :model-value="model[s.key] || []" :hash="false" placeholder="слова через кому" @update:model-value="set(s.key, $event)" />
          <Tip v-if="s.hint" :id="`field-${s.key}`">{{ s.hint }}</Tip>
        </div>
      </template>
    </template>
  </div>
</template>

<style scoped>
/* captions in a left gutter, a long one wraps; on a phone they stand over their fields */
.props { display: grid; grid-template-columns: fit-content(8rem) minmax(0, 1fr); align-items: baseline; gap: .4rem .6rem; }
.cap { font-size: .8rem; color: var(--bs-secondary-color); }
.whole { grid-column: 1 / -1; }
.text { max-width: 26rem; }
@media (max-width: 575.98px) {
  .props { grid-template-columns: minmax(0, 1fr); row-gap: .15rem; }
  .cap:not(:first-child), .whole:not(:first-child) { margin-top: .35rem; }
}
</style>
