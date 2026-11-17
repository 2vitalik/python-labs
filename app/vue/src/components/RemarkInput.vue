<script setup>
import { nextTick, ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import Icon from '@core/components/Icon.vue'
import { postRemarks } from '../api.js'

// where the teacher dictates (T328 §6): Enter turns the text into remarks, a line each — their tags come with them;
// Shift+Enter is one more line of the same batch. The field keeps the focus: the next remark is typed right away
const props = defineProps({ id: String })
const emit = defineEmits(['added'])
const text = ref('')
const busy = ref(false)
const error = ref('')
const box = ref()
async function add() {
  if (!text.value.trim() || busy.value) return
  busy.value = true
  try {
    emit('added', await postRemarks(props.id, text.value))
    text.value = error.value = ''
    await nextTick()
    box.value.scrollIntoView({ block: 'nearest' })
  } catch (e) {
    error.value = e.message
  }
  busy.value = false
}
const key = (e) => {
  if (e.key !== 'Enter' || e.shiftKey || e.isComposing) return
  e.preventDefault()
  add()
}
</script>

<template>
  <div ref="box" class="input">
    <div class="d-flex align-items-start gap-2">
      <GrowArea v-model="text" class="form-control" placeholder="Диктуй або пиши зауваження — Enter додає" @keydown="key" />
      <button type="button" class="btn btn-add text-nowrap" :disabled="!text.trim() || busy" @click="add"><Icon name="plus" /> Додати</button>
    </div>
    <div class="tip">Кожен рядок стане окремим зауваженням з тегами · Shift+Enter — новий рядок</div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.input { scroll-margin-bottom: 1rem; }
.tip { margin-top: .2rem; font-size: .74rem; color: var(--bs-secondary-color); }
</style>
