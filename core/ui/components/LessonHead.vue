<script setup>
import { computed } from 'vue'

import { fmtDate, fmtSize, withInfo } from '../lesson.js'

// under the h1: when, with whom, the links (video, Drive, Telegram…) and the files the class worked with
const props = defineProps({ lesson: Object })
const links = computed(() => withInfo(props.lesson.links))
const files = computed(() => props.lesson.files.filter((f) => f.role === 'file'))
const when = computed(() => [fmtDate(props.lesson.date, true), props.lesson.time, props.lesson.groups.join(', ')].filter(Boolean).join(' · '))
</script>

<template>
  <div class="text-secondary">{{ when || 'Дата ще не вказана' }}</div>
  <div v-if="links.length" class="d-flex flex-wrap gap-2 mt-2">
    <a v-for="l in links" :key="l.url" :href="l.url" target="_blank" rel="noopener" class="btn btn-outline-secondary btn-sm">{{ l.icon }} {{ l.label }}</a>
  </div>
  <ul v-if="files.length" class="list-unstyled d-flex flex-wrap gap-3 mt-2 mb-0 small">
    <li v-for="f in files" :key="f.id">
      <a :href="`/api/lessons/${lesson.slug}/files/${f.id}`" target="_blank" rel="noopener">📎 {{ f.name }}</a>
      <span class="text-body-tertiary ms-1">{{ fmtSize(f.size) }}</span>
    </li>
  </ul>
</template>
