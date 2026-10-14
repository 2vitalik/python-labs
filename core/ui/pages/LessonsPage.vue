<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getLessons } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import { KINDS_MANY, fmtDate } from '../lesson.js'
import { user } from '../user.js'

// every meeting, newest first; chips narrow to one kind (?kind=) when there are several; a draft is dimmed, the admin's only
const route = useRoute()
const router = useRouter()
const all = ref([])
const admin = computed(() => user.value?.status === 'admin')
const kinds = computed(() => Object.keys(KINDS_MANY).filter((k) => all.value.some((l) => l.kind === k)))
const kind = computed(() => route.query.kind || '')
const rows = computed(() => all.value.filter((l) => !kind.value || l.kind === kind.value))
const pick = (k) => router.replace({ query: k ? { kind: k } : {} })
const marks = (l) => [l.has.summary && ['📝', 'конспект'], l.has.transcript && ['🗣', 'транскрипт'], l.links.length && ['🎬', 'посилання'],
                      l.has.files && ['📎', 'файли'], l.has.zoom && ['👥', 'відвідування']].filter(Boolean)
onMounted(async () => (all.value = await getLessons()))
</script>

<template>
  <Crumbs :items="['Пари']">
    <div v-if="admin" class="d-flex gap-2 ms-auto">
      <RouterLink to="/attendance" class="btn btn-outline-secondary btn-sm">👥 Відвідування</RouterLink>
      <RouterLink to="/lessons/new" class="btn btn-outline-primary btn-sm">＋ Пара</RouterLink>
    </div>
  </Crumbs>
  <h1 class="h2 mb-3">Пари</h1>
  <div v-if="kinds.length > 1" class="d-flex flex-wrap gap-1 mb-3">
    <button class="btn btn-sm chip" :class="kind ? 'btn-outline-secondary' : 'btn-secondary'" @click="pick('')">Усі</button>
    <button v-for="k in kinds" :key="k" class="btn btn-sm chip" :class="kind === k ? 'btn-secondary' : 'btn-outline-secondary'" @click="pick(k)">
      {{ KINDS_MANY[k] }}
    </button>
  </div>
  <p v-if="!rows.length" class="text-secondary">Записів ще нема.</p>
  <ol class="lessons list-unstyled">
    <li v-for="l in rows" :key="l.slug" :class="{ draft: !l.published }">
      <span class="date text-secondary">{{ fmtDate(l.date) || '—' }}</span>
      <span class="badge rounded-pill text-bg-light border fw-normal">{{ l.label }}</span>
      <RouterLink :to="`/lessons/${l.slug}`" class="title">{{ l.title || 'без назви' }}</RouterLink>
      <span v-if="!l.published" class="badge text-bg-warning fw-normal">чернетка</span>
      <span class="groups small text-body-tertiary d-none d-sm-inline">{{ l.groups.join(', ') }}</span>
      <span class="marks text-nowrap"><span v-for="[m, t] in marks(l)" :key="m" :title="t">{{ m }}</span></span>
    </li>
  </ol>
</template>

<style scoped>
.lessons li { display: flex; flex-wrap: wrap; align-items: baseline; gap: .25rem .6rem; padding: .45rem 0; border-bottom: 1px solid var(--bs-border-color-translucent); }
.date { min-width: 3.6rem; font-variant-numeric: tabular-nums; }
.title { text-decoration: none; }
.title:hover { text-decoration: underline; }
.draft .title { color: var(--bs-secondary-color); }
.marks { margin-left: auto; letter-spacing: .15rem; }
</style>
