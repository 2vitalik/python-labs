<script setup>
import { ref } from 'vue'

import Icon from './Icon.vue'
import Pop from './Pop.vue'

// the trash icon of an object: it asks in a small panel over the page, so the row it sits in does not jump
defineProps({ what: String, note: String, title: { type: String, default: 'Видалити' } })
const emit = defineEmits(['yes'])
const open = ref(false)
const yes = () => { open.value = false; emit('yes') }
</script>

<template>
  <Pop v-model="open" width="16rem">
    <template #trigger="{ toggle }">
      <button type="button" class="iact del" :title @click.stop="toggle"><Icon name="trash" /></button>
    </template>
    <div class="mb-2">Видалити {{ what }}?<div v-if="note" class="text-secondary small">{{ note }}</div></div>
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-danger" @click="yes">Видалити</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false">Скасувати</button>
    </div>
  </Pop>
</template>
