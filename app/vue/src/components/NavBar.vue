<script setup>
import { computed } from 'vue'

import { user } from '../user.js'

const isDev = import.meta.env.DEV
const active = computed(() => user.value && user.value.status !== 'pending')
</script>

<template>
  <nav class="navbar navbar-expand bg-body-tertiary border-bottom">
    <div class="container">
      <RouterLink class="navbar-brand" to="/">Python Labs</RouterLink>
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/games">Ігри</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/tasks">Завдання</RouterLink>
        </li>
        <li v-if="active" class="nav-item">
          <RouterLink class="nav-link" to="/students">Студенти</RouterLink>
        </li>
        <li v-if="active" class="nav-item">
          <RouterLink class="nav-link" to="/refs">Знахідки</RouterLink>
        </li>
        <li v-if="active" class="nav-item">
          <RouterLink class="nav-link" to="/my/game">Моя гра</RouterLink>
        </li>
        <li v-if="active" class="nav-item">
          <RouterLink class="nav-link" to="/profile">Профіль</RouterLink>
        </li>
      </ul>
      <div class="d-flex align-items-center gap-2">
        <template v-if="user">
          <img v-if="user.picture" :src="user.picture" class="rounded-circle" width="32" height="32" :alt="user.name">
          <span>{{ user.name || user.email }}</span>
          <a class="btn btn-outline-secondary btn-sm" href="/api/auth/logout">Вийти</a>
        </template>
        <template v-else>
          <a v-if="isDev" class="btn btn-outline-secondary btn-sm" href="/api/auth/dev-login">Dev-вхід</a>
          <a class="btn btn-primary btn-sm" href="/api/auth/login">Увійти з Google</a>
        </template>
      </div>
    </div>
  </nav>
</template>
