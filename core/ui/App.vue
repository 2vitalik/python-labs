<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash } from './anchors.js'
import { postView } from './api.js'
import DownBar from './components/DownBar.vue'
import NavBar from './components/NavBar.vue'
import Oops from './components/Oops.vue'
import PageJump from './components/PageJump.vue'
import TocBar from './components/TocBar.vue'
import ViewBar from './components/ViewBar.vue'
import { down } from './http.js'
import NotFoundPage from './pages/NotFoundPage.vue'
import { problem } from './problem.js'
import { watchTitle } from './title.js'
import { user } from './user.js'
import { wideOf } from './wide.js'

const route = useRoute()
watchTitle(route)
useRouter().afterEach((to, from) => {
  if (to.path !== from.path) problem.value = ''  // a new page starts clean; filters in the query leave it where it is
  // footprint for the activity map: every page a signed-in user opens (after the guards, so `user` is known)
  if (user.value) postView(to.fullPath).catch(() => {})
})
// a meta.wide page on the whole window: the reader's remembered choice (wide.js); 'admin' — always, for the admin (/week, T186)
const wide = computed(() => (route.meta.wide === 'admin' ? user.value?.status === 'admin' : !!wideOf(route.meta.wide)?.on.value))
watch(() => route.hash, (h) => h && flash(h.slice(1)))  // #target changed on a loaded page; page load is GuideText's job
// the shelf at the top (T344): the menu and whatever is pinned under it stay in sight while the page scrolls, and what
// sticks below — a page's headings, TocBar — reads the shelf's height as --nav-h. A page pins a strip of its own with
// <Teleport defer to="#top-shelf">
const shelf = ref()
const sized = new ResizeObserver(() => document.documentElement.style.setProperty('--nav-h', `${shelf.value.offsetHeight}px`))
onMounted(() => sized.observe(shelf.value, { box: 'border-box' }))  // the menu's own padding is animated: the content box alone would miss it
onBeforeUnmount(() => sized.disconnect())
</script>

<template>
  <header ref="shelf" class="sticky-top">
    <NavBar />
    <ViewBar v-if="user?.viewing" />
    <div id="top-shelf" />
  </header>
  <TocBar :wide />
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
  <PageJump :wide />
</template>
