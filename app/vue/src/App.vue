<script setup>
import { computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash } from './anchors.js'
import { postView } from './api.js'
import NavBar from './components/NavBar.vue'
import { user } from './user.js'
import { wideOn } from './wide.js'

const route = useRoute()
// footprint for the activity map: every page a signed-in user opens (after the guards, so `user` is known)
useRouter().afterEach((to) => user.value && postView(to.fullPath).catch(() => {}))
const wide = computed(() => route.meta.wide && wideOn.value)  // /tasks catalog on the whole window: the admin's remembered choice
watch(() => route.hash, (h) => h && flash(h.slice(1)))  // #target changed on a loaded page; page load is GuideText's job
</script>

<template>
  <NavBar />
  <main class="py-4" :class="wide ? 'container-fluid px-4' : 'page'">
    <RouterView />
  </main>
</template>
