<script setup>
// a section's heading in the editor: icon and title, a count, a muted note, and the section's own actions on the right
defineProps({ icon: String, title: String, count: [Number, String], note: String })
</script>

<template>
  <h2 class="h6 head d-flex flex-wrap align-items-center gap-2">
    <span>{{ icon }} {{ title }} <span v-if="count !== undefined" class="count">({{ count }})</span></span>
    <span v-if="note" class="note">{{ note }}</span>
    <span class="ms-auto d-flex align-items-center gap-1"><slot /></span>
  </h2>
</template>

<style scoped>
.head { min-height: 2.1rem; margin-bottom: .5rem; padding-bottom: .25rem; border-bottom: 1px solid var(--bs-border-color); font-weight: 700; }
.count { font-weight: 400; opacity: .55; }
.note { font-size: .8rem; font-weight: 400; color: var(--bs-secondary-color); }
</style>
