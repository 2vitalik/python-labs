<script setup>
import { useRoute } from 'vue-router'

import Crumbs from '../components/Crumbs.vue'

const route = useRoute()
</script>

<template>
  <div class="text-center mt-4">
    <Crumbs :items="['404']" class="text-start" />
    <div class="display-1 text-body-tertiary">404</div>
    <h1 class="h3 mb-3">Такої сторінки нема</h1>
    <p>За адресою <code>{{ route.path }}</code> нічого не знайшлось: помилка в посиланні або сторінку перенесли.</p>
    <RouterLink to="/" class="btn btn-outline-secondary">На головну</RouterLink>
  </div>
</template>
