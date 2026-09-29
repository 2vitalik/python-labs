<script setup>
import Avatar from '@core/components/Avatar.vue'

// /students as a gallery: every student with the cover of their game
defineProps({ students: Array })
const fio = (s) => s.name || s.nick
</script>

<template>
  <div class="row g-3">
    <div v-for="s in students" :key="s.nick" class="col-md-6 col-lg-4">
      <RouterLink :to="`/students/${s.nick}`" class="card h-100 text-decoration-none text-body">
        <img v-if="s.game.cover" :src="s.game.cover" class="card-img-top object-fit-cover cover">
        <div class="card-body">
          <div class="d-flex align-items-center gap-2">
            <Avatar :user="s" :size="28" />
            <span class="fw-semibold">{{ fio(s) }}</span>
            <span v-if="s.status === 'admin'" class="badge text-bg-secondary fw-normal">викладач</span>
            <span v-else-if="s.status === 'pending'" class="badge text-bg-warning fw-normal">очікує</span>
            <span class="text-secondary small ms-auto">{{ s.group }}</span>
          </div>
          <div v-if="s.game.id" class="mt-1">
            🎮 {{ s.game.title }}
            <div class="text-secondary small">вікон: {{ s.game.windows }} · меню: {{ s.game.menus }} · заявок: {{ s.game.claims }}</div>
          </div>
          <div v-else class="text-secondary mt-1">Гра ще не створена</div>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.cover { height: 140px; }
</style>
