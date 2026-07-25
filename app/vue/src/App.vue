<script setup>
import NavBar from './components/NavBar.vue'
import { loadUser } from './user.js'

loadUser()
</script>

<template>
  <NavBar />
  <main class="container py-4">
    <RouterView />
  </main>
</template>
