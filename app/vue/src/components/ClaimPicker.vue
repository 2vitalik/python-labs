<script setup>
import { computed, ref } from 'vue'

import { COINS, tasks } from '../catalog.js'

defineProps({ placeholder: { type: String, default: '＋ заявка: пошук картки…' } })
const emit = defineEmits(['pick'])
const q = ref('')
const open = ref(false)
const found = computed(() => {
  const s = q.value.trim().toLowerCase()
  if (s.length < 2) return []
  return tasks.value.filter((t) => (t.title + ' ' + t.slug).toLowerCase().includes(s)).slice(0, 8)
})

function pick(t) {
  emit('pick', t.slug)
  q.value = ''
  open.value = false
}
</script>

<template>
  <div class="position-relative">
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
