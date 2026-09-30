<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import { deletePollTemplate, getPollTemplates, postPollTemplate, putPollTemplate } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import PollForm from '../components/PollForm.vue'
import { emptyForm, fromPoll, optionLabel, review, toPayload } from '../polls.js'

// polls asked again and again: «Опитати» opens a new poll filled from the template; editing a template never changes
// the polls made from it — each keeps its own copy
const templates = ref([])
const known = ref([])
const editing = ref('')  // a template's id, or 'new'
const form = reactive(emptyForm())
const busy = ref(false)
const error = ref('')
const ready = computed(() => review(form).ready)

async function load() {
  const data = await getPollTemplates()
  templates.value = data.templates
  known.value = data.tags
}
function edit(t) {
  Object.assign(form, t ? fromPoll(t) : emptyForm())
  editing.value = t ? t.id : 'new'
  error.value = ''
}
async function run(step) {
  busy.value = true
  error.value = ''
  try {
    await step()
    await load()
  } catch (e) {
    error.value = e.message
  }
  busy.value = false
}
const save = () => run(async () => {
  await (editing.value === 'new' ? postPollTemplate(toPayload(form)) : putPollTemplate(editing.value, toPayload(form)))
  editing.value = ''
})
const remove = (t) => confirm(`Видалити шаблон «${t.title}»? Опитування, зроблені з нього, лишаться як були.`) && run(() => deletePollTemplate(t.id))
onMounted(load)
</script>

<template>
  <div>
    <Crumbs :items="[['/polls', 'Опитування'], 'Шаблони']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
      <h1 class="h3 mb-0 me-auto">Шаблони</h1>
      <button v-if="editing !== 'new'" type="button" class="btn btn-primary btn-sm" @click="edit(null)">➕ Новий шаблон</button>
    </div>
    <p class="text-secondary small">Питання, які ставиш знову й знову: «🗳 Опитати» відкриває нове опитування, заповнене з шаблону, — лишається обрати, куди.
      Правка шаблону не змінює вже зроблених з нього опитувань.</p>
    <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>

    <template v-for="t in [...(editing === 'new' ? [{ id: 'new' }] : []), ...templates]" :key="t.id">
      <div v-if="editing === t.id" class="card card-body mb-2 border-primary">
        <PollForm v-model="form" :known template />
        <div class="d-flex gap-2 mt-3">
          <button type="button" class="btn btn-primary" :disabled="busy || !ready" @click="save">💾 Зберегти шаблон</button>
          <button type="button" class="btn btn-link text-secondary" @click="editing = ''">Скасувати</button>
        </div>
      </div>
      <div v-else class="card card-body py-2 px-3 mb-2">
        <div class="d-flex flex-wrap align-items-center gap-2">
          <span class="fw-semibold me-auto">{{ t.title }}</span>
          <RouterLink :to="`/polls/new?template=${t.id}`" class="btn btn-primary btn-sm">🗳 Опитати</RouterLink>
          <button type="button" class="btn btn-outline-secondary btn-sm" title="Редагувати" @click="edit(t)">✏️</button>
          <button type="button" class="btn btn-outline-danger btn-sm" title="Видалити" :disabled="busy" @click="remove(t)">🗑</button>
        </div>
        <div class="small text-break">{{ t.question }}</div>
        <div class="small text-secondary d-flex flex-wrap column-gap-2">
          <span>{{ t.options.map(optionLabel).join(' · ') }}</span>
          <span v-if="t.multiple">· кілька відповідей</span>
          <span v-for="tag in t.tags" :key="tag">#{{ tag }}</span>
        </div>
      </div>
    </template>
    <p v-if="!templates.length && editing !== 'new'" class="text-secondary text-center my-4">
      Шаблонів ще нема. Зроби перший — або збережи вдале опитування кнопкою «📋 У шаблони» на його сторінці.
    </p>
  </div>
</template>
