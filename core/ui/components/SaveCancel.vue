<script setup>
import Icon from './Icon.vue'

// «Зберегти / Скасувати» of a form in the description (T294 §5): the standard pair as two small drawn buttons at the
// bottom right of the framed form — the green tick saves, the grey cross closes it unsaved; the words come under the
// mouse at once. `disabled` — nothing to save yet; the slot — the form's other actions, on the left
defineProps({ disabled: Boolean })
defineEmits(['save', 'cancel'])
</script>

<template>
  <div class="sc">
    <slot />
    <span class="ms-auto d-flex gap-1">
      <button type="button" class="btn btn-sm btn-outline-secondary sc-b qtip" data-tip="Скасувати" aria-label="Скасувати" @click="$emit('cancel')"><Icon name="x" /></button>
      <button type="button" class="btn btn-sm btn-success sc-b qtip qtip-end" :disabled data-tip="Зберегти" aria-label="Зберегти" @click="$emit('save')"><Icon name="check" /></button>
    </span>
  </div>
</template>

<style scoped>
.sc { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; }
.sc-b { justify-content: center; width: 2.2rem; padding: .2rem 0; }
</style>
