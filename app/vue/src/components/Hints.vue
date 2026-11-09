<script setup>
// gentle «чого бракує» list; a click scrolls to the section or the part in question
defineProps({ items: Array })
const emit = defineEmits(['go'])
</script>

<template>
  <ul v-if="items.length" class="hints list-unstyled small mb-0 vstack gap-1">
    <li v-for="h in items" :key="h.text" role="button" class="d-flex gap-1" @click="emit('go', h.to)">
      <span>💡</span><span class="text-secondary">{{ h.text }}</span>
    </li>
  </ul>
</template>

<style scoped>
.hints li:hover span:last-child { color: var(--bs-body-color) !important; text-decoration: underline dotted; }
</style>
