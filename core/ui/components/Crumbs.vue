<script setup>
import { useRoute } from 'vue-router'

import { site } from '../site.js'
import Icon from './Icon.vue'
import IconHome from './IconHome.vue'

// the way to the page: 🏠 › parents as [to, text] › the page itself as a plain string (its full title is the h1 below);
// the slot sits at the right edge — what the page wants at hand (e.g. «Моя гра», the numbers of the labs). A crumb that is
// a page of the menu wears the menu's drawing (T296 §2): the reader meets the icons where the words are
defineProps({ items: { type: Array, default: () => [] } })
const route = useRoute()
const pic = (to) => site.links.find(([path]) => path === to)?.[4]
</script>

<template>
  <nav aria-label="Шлях" class="crumbs d-flex flex-wrap align-items-center justify-content-between gap-2">
    <ol class="breadcrumb small mb-0">
      <li class="breadcrumb-item"><RouterLink to="/" title="Головна"><IconHome :size="14" /></RouterLink></li>
      <li v-for="(item, i) in items" :key="i" class="breadcrumb-item" :class="{ active: !Array.isArray(item) }">
        <RouterLink v-if="Array.isArray(item)" :to="item[0]"><Icon v-if="pic(item[0])" :name="pic(item[0])" class="pic" />{{ item[1] }}</RouterLink>
        <template v-else><Icon v-if="i === items.length - 1 && pic(route.path)" :name="pic(route.path)" class="pic" />{{ item }}</template>
      </li>
    </ol>
    <slot />
  </nav>
</template>

<style scoped>
/* closer to the menu than the page's own top padding, with air before the h1 */
.crumbs { margin: -.6rem 0 1rem; }
.breadcrumb { --bs-breadcrumb-divider: '›'; }
.breadcrumb a { color: var(--bs-secondary-color); text-decoration: none; }
.breadcrumb a:hover { color: var(--bs-body-color); }
.breadcrumb svg { vertical-align: -.125em; }
.pic { margin-right: .25rem; font-size: 1.05em; stroke-width: 1.3; opacity: .85; }
</style>
