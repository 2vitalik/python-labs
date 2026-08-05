<script setup>
import { KLASSES, STATUSES } from '../catalog.js'

defineProps({ game: Object })
</script>

<template>
  <RouterLink :to="`/games/${game.slug}`" class="card h-100 text-decoration-none text-body">
    <div class="card-body">
      <div class="d-flex align-items-center gap-2 mb-1">
        <span class="fs-3">{{ game.icon }}</span>
        <span class="fs-5 fw-semibold">{{ game.title }}</span>
        <span v-if="game.status !== 'active'" class="badge text-bg-warning ms-auto">{{ STATUSES[game.status] }}</span>
      </div>
      <div class="text-secondary small mb-1">{{ KLASSES[game.klass] }}</div>
      <div>{{ game.summary }}</div>
    </div>
  </RouterLink>
</template>
