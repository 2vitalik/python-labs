<script setup>
import { computed, ref, watch } from 'vue'

// Google avatar links fail now and then (rate limit, stale link): no referrer helps, an initial stands in on error
const props = defineProps({ user: { type: Object, required: true }, size: { type: Number, default: 32 } })
const failed = ref(false)
watch(() => props.user.picture, () => (failed.value = false))
const initial = computed(() =>
  (props.user.last_name || props.user.name || props.user.nick || props.user.email || '?')[0].toUpperCase())
</script>

<template>
  <img v-if="user.picture && !failed" :src="user.picture" class="rounded-circle flex-shrink-0" :width="size" :height="size"
       :alt="user.name" referrerpolicy="no-referrer" @error="failed = true">
  <span v-else class="rounded-circle flex-shrink-0 bg-secondary-subtle text-secondary d-inline-flex align-items-center justify-content-center fw-semibold"
        :style="{ width: size + 'px', height: size + 'px', fontSize: size * 0.45 + 'px' }">{{ initial }}</span>
</template>
