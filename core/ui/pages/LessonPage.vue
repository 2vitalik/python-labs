<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { flash } from '../anchors.js'
import { getLesson, getLessonClicks, postLesson, putLesson } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import GuideBody from '../components/GuideBody.vue'
import GuideEditor from '../components/GuideEditor.vue'
import GuideText from '../components/GuideText.vue'
import Icon from '../components/Icon.vue'
import IconChevron from '../components/IconChevron.vue'
import LessonChat from '../components/LessonChat.vue'
import LessonHead from '../components/LessonHead.vue'
import LessonParts from '../components/LessonParts.vue'
import LessonSources from '../components/LessonSources.vue'
import LessonWho from '../components/LessonWho.vue'
import Toc from '../components/Toc.vue'
import Transcript from '../components/Transcript.vue'
import { fmtWords, lessonName, parseTranscript, reportView, stats, summaryView, withInfo } from '../lesson.js'
import { problem } from '../problem.js'
import { useTitle } from '../title.js'
import { user } from '../user.js'

// one day: its parts on a scale of time, the summary in full, the transcript folded under it (a «Теми» time or a #t-… link
// unfolds it at that section), Zoom's chat, and for the admin — the merge notes, the sources card, inline editors of both
// texts, «показати студентам». A day the site made of its own parts alone (`virtual`) has only the parts
const route = useRoute()
const lesson = ref(null)
const clicks = ref({})
const open = ref(false)
const long = ref(false)  // the long report unfolded
const editing = ref('')  // «transcript» or «report»: which text has its editor open
const error = ref('')
const slug = computed(() => route.params.slug)
const admin = computed(() => user.value?.status === 'admin')
const name = computed(() => lesson.value && lessonName(lesson.value))
const heading = computed(() => lesson.value && [name.value, lesson.value.title].filter(Boolean).join(' · '))
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
const textPage = (key) => summary.value && { ...summary.value, body: lesson.value[key] }

async function load() {
  try {
    lesson.value = await getLesson(slug.value)
    if (admin.value && !lesson.value.virtual) clicks.value = await getLessonClicks(slug.value)
    await hash(route.hash)
  } catch (e) {
    problem.value = e.status === 404 ? 'lost' : e.message
  }
}
async function act(job) {
  error.value = ''
  try {
    lesson.value = await job()
  } catch (e) {
    error.value = e.message
  }
}
const publish = (yes) => act(() => putLesson(slug.value, { published: yes, rev: lesson.value.rev }))
const create = () => act(() => postLesson({ date: slug.value }))  // the day gets its own record: a title, a video, the texts
async function hash(h) {  // a link into the transcript or to a part: unfold, then light it
  if (!/^#[tp]-/.test(h)) return
  if (h.startsWith('#t-')) open.value = true
  await nextTick()
  flash(h.slice(1))
}
watch(slug, load, { immediate: true })
watch(() => route.hash, (h) => lesson.value && hash(h))  // a save replaces `lesson` without re-scrolling
</script>

<template>
  <div v-if="lesson">
    <Crumbs :items="[['/lessons', 'Пари'], name]">
      <RouterLink v-if="admin && !lesson.virtual" :to="`/lessons/${slug}/edit`" class="btn btn-outline-secondary btn-sm ms-auto"><Icon name="pencil" /> Пара</RouterLink>
    </Crumbs>
    <h1 class="h2 mb-1">{{ heading }}</h1>
    <LessonHead v-if="!lesson.virtual" :lesson :clicks />
    <div v-if="admin" class="d-flex flex-wrap align-items-center gap-2 mt-3 small">
      <template v-if="lesson.virtual">
        <span class="text-secondary">Заняття за цей день ще не заведено — є лише захисти.</span>
        <a href="#" @click.prevent="create">завести заняття</a>
      </template>
      <template v-else>
        <span v-if="lesson.published" class="badge text-bg-success fw-normal">показано студентам</span>
        <span v-else class="badge text-bg-warning fw-normal">чернетка — бачиш лише ти</span>
        <a href="#" class="text-secondary" @click.prevent="publish(!lesson.published)">{{ lesson.published ? 'сховати' : 'показати студентам' }}</a>
      </template>
      <span v-if="error" class="text-danger">{{ error }}</span>
    </div>

    <LessonParts :lesson :admin :clicks @saved="lesson = $event" />

    <template v-if="!lesson.virtual">
      <section v-if="lesson.summary || admin" class="mt-4">
        <GuideBody :page="summary" :view="summaryView" :put="putText('summary')" history="" placeholder="Конспекту ще нема — bin/lesson pull, /lesson summary, push" />
      </section>

      <section v-if="lesson.report || admin" class="mt-4">
        <div class="d-flex align-items-center gap-2">
          <a v-if="lesson.report" href="#" class="fold text-decoration-none text-reset d-inline-flex align-items-center gap-1" @click.prevent="long = !long">
            <IconChevron :dir="long ? 'down' : 'right'" :size="12" /><span class="fw-semibold">📖 Докладно</span>
            <span class="text-secondary small">· для тих, хто не був · {{ fmtWords(lesson.report.split(/\s+/).length) }}</span>
          </a>
          <span v-else class="text-secondary small">📖 Докладного звіту ще нема</span>
          <a v-if="admin && lesson.report" href="#" class="small text-secondary ms-auto" @click.prevent="editing = editing === 'report' ? '' : 'report'"><Icon name="pencil" /> докладно</a>
        </div>
        <GuideEditor v-if="editing === 'report'" :page="textPage('report')" :put="putText('report')" notitle @saved="editing = ''" @close="editing = ''" />
        <GuideText v-if="long" :text="reportView(lesson.report)" class="mt-2" />
      </section>

      <section v-if="lesson.transcript || admin" class="mt-4">
        <div class="d-flex align-items-center gap-2">
          <a v-if="lesson.transcript" href="#" class="fold text-decoration-none text-reset d-inline-flex align-items-center gap-1" @click.prevent="open = !open">
            <IconChevron :dir="open ? 'down' : 'right'" :size="12" /><span class="fw-semibold">🗣 Транскрипт</span>
            <span class="text-secondary small">· {{ sum.sections }} розділів · {{ sum.lines }} реплік · {{ sum.speakers }} мовців</span>
          </a>
          <span v-else class="text-secondary small">🗣 Транскрипту ще нема</span>
          <a v-if="admin && lesson.transcript" href="#" class="small text-secondary ms-auto" @click.prevent="editing = editing === 'transcript' ? '' : 'transcript'"><Icon name="pencil" /> транскрипт</a>
        </div>
        <GuideEditor v-if="editing === 'transcript'" :page="textPage('transcript')" :put="putText('transcript')" notitle @saved="editing = ''" @close="editing = ''" />
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
    </template>
  </div>
</template>

<style scoped>
.fold:hover .fw-semibold { text-decoration: underline; }
</style>
