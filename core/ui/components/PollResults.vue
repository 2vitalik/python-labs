<script setup>
import { computed } from 'vue'

import { moment, optionLabel, plural, whoKey, whoName } from '../polls.js'
import PollPeople from './PollPeople.vue'

// the answers as in Telegram — a bar each, and under it who chose it; then who took the vote back, which students with the bot
// have not voted yet, and every vote as it came. `res` — GET /api/polls/:id
const props = defineProps({ res: { type: Object, required: true } })
const options = computed(() => props.res.poll.options)
const voters = computed(() => new Set(props.res.options.flatMap((o) => o.voters.map((v) => whoKey(v.who)))).size)
const missing = computed(() => props.res.missing.reduce((n, g) => n + g.people.length, 0))
// groups some student already voted from come first: the rest most likely never got the poll
const heard = computed(() => new Set([...props.res.options.flatMap((o) => o.voters), ...props.res.retracted].map((v) => v.who.group).filter(Boolean)))
const groups = computed(() => [...props.res.missing].sort((a, b) => heard.value.has(b.group) - heard.value.has(a.group)))
const many = computed(() => new Set(props.res.sends.map((s) => s.where)).size > 1)  // where a vote came from matters only then
const share = (n) => (voters.value ? Math.round((100 * n) / voters.value) : 0)
const answer = (ids) => (ids.length ? ids.map((i) => optionLabel(options.value[i] || { text: `#${i + 1}` })).join(', ') : '↩︎ голос відкликано')
</script>

<template>
  <div>
    <div class="d-flex align-items-baseline gap-2 mb-2">
      <h2 class="h5 mb-0">Відповіді</h2>
      <span class="text-secondary">{{ voters }} {{ plural(voters, 'людина', 'людини', 'людей') }}</span>
    </div>
    <div v-for="(o, i) in res.options" :key="i" class="mb-3">
      <div class="d-flex align-items-baseline gap-2">
        <span class="text-break">{{ optionLabel(o) }}</span>
        <span class="ms-auto fw-semibold">{{ o.voters.length }}</span>
        <span class="pct text-secondary small text-end">{{ share(o.voters.length) }}%</span>
      </div>
      <div class="bar my-1"><div :style="{ width: `${share(o.voters.length)}%` }"></div></div>
      <PollPeople v-if="o.voters.length" :list="o.voters" />
    </div>

    <div v-if="res.tries.length" class="mb-3">
      <div class="small fw-semibold text-secondary mb-1" title="Голоси викладачів і тестових студентів — у підрахунок не йдуть">🧪 Спроби · {{ res.tries.length }}</div>
      <div v-for="t in res.tries" :key="whoKey(t.who)" class="small text-secondary">{{ whoName(t.who) }} — {{ answer(t.ids) }}</div>
    </div>

    <div v-if="res.retracted.length" class="mb-3">
      <div class="small fw-semibold text-secondary mb-1">↩︎ Відкликали голос · {{ res.retracted.length }}</div>
      <PollPeople :list="res.retracted" />
    </div>

    <details class="mb-3" :open="missing > 0 && missing <= 30">
      <summary class="small fw-semibold text-secondary">⏳ Ще не відповіли · {{ missing }}</summary>
      <div v-for="g in groups" :key="g.group" class="mt-2" :class="{ 'opacity-75': !heard.has(g.group) }">
        <div class="small text-secondary mb-1">{{ g.group || 'Без групи' }} · {{ g.people.length }}
          <i v-if="!heard.has(g.group)">· з групи ще ніхто не голосував — мабуть, туди не надсилали</i></div>
        <PollPeople :list="g.people" />
      </div>
      <p class="small text-secondary mt-2 mb-0">
        Тут лише студенти з привʼязаним ботом — з усіх груп: сайт не знає, яка гілка чиєї групи.
        <template v-if="res.unlinked">Ще {{ res.unlinked }} {{ plural(res.unlinked, 'студент', 'студенти', 'студентів') }} без бота: якщо голосували, то вони серед невпізнаних «?».</template>
      </p>
    </details>

    <details v-if="res.timeline.length">
      <summary class="small fw-semibold text-secondary">🕘 Хід голосування · {{ res.timeline.length }}</summary>
      <div v-for="(v, i) in res.timeline" :key="i" class="d-flex gap-2 small py-1 border-bottom">
        <span class="text-secondary when">{{ moment(v.at) }}</span>
        <span class="who text-truncate">{{ whoName(v.who) }}</span>
        <span class="text-truncate" :class="{ 'text-secondary': !v.ids.length }">{{ answer(v.ids) }}</span>
        <span v-if="many" class="ms-auto text-secondary text-truncate">📍 {{ v.where }}</span>
      </div>
    </details>
  </div>
</template>

<style scoped>
.bar { height: .5rem; border-radius: .25rem; background: var(--bs-secondary-bg); overflow: hidden; }
.bar div { height: 100%; background: var(--bs-primary); border-radius: .25rem; transition: width .3s; }
.pct { flex: 0 0 2.5rem; }
.when { flex: 0 0 7.5rem; }
.who { flex: 0 0 11rem; }
summary { cursor: pointer; }
</style>
