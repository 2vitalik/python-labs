<script setup>
import { computed } from 'vue'

import { taskIndex, zones } from '../catalog.js'
import { zonePath } from '../ideas.js'

// what a record is about: its category → subcategory (to /tasks with that filter) and its card (to /tasks, searched by name)
const props = defineProps({ r: Object })
const path = computed(() => zonePath(props.r.zone, props.r.subzone))
const toZone = computed(() => ({ path: '/tasks', query: props.r.subzone ? { zone: props.r.zone, sub: props.r.subzone } : { zone: props.r.zone } }))
const name = computed(() => taskIndex.value[props.r.task]?.title || props.r.task)
</script>

<template>
  <RouterLink v-if="path" :to="toZone" class="rchip zone" :style="{ '--zc': zones[r.zone].color }">{{ path }}</RouterLink>
  <RouterLink v-if="r.task" :to="{ path: '/tasks', query: { q: name } }" class="rchip" title="Картка в каталозі">{{ name }}</RouterLink>
</template>

<style scoped>
.rchip { display: inline-block; max-width: 100%; padding: 0 .5rem; border: 1px solid var(--bs-border-color); border-radius: 1rem;
         color: var(--bs-body-color); font-size: .78rem; line-height: 1.6; text-decoration: none; }
.rchip:hover { background: var(--bs-tertiary-bg); }
.rchip.zone { color: var(--zc); background: color-mix(in srgb, var(--zc) 8%, var(--bs-body-bg));
              border-color: color-mix(in srgb, var(--zc) 40%, var(--bs-body-bg)); }
.rchip.zone:hover { background: color-mix(in srgb, var(--zc) 16%, var(--bs-body-bg)); }
[data-bs-theme=dark] .rchip.zone { color: color-mix(in srgb, var(--zc) 60%, var(--bs-body-color)); }
</style>
