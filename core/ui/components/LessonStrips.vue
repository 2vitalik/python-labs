<script setup>
import { computed } from 'vue'

import { byStart, fmtDur, partOf } from '../lesson.js'

// who was in the meeting when (T333): a strip per person across the meeting's span, the day's parts as the ruler on top —
// which part somebody came to and which they left is seen at a glance. The teacher's view: the segments are the admin's
const props = defineProps({ data: Object, lesson: Object })
const start = computed(() => new Date(props.data.meeting.start).getTime())
const total = computed(() => props.data.seconds * 1000 || 1)
const pct = (ms) => Math.min(100, Math.max(0, (100 * (ms - start.value)) / total.value))
const pos = (a, b) => ({ left: `${pct(a)}%`, width: `${pct(b) - pct(a)}%` })
const at = (t) => new Date(`${props.lesson.date}T${t.length === 5 ? `${t}:00` : t}`).getTime()  // the reader's clock is the classes' one
const ruler = computed(() => byStart(props.lesson.parts || []).filter((p) => p.start && p.end && !p.site && props.lesson.date)
  .map((p) => ({ key: p.key, title: [partOf(p).name, p.title].filter(Boolean).join(' · '), style: { ...pos(at(p.start), at(p.end)), background: partOf(p).color } })))
const rows = computed(() => [...props.data.people.map((p) => ({ ...p, label: p.person.name, group: p.person.group || '' })),
                             ...props.data.unknown.map((u) => ({ ...u, label: `? ${u.name}`, group: '￿' }))]
  .sort((a, b) => a.group.localeCompare(b.group) || a.label.localeCompare(b.label, 'uk')))
const hint = (r) => [r.label, fmtDur(r.seconds), ...(r.segments || []).map((s) => `${time(s.join)}–${time(s.leave)}`)].join('\n')
const time = (iso) => new Date(iso).toLocaleTimeString('uk-UA', { hour: '2-digit', minute: '2-digit' })
</script>

<template>
  <div class="strips mt-2">
    <div v-if="ruler.length" class="line">
      <span class="who small text-body-tertiary">частини</span>
      <span class="bar ruler"><i v-for="p in ruler" :key="p.key" :style="p.style" :title="p.title"></i></span>
      <span class="min"></span>
    </div>
    <div v-for="r in rows" :key="r.name" class="line" :class="{ pale: !r.present }" :title="hint(r)">
      <RouterLink v-if="r.person" :to="`/students/${r.person.nick}`" class="who small text-decoration-none text-reset">{{ r.label }}</RouterLink>
      <span v-else class="who small text-warning-emphasis">{{ r.label }}</span>
      <span class="bar"><i v-for="(s, i) in r.segments" :key="i" :style="pos(new Date(s.join).getTime(), new Date(s.leave).getTime())"></i></span>
      <span class="min small text-secondary">{{ Math.round(r.seconds / 60) }}</span>
    </div>
  </div>
</template>

<style scoped>
.line { display: flex; align-items: center; gap: .5rem; height: 1.25rem; }
.who { flex: 0 0 11rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.bar { position: relative; flex: 1; height: .6rem; border-radius: .2rem; background: var(--bs-tertiary-bg); overflow: hidden; }
.bar i { position: absolute; top: 0; bottom: 0; min-width: 1px; background: var(--bs-success); }
.ruler { height: .4rem; }
.ruler i { opacity: .8; box-shadow: inset -1px 0 var(--bs-body-bg); }
.min { flex: 0 0 2.2rem; text-align: right; font-variant-numeric: tabular-nums; }
.pale .bar i { opacity: .45; }
@media (max-width: 575px) { .who { flex-basis: 6.5rem; } }
</style>
