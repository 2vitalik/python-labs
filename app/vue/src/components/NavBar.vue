<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { SECTIONS } from '../guide.js'
import { canAccess, user } from '../user.js'

const isDev = import.meta.env.DEV
const route = useRoute()
const router = useRouter()
const links = [
  ...SECTIONS.map((s) => [s.path, s.nav]),
  ['/students', 'Студенти'], ['/refs', 'Знахідки'], ['/my/game', 'Моя гра'], ['/profile', 'Профіль'],
]
// menu follows route access, so a page and its link open together
const visible = computed(() => links.filter(([to]) => canAccess(router.resolve(to).meta.access)))
// sign-in buttons bring the user back to the page they were on
const next = computed(() => `?next=${encodeURIComponent(route.fullPath)}`)
// bootstrap JS is not loaded, so the phone menu toggles here; the admin's 9 links need a wider row
const open = ref(false)
const expand = computed(() => (user.value?.status === 'admin' ? 'navbar-expand-xl' : 'navbar-expand-lg'))
watch(() => route.fullPath, () => (open.value = false))
</script>

<template>
  <nav class="navbar bg-body-tertiary border-bottom" :class="expand">
    <div class="container">
      <RouterLink class="navbar-brand" to="/">Python Labs</RouterLink>
      <button class="navbar-toggler" type="button" aria-label="Меню" @click="open = !open">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" :class="{ show: open }">
        <ul class="navbar-nav me-auto">
          <li v-for="[to, text] in visible" :key="to" class="nav-item">
            <RouterLink class="nav-link" :to="to">{{ text }}</RouterLink>
          </li>
        </ul>
        <div class="d-flex align-items-center gap-2 py-2 py-lg-0">
          <template v-if="user">
            <img v-if="user.picture" :src="user.picture" class="rounded-circle" width="32" height="32" :alt="user.name">
            <span class="d-none d-xl-inline">{{ user.name || user.email }}</span>
            <a class="btn btn-outline-secondary btn-sm" href="/api/auth/logout">Вийти</a>
          </template>
          <template v-else>
            <a v-if="isDev" class="btn btn-outline-secondary btn-sm" :href="'/api/auth/dev-login' + next">Dev-вхід</a>
            <a class="btn btn-primary btn-sm" :href="'/api/auth/login' + next">Увійти з Google</a>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>
