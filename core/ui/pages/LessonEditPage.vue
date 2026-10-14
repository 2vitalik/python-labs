<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { deleteLesson, getLesson, getStudents, postLesson, putLesson } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import TagInput from '../components/TagInput.vue'
import { KINDS } from '../lesson.js'
import { problem } from '../problem.js'
import { useTitle } from '../title.js'
import { user } from '../user.js'

// a new meeting or the meta of one (kind and number are fixed at birth: they are its address); the texts have their own editors
const route = useRoute()
const router = useRouter()
const slug = computed(() => route.params.slug || '')
const form = reactive({ kind: 'pz', n: '', date: '', time: '', title: '', groups: [], links: [], video_start: '', meeting: '', context: '', published: false })
const rev = ref(0)
const label = ref('')
const groups = ref([])
const error = ref('')
const busy = ref(false)
useTitle(() => (slug.value ? `${label.value}: редагування` : 'Нове заняття'))
const addLink = () => form.links.push({ label: '', url: '' })

onMounted(async () => {
  groups.value = [...new Set((await getStudents()).map((s) => s.group).filter(Boolean))].sort()
  if (!slug.value) return addLink()
  try {
    const l = await getLesson(slug.value)
    Object.assign(form, { kind: l.kind, n: l.n, date: l.date, time: l.time, title: l.title, groups: l.groups, links: l.links.map((x) => ({ ...x })),
                          video_start: l.video_start, meeting: l.meeting, context: l.context, published: l.published })
    rev.value = l.rev
    label.value = l.label
    if (!form.links.length) addLink()
  } catch (e) {
    problem.value = e.status === 404 ? 'lost' : e.message
  }
})

async function save() {
  busy.value = true
  error.value = ''
  const data = { ...form, n: form.n ? Number(form.n) : null, links: form.links.filter((l) => l.url.trim()) }
  try {
    const l = slug.value ? await putLesson(slug.value, { ...data, rev: rev.value }) : await postLesson(data)
    router.push(`/lessons/${l.slug}`)
  } catch (e) {
    error.value = e.message
  }
  busy.value = false
}
async function remove() {
  if (!confirm(`Видалити ${label.value} разом із файлами й текстами? Історія правок лишається.`)) return
  await deleteLesson(slug.value)
  router.push('/lessons')
}
</script>

<template>
  <div v-if="user?.status === 'admin'">
    <Crumbs :items="[['/lessons', 'Заняття'], ...(slug ? [[`/lessons/${slug}`, label], 'Редагування'] : ['Нове'])]" />
    <h1 class="h3 mb-3">{{ slug ? `${label}: редагування` : 'Нове заняття' }}</h1>
    <form @submit.prevent="save">
      <div class="row g-3">
        <div class="col-6 col-md-3">
          <label class="form-label">Вид</label>
          <select v-model="form.kind" class="form-select" :disabled="!!slug">
            <option v-for="(name, k) in KINDS" :key="k" :value="k">{{ name }}</option>
          </select>
        </div>
        <div class="col-6 col-md-2">
          <label class="form-label">Номер</label>
          <input v-model="form.n" class="form-control" type="number" min="1" :disabled="!!slug" placeholder="наступний">
        </div>
        <div class="col-6 col-md-3">
          <label class="form-label">Дата</label>
          <input v-model="form.date" class="form-control" type="date">
        </div>
        <div class="col-6 col-md-4">
          <label class="form-label">Час</label>
          <input v-model="form.time" class="form-control" placeholder="18:35–20:10">
        </div>
        <div class="col-12">
          <label class="form-label">Назва</label>
          <input v-model="form.title" class="form-control" placeholder="Знайомство з курсом">
        </div>
        <div class="col-12">
          <label class="form-label">Групи</label>
          <TagInput v-model="form.groups" :known="groups" :hash="false" />
        </div>
        <div class="col-12">
          <label class="form-label">Посилання <span class="text-body-tertiary fw-normal">— відео, тека в Google Drive, пост у Telegram; підпис можна лишити порожнім</span></label>
          <div v-for="(l, i) in form.links" :key="i" class="input-group mb-2">
            <input v-model="l.label" class="form-control" style="max-width: 11rem" placeholder="Відео">
            <input v-model="l.url" class="form-control" type="url" placeholder="https://">
            <button type="button" class="btn btn-outline-secondary" title="Прибрати" @click="form.links.splice(i, 1)">✕</button>
          </div>
          <button type="button" class="btn btn-outline-secondary btn-sm" @click="addLink">＋ посилання</button>
        </div>
        <div class="col-md-4">
          <label class="form-label">Старт запису</label>
          <input v-model="form.video_start" class="form-control" placeholder="18:34:50" pattern="\d{1,2}:\d{2}(:\d{2})?">
          <div class="form-text">Час за годинником, коли почалось відео: клік по часу репліки відкриє це місце (YouTube)</div>
        </div>
        <div class="col-md-8">
          <label class="form-label">Зустріч Zoom</label>
          <input v-model="form.meeting" class="form-control" placeholder="ID зустрічі з посилання (цифри) або UUID одного проведення">
          <div class="form-text">«Оновити із Zoom» на сторінці заняття забере, хто був і скільки; за датою заняття знайдеться потрібне проведення</div>
        </div>
        <div class="col-12">
          <label class="form-label">Контекст для конспекту</label>
          <textarea v-model="form.context" class="form-control" rows="3" placeholder="що підкреслити, що пропустити — для /lesson summary"></textarea>
        </div>
        <div class="col-12 form-check ms-2">
          <input id="published" v-model="form.published" class="form-check-input" type="checkbox">
          <label for="published" class="form-check-label">Показувати студентам</label>
        </div>
      </div>
      <div class="d-flex align-items-center gap-3 mt-4">
        <button class="btn btn-primary" :disabled="busy">Зберегти</button>
        <RouterLink :to="slug ? `/lessons/${slug}` : '/lessons'" class="btn btn-outline-secondary">Скасувати</RouterLink>
        <span v-if="error" class="text-danger small">{{ error }}</span>
        <button v-if="slug" type="button" class="btn btn-link text-danger ms-auto" @click="remove">Видалити</button>
      </div>
    </form>
  </div>
  <p v-else-if="user && user.status !== 'admin'" class="text-center mt-5">Сторінка доступна лише викладачу.</p>
</template>
