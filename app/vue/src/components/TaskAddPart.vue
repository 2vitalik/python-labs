<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { kindOf, roleOf } from '../catalog.js'
import EmojiField from './EmojiField.vue'

// «＋» of a window type or an entity type asks the new object's name first (T278 §1). A window starts with the type's name,
// selected to type over; an entity's starts empty — a type's name is rarely an entity's. Emits send({ icon, title, description })
const props = defineProps({ task: Object, busy: Boolean })
const emit = defineEmits(['send', 'cancel'])
const isWindow = kindOf(props.task) === 'window'
const form = reactive({ icon: '', title: isWindow ? props.task.title : '', description: '' })
const titleInput = ref()
const ready = computed(() => !!form.title.trim() && !props.busy)
const send = () => ready.value && emit('send', { ...form, title: form.title.trim(), description: form.description.trim() })
onMounted(() => {
  titleInput.value.focus({ preventScroll: true })
  titleInput.value.select()
})
</script>

<template>
  <div class="small mb-1">{{ isWindow ? 'Нове вікно' : 'Нова сутність' }} типу «{{ task.title }}»</div>
  <div class="d-flex gap-2 mb-2">
    <EmojiField v-if="!isWindow" v-model="form.icon" :placeholder="roleOf(task.opt).icon" />
    <input ref="titleInput" v-model="form.title" class="form-control form-control-sm"
           :placeholder="isWindow ? 'Назва вікна' : 'Назва: Привид, Стіна…'" @keydown.enter="send">
  </div>
  <input v-model="form.description" class="form-control form-control-sm mb-2" @keydown.enter="send"
         :placeholder="isWindow ? 'Що на цьому вікні (необовʼязково)' : 'Що це і як поводиться (необовʼязково)'">
  <div class="d-flex gap-2">
    <button type="button" class="btn btn-sm btn-success" :disabled="!ready" @click="send"><Icon name="check" /> Додати</button>
    <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
  </div>
</template>
