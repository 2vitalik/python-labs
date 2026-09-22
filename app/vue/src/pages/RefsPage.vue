<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import { deleteRef, getRefs, postRef } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import RefCard from '../components/RefCard.vue'

// one stream of finds (links) and ideas (no url); an idea may hang under a find (`parent`) and shows indented below it
const FILTERS = { all: 'усе', link: '🔗 лінки', idea: '💡 ідеї' }
const refs = ref([])
const denied = ref(false)
const error = ref('')
const filter = ref('all')
const form = reactive({ url: '', note: '' })
const ideaFor = ref('')  // find id the mini-form under a card belongs to
const ideaNote = ref('')
const canAdd = computed(() => form.url.trim() || form.note.trim())

const shown = computed(() => {  // [find, ideas under it][]; the ideas filter lists every idea flat
  const ids = new Set(refs.value.map((r) => r.id))
  if (filter.value === 'idea') return refs.value.filter((r) => r.kind === 'idea').map((r) => [r, []])
  const top = refs.value.filter((r) => !(r.parent && ids.has(r.parent)) && (filter.value === 'all' || r.kind === 'link'))
  return top.map((r) => [r, filter.value === 'all' ? refs.value.filter((k) => k.parent === r.id).reverse() : []])
})

async function load() {
  try {
    refs.value = await getRefs()
  } catch {
    denied.value = true
  }
}
async function run(fn) {
  error.value = ''
  try {
    await fn()
    await load()
  } catch (e) {
    error.value = e.message
  }
}
const add = () => run(async () => {
  await postRef(form)
  form.url = form.note = ''
})
const addIdea = () => run(async () => {
  await postRef({ note: ideaNote.value, parent: ideaFor.value })
  ideaFor.value = ideaNote.value = ''
})
const remove = (r) => run(() => deleteRef(r.id))

onMounted(load)
</script>

<template>
  <div>
    <Crumbs :items="['Знахідки']" />
    <p v-if="denied" class="text-center mt-5">Сторінка для учасників курсу — увійди з поштою @nure.ua.</p>
    <template v-else>
      <h1 class="h3 mb-1">Знахідки</h1>
      <p class="text-secondary">Побачив круту гру, механіку чи ідею — відео, стаття, сайт, сама гра — кинь лінк сюди, поки не загубився.
        Своя ідея без лінка — теж сюди. Розбір і розкладання по картках каталогу — потім.</p>

      <div class="card mb-3">
        <div class="card-body d-flex gap-2 flex-wrap">
          <input v-model="form.url" class="form-control w-auto flex-grow-1" placeholder="https://… (порожнє = ідея)">
          <input v-model="form.note" class="form-control w-auto flex-grow-1" placeholder="Що тут крутого? — або сама ідея">
          <button class="btn btn-primary" :disabled="!canAdd" @click="add">{{ form.url.trim() ? 'Кинути лінк' : 'Записати ідею' }}</button>
        </div>
      </div>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div class="d-flex gap-2 mb-3">
        <button v-for="(t, k) in FILTERS" :key="k" class="btn btn-sm" :class="filter === k ? 'btn-secondary' : 'btn-outline-secondary'"
                @click="filter = k">{{ t }}</button>
      </div>

      <div class="vstack gap-2">
        <template v-for="[r, kids] in shown" :key="r.id">
          <RefCard :r @changed="load" @remove="remove(r)" @idea="ideaFor = r.id" />
          <div v-if="ideaFor === r.id" class="ms-4 d-flex gap-2">
            <input v-model="ideaNote" class="form-control form-control-sm" placeholder="Ідея до цієї знахідки" @keyup.enter="addIdea">
            <button class="btn btn-primary btn-sm" :disabled="!ideaNote.trim()" @click="addIdea">Записати</button>
            <button class="btn btn-outline-secondary btn-sm" @click="ideaFor = ''">✕</button>
          </div>
          <RefCard v-for="k in kids" :key="k.id" :r="k" class="ms-4" @changed="load" @remove="remove(k)" />
        </template>
      </div>
      <p v-if="!shown.length" class="text-secondary text-center mt-4">Поки порожньо — кинь перший лінк 🙂</p>
    </template>
  </div>
</template>
