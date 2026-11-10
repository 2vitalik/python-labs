<script setup>
// the teacher's word on an auto-claim, tiny, inside a pill or a label: ✓ accepted, ↩ returned (the verdict as the tooltip)
defineProps({ claim: Object })
</script>

<template>
  <span v-if="claim?.status === 'accepted'" class="jm text-success" :title="claim.verdict || 'зараховано'">✓</span>
  <span v-else-if="claim?.status === 'returned'" class="jm text-danger" :title="claim.verdict || 'повернуто — доробити'">↩</span>
</template>

<style scoped>
.jm { margin-left: .2rem; font-size: .8em; font-weight: 700; }
</style>
