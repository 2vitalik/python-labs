<script setup>
import { onMounted, ref } from 'vue'

import { zones } from '../catalog.js'
import DraftHead from './DraftHead.vue'

// a new level (T310): its card's head — 🪜 and the name; Enter saves, the rest is added on the card
const emit = defineEmits(['done', 'cancel'])
const title = ref('')
const head = ref()
onMounted(() => head.value.focus({ preventScroll: true }))  // the editor scrolls to the section itself
const enter = () => title.value.trim() && head.value.create({ kind: 'level' })
</script>

<template>
  <DraftHead ref="head" v-model="title" :zone="zones.levels?.color" placeholder="Назва: Рівень 1, Печери 5–9…"
             @enter="enter" @done="emit('done')" @cancel="emit('cancel')">
    <template #sign><span class="sign">🪜</span></template>
  </DraftHead>
</template>

<style scoped>
.sign { flex-shrink: 0; }
</style>
