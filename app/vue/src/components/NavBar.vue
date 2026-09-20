<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { SECTIONS } from '../guide.js'
import { useNavFit } from '../navFit.js'
import { canAccess, user } from '../user.js'
import NavUser from './NavUser.vue'

const route = useRoute()
const router = useRouter()
const links = [
  ...SECTIONS.map((s) => [s.path, s.nav]),
  ['/students', 'Студи'], ['/my/game', 'Моя гра'], ['/profile', 'Профіль'],
]
// menu follows route access, so a page and its link open together
const visible = computed(() => links.filter(([to]) => canAccess(router.resolve(to).meta.access)))
const { bar, list, more, fit, stage, layout } = useNavFit(visible)
const row = computed(() => visible.value.slice(0, fit.value))
const rest = computed(() => visible.value.slice(fit.value))
const restActive = computed(() => rest.value.some(([to]) => route.path.startsWith(to)))

const open = ref(false)
const close = (e) => (!e || !more.value?.contains(e.target)) && (open.value = false)
watch(() => route.fullPath, () => close())
watch(user, () => layout(), { flush: 'post' })  // the name appears/changes → re-fit
onMounted(() => document.addEventListener('click', close))
onUnmounted(() => document.removeEventListener('click', close))
</script>

<template>
  <nav ref="bar" class="navbar navbar-expand bg-body-tertiary border-bottom">
    <div class="page d-flex align-items-center">
      <RouterLink class="navbar-brand d-flex align-items-center" to="/" title="Python Labs">
        <template v-if="stage < 2">Python Labs</template>
        <svg v-else width="20" height="20" viewBox="0 0 16 16" fill="currentColor" aria-label="Python Labs">
          <path d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5"/>
        </svg>
      </RouterLink>
      <ul ref="list" class="navbar-nav">
        <li v-for="[to, text] in row" :key="to" class="nav-item">
          <RouterLink class="nav-link" :to="to">{{ text }}</RouterLink>
        </li>
        <li ref="more" class="nav-item dropdown" :class="{ 'invisible position-absolute': !rest.length }">
          <a class="nav-link dropdown-toggle" :class="{ active: restActive }" href="#" @click.prevent="open = !open">Ще</a>
          <ul class="dropdown-menu dropdown-menu-end" :class="{ show: open }">
            <li v-for="[to, text] in rest" :key="to"><RouterLink class="dropdown-item" :to="to">{{ text }}</RouterLink></li>
          </ul>
        </li>
      </ul>
      <NavUser :stage />
    </div>
  </nav>
</template>

<style scoped>
.navbar-brand { margin-right: .5rem; }
/* the row takes the free width; links never shrink or wrap — the fit is computed in navFit.js */
.navbar-nav { flex: 1 1 0; min-width: 0; }
.nav-item { flex-shrink: 0; white-space: nowrap; }
.nav-link { padding-left: .45rem; padding-right: .45rem; }
</style>
