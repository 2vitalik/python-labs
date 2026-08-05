<script setup>
import { useRoute } from 'vue-router'

import NavBar from './components/NavBar.vue'
import { loadUser } from './user.js'

const route = useRoute()
loadUser()
</script>

<template>
  <NavBar />
  <main class="py-4" :class="route.meta.wide ? 'container-fluid px-4' : 'container'">
    <RouterView />
  </main>
</template>
