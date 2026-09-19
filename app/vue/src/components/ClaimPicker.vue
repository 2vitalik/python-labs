<script setup>
import { computed, ref } from 'vue'

import { COINS, tasks } from '../catalog.js'
import SlotFields from './SlotFields.vue'

defineProps({ placeholder: { type: String, default: '＋ заявка: пошук картки…' } })
const emit = defineEmits(['pick'])
const q = ref('')
const open = ref(false)
const picked = ref(null) // card with slots waits for its params
const params = ref({})
const found = computed(() => {
  const s = q.value.trim().toLowerCase()
  if (s.length < 2) return []
  return tasks.value.filter((t) => (t.title + ' ' + t.slug).toLowerCase().includes(s)).slice(0, 8)
})
const ready = computed(() =>
  picked.value.slots.every((s) => !s.required || params.value[s.key] || params.value[s.key] === 0))

function pick(t) {
  q.value = ''
  open.value = false
  if (t.slots?.length) {
    picked.value = t
    params.value = {}
  } else {
    emit('pick', t.slug, {})
  }
}

function send() {
  emit('pick', picked.value.slug, params.value)
  picked.value = null
}
</script>

<template>
  <div v-if="picked" class="d-flex gap-1 flex-wrap align-items-center">
    <span class="small text-nowrap">{{ COINS[picked.coin] || '·' }} {{ picked.title }}:</span>
    <SlotFields :specs="picked.slots" :params="params" />
    <button class="btn btn-primary btn-sm" :disabled="!ready" @click="send">Додати</button>
    <button class="btn btn-outline-secondary btn-sm" @click="picked = null">✕</button>
  </div>
  <div v-else class="position-relative">
    <input v-model="q" class="form-control form-control-sm" :placeholder="placeholder"
           @focus="open = true" @blur="open = false">
    <div v-if="open && found.length" class="list-group position-absolute w-100 shadow" style="z-index: 10">
      <button v-for="t in found" :key="t.slug" type="button"
              class="list-group-item list-group-item-action py-1 small" @mousedown.prevent="pick(t)">
        {{ COINS[t.coin] || '·' }} {{ t.title }} <span class="text-secondary">— {{ t.subzone }}</span>
      </button>
    </div>
  </div>
</template>
