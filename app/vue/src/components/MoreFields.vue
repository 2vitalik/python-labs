<script setup>
import { computed } from 'vue'

// the quiet row of a form's rare fields under it (T291 §4): «＋ нотатка · ＋ стани» — a click brings that field, so the
// form holds no empty fields «just in case». `fields` — { key: label }; `shown` — which of them are in the form already
const props = defineProps({ fields: Object, shown: Object })
defineEmits(['show'])
const hidden = computed(() => Object.entries(props.fields).filter(([k]) => !props.shown[k]))
</script>

<template>
  <div v-if="hidden.length" class="more-row">
    <button v-for="[k, label] in hidden" :key="k" type="button" class="more-field" @click="$emit('show', k)">＋ {{ label }}</button>
  </div>
</template>

<style scoped>
.more-row { display: flex; flex-wrap: wrap; gap: .1rem .9rem; }
</style>
