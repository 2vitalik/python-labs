<script setup>
import { dark, toggleTheme } from '../theme.js'
</script>

<template>
  <!-- the icon shows where the click leads: a moon on the light page, a sun on the dark one -->
  <button type="button" class="btn btn-sm border-0 p-1 d-inline-flex text-body-secondary"
          :title="dark ? 'Світла тема' : 'Темна тема'" @click="toggleTheme">
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"
         stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <template v-if="dark">
        <circle cx="8" cy="8" r="3" />
        <path d="M8 1v1.5M8 13.5V15M1 8h1.5M13.5 8H15M3.05 3.05l1.06 1.06M11.89 11.89l1.06 1.06M3.05 12.95l1.06-1.06M11.89 4.11l1.06-1.06" />
      </template>
      <path v-else d="M14 8.53A6 6 0 1 1 7.47 2 4.67 4.67 0 0 0 14 8.53z" />
    </svg>
  </button>
</template>

<style scoped>
button:hover { color: var(--bs-body-color) !important; }
</style>
