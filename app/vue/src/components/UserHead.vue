<script setup>
import { computed } from 'vue'

import Avatar from './Avatar.vue'

const props = defineProps({ user: { type: Object, required: true }, title: String })
const heading = computed(() => props.title
  || `${props.user.last_name} ${props.user.first_name}`.trim() || props.user.name || props.user.nick)
const checks = computed(() => [
  ['ПІБ', props.user.last_name && props.user.first_name],
  ['GitHub', props.user.github],
  ['Telegram', props.user.tg_linked],
])
</script>

<template>
  <div class="d-flex align-items-center gap-3 mb-4">
    <Avatar :user :size="56" />
    <div>
      <h1 class="h3 mb-0">{{ heading }}</h1>
      <div class="text-secondary">{{ [user.group, user.email].filter(Boolean).join(' · ') }}</div>
      <div class="d-flex gap-1 mt-1">
        <span v-for="[label, ok] in checks" :key="label" class="badge rounded-pill fw-normal"
              :class="ok ? 'bg-success-subtle text-success-emphasis' : 'bg-danger-subtle text-danger-emphasis'">
          {{ ok ? '✓' : '○' }} {{ label }}
        </span>
      </div>
    </div>
  </div>
</template>
