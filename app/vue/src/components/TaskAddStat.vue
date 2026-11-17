<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { iconOf, statOf } from '../catalog.js'
import { hasStat } from '../gameAdd.js'
import { useGameCtx } from '../gameCtx.js'

// «＋» of a stat card asks whom to give it: the game's entities ticked (those that have it — ticked and locked) and the value;
// emits send(parts, value)
const props = defineProps({ task: Object, busy: Boolean })
const emit = defineEmits(['send', 'cancel'])
const { parts } = useGameCtx()
const entities = computed(() => parts.value.filter((p) => p.kind === 'entity'))
const picked = ref([])
const value = ref('')
const unit = computed(() => statOf(props.task.opt)?.unit || props.task.slots?.[0]?.unit || '')
const ready = computed(() => picked.value.length && value.value.trim() && !props.busy)
const send = () => ready.value && emit('send', entities.value.filter((p) => picked.value.includes(p.id)), value.value.trim())
</script>

<template>
  <div v-if="!entities.length" class="small text-secondary">Спершу додай сутність: «＋» на типі сутності або в «Моїй грі»</div>
  <template v-else>
    <div class="small mb-1">Кому додати «{{ task.title }}»?</div>
    <label v-for="p in entities" :key="p.id" class="form-check small mb-0">
      <input v-if="hasStat(p, task.opt)" class="form-check-input" type="checkbox" checked disabled>
      <input v-else v-model="picked" class="form-check-input" type="checkbox" :value="p.id">
      {{ iconOf(p) }} {{ p.title }} <span v-if="hasStat(p, task.opt)" class="text-secondary">— уже є</span>
    </label>
    <div class="d-flex align-items-center gap-2 my-2">
      <input v-model="value" class="form-control form-control-sm val" placeholder="значення" @keydown.enter="send">
      <span v-if="unit" class="small text-secondary">{{ unit }}</span>
    </div>
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-add" :disabled="!ready" @click="send"><Icon name="plus" /> Додати</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
    </div>
  </template>
</template>

<style scoped>
.val { width: 6rem; }
</style>
