<script setup>
import { problem } from '../problem.js'

// an error nobody caught (problem.js): sticks to the top, so it is seen wherever the page was scrolled to
const reload = () => location.reload()
const hide = () => (problem.value = '')
</script>

<template>
  <div class="oops alert alert-danger d-flex flex-wrap align-items-center gap-2 mb-4">
    <div class="me-auto">
      <b>😵 Щось пішло не так</b>
      <div class="small">Викладач уже отримав звіт про помилку. Спробуй оновити сторінку.</div>
    </div>
    <button class="btn btn-outline-danger btn-sm" @click="reload">Оновити</button>
    <button class="btn-close" title="Сховати" @click="hide"></button>
  </div>
</template>

<style scoped>
.oops { position: sticky; top: .5rem; z-index: 5; }
</style>
