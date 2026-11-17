<script setup>
import { computed, onMounted, ref } from 'vue'

import Crumbs from '@core/components/Crumbs.vue'
import Icon from '@core/components/Icon.vue'
import { getDefenses } from '../api.js'
import DefenseRow from '../components/DefenseRow.vue'
import DefenseStart from '../components/DefenseStart.vue'
import { isToday, loadVocab, vocab } from '../defense.js'
import '../defense.css'

// the teacher's defenses (T327 §5): the ones going on first, then today's, then the rest, the newest above; a new one
// starts here
const list = ref(null)
const starting = ref(false)
const error = ref('')
const groups = computed(() => [
  ['Тривають', list.value.filter((d) => !d.ended_at)],
  ['Сьогодні', list.value.filter((d) => d.ended_at && isToday(d.started_at))],
  ['Раніше', list.value.filter((d) => d.ended_at && !isToday(d.started_at))],
].filter(([, rows]) => rows.length))
const waiting = computed(() => list.value.reduce((n, d) => n + d.counts.answered, 0))

onMounted(async () => {
  try {
    await loadVocab()
    list.value = await getDefenses()
  } catch (e) {
    error.value = e.message
  }
})
</script>

<template>
  <div>
    <Crumbs :items="['Захисти']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
      <h1 class="h3 mb-0 me-auto">Захисти</h1>
      <span v-if="list && waiting" class="dhint"><Icon name="clock" /> відповідей чекають перевірки: {{ waiting }}</span>
      <button v-if="!starting" type="button" class="btn btn-sm btn-add" :disabled="!vocab" @click="starting = true"><Icon name="plus" /> Почати захист</button>
    </div>
    <DefenseStart v-if="starting" @cancel="starting = false" />
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <template v-if="list">
      <template v-for="[title, rows] in groups" :key="title">
        <div class="dsub">{{ title }}</div>
        <DefenseRow v-for="d in rows" :key="d.id" :d />
      </template>
      <p v-if="!list.length" class="text-secondary text-center mt-4">Захистів ще не було — почни перший кнопкою вгорі.</p>
    </template>
  </div>
</template>
