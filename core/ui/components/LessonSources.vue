<script setup>
import { computed, onMounted, ref } from 'vue'

import { deleteLessonFile, getStudents, postLessonAlias, uploadLessonFile } from '../api.js'
import { fmtSize, fmtWords } from '../lesson.js'
import Avatar from './Avatar.vue'

// the admin's card: raw transcripts and attachments (upload · drop), who the speakers are (an unknown name → a student,
// remembered as their alias), and the local way to the texts — bin/lesson and the /lesson skill
const props = defineProps({ lesson: Object })
const emit = defineEmits(['changed'])
const students = ref([])
const error = ref('')
const busy = ref('')
const sources = computed(() => props.lesson.files.filter((f) => f.role === 'source'))
const attachments = computed(() => props.lesson.files.filter((f) => f.role === 'file'))
const unknown = computed(() => props.lesson.speakers.filter((w) => !props.lesson.people[w]))
const known = computed(() => props.lesson.speakers.filter((w) => props.lesson.people[w]))
const when = (iso) => new Date(iso).toLocaleDateString('uk-UA', { day: 'numeric', month: 'short' })

async function run(what, job) {
  busy.value = what
  error.value = ''
  try {
    await job()
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
  busy.value = ''
}
const add = (e, role) => Promise.all([...e.target.files].map((f) => run(f.name, () => uploadLessonFile(props.lesson.slug, f, role)))).then(() => (e.target.value = ''))
const drop = (f) => confirm(`Прибрати ${f.name}?`) && run(f.id, () => deleteLessonFile(props.lesson.slug, f.id))
const assign = (name, nick) => nick && run(name, () => postLessonAlias(props.lesson.slug, { name, nick }))
onMounted(async () => (students.value = (await getStudents()).filter((s) => s.status !== 'pending')))
</script>

<template>
  <div class="card mt-4">
    <div class="card-header d-flex align-items-center gap-2">
      <span>🧑‍🏫 Джерела й мовці</span><span class="text-secondary small">лише викладачу</span>
      <span v-if="busy" class="ms-auto small text-secondary">{{ busy }}…</span>
    </div>
    <div class="card-body small">
      <div v-if="error" class="alert alert-danger py-1">{{ error }}</div>
      <div class="row g-4">
        <div class="col-md-6">
          <div class="fw-semibold mb-1">Сирі транскрипти</div>
          <ul class="list-unstyled mb-2">
            <li v-for="f in sources" :key="f.id" class="d-flex gap-2 align-items-baseline">
              <a :href="`/api/lessons/${lesson.slug}/files/${f.id}`" target="_blank" class="font-monospace">{{ f.name }}</a>
              <span class="text-body-tertiary">{{ fmtWords(f.words) }} · {{ f.by }} · {{ when(f.uploaded) }}</span>
              <a href="#" class="ms-auto text-body-tertiary text-decoration-none" title="Прибрати" @click.prevent="drop(f)">✕</a>
            </li>
            <li v-if="!sources.length" class="text-body-tertiary">ще нема — zoom.txt, plaud.txt, whisper.txt, chat.txt…</li>
          </ul>
          <label class="btn btn-outline-secondary btn-sm">＋ сирий транскрипт<input type="file" multiple hidden @change="add($event, 'source')"></label>
          <div class="fw-semibold mt-3 mb-1">Файли для студентів</div>
          <ul class="list-unstyled mb-2">
            <li v-for="f in attachments" :key="f.id" class="d-flex gap-2 align-items-baseline">
              <a :href="`/api/lessons/${lesson.slug}/files/${f.id}`" target="_blank">📎 {{ f.name }}</a>
              <span class="text-body-tertiary">{{ fmtSize(f.size) }}</span>
              <a href="#" class="ms-auto text-body-tertiary text-decoration-none" title="Прибрати" @click.prevent="drop(f)">✕</a>
            </li>
          </ul>
          <label class="btn btn-outline-secondary btn-sm">＋ файл<input type="file" multiple hidden @change="add($event, 'file')"></label>
        </div>
        <div class="col-md-6">
          <div class="fw-semibold mb-1">Мовці</div>
          <p v-if="!lesson.speakers.length" class="text-body-tertiary">зʼявляться з транскриптом</p>
          <div v-for="w in unknown" :key="w" class="who mb-1">
            <span><span class="badge text-bg-warning fw-normal me-2">?</span>{{ w }}</span>
            <select class="form-select form-select-sm" @change="assign(w, $event.target.value)">
              <option value="">хто це?</option>
              <option v-for="s in students" :key="s.nick" :value="s.nick">{{ s.name }} {{ s.group }}</option>
            </select>
          </div>
          <div v-for="w in known" :key="w" class="d-flex align-items-center gap-2 mb-1">
            <Avatar :user="lesson.people[w]" :size="22" /><span>{{ w }}</span>
            <RouterLink :to="`/students/${lesson.people[w].nick}/edit`" class="text-body-tertiary">{{ lesson.people[w].name }} {{ lesson.people[w].group }}</RouterLink>
          </div>
          <div class="fw-semibold mt-3 mb-1">Обробка — локально, через Claude Code</div>
          <pre class="mb-0 text-body-secondary">bin/lesson pull {{ lesson.slug }}
/lesson merge data/transcripts/{{ lesson.slug }}
/lesson summary data/transcripts/{{ lesson.slug }}
bin/lesson push {{ lesson.slug }} -m "…"
bin/zoom pull {{ lesson.slug }} [--meeting ID] [--sources]</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.who { display: grid; grid-template-columns: 1fr auto; gap: .5rem; align-items: center; }
</style>
