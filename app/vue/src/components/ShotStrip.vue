<script setup>
import { ref } from 'vue'

import { deleteShot, uploadShot } from '../api.js'

const props = defineProps({ part: Object })
const emit = defineEmits(['changed'])
const error = ref('')
const busy = ref(false)

async function onFile(e) {
  const file = e.target.files[0]
  e.target.value = ''
  if (!file) return
  error.value = ''
  busy.value = true
  try {
    await uploadShot(props.part.id, file)
    emit('changed')
  } catch (err) {
    error.value = err.message
  } finally {
    busy.value = false
  }
}

async function remove(name) {
  await deleteShot(props.part.id, name)
  emit('changed')
}
</script>

<template>
  <div class="d-flex flex-wrap gap-2 align-items-center">
    <div v-for="s in part.screenshots" :key="s" class="position-relative">
      <a :href="`/api/uploads/${part.game}/${s}`" target="_blank">
        <img :src="`/api/uploads/${part.game}/${s}`" class="rounded border shot">
      </a>
      <button class="btn-close bg-white border rounded-circle position-absolute top-0 end-0 m-1 p-1"
              title="У кошик" @click="remove(s)"></button>
    </div>
    <label class="btn btn-outline-secondary btn-sm" :class="{ disabled: busy }">
      📷 Скриншот
      <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" hidden @change="onFile">
    </label>
    <div v-if="error" class="text-danger small w-100">{{ error }}</div>
  </div>
</template>

<style scoped>
.shot { height: 72px; }
</style>
