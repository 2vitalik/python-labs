<script setup>
import { onMounted, ref, watch } from 'vue'

// textarea that grows and shrinks with its text: one row when empty, never a scrollbar
const model = defineModel({ default: '' })
const el = ref()
function fit() {
  el.value.style.height = 'auto'
  el.value.style.height = `${el.value.scrollHeight + el.value.offsetHeight - el.value.clientHeight}px`
}
onMounted(fit)
watch(model, fit, { flush: 'post' })
</script>

<template>
  <textarea ref="el" v-model="model" rows="1"></textarea>
</template>

<style scoped>
textarea { overflow: hidden; resize: none; }
</style>
