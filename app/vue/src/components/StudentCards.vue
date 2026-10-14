<script setup>
import { computed } from 'vue'

import Avatar from '@core/components/Avatar.vue'
import { getGames } from '../api.js'
import { games } from '../catalog.js'
import { user } from '@core/user.js'

// /students as a gallery: who picked which game — and its cover, once a window has a screenshot;
// the counters of the game's insides are the admin's, like the insides themselves (T216)
defineProps({ students: Array })
const admin = computed(() => user.value?.status === 'admin')
const fio = (s) => s.name || s.nick
const base = (g) => games.value.find((b) => b.slug === g.base_game)
const baseText = (g) => (base(g) ? `${base(g).icon} ${base(g).title}` : `✨ ${g.base_custom}`)
if (!games.value.length) getGames().then((g) => (games.value = g))
</script>

<template>
  <p v-if="!students.length" class="text-secondary">Ще ніхто не обрав гру.</p>
  <div class="row g-3">
    <div v-for="s in students" :key="s.nick" class="col-md-6 col-lg-4">
      <RouterLink :to="`/students/${s.nick}`" class="card h-100 text-decoration-none text-body">
        <img v-if="s.game.cover" :src="s.game.cover" class="card-img-top object-fit-cover cover">
        <div class="card-body">
          <div class="d-flex flex-wrap align-items-center gap-2">
            <Avatar :user="s" :size="28" />
            <span class="fw-semibold text-nowrap">{{ fio(s) }}</span>
            <span v-if="s.status === 'admin'" class="badge text-bg-secondary fw-normal">викладач</span>
            <span v-else-if="s.status === 'pending'" class="badge text-bg-warning fw-normal">очікує</span>
            <span class="text-secondary small ms-auto text-nowrap">{{ s.group }}</span>
          </div>
          <div v-if="s.game.id" class="mt-1">
            🎮 {{ s.game.title }}
            <div class="text-secondary small">основа: {{ baseText(s.game) }}</div>
            <div v-if="admin" class="text-secondary small">вікон: {{ s.game.windows }} · меню: {{ s.game.menus }} · заявок: {{ s.game.claims }}</div>
          </div>
          <div v-else class="text-secondary mt-1">Гру ще не обрано</div>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.cover { height: 140px; }
</style>
