<script setup>
import { computed } from 'vue'

import { fmtDate, fmtSize } from '../lesson.js'
import LessonLinks from './LessonLinks.vue'

// under the h1: when, with whom, the links (video, Drive, Telegram…) and the files the class worked with
const props = defineProps({ lesson: Object, clicks: Object })
const files = computed(() => props.lesson.files.filter((f) => f.role === 'file'))
// a day's date is already its heading; an old address (pz1) shows it here
const when = computed(() => [props.lesson.kind && fmtDate(props.lesson.date, true), props.lesson.time, props.lesson.groups.join(', ')].filter(Boolean).join(' · '))
</script>

<template>
  <div class="text-secondary">{{ when || (lesson.date ? '' : 'Дата ще не вказана') }}</div>
  <LessonLinks :slug="lesson.slug" :links="lesson.links" :clicks class="mt-2" />
  <ul v-if="files.length" class="list-unstyled d-flex flex-wrap gap-3 mt-2 mb-0 small">
    <li v-for="f in files" :key="f.id">
      <a :href="`/api/lessons/${lesson.slug}/files/${f.id}`" target="_blank" rel="noopener">📎 {{ f.name }}</a>
      <span class="text-body-tertiary ms-1">{{ fmtSize(f.size) }}</span>
    </li>
  </ul>
</template>
