<script setup>
import { ref } from 'vue'

import Crumbs from '@core/components/Crumbs.vue'
import Tip from '@core/components/Tip.vue'
import { getAsks } from '../api.js'
import { loadCatalog } from '../catalog.js'
import AskCard from '../components/AskCard.vue'

// the teacher's «Запити» (T319): the cards «за запитом» students added to their games, the most asked first; under each —
// the requests with the students' sentences, and what the teacher does with them (AskCard, AskRow)
const items = ref(null)  // null — not loaded yet: «Запитів нема» is not said before the answer
const error = ref('')
async function load() {
  error.value = ''
  try {
    items.value = await getAsks()
  } catch (e) {
    error.value = e.message
  }
}
load()
loadCatalog()  // «Відкрити для всіх» saves the catalog's card; the move to another card picks from it
</script>

<template>
  <div>
    <Crumbs :items="[['/method', 'Методичка'], ['/tasks', 'Таски'], 'Запити']" />
    <div data-dock class="mb-3">
      <h1 class="h2 mb-2 d-flex align-items-center gap-2">Запити<span v-if="items" class="count fs-5">{{ items.length }}</span><span class="tip-dock" /></h1>
      <Tip id="asks-page">Картки за запитом, які студенти додали в ігри, — найчастіші зверху; під карткою — їхні пояснення.
        «Відкрити для всіх» кладе картку в основу: усі запити на неї стають звичайними заявками. На окремий запит можна відповісти рядком,
        повернути його, зарахувати лише цьому студентові або перенести на іншу картку</Tip>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <AskCard v-for="a in items" :key="a.task.slug" :ask="a" class="mb-3" @changed="load" />
    <p v-if="items && !items.length" class="text-secondary text-center mt-4">Запитів нема</p>
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; }
</style>
