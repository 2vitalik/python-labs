<script setup>
import { computed, onMounted, ref } from 'vue'

import Crumbs from '@core/components/Crumbs.vue'
import Icon from '@core/components/Icon.vue'
import { getRefs } from '../api.js'
import { loadCatalog } from '../catalog.js'
import { useRefFilter } from '../refFilter.js'
import IdeaForm from '../components/IdeaForm.vue'
import RefCard from '../components/RefCard.vue'
import RefFilters from '../components/RefFilters.vue'

// one stream of finds, card ideas and words about cards and the site (T274 §4); an idea under a find (`parent`) sits
// indented below it when both are on screen
const refs = ref([])
const loaded = ref(false)
const error = ref('')
const writing = ref(false)
const ideaFor = ref('')  // the find whose «＋ ідея» form is open
const { f, set, clear, counts, shown } = useRefFilter(refs)

const rows = computed(() => {  // [record, ideas under it][]
  const ids = new Set(shown.value.map((r) => r.id))
  return shown.value.filter((r) => !ids.has(r.parent)).map((r) => [r, shown.value.filter((k) => k.parent === r.id).reverse()])
})

async function load() {
  error.value = ''
  try {
    refs.value = await getRefs()
    loaded.value = true
  } catch (e) {
    error.value = e.message
  }
}
const done = () => { writing.value = false; ideaFor.value = ''; load() }

onMounted(() => { loadCatalog(); load() })
</script>

<template>
  <div>
    <Crumbs :items="['Знахідки']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
      <h1 class="h3 mb-0 me-auto">Знахідки й ідеї</h1>
      <button v-if="!writing" type="button" class="btn btn-sm btn-add" @click="writing = true"><Icon name="plus" /> Записати</button>
    </div>
    <p class="text-secondary">Знахідки — посилання на круті ігри й відео, ідеї — чого бракує в каталозі, а ще думки про картки
      й про сам сайт; бачать усі, викладач відповідає.</p>

    <div v-if="writing" class="card mb-3"><div class="card-body"><IdeaForm @done="done" @cancel="writing = false" /></div></div>
    <RefFilters :f :counts @set="set" />
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div class="vstack gap-2">
      <template v-for="[r, kids] in rows" :key="r.id">
        <RefCard :r @changed="load" @idea="ideaFor = r.id" />
        <div v-if="ideaFor === r.id" class="card ms-4">
          <div class="card-body py-2"><IdeaForm kind="idea" :parent="r.id" compact @done="done" @cancel="ideaFor = ''" /></div>
        </div>
        <RefCard v-for="k in kids" :key="k.id" :r="k" class="ms-4" @changed="load" />
      </template>
    </div>
    <p v-if="loaded && !rows.length" class="text-secondary text-center mt-4">
      <template v-if="refs.length">Нічого не знайдено — <a href="#" @click.prevent="clear">зніми фільтри</a></template>
      <template v-else>Поки порожньо — запиши першу знахідку 🙂</template>
    </p>
  </div>
</template>
