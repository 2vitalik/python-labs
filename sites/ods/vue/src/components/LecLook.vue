<script setup>
import Icon from '@core/components/Icon.vue'

import { author, toggleLook } from '../lecLook.js'

// the switch of a lecture's look (lecLook.js): the lecturer's colours or the calm one. Pressed — his colours are on; the word
// is the same either way (nothing moves), the hint says what a click will do
</script>

<template>
  <button class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1" :class="{ active: author }" :aria-pressed="author"
          :title="author ? 'Вимкнути кольори лектора — спокійний вигляд' : 'Увімкнути кольори лектора — як на його слайдах'"
          @click="toggleLook"><Icon name="brush" />Кольори лектора</button>
</template>
