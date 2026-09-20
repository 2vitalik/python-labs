<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import { user } from '../user.js'
import Avatar from './Avatar.vue'

// right side of the menu: avatar · name · «Вийти», or the sign-in buttons; `stage` comes from useNavFit
defineProps({ stage: Number })
const isDev = import.meta.env.DEV
const route = useRoute()
// sign-in buttons bring the user back to the page they were on
const next = computed(() => `?next=${encodeURIComponent(route.fullPath)}`)
</script>

<template>
  <div class="d-flex align-items-center gap-2 ms-2 flex-shrink-0 text-nowrap">
    <template v-if="user">
      <Avatar :user />
      <span v-if="stage < 1">{{ user.name || user.email }}</span>
      <a class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center" href="/api/auth/logout" title="Вийти">
        <template v-if="stage < 2">Вийти</template>
        <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-label="Вийти">
          <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z"/>
          <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z"/>
        </svg>
      </a>
    </template>
    <template v-else>
      <a v-if="isDev && stage < 2" class="btn btn-outline-secondary btn-sm" :href="'/api/auth/dev-login' + next">Dev-вхід</a>
      <a class="btn btn-primary btn-sm" :href="'/api/auth/login' + next">{{ stage < 2 ? 'Увійти з Google' : 'Увійти' }}</a>
    </template>
  </div>
</template>
