<script setup>
import { reactive, ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import { postPart, putPart } from '../api.js'
import { useEd } from '../ed.js'
import FieldProps from './FieldProps.vue'
import SaveCancel from './SaveCancel.vue'

// the field's form in place of its card: the properties as tiles and a line about the field; no `part` — a new field
const p = defineProps({ part: Object })
const emit = defineEmits(['done', 'cancel'])
const ed = useEd()
const form = reactive({ props: { ...(p.part?.props || {}) }, description: p.part?.description || '' })
const error = ref('')
const busy = ref(false)

async function save() {
  error.value = ''
  busy.value = true
  try {
    const data = { title: 'Поле', props: form.props, description: form.description.trim() }
    if (p.part) await putPart(p.part.id, data)
    else await postPart({ kind: 'field', ...data })
    await ed.changed()
    emit('done')
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="vstack frm">
    <FieldProps v-model="form.props" />
    <!-- one paragraph, as the card shows it: a long one wraps into more rows, Enter still saves -->
    <GrowArea v-model="form.description" class="form-control form-control-sm" placeholder="Коротко про поле: як генерується, камера…"
              @keydown.enter.prevent="save" />
    <div v-if="error" class="text-danger small">{{ error }}</div>
    <SaveCancel :disabled="busy" @save="save" @cancel="emit('cancel')" />
  </div>
</template>

<style scoped>
.frm { gap: .45rem; }
</style>
