<script setup>
import { shown, toggleDrafts } from '../drafts.js'
</script>

<template>
  <a href="#" title="Чернетки — нотатки й неготове в коментарях: показати їх чи сховати" @click.prevent="toggleDrafts">
    {{ shown ? '👁 з чернетками' : '🙈 без чернеток' }}
  </a>
</template>
