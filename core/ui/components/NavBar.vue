<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { icons, useNavFit } from '../navFit.js'
import { site } from '../site.js'
import { canAccess, user } from '../user.js'
import Icon from './Icon.vue'
import IconHome from './IconHome.vue'
import NavUser from './NavUser.vue'

const route = useRoute()
const router = useRouter()
// menu follows route access, so a page and its link open together; a link with its own access is narrower than its page
const visible = computed(() => site.links.filter(([to, , access]) => canAccess(access ?? router.resolve(to).meta.access)))
const { bar, list, more, tail, fit, stage, compact, bare, layout, setIcons } = useNavFit(visible)
const row = computed(() => visible.value.slice(0, fit.value))
const rest = computed(() => visible.value.slice(fit.value))
const isActive = (to) => route.path === to || route.path.startsWith(to + '/')  // /labs/1 lights «Лаби»
const restActive = computed(() => rest.value.some(([to]) => isActive(to)))

// «Ще» opens under a mouse that stopped on it (T291 §9): a pause, so a mouse passing by opens nothing, and a longer one
// before it goes — the way from the word to the list. A finger has no hover: there a tap opens and closes it
const open = ref(false)
const hovers = matchMedia('(hover: hover)').matches
let timer
const hover = (on) => {
  if (!hovers) return
  clearTimeout(timer)
  timer = setTimeout(() => (open.value = on), on ? 200 : 300)
}
const tap = () => { clearTimeout(timer); open.value = hovers || !open.value }
const close = (e) => (!e || !more.value?.contains(e.target)) && (open.value = false)
watch(() => route.fullPath, () => close())
watch(user, () => layout(), { flush: 'post' })  // the name appears/changes → re-fit

// always in sight (T284 §3): the bar sticks to the top and, once the page is scrolled, gets lower; whatever sticks under
// it reads its height as --nav-h. Two thresholds, so the bar does not flicker where it changes
const small = ref(false)
const scrolled = () => (small.value = scrollY > (small.value ? 40 : 120))
const sized = new ResizeObserver(() => document.documentElement.style.setProperty('--nav-h', `${bar.value.offsetHeight}px`))
onMounted(() => {
  document.addEventListener('click', close)
  addEventListener('scroll', scrolled, { passive: true })
  sized.observe(bar.value, { box: 'border-box' })  // the bar's own padding is animated: the content box alone would miss it
})
onUnmounted(() => {
  document.removeEventListener('click', close)
  removeEventListener('scroll', scrolled)
  sized.disconnect()
  clearTimeout(timer)
})
</script>

<template>
  <nav ref="bar" class="navbar navbar-expand bg-body-tertiary border-bottom sticky-top" :class="{ small }">
    <div class="page d-flex align-items-center">
      <RouterLink class="navbar-brand d-flex align-items-center" to="/" :title="site.name"><IconHome :size="20" /></RouterLink>
      <ul ref="list" class="navbar-nav">
        <!-- tight and the reader chose icons (navFit.js): a link is its icon, named under the mouse; the page we are on keeps its
             word while it fits (`bare` — not even that) -->
        <li v-for="[to, text, , bold, icon] in row" :key="to" class="nav-item">
          <RouterLink class="nav-link" :class="{ active: isActive(to), main: bold, ico: compact }" :to="to"
                      :data-tip="compact && (!isActive(to) || bare) ? text : null" :aria-label="text">
            <template v-if="compact">
              <span class="pic"><Icon v-if="icon" :name="icon" /><template v-else>{{ text.slice(0, 2) }}</template></span>
              <span v-if="isActive(to) && !bare" class="word">{{ text }}</span>
            </template>
            <template v-else>{{ text }}</template>
          </RouterLink>
        </li>
        <li ref="more" class="nav-item dropdown" :class="{ 'invisible position-absolute': !rest.length }" @mouseenter="hover(true)" @mouseleave="hover(false)">
          <a class="nav-link dropdown-toggle" :class="{ active: restActive }" href="#" :aria-expanded="open" @click.prevent="tap">Ще</a>
          <!-- the list reads as the bar going on downwards: its ground, its type, its colours; a bar of icons lends them its icons -->
          <ul class="dropdown-menu dropdown-menu-end" :class="{ show: open }">
            <li v-for="[to, text, , bold, icon] in rest" :key="to">
              <RouterLink class="dropdown-item" :class="{ active: isActive(to), main: bold }" :to="to"><Icon v-if="compact && icon" :name="icon" class="ipic" />{{ text }}</RouterLink>
            </li>
            <li><hr class="dropdown-divider"></li>
            <li>
              <button type="button" class="dropdown-item look" :title="icons ? 'Меню словами: що не вміщається — у «Ще»' : 'Меню значками: вміщається все, назва — під мишкою'"
                      @click="setIcons(!icons); open = false">
                <template v-if="icons">Аа словами</template><template v-else><Icon name="grid" /> значками</template>
              </button>
            </li>
          </ul>
        </li>
        <li v-if="compact && !rest.length" ref="tail" class="nav-item">
          <button type="button" class="nav-link look" data-tip="Меню словами: що не вміщається — у «Ще»" @click="setIcons(false)">Аа</button>
        </li>
      </ul>
      <NavUser :stage />
    </div>
  </nav>
