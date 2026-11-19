<script setup>
import IconArrows from '@core/components/IconArrows.vue'
import { toggleWide, wide } from '@core/wide.js'

// a meta.wide page: on the whole window or in the page column — the reader's choice, as on the other wide pages
</script>

<template>
  <button type="button" class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center px-2"
          :title="wide ? 'Назад у колонку сторінки' : 'На всю ширину'" @click="toggleWide"><IconArrows :out="!wide" /></button>
</template>
