<script setup>
import { computed } from 'vue'

import Avatar from '@core/components/Avatar.vue'
import { games } from '../catalog.js'

// the top of «Моя гра» and of a student's game page, the profile's way (UserHead): a big icon, the title, a line on the base;
// under it — the owner's checks on their own page, or the student whose game it is; the slot sits at the right edge
const props = defineProps({ game: Object, title: String, checks: Boolean, student: Object })
const base = computed(() => games.value.find((g) => g.slug === props.game?.base_game))
const icon = computed(() => (props.game ? base.value?.icon || '✨' : '🎮'))
const checkList = computed(() => [['основа', props.game], ['назва', props.game], ['опис', props.game?.description]])
</script>

<template>
  <div class="d-flex align-items-center gap-3 mb-4">
    <span class="icon rounded-circle bg-secondary-subtle d-inline-flex align-items-center justify-content-center flex-shrink-0">{{ icon }}</span>
    <div>
      <h1 class="h3 mb-0">{{ game?.title || title }}</h1>
      <div class="text-secondary">
        <template v-if="!game">Гру ще не обрано</template>
        <template v-else-if="base">основа: <RouterLink :to="`/games/${base.slug}`">{{ base.title }}</RouterLink></template>
        <template v-else>своя основа: {{ game.base_custom }}</template>
      </div>
      <div v-if="checks" class="d-flex gap-1 mt-1">
        <span v-for="[label, ok] in checkList" :key="label" class="badge rounded-pill fw-normal"
              :class="ok ? 'bg-success-subtle text-success-emphasis' : 'bg-danger-subtle text-danger-emphasis'">{{ ok ? '✓' : '○' }} {{ label }}</span>
      </div>
      <div v-else-if="student" class="d-flex align-items-center gap-2 mt-1 small">
        <Avatar :user="student" :size="22" />
        <span>{{ student.name }}</span>
        <span v-if="student.group" class="text-secondary">· {{ student.group }}</span>
      </div>
    </div>
    <slot />
  </div>
</template>

<style scoped>
.icon { width: 56px; height: 56px; font-size: 28px; }
</style>
