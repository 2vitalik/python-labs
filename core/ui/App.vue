<script setup>
import { computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash } from './anchors.js'
import { postView } from './api.js'
import DownBar from './components/DownBar.vue'
import NavBar from './components/NavBar.vue'
import Oops from './components/Oops.vue'
import ViewBar from './components/ViewBar.vue'
import { down } from './http.js'
import NotFoundPage from './pages/NotFoundPage.vue'
import { problem } from './problem.js'
import { watchTitle } from './title.js'
import { user } from './user.js'
import { wideOn } from './wide.js'

const route = useRoute()
watchTitle(route)
useRouter().afterEach((to, from) => {
  if (to.path !== from.path) problem.value = ''  // a new page starts clean; filters in the query leave it where it is
  // footprint for the activity map: every page a signed-in user opens (after the guards, so `user` is known)
  if (user.value) postView(to.fullPath).catch(() => {})
})
const wide = computed(() => route.meta.wide && wideOn.value)  // a meta.wide page on the whole window: the admin's remembered choice
watch(() => route.hash, (h) => h && flash(h.slice(1)))  // #target changed on a loaded page; page load is GuideText's job
</script>

<template>
  <NavBar />
  <ViewBar v-if="user?.viewing" />
  <main class="py-4" :class="wide ? 'container-fluid px-4' : 'page'">
    <DownBar v-if="down" />
    <!-- the API is silent and nobody is signed in: whether the page is theirs to see is unknown -->
    <template v-if="user || !down">
      <NotFoundPage v-if="problem === 'lost'" />
      <template v-else>
        <Oops v-if="problem" />
        <RouterView />
      </template>
    </template>
  </main>
</template>
