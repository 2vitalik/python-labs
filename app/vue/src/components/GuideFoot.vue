<script setup>
// under a guide page: «Оновлено» (when the page has a date), the caller's own line, and the way to the whole guide
defineProps({ updated: String })
const fmt = (d) => new Date(d).toLocaleDateString('uk-UA')
</script>

<template>
  <div class="foot small mt-4 text-end">
    <div v-if="updated" class="text-body-tertiary">Оновлено {{ fmt(updated) }}</div>
    <slot />
    <div class="mt-1"><RouterLink to="/all">📖 Уся методичка</RouterLink></div>
  </div>
</template>

<style scoped>
.foot a { color: var(--bs-secondary-color); text-decoration: none; }
.foot a:hover { text-decoration: underline; }
</style>
