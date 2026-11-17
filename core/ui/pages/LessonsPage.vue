<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getClicks, getLessons } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import Icon from '../components/Icon.vue'
import { PARTS, dayShort, hm, lacks } from '../lesson.js'
import { user } from '../user.js'

// every day with students, newest first, month by month: what the day consisted of (its parts as chips), what is there
// to read and watch. Chips on top narrow to the days with one kind of part (?part=). The admin also sees drafts (dimmed),
// what a past day still lacks, and which hosting the students open the recordings on
const HOSTS = { telegram: '✈️ Telegram', drive: '📁 Google Drive', youtube: '🎬 YouTube', zoom: '🎬 Zoom', other: '🔗 інше' }
const route = useRoute()
const router = useRouter()
const all = ref([])
const clicks = ref(null)
const admin = computed(() => user.value?.status === 'admin')
const kinds = computed(() => Object.keys(PARTS).filter((k) => k !== 'break' && all.value.some((l) => l.parts.some((p) => p.kind === k))))
const part = computed(() => route.query.part || '')
const rows = computed(() => all.value.filter((l) => !part.value || l.parts.some((p) => p.kind === part.value)))
const pick = (k) => router.replace({ query: k ? { part: k } : {} })
const month = (l) => (l.date ? new Date(`${l.date}T00:00:00`).toLocaleDateString('uk-UA', { month: 'long', year: 'numeric' }).replace(' р.', '') : 'без дати')
// a day the site made of defenses alone has no title of its own: the teacher reads who defended, a student — «Мій захист»
const title = (l) => l.title || (!l.virtual ? 'без назви' : admin.value ? l.parts.flatMap((p) => p.people || []).map((u) => u.name).join(', ') || 'Захист' : 'Мій захист')
const head = (i) => (i === 0 || month(rows.value[i]) !== month(rows.value[i - 1]) ? month(rows.value[i]) : '')
// one chip per kind: «Захист ×3»; the hint lists the parts
const chips = (l) => Object.keys(PARTS).filter((k) => k !== 'break').map((k) => [k, l.parts.filter((p) => p.kind === k)]).filter(([, found]) => found.length)
  .map(([k, found]) => ({ ...PARTS[k], key: k, n: found.length, own: found.some((p) => p.private && !admin.value),
                         hint: found.map((p) => [hm(p.start), p.title, p.people?.map((u) => u.name).join(', ')].filter(Boolean).join(' ')).join('\n') }))
const marks = (l) => [l.has.summary && ['📝', 'конспект'], l.has.transcript && ['🗣', 'транскрипт'], l.has.video && ['🎬', 'відео'],
                      l.has.files && ['📎', 'файли'], l.has.zoom && ['👥', 'відвідування']].filter(Boolean)
onMounted(async () => {
  all.value = await getLessons()
  if (admin.value) clicks.value = (await getClicks()).hostings
})
</script>

<template>
  <Crumbs :items="['Пари']">
    <div v-if="admin" class="d-flex gap-2 ms-auto">
      <RouterLink to="/attendance" class="btn btn-outline-secondary btn-sm"><Icon name="users" /> Відвідування</RouterLink>
      <RouterLink to="/lessons/new" class="btn btn-outline-primary btn-sm d-inline-flex align-items-center gap-1"><Icon name="plus" /> Пара</RouterLink>
    </div>
  </Crumbs>
  <h1 class="h2 mb-3">Пари</h1>
  <p v-if="clicks && Object.keys(clicks).length" class="small text-secondary">
    Куди клікають студенти:
    <span v-for="(c, k) in clicks" :key="k" class="me-3 text-nowrap" :title="`${c.clicks} кліків · ${c.people} людей`">{{ HOSTS[k] }} <b>{{ c.people }}</b></span>
  </p>
  <div v-if="kinds.length > 1" class="d-flex flex-wrap gap-1 mb-3">
    <button class="btn btn-sm chip" :class="part ? 'btn-outline-secondary' : 'btn-secondary'" @click="pick('')">Усі</button>
    <button v-for="k in kinds" :key="k" class="btn btn-sm chip" :class="part === k ? 'btn-secondary' : 'btn-outline-secondary'" @click="pick(k)">{{ PARTS[k].name }}</button>
  </div>
  <p v-if="!rows.length" class="text-secondary">Записів ще нема.</p>
  <ol class="lessons list-unstyled">
    <template v-for="(l, i) in rows" :key="l.slug">
      <li v-if="head(i)" class="month small text-body-tertiary">{{ head(i) }}</li>
      <li class="day" :class="{ draft: !l.published }">
        <span class="date text-secondary">{{ dayShort(l.date) }}</span>
        <span v-if="l.kind" class="badge rounded-pill text-bg-light border fw-normal">{{ l.label }}</span>
        <RouterLink :to="`/lessons/${l.slug}`" class="title">{{ title(l) }}</RouterLink>
        <span v-if="!l.published" class="badge text-bg-warning fw-normal">чернетка</span>
        <span v-for="c in chips(l)" :key="c.key" class="part text-nowrap" :style="{ color: c.color }" :title="c.hint">
          <Icon :name="c.icon" /> {{ c.name }}<template v-if="c.n > 1"> ×{{ c.n }}</template><Icon v-if="c.own" name="eyeoff" class="ms-1" title="лише тобі" />
        </span>
        <span class="groups small text-body-tertiary d-none d-sm-inline">{{ l.groups.join(', ') }}</span>
        <span class="marks text-nowrap"><span v-for="[m, t] in marks(l)" :key="m" :title="t">{{ m }}</span></span>
        <span v-if="admin && lacks(l).length" class="lacks small">бракує: {{ lacks(l).join(' · ') }}</span>
      </li>
    </template>
  </ol>
</template>

<style scoped>
.day { display: flex; flex-wrap: wrap; align-items: baseline; gap: .25rem .6rem; padding: .45rem 0; border-bottom: 1px solid var(--bs-border-color-translucent); }
.month { padding-top: .9rem; }
.month::first-letter { text-transform: uppercase; }
.date { min-width: 5.6rem; font-variant-numeric: tabular-nums; }
.title { text-decoration: none; }
.title:hover { text-decoration: underline; }
.draft .title { color: var(--bs-secondary-color); }
.part { font-size: .85rem; }
.marks { margin-left: auto; letter-spacing: .15rem; }
.lacks { flex-basis: 100%; padding-left: 6.2rem; color: var(--bs-danger); }
@media (max-width: 575px) { .lacks { padding-left: 0; } }
</style>
