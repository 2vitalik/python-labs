<script setup>
import IconHome from './IconHome.vue'

// the way to the page: 🏠 › parents as [to, text] › the page itself as a plain string (its full title is the h1 below)
defineProps({ items: { type: Array, default: () => [] } })
</script>

<template>
  <nav aria-label="Шлях">
    <ol class="breadcrumb small mb-2">
      <li class="breadcrumb-item"><RouterLink to="/" title="Головна"><IconHome :size="14" /></RouterLink></li>
      <li v-for="(item, i) in items" :key="i" class="breadcrumb-item" :class="{ active: !Array.isArray(item) }">
        <RouterLink v-if="Array.isArray(item)" :to="item[0]">{{ item[1] }}</RouterLink>
        <template v-else>{{ item }}</template>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
.breadcrumb { --bs-breadcrumb-divider: '›'; }
.breadcrumb a { color: var(--bs-secondary-color); text-decoration: none; }
.breadcrumb a:hover { color: var(--bs-body-color); }
.breadcrumb svg { vertical-align: -.125em; }
</style>
