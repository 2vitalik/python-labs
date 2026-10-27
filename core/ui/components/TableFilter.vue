<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

import { optionLabel } from '../table.js'

// a column's filter under its header: yes/no for a checkmark, answers to tick for a choice, from–to for a number, a substring for text,
// has/none or a date for a date; «∅» — the empty cells. The result is the spec table.js passes() reads
const props = defineProps({ col: { type: Object, required: true }, spec: { type: String, default: '' } })
const emit = defineEmits(['set', 'close'])
const box = ref()
const at = ref({})  // fixed under the cell: the table scrolls and would clip an absolute one
const text = ref(props.col.type === 'text' && props.spec !== '-' ? props.spec : '')
const range = props.spec.match(/^(\d*\.?\d*)-(\d*\.?\d*)$/)
const from = ref(range ? range[1] : '')
const to = ref(range ? range[2] : '')
const date = ref(props.spec.length > 1 && '<>'.includes(props.spec[0]) ? props.spec.slice(1) : '')
const chosen = () => (props.spec ? props.spec.split(',') : [])
const has = (id) => chosen().includes(id)
const flip = (id) => emit('set', (has(id) ? chosen().filter((x) => x !== id) : [...chosen(), id]).join())
const number = () => emit('set', from.value || to.value ? `${from.value}-${to.value}` : '')
const away = (e) => !box.value?.contains(e.target) && emit('close')
const key = (e) => e.key === 'Escape' && emit('close')
onMounted(() => {
  const r = box.value.parentElement.getBoundingClientRect()
  at.value = { left: `${Math.max(4, Math.min(r.left, window.innerWidth - 330))}px`, top: `${r.bottom + 2}px` }
  setTimeout(() => (document.addEventListener('click', away), document.addEventListener('keydown', key)))
})
onUnmounted(() => (document.removeEventListener('click', away), document.removeEventListener('keydown', key)))
const btn = (on) => (on ? 'btn-secondary' : 'btn-outline-secondary')
</script>

<template>
  <div ref="box" class="pop card shadow-sm text-start p-2 small" :style="at" @click.stop>
    <div class="text-secondary mb-1 text-truncate">{{ col.title }}</div>
    <div v-if="['bool', 'link'].includes(col.type)" class="btn-group btn-group-sm">
      <button type="button" class="btn" :class="btn(spec === '1')" @click="emit('set', spec === '1' ? '' : '1')">так</button>
      <button type="button" class="btn" :class="btn(spec === '0')" @click="emit('set', spec === '0' ? '' : '0')">ні</button>
    </div>
    <template v-else-if="col.type === 'date'">
      <div class="btn-group btn-group-sm mb-2">
        <button type="button" class="btn" :class="btn(spec === '1')" @click="emit('set', spec === '1' ? '' : '1')">є</button>
        <button type="button" class="btn" :class="btn(spec === '0')" @click="emit('set', spec === '0' ? '' : '0')">нема</button>
      </div>
      <div class="d-flex gap-1 align-items-center">
        <input v-model="date" type="date" class="form-control form-control-sm">
        <button type="button" class="btn btn-sm" :class="btn(spec[0] === '>')" title="Від цієї дати" :disabled="!date" @click="emit('set', `>${date}`)">≥</button>
        <button type="button" class="btn btn-sm" :class="btn(spec[0] === '<')" title="До цієї дати" :disabled="!date" @click="emit('set', `<${date}`)">≤</button>
      </div>
    </template>
    <form v-else-if="col.type === 'number'" class="d-flex gap-1 align-items-center" @submit.prevent="number">
      <input v-model="from" type="number" step="any" class="form-control form-control-sm" placeholder="від" @change="number">
      <input v-model="to" type="number" step="any" class="form-control form-control-sm" placeholder="до" @change="number">
      <button type="button" class="btn btn-sm" :class="btn(spec === '-')" title="Порожні" @click="emit('set', spec === '-' ? '' : '-')">∅</button>
    </form>
    <form v-else-if="col.type === 'text'" class="d-flex gap-1" @submit.prevent="emit('set', text)">
      <input v-model="text" class="form-control form-control-sm" placeholder="містить…" autofocus>
      <button type="button" class="btn btn-sm" :class="btn(spec === '-')" title="Порожні" @click="emit('set', spec === '-' ? '' : '-')">∅</button>
    </form>
    <div v-else class="d-flex flex-column gap-1">
      <label v-for="[id, o] in Object.entries(col.options || {})" :key="id" class="d-flex gap-2 align-items-center">
        <input type="checkbox" class="form-check-input m-0" :checked="has(id)" @change="flip(id)"> <span class="text-truncate">{{ optionLabel(o) }}</span>
      </label>
      <label class="d-flex gap-2 align-items-center text-secondary"><input type="checkbox" class="form-check-input m-0" :checked="has('-')" @change="flip('-')"> ∅ порожньо</label>
    </div>
    <a v-if="spec" href="#" class="d-block mt-2 text-secondary" @click.prevent="emit('set', '')">зняти фільтр</a>
  </div>
</template>

<style scoped>
.pop { position: fixed; z-index: 1030; min-width: 13rem; max-width: 18rem; max-height: 20rem; overflow-y: auto; white-space: normal; font-weight: 400; }
</style>
