<script setup>
import { reactive, ref } from 'vue'

import { postMyGame, putMyGame } from '../api.js'
import { games } from '../catalog.js'

const props = defineProps({ game: Object })
const emit = defineEmits(['saved'])
const form = reactive({
  title: props.game?.title || '',
  base_game: props.game?.base_game || '',
  base_custom: props.game?.base_custom || '',
  description: props.game?.description || '',
})
const error = ref('')

async function save() {
  error.value = ''
  try {
    emit('saved', await (props.game ? putMyGame(form) : postMyGame(form)))
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <form class="card" @submit.prevent="save">
    <div class="card-body vstack gap-3">
      <div>
        <label class="form-label">Назва гри</label>
        <input v-model="form.title" class="form-control" placeholder="Наприклад: Танчики делюкс">
      </div>
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label">Гра-основа з каталогу</label>
          <select v-model="form.base_game" class="form-select">
            <option value="">— своя основа —</option>
            <option v-for="g in games" :key="g.slug" :value="g.slug">{{ g.icon }} {{ g.title }}</option>
          </select>
        </div>
        <div v-if="!form.base_game" class="col-md-6">
          <label class="form-label">Своя основа</label>
          <input v-model="form.base_custom" class="form-control" placeholder="Опиши гру кількома словами">
        </div>
      </div>
      <div>
        <label class="form-label">Опис <span class="text-secondary small">(markdown)</span></label>
        <textarea v-model="form.description" class="form-control" rows="4"></textarea>
      </div>
      <div v-if="error" class="alert alert-danger mb-0">{{ error }}</div>
      <div><button class="btn btn-primary">{{ game ? 'Зберегти' : 'Створити гру' }}</button></div>
    </div>
  </form>
</template>
