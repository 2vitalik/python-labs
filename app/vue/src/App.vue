<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import NavBar from './components/NavBar.vue'
import { user } from './user.js'

const route = useRoute()
const wide = computed(() => route.meta.wide && user.value?.status === 'admin')  // guests read guide text there
</script>

<template>
  <NavBar />
  <main class="py-4" :class="wide ? 'container-fluid px-4' : 'page'">
    <RouterView />
  </main>
</template>
