<script setup>
import { onMounted, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { postRef } from '../api.js'

// «нема потрібного — запропонуй» (T270 §10.2): a name and two words go to the teacher as an idea (/ideas + Telegram)
const props = defineProps({ what: String, allTo: String })
const emit = defineEmits(['done', 'cancel'])
const name = ref('')
const note = ref('')
const error = ref('')
const sent = ref(false)
const first = ref()
onMounted(() => first.value?.focus())

async function send() {
  error.value = ''
  try {
    await postRef({ title: `Пропозиція: ${props.what} «${name.value.trim()}»`, note: note.value.trim() })
    sent.value = true
    setTimeout(() => emit('done', name.value.trim()), 1200)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="vstack gap-2 small">
    <div v-if="allTo" class="text-secondary">
      Спершу глянь <RouterLink :to="allTo">усі</RouterLink> — може, потрібне є під іншою назвою
    </div>
    <div v-if="sent" class="text-success">Надіслано викладачу ✓</div>
    <template v-else>
      <input ref="first" v-model="name" class="form-control form-control-sm" placeholder="Назва" @keydown.enter="name.trim() && send()">
      <input v-model="note" class="form-control form-control-sm" placeholder="Що це — два слова" @keydown.enter="name.trim() && send()">
      <div class="d-flex gap-2">
        <button type="button" class="btn btn-sm btn-add" :disabled="!name.trim()" @click="send"><Icon name="plus" /> Запропонувати</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
      </div>
    </template>
    <div v-if="error" class="text-danger">{{ error }}</div>
  </div>
</template>
