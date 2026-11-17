<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

import { optionLabel } from '../table.js'
import Icon from './Icon.vue'

// the small editor under an editable cell: a list of answers (one or many), or a field for a number, a text, a date; Esc or
// a click outside closes it. It lives on the body, fixed under `anchor`: the table scrolls and would clip it, and a pale
// (другорядна) column would pale it too
const props = defineProps({ col: { type: Object, required: true }, row: { type: Object, required: true }, anchor: { type: Object, required: true } })
const emit = defineEmits(['save', 'close'])
const box = ref()
const input = ref()
const at = ref({})
const value = props.col.get(props.row)
const has = value !== null && value !== undefined && value !== ''
const text = ref(value ?? '')
const options = Object.entries(props.col.options || {})
const picked = (id) => (props.col.type === 'multi' ? (value || []).includes(id) : value === id)
function choose(id) {
  if (props.col.type === 'multi') emit('save', picked(id) ? value.filter((x) => x !== id) : [...(value || []), id])
  else emit('save', picked(id) ? null : id)  // the same answer again clears the cell
}
const submit = () => emit('save', props.col.type === 'number' && text.value !== '' ? Number(text.value) : text.value || null)
const away = (e) => !box.value?.contains(e.target) && emit('close')
const key = (e) => e.key === 'Escape' && emit('close')
onMounted(() => {
  const r = props.anchor.getBoundingClientRect()
  at.value = { left: `${Math.max(4, Math.min(r.left, innerWidth - box.value.offsetWidth - 8))}px`, top: `${r.bottom + 2}px` }  // under its cell, inside the window
  input.value?.focus()
  setTimeout(() => (document.addEventListener('click', away), document.addEventListener('keydown', key)))
})
onUnmounted(() => (document.removeEventListener('click', away), document.removeEventListener('keydown', key)))
</script>

<template>
  <Teleport to="body">
    <div ref="box" class="tedit card shadow-sm" :style="at">
      <div v-if="options.length" class="d-flex flex-column p-1">
        <button v-for="[id, o] in options" :key="id" type="button" class="opt" :class="{ on: picked(id) }" @click="choose(id)">
          <span class="text-truncate">{{ optionLabel(o) }}</span><Icon v-if="picked(id)" name="check" class="ms-auto" /></button>
        <button v-if="col.type === 'multi' && value?.length" type="button" class="opt text-secondary" @click="emit('save', null)">
          <Icon name="eraser" /> очистити</button>
      </div>
      <form v-else class="p-2 d-flex gap-1" @submit.prevent="submit">
        <input ref="input" v-model="text" :type="col.type === 'number' ? 'number' : col.type === 'date' ? 'date' : 'text'" step="any" class="form-control form-control-sm">
        <button type="submit" class="btn btn-sm btn-success" title="Зберегти"><Icon name="check" /></button>
        <button v-if="has" type="button" class="btn btn-sm btn-outline-secondary" title="Очистити" @click="emit('save', null)"><Icon name="eraser" /></button>
      </form>
    </div>
  </Teleport>
</template>

<style scoped>
.tedit { position: fixed; z-index: 1030; min-width: 11rem; max-width: 18rem; max-height: 16rem; overflow-y: auto; font-size: .85rem; }
.tedit input { min-width: 7rem; }
.opt { display: flex; align-items: center; gap: .4rem; padding: .2rem .5rem; border: 0; border-radius: .3rem; background: none; color: var(--bs-body-color); text-align: start; }
.opt:hover { background: var(--bs-tertiary-bg); }
.opt.on { background: var(--bs-secondary-bg); font-weight: 500; }
</style>
