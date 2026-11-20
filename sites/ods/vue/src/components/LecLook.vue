<script setup>
import { author, toggleLook } from '../lecLook.js'

// the switch of a lecture's look (lecLook.js): the lecturer's colours or the calm one
</script>

<template>
  <button class="btn btn-sm btn-outline-secondary" :class="{ active: author }" :aria-pressed="author"
          :title="author ? 'Кольори лектора — увімкнено' : 'Кольори лектора — вимкнено'" @click="toggleLook">Кольори</button>
</template>
