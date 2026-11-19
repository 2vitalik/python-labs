<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

import { vHint } from '@core/hint.js'

// a message's words: two lines at most until clicked; the teacher's own line says «ти:»
defineProps({ text: String, mine: Boolean })
const el = ref()
const open = ref(false)
const long = ref(false)
const sized = new ResizeObserver(() => (long.value = open.value || el.value.scrollHeight > el.value.clientHeight + 1))
onMounted(() => sized.observe(el.value))
onBeforeUnmount(() => sized.disconnect())
</script>

<template>
  <p ref="el" v-hint="long && !open ? 'клік — увесь текст' : ''" class="text" :class="{ cut: !open, long }"
     @click="long && (open = !open)"><span v-if="mine" class="me">ти: </span>{{ text }}</p>
</template>

<style scoped>
.text { margin: 0; white-space: pre-line; overflow-wrap: anywhere; }
.cut { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; line-clamp: 2; overflow: hidden; }
.long { cursor: pointer; }
.me { font-style: italic; }
</style>
