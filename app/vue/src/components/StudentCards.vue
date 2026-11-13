<script setup>
import { computed } from 'vue'

import Avatar from '@core/components/Avatar.vue'
import { getGames } from '../api.js'
import { games } from '../catalog.js'
import { lookAs, user } from '@core/user.js'

// /students as a gallery: who picked which game — and its cover, once a window has a screenshot; the counters of the
// description are everyone's since the insides opened (T259); the admin also sees what is accepted, what waits for
// their word (⏳) and has «👁» — straight into the student's own «Моя гра» as them
defineProps({ students: Array })
const admin = computed(() => user.value?.status === 'admin')
const fio = (s) => s.name || s.nick
const counts = (g) => [[g.entities, 'сут.'], [g.rules, 'правил'], [g.windows, 'вікон'], [g.claims, 'заявок']].filter(([n]) => n).map(([n, w]) => `${n} ${w}`).join(' · ')
const base = (g) => games.value.find((b) => b.slug === g.base_game)
const few = (n) => n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)
const waits = (n) => `${n} ${n % 10 === 1 && n % 100 !== 11 ? 'заявка чекає' : few(n) ? 'заявки чекають' : 'заявок чекають'} вердикту`
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
            <span class="ms-auto d-inline-flex align-items-center gap-2 text-nowrap">
              <span class="text-secondary small">{{ s.group }}</span>
              <a v-if="admin && s.status !== 'admin'" href="#" class="ibtn" :title="`Очима студента: його «Моя гра»${s.test ? '' : ' — лише перегляд'}`"
                 @click.prevent.stop="lookAs(s.nick, '/my/game')">👁</a>
            </span>
          </div>
          <div v-if="s.game.id" class="mt-1">
            🎮 {{ s.game.title }}
            <div class="text-secondary small">основа: {{ baseText(s.game) }}</div>
            <div v-if="counts(s.game)" class="text-secondary small">{{ counts(s.game) }}<span v-if="admin && s.game.accepted" class="text-success"> · ✓ {{ s.game.accepted }}</span><span
              v-if="admin && s.game.waiting" class="wait" :title="waits(s.game.waiting)"> · ⏳ {{ s.game.waiting }}</span></div>
          </div>
          <div v-else class="text-secondary mt-1">Гру ще не обрано</div>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.cover { height: 140px; }
.wait { color: var(--bs-warning-text-emphasis); }
</style>
