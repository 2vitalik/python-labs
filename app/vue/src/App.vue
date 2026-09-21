<script setup>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'

import { flash } from './anchors.js'
import NavBar from './components/NavBar.vue'
import { user } from './user.js'

const route = useRoute()
const wide = computed(() => route.meta.wide && user.value?.status === 'admin')  // guests read guide text there
watch(() => route.hash, (h) => h && flash(h.slice(1)))  // #target changed on a loaded page; page load is GuideText's job
</script>

<template>
  <NavBar />
  <main class="py-4" :class="wide ? 'container-fluid px-4' : 'page'">
    <RouterView />
  </main>
</template>
