<script setup>
import CopyNicks from './CopyNicks.vue'

// those who can't come to nearly any class (T186): they weigh the same on every window and hide the difference between them.
// Left out — they leave the strips and every count, and stay named here: they need a talk, not a better hour
defineProps({ people: { type: Array, required: true } })
const counted = defineModel({ type: Boolean, required: true })
</script>

<template>
  <div v-if="people.length" class="small mb-3">
    <span>🧱 Майже ніколи не можуть — {{ people.length }}:</span>
    <template v-for="({ s }, i) in people" :key="s.nick">{{ i ? ',' : '' }} <RouterLink :to="`/activity?user=${s.nick}`">{{ s.name || s.nick }}</RouterLink></template>
    <CopyNicks class="ms-1" :people="people.map((p) => p.s)" />
    <div class="form-check form-switch mt-1 mb-0">
      <input id="week-stuck" v-model="counted" class="form-check-input" type="checkbox">
      <label for="week-stuck" class="form-check-label">{{ counted ? 'рахуються в усіх числах' : 'не рахуються: їх нема ні на смужках, ні в числах' }}</label>
    </div>
  </div>
</template>
