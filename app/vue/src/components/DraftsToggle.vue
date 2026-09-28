<script setup>
import { shown, toggleDrafts } from '../drafts.js'
</script>

<template>
  <a href="#" title="Чернетки — те, чого студенти не бачать: показати їх чи сховати" @click.prevent="toggleDrafts">
    {{ shown ? '👁 з чернетками' : '🙈 як у студентів' }}
  </a>
</template>
