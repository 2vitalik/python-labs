<script setup>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'

import { flash } from './anchors.js'
import NavBar from './components/NavBar.vue'
import { wideOn } from './wide.js'

const route = useRoute()
const wide = computed(() => route.meta.wide && wideOn.value)  // /tasks catalog on the whole window: the admin's remembered choice
watch(() => route.hash, (h) => h && flash(h.slice(1)))  // #target changed on a loaded page; page load is GuideText's job
</script>

<template>
  <NavBar />
  <main class="py-4" :class="wide ? 'container-fluid px-4' : 'page'">
    <RouterView />
  </main>
</template>
