<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { SECTIONS } from '../guide.js'
import { useNavFit } from '../navFit.js'
import { canAccess, user } from '../user.js'
import IconHome from './IconHome.vue'
import NavUser from './NavUser.vue'

const route = useRoute()
const router = useRouter()
const links = [
  ...SECTIONS.map((s) => [s.path, s.nav]),
  ['/students', 'Студи'], ['/my/game', 'Моя гра'], ['/my/profile', 'Профіль'],
]
// menu follows route access, so a page and its link open together
const visible = computed(() => links.filter(([to]) => canAccess(router.resolve(to).meta.access)))
const { bar, list, more, fit, stage, layout } = useNavFit(visible)
const row = computed(() => visible.value.slice(0, fit.value))
const rest = computed(() => visible.value.slice(fit.value))
const isActive = (to) => route.path === to || route.path.startsWith(to + '/')  // /labs/1 lights «Лаби»
const restActive = computed(() => rest.value.some(([to]) => isActive(to)))

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
      <RouterLink class="navbar-brand d-flex align-items-center" to="/" title="Python Labs"><IconHome :size="20" /></RouterLink>
      <ul ref="list" class="navbar-nav">
        <li v-for="[to, text] in row" :key="to" class="nav-item">
          <RouterLink class="nav-link" :class="{ active: isActive(to) }" :to="to">{{ text }}</RouterLink>
        </li>
        <li ref="more" class="nav-item dropdown" :class="{ 'invisible position-absolute': !rest.length }">
          <a class="nav-link dropdown-toggle" :class="{ active: restActive }" href="#" @click.prevent="open = !open">Ще</a>
          <ul class="dropdown-menu dropdown-menu-end" :class="{ show: open }">
            <li v-for="[to, text] in rest" :key="to">
              <RouterLink class="dropdown-item" :class="{ active: isActive(to) }" :to="to">{{ text }}</RouterLink>
            </li>
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
.nav-link { padding-left: .45rem; padding-right: .45rem; position: relative; }
/* current page: a bar under the word (::before — ::after is the «Ще» caret); colour and weight stay, so navFit's widths hold */
.nav-link.active::before { content: ''; position: absolute; left: .45rem; right: .45rem; bottom: .2rem; height: 2px;
                          border-radius: 1px; background: var(--bs-primary); }
</style>
