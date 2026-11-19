<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import IconArrows from '@core/components/IconArrows.vue'
import { wideOf } from '@core/wide.js'

// a meta.wide page: on the whole window or in the page column — the reader's choice, kept in the memory the route names
const route = useRoute()
const w = computed(() => wideOf(route.meta.wide) || wideOf(true))
</script>

<template>
  <button type="button" class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center px-2"
          :title="w.on.value ? 'Назад у колонку сторінки' : 'На всю ширину'" @click="w.toggle()"><IconArrows :out="!w.on.value" /></button>
</template>
