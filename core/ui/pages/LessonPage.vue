<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { flash } from '../anchors.js'
import { getLesson, putLesson } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import GuideBody from '../components/GuideBody.vue'
import GuideEditor from '../components/GuideEditor.vue'
import GuideText from '../components/GuideText.vue'
import IconChevron from '../components/IconChevron.vue'
import LessonChat from '../components/LessonChat.vue'
import LessonHead from '../components/LessonHead.vue'
import LessonSources from '../components/LessonSources.vue'
import LessonWho from '../components/LessonWho.vue'
import Toc from '../components/Toc.vue'
import Transcript from '../components/Transcript.vue'
import { parseTranscript, stats, summaryView, withInfo } from '../lesson.js'
import { problem } from '../problem.js'
import { useTitle } from '../title.js'
import { user } from '../user.js'

// one meeting: the summary in full, the transcript folded under it (a «Теми» time or a #t-… link unfolds it at that section),
// Zoom's chat, and for the admin — the merge notes, the sources card, inline editors of both texts, «показати студентам»
const route = useRoute()
const lesson = ref(null)
const open = ref(false)
const editing = ref(false)
const error = ref('')
const slug = computed(() => route.params.slug)
const admin = computed(() => user.value?.status === 'admin')
const heading = computed(() => lesson.value && [lesson.value.label, lesson.value.title].filter(Boolean).join(' · '))
useTitle(() => heading.value)
const sections = computed(() => parseTranscript(lesson.value?.transcript))
const sum = computed(() => stats(sections.value))
const toc = computed(() => (open.value ? sections.value.filter((s) => s.title).map((s) => ({ id: s.id, text: s.title, depth: 2 })) : []))
const video = computed(() => withInfo(lesson.value?.links || []).find((l) => l.at))
// the summary as a guide page for GuideBody: its editor saves the lesson's text and brings the lesson back
const summary = computed(() => lesson.value && { slug: slug.value, title: heading.value, body: lesson.value.summary, rev: lesson.value.rev })
const putText = (key) => async (s, data) => {
  lesson.value = await putLesson(s, { [key]: data.body, rev: data.rev, note: data.note })
  return summary.value
}
const transcriptPage = computed(() => summary.value && { ...summary.value, body: lesson.value.transcript })

async function load() {
  try {
    lesson.value = await getLesson(slug.value)
    await hash(route.hash)
  } catch (e) {
    problem.value = e.status === 404 ? 'lost' : e.message
  }
}
async function publish(yes) {
  error.value = ''
  try {
    lesson.value = await putLesson(slug.value, { published: yes, rev: lesson.value.rev })
  } catch (e) {
    error.value = e.message
  }
}
async function hash(h) {  // a link into the transcript: unfold, then light the section
  if (!h.startsWith('#t-')) return
  open.value = true
  await nextTick()
  flash(h.slice(1))
}
watch(slug, load, { immediate: true })
watch(() => route.hash, (h) => lesson.value && hash(h))  // a save replaces `lesson` without re-scrolling
</script>

<template>
  <div v-if="lesson">
    <Crumbs :items="[['/lessons', 'Пари'], lesson.label]">
      <RouterLink v-if="admin" :to="`/lessons/${slug}/edit`" class="btn btn-outline-secondary btn-sm ms-auto">✏️ Пара</RouterLink>
    </Crumbs>
    <h1 class="h2 mb-1">{{ heading }}</h1>
    <LessonHead :lesson />
    <div v-if="admin" class="d-flex flex-wrap align-items-center gap-2 mt-3 small">
      <span v-if="lesson.published" class="badge text-bg-success fw-normal">показано студентам</span>
      <span v-else class="badge text-bg-warning fw-normal">чернетка — бачиш лише ти</span>
      <a href="#" class="text-secondary" @click.prevent="publish(!lesson.published)">{{ lesson.published ? 'сховати' : 'показати студентам' }}</a>
      <span v-if="error" class="text-danger">{{ error }}</span>
    </div>

    <section v-if="lesson.summary || admin" class="mt-4">
      <GuideBody :page="summary" :view="summaryView" :put="putText('summary')" history="" placeholder="Конспекту ще нема — bin/lesson pull, /lesson summary, push" />
    </section>

    <section v-if="lesson.transcript || admin" class="mt-4">
      <div class="d-flex align-items-center gap-2">
        <a v-if="lesson.transcript" href="#" class="fold text-decoration-none text-reset d-inline-flex align-items-center gap-1" @click.prevent="open = !open">
          <IconChevron :dir="open ? 'down' : 'right'" :size="12" /><span class="fw-semibold">🗣 Транскрипт</span>
          <span class="text-secondary small">· {{ sum.sections }} розділів · {{ sum.lines }} реплік · {{ sum.speakers }} мовців</span>
        </a>
        <span v-else class="text-secondary small">🗣 Транскрипту ще нема</span>
        <a v-if="admin && lesson.transcript" href="#" class="small text-secondary ms-auto" @click.prevent="editing = !editing">✏️ транскрипт</a>
      </div>
      <GuideEditor v-if="editing" :page="transcriptPage" :put="putText('transcript')" notitle @saved="editing = false" @close="editing = false" />
      <Transcript v-if="open" :sections :people="lesson.people" :video :start="lesson.video_start" />
      <Toc :items="toc" />
    </section>

    <LessonWho v-if="lesson.zoom.uuid || admin" :lesson :admin @changed="load" />
    <LessonChat v-if="lesson.chat" :text="lesson.chat" />
    <details v-if="admin && lesson.notes" class="mt-4 small">
      <summary class="text-secondary">🗒 Нотатки злиття (лише тобі)</summary>
      <GuideText :text="lesson.notes" class="mt-2" />
    </details>
    <LessonSources v-if="admin" :lesson @changed="load" />
  </div>
</template>

<style scoped>
.fold:hover .fw-semibold { text-decoration: underline; }
</style>
