<script setup>
import { computed } from 'vue'

const props = defineProps({ user: { type: Object, required: true }, title: String })
const heading = computed(() => props.title
  || `${props.user.last_name} ${props.user.first_name}`.trim() || props.user.name || props.user.nick)
const checks = computed(() => [
  ['ПІБ', props.user.last_name && props.user.first_name],
  ['GitHub', props.user.github],
  ['Telegram-бот', props.user.tg_linked],
])
</script>

<template>
  <div class="d-flex align-items-center gap-3 mb-4">
    <img v-if="user.picture" :src="user.picture" class="rounded-circle avatar" :alt="heading">
    <div v-else class="rounded-circle avatar bg-secondary-subtle text-secondary d-flex align-items-center justify-content-center fs-4">
      {{ (user.last_name || user.nick)[0].toUpperCase() }}
    </div>
    <div>
      <h1 class="h3 mb-0">{{ heading }}</h1>
      <div class="text-secondary">{{ [user.group, user.email].filter(Boolean).join(' · ') }}</div>
      <div class="d-flex gap-1 mt-1">
        <span v-for="[label, ok] in checks" :key="label" class="badge rounded-pill fw-normal"
              :class="ok ? 'bg-success-subtle text-success-emphasis' : 'bg-body-secondary text-secondary'">
          {{ ok ? '✓' : '○' }} {{ label }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.avatar { width: 56px; height: 56px; flex: none; }
</style>
