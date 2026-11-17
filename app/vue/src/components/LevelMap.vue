<script setup>
import { computed, ref } from 'vue'

import { useEd } from '../ed.js'
import { gameBrushes } from '../momentMap.js'
import MomentField from './MomentField.vue'
import MomentMap from './MomentMap.vue'
import SaveCancel from './SaveCancel.vue'

// a level's map drawn in cells (T276): to read — the picture. With the card's tools on (T310) — «змінити мапу» or
// «＋ намалювати рівень» under it: the editor opens in the picture's place, framed alone, with its own «Зберегти /
// Скасувати» — a drawing is many strokes, not one value. `save(text)` is awaited
const p = defineProps({ text: String, tools: Boolean, save: Function })
const ed = useEd()
const draw = ref(null)  // the map being drawn; null — the editor is closed
const busy = ref(false)
const error = ref('')
const brushes = computed(() => gameBrushes(ed.entities))
async function commit() {
  busy.value = true
  error.value = ''
  try {
    await p.save(draw.value)
    draw.value = null
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div v-if="draw !== null" class="editing box vstack gap-1">
    <MomentMap v-model="draw" :palette="brushes" />
    <div v-if="error" class="text-danger small">{{ error }}</div>
    <SaveCancel :disabled="busy" @save="commit" @cancel="draw = null" />
  </div>
  <template v-else>
    <MomentField v-if="text" :text />
    <Transition name="tool">
      <button v-if="tools" type="button" class="more-field align-self-start" title="рівень клітинками зі значків сутностей — заявляє картку «Мапа рівня на сайті»"
              @click="draw = text || ''">{{ text ? 'змінити мапу' : '＋ намалювати рівень' }}</button>
    </Transition>
  </template>
</template>

<style scoped>
.box { padding: .45rem; }
</style>
