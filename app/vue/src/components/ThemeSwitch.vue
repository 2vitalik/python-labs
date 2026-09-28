<script setup>
import { mode, toggleTheme } from '../theme.js'
import IconTheme from './IconTheme.vue'

const TITLES = { light: 'світла', dark: 'темна', auto: 'як на пристрої' }
</script>

<template>
  <button type="button" class="btn btn-sm border-0 p-1 d-inline-flex text-body-secondary"
          :title="`Тема: ${TITLES[mode]}`" @click="toggleTheme">
    <IconTheme :mode />
  </button>
</template>

<style scoped>
.btn:hover { color: var(--bs-body-color) !important; }
</style>
