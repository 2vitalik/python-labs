<script setup>
import { computed } from 'vue'

import { lookBack, user } from '../user.js'

// «Очима студента»: on every page while the admin looks at the site as a test student
const fio = computed(() => `${user.value.last_name} ${user.value.first_name}`.trim() || user.value.name || user.value.nick)
</script>

<template>
  <div class="bg-warning-subtle border-bottom small">
    <div class="page d-flex align-items-center gap-2 py-1">
      <span>👁 Ти дивишся сайт як <b>{{ fio }}</b></span>
      <span v-if="user.status === 'pending'" class="badge text-bg-warning fw-normal">очікує</span>
      <button class="btn btn-outline-secondary btn-sm ms-auto" @click="lookBack">Повернутись</button>
    </div>
  </div>
</template>
