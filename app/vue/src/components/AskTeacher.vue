<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { postRef } from '../api.js'

// «Картка мала б бути деінде?» (T270 §6): one line to the teacher — an idea and a Telegram alert; the teacher moves the card
const props = defineProps({ title: String })
const open = ref(false)
const text = ref('')
const sent = ref(false)
const error = ref('')

async function send() {
  error.value = ''
  try {
    await postRef({ title: `Картка «${props.title}»: інше місце`, note: text.value.trim() })
    sent.value = true
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="small">
    <span v-if="sent" class="text-success">Надіслано ✓</span>
    <a v-else-if="!open" href="#" class="text-secondary" @click.prevent="open = true">Картка мала б бути деінде?</a>
    <div v-else class="d-flex flex-wrap gap-2">
      <input v-model="text" class="form-control form-control-sm flex-grow-1 w-auto" placeholder="де їй місце і чому" @keydown.enter="text.trim() && send()">
      <button type="button" class="btn btn-sm btn-add" :disabled="!text.trim()" @click="send"><Icon name="plus" /> Написати викладачу</button>
    </div>
    <div v-if="error" class="text-danger">{{ error }}</div>
  </div>
</template>
