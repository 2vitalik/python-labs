<script setup>
import IconHome from './IconHome.vue'

// the way to the page: 🏠 › parents as [to, text] › the page itself as a plain string (its full title is the h1 below);
// the slot sits at the right edge — a button the page wants at hand (e.g. «Моя гра»)
defineProps({ items: { type: Array, default: () => [] } })
</script>

<template>
  <nav aria-label="Шлях" class="crumbs d-flex align-items-center justify-content-between gap-2">
    <ol class="breadcrumb small mb-0">
      <li class="breadcrumb-item"><RouterLink to="/" title="Головна"><IconHome :size="14" /></RouterLink></li>
      <li v-for="(item, i) in items" :key="i" class="breadcrumb-item" :class="{ active: !Array.isArray(item) }">
        <RouterLink v-if="Array.isArray(item)" :to="item[0]">{{ item[1] }}</RouterLink>
        <template v-else>{{ item }}</template>
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
</style>
