<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { missingParams } from '../catalog.js'
import SlotFields from './SlotFields.vue'

// «＋» of a card whose claim takes params: its slots to fill first; emits send(params)
const props = defineProps({ task: Object, busy: Boolean })
const emit = defineEmits(['send', 'cancel'])
const params = ref({})
const ready = computed(() => !missingParams(props.task, params.value).length && !props.busy)
</script>

<template>
  <div class="small text-secondary mb-1">Параметри заявки</div>
  <div class="d-flex flex-wrap gap-2 align-items-center mb-2"><SlotFields :specs="task.slots" :params /></div>
  <div class="d-flex gap-2">
    <button type="button" class="btn btn-sm btn-add" :disabled="!ready" @click="emit('send', params)"><Icon name="plus" /> Додати</button>
    <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
  </div>
</template>
