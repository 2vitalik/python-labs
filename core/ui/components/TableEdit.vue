<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

import { optionLabel } from '../table.js'

// the small editor under an editable cell: a list of answers (one or many), or a field for a number, a text, a date; Esc or a click outside closes it
const props = defineProps({ col: { type: Object, required: true }, row: { type: Object, required: true } })
const emit = defineEmits(['save', 'close'])
const box = ref()
const at = ref({})  // fixed under the cell: the table scrolls and would clip an absolute one
const value = ref(props.col.get(props.row))
const text = ref(value.value ?? '')
const options = Object.entries(props.col.options || {})
const picked = (id) => (props.col.type === 'multi' ? (value.value || []).includes(id) : value.value === id)
function choose(id) {
  if (props.col.type === 'multi') {
    const list = value.value || []
    emit('save', list.includes(id) ? list.filter((x) => x !== id) : [...list, id])
  } else emit('save', value.value === id ? null : id)  // the same answer again clears the cell
}
const submit = () => emit('save', props.col.type === 'number' && text.value !== '' ? Number(text.value) : text.value || null)
const away = (e) => !box.value?.contains(e.target) && emit('close')
const key = (e) => e.key === 'Escape' && emit('close')
onMounted(() => {
  const r = box.value.parentElement.getBoundingClientRect()
  at.value = { left: `${Math.max(4, Math.min(r.left, window.innerWidth - 330))}px`, top: `${r.bottom + 2}px` }
  setTimeout(() => (document.addEventListener('click', away), document.addEventListener('keydown', key)))
})
onUnmounted(() => (document.removeEventListener('click', away), document.removeEventListener('keydown', key)))
</script>

<template>
  <div ref="box" class="pop card shadow-sm text-start" :style="at" @click.stop>
    <div v-if="options.length" class="list-group list-group-flush small">
      <button v-for="[id, o] in options" :key="id" type="button" class="list-group-item list-group-item-action py-1 px-2" :class="{ active: picked(id) }" @click="choose(id)">
        {{ optionLabel(o) }}</button>
      <button v-if="col.type === 'multi' && value?.length" type="button" class="list-group-item list-group-item-action py-1 px-2 text-secondary" @click="emit('save', null)">∅ очистити</button>
    </div>
    <form v-else class="p-2 d-flex gap-1" @submit.prevent="submit">
      <input v-model="text" :type="col.type === 'number' ? 'number' : col.type === 'date' ? 'date' : 'text'" step="any" class="form-control form-control-sm" autofocus @keydown.esc="emit('close')">
      <button type="submit" class="btn btn-sm btn-primary">OK</button>
      <button v-if="value !== null && value !== undefined && value !== ''" type="button" class="btn btn-sm btn-outline-secondary" title="Очистити" @click="emit('save', null)">∅</button>
    </form>
  </div>
</template>

<style scoped>
.pop { position: fixed; z-index: 1030; min-width: 11rem; max-height: 16rem; overflow-y: auto; white-space: normal; }
.pop form input { min-width: 7rem; }
</style>
