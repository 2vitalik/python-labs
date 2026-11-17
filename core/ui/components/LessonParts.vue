<script setup>
import { computed, ref } from 'vue'

import { flash } from '../anchors.js'
import { putLesson } from '../api.js'
import { byStart, clock, fmtDur, hm, parseTranscript, partDur, partOf, partSpan } from '../lesson.js'
import Avatar from './Avatar.vue'
import DelButton from './DelButton.vue'
import GuideText from './GuideText.vue'
import Icon from './Icon.vue'
import LessonLinks from './LessonLinks.vue'
import LessonPartForm from './LessonPartForm.vue'
import Transcript from './Transcript.vue'

// the day by its parts (T333): a scale of time on top, a card per part under it — when, what, for whom, its video and
// texts. A `site` part is the site's own (a defense): it leads to its page and is not edited here
const props = defineProps({ lesson: Object, admin: Boolean, clicks: Object })
const emit = defineEmits(['saved'])
const editing = ref('')  // a part's key, or «new»
const error = ref('')
const parts = computed(() => byStart(props.lesson.parts))
const own = computed(() => props.lesson.parts.filter((p) => !p.site))
const timed = computed(() => parts.value.filter((p) => p.start && p.end))
const from = computed(() => Math.min(...timed.value.map((p) => clock(p.start))))
const span = computed(() => Math.max(...timed.value.map((p) => clock(p.end))) - from.value || 1)
const place = (p) => ({ left: `${(100 * (clock(p.start) - from.value)) / span.value}%`, width: `${(100 * partDur(p)) / span.value}%`, background: partOf(p).color })
const hint = (p) => [partOf(p).name, p.title, partSpan(p), p.people?.map((u) => u.name).join(', ')].filter(Boolean).join(' · ')

async function put(list) {  // the whole list goes: what is not sent is gone
  error.value = ''
  try {
    emit('saved', await putLesson(props.lesson.slug, { rev: props.lesson.rev, parts: list, note: 'частини' }))
    editing.value = ''
  } catch (e) {
    error.value = e.message
  }
}
const save = (part) => put(editing.value === 'new' ? [...own.value, part] : own.value.map((p) => (p.key === part.key ? part : p)))
const next = computed(() => ({ start: hm(byStart(own.value).at(-1)?.end) }))  // a new part starts where the last one ended
</script>

<template>
  <section v-if="parts.length || admin" class="mt-4">
    <div v-if="timed.length > 1" class="scale mb-3">
      <div class="lane"><a v-for="p in timed.filter((x) => !x.site)" :key="p.key" href="#" :style="place(p)" :title="hint(p)" @click.prevent="flash(`p-${p.key}`)"></a></div>
      <div v-if="timed.some((x) => x.site)" class="lane thin"><a v-for="p in timed.filter((x) => x.site)" :key="p.key" href="#" :style="place(p)" :title="hint(p)" @click.prevent="flash(`p-${p.key}`)"></a></div>
      <div class="d-flex justify-content-between small text-body-tertiary"><span>{{ hm(timed[0].start) }}</span><span>{{ fmtDur(span) }}</span><span>{{ hm(timed.at(-1).end) }}</span></div>
    </div>
    <div v-if="error" class="text-danger small mb-2">{{ error }}</div>
    <article v-for="p in parts" :id="`p-${p.key}`" :key="p.key" class="part" :class="{ rest: p.kind === 'break' }" :style="{ '--c': partOf(p).color }">
      <LessonPartForm v-if="editing === p.key" :part="p" @save="save" @close="editing = ''" />
      <template v-else>
        <header class="d-flex flex-wrap align-items-center gap-2">
          <span class="kind"><Icon :name="partOf(p).icon" /> {{ partOf(p).name }}</span>
          <span v-if="p.title" class="fw-semibold">{{ p.title }}</span>
          <span class="text-secondary small text-nowrap">{{ partSpan(p) }}<template v-if="partDur(p)"> · {{ fmtDur(partDur(p)) }}</template></span>
          <span v-for="u in p.people" :key="u.nick" class="d-inline-flex align-items-center gap-1 small"><Avatar :user="u" :size="20" /> {{ u.name }}</span>
          <span v-if="p.badge" class="small text-nowrap">{{ p.badge }}</span>
          <span v-if="p.private" class="small text-secondary text-nowrap" :title="admin ? 'Цю частину бачать лише названі студенти й ти' : 'Цю частину бачиш лише ти й викладач'">
            <Icon name="eyeoff" /> {{ admin ? 'приватно' : 'лише тобі' }}</span>
          <span v-if="admin && !p.site" class="d-inline-flex ms-auto">
            <button type="button" class="iact" title="Редагувати частину" @click="editing = p.key"><Icon name="pencil" /></button>
            <DelButton what="частину" :note="p.title || partSpan(p)" @yes="put(own.filter((x) => x.key !== p.key))" />
          </span>
        </header>
        <div v-if="p.note" class="small text-secondary mt-1">{{ p.note }}</div>
        <LessonLinks :slug="lesson.slug" :links="p.links" :clicks class="mt-2" />
        <RouterLink v-if="p.to" :to="p.to" class="small d-inline-block mt-1">{{ p.more || 'Докладніше' }} →</RouterLink>
        <GuideText v-if="p.summary" :text="p.summary" class="mt-2" />
        <details v-if="p.transcript" class="mt-2">
          <summary class="small text-secondary">🗣 Транскрипт цієї частини</summary>
          <Transcript :sections="parseTranscript(p.transcript)" :people="lesson.people" />
        </details>
      </template>
    </article>
    <template v-if="admin && !lesson.virtual">
      <LessonPartForm v-if="editing === 'new'" :part="next" is-new class="mt-2" @save="save" @close="editing = ''" />
      <button v-else type="button" class="btn btn-add btn-sm mt-2 d-inline-flex align-items-center gap-1" @click="editing = 'new'"><Icon name="plus" /> частина</button>
    </template>
  </section>
</template>

<style scoped>
.lane { position: relative; height: .9rem; margin-bottom: 2px; border-radius: .3rem; background: var(--bs-tertiary-bg); overflow: hidden; }
.lane.thin { height: .45rem; }
.lane a { position: absolute; top: 0; bottom: 0; min-width: 2px; opacity: .8; box-shadow: inset -1px 0 var(--bs-body-bg); }
.lane a:hover { opacity: 1; }
.part { padding: .5rem .75rem; margin-bottom: .5rem; border: 1px solid var(--bs-border-color); border-left: 3px solid var(--c); border-radius: .45rem; }
.part.rest { opacity: .6; }
.kind { display: inline-flex; align-items: center; gap: .3rem; color: var(--c); font-weight: 600; white-space: nowrap; }
</style>
