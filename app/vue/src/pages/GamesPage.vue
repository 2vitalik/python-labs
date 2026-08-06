<script setup>
import { computed, onMounted, ref } from 'vue'

import GameCard from '../components/GameCard.vue'
import { games, KLASSES, loadCatalog } from '../catalog.js'
import { user } from '../user.js'

const klass = ref('')
const shown = computed(() => games.value.filter((g) => !klass.value || g.klass === klass.value))

onMounted(loadCatalog)
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h1 class="h3 mb-0">Ігри <span class="text-secondary fs-6">({{ shown.length }})</span></h1>
      <RouterLink v-if="user?.status === 'admin'" to="/games/new" class="btn btn-outline-primary btn-sm">➕ Нова гра</RouterLink>
    </div>

    <div class="mb-3 d-flex gap-2 flex-wrap">
      <button class="btn btn-sm" :class="klass === '' ? 'btn-primary' : 'btn-outline-secondary'" @click="klass = ''">всі</button>
      <button v-for="(label, k) in KLASSES" :key="k" class="btn btn-sm"
              :class="klass === k ? 'btn-primary' : 'btn-outline-secondary'" @click="klass = k">{{ label }}</button>
    </div>

    <div class="row g-3">
      <div v-for="g in shown" :key="g.id" class="col-md-6 col-lg-4"><GameCard :game="g" /></div>
    </div>
  </div>
</template>