</template>

<style scoped>
/* scrolled: the same row with less air; the type stays, so navFit's widths hold */
.navbar { transition: padding .15s; }
.navbar.small { --bs-navbar-padding-y: 0; }
.small .nav-link, .small .navbar-brand { padding-top: .3rem; padding-bottom: .3rem; }
.navbar-brand { margin-right: .5rem; }
/* the row takes the free width; links never shrink or wrap — the fit is computed in navFit.js */
.navbar-nav { flex: 1 1 0; min-width: 0; }
.nav-item { flex-shrink: 0; white-space: nowrap; }
.nav-link { padding-left: .45rem; padding-right: .45rem; position: relative; }
/* current page: a bar under the word (::before — ::after is the «Ще» caret); colour and weight stay, so navFit's widths hold */
.nav-link.active::before { content: ''; position: absolute; left: .45rem; right: .45rem; bottom: .2rem; height: 2px;
                          border-radius: 1px; background: var(--bs-primary); }
/* the site's main page (T291 §9): bold, and at rest a shade darker than its neighbours — not black */
.main { font-weight: 700; }
.nav-link.main:not(.active):not(:hover) { color: rgba(var(--bs-emphasis-color-rgb), .8); }
/* an icon as tall as a word, so the bar keeps its height, drawn as large as «Додому» in finer lines, with air between
   (T294 §13); its name comes under the mouse at once, not after the browser's second */
.pic { display: inline-block; font-size: 1.3rem; line-height: 1.5rem; vertical-align: top; }
.pic .icon { stroke-width: 1.15; vertical-align: -.2em; }
/* the main page is bold in words; in icons it is a larger drawing in bolder lines (T296 §1) — it stands out the same way */
.main .pic { font-size: 1.6rem; }
.main .pic .icon { stroke-width: 1.55; }
.nav-link.ico { padding-left: .5rem; padding-right: .5rem; }
.nav-link.ico.active::before { left: .5rem; right: .5rem; }
/* the current page's word beside its icon: lighter than the bar's words, so it reads as a caption (T294 §14) */
.word { margin-left: .3rem; font-size: .85rem; font-weight: 400; }
.nav-link[data-tip]:hover::after { content: attr(data-tip); position: absolute; z-index: 5; top: calc(100% + .15rem); left: 50%; transform: translateX(-50%);
                                   padding: .1rem .45rem; border-radius: .3rem; background: var(--bs-emphasis-color); color: var(--bs-body-bg);
                                   font-size: .75rem; font-weight: 400; white-space: nowrap; pointer-events: none; }
/* «Ще»: the bar's own ground and link colours, rows as tight as the bar's words, no wider than its longest word */
.dropdown-menu { --bs-dropdown-bg: var(--bs-tertiary-bg); --bs-dropdown-min-width: 0; --bs-dropdown-padding-y: .25rem; --bs-dropdown-spacer: 0;
                 --bs-dropdown-item-padding-x: .8rem; --bs-dropdown-item-padding-y: .2rem; --bs-dropdown-divider-margin-y: .25rem;
                 --bs-dropdown-link-color: var(--bs-navbar-color); --bs-dropdown-link-hover-color: var(--bs-navbar-hover-color);
                 --bs-dropdown-link-hover-bg: rgba(var(--bs-emphasis-color-rgb), .06);
                 --bs-dropdown-link-active-color: var(--bs-navbar-active-color); --bs-dropdown-link-active-bg: transparent;
                 border-top-left-radius: 0; border-top-right-radius: 0; }
.dropdown-item { position: relative; display: flex; align-items: center; }
.ipic { margin-right: .5rem; font-size: 1.1rem; stroke-width: 1.15; }
.main .ipic { stroke-width: 1.55; }
/* scrolled, the bar has less air — so has its list (T294 §12) */
.small .dropdown-menu { --bs-dropdown-item-padding-y: .1rem; --bs-dropdown-font-size: .9rem; --bs-dropdown-padding-y: .15rem; }
.dropdown-item.active::before { content: ''; position: absolute; left: .3rem; top: .35rem; bottom: .35rem; width: 2px; border-radius: 1px; background: var(--bs-primary); }
.look { color: var(--bs-secondary-color); font-size: .8rem; }
.dropdown-item.look { display: flex; align-items: center; gap: .35rem; }
button.nav-link.look { border: 0; background: none; line-height: 1.5rem; }
</style>
