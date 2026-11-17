<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { whyOk } from '../asked.js'
import { missingParams } from '../catalog.js'
import SlotFields from './SlotFields.vue'
import WhyField from './WhyField.vue'

// «＋» of a card whose claim takes params, or of a card «за запитом» (`why`, T319): its sentence and its slots to fill
// first; emits send(params, why)
const props = defineProps({ task: Object, busy: Boolean, why: Boolean })
const emit = defineEmits(['send', 'cancel'])
const params = ref({})
const text = ref('')
const ready = computed(() => !missingParams(props.task, params.value).length && (!props.why || whyOk(text.value)) && !props.busy)
</script>

<template>
  <WhyField v-if="why" v-model="text" class="mb-2" />
  <template v-if="task.slots?.length">
    <div class="small text-secondary mb-1">Параметри заявки</div>
    <div class="d-flex flex-wrap gap-2 align-items-center mb-2"><SlotFields :specs="task.slots" :params /></div>
  </template>
  <div class="d-flex gap-2">
    <button type="button" class="btn btn-sm btn-add" :disabled="!ready" @click="emit('send', params, why ? text.trim() : '')"><Icon name="plus" /> Додати</button>
    <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
  </div>
</template>
