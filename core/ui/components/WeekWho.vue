<script setup>
import { byGroup } from '../studentFilter.js'
import { DAYS, span } from '../week.js'
import { byReason } from '../weekSum.js'
import CopyNicks from './CopyNicks.vue'

// who is in the way of the window looked at. Those who can't — by reason, and within it by group: a class by the timetable
// takes a whole group at once; a person's own words follow their name. Those who would rather not — by name.
// `found` — who() of weekSum.js
defineProps({ found: { type: Object, required: true } })
const said = (p, title) => p.marks.map((m) => m.why.trim()).filter((why) => why && why !== title).join('; ')
const hint = (p) => [p.tg_username && `@${p.tg_username}`, ...p.marks.map((m) => `${DAYS[m.day]} ${span(m)} ${m.why}`)].filter(Boolean).join('\n')
</script>

<template>
  <div class="who small">
    <div v-if="!found.no.length && !found.meh.length" class="text-secondary">Ніхто не проти 🎉</div>
    <div v-for="[title, people] in byReason(found.no)" :key="title" class="mb-2">
      <b>{{ title }}</b> <span class="text-secondary me-1">{{ people.length }}</span> <CopyNicks :people />
      <div v-for="g in byGroup(people)" :key="g.name">
        <span class="text-secondary">{{ g.name || 'без групи' }} · {{ g.list.length }}:</span>
        <template v-for="(p, i) in g.list" :key="p.nick">{{ i ? ', ' : ' ' }}<RouterLink :to="`/activity?user=${p.nick}`" :title="hint(p)">{{ p.name || p.nick }}</RouterLink><i v-if="said(p, title)" class="text-secondary"> — {{ said(p, title) }}</i></template>
      </div>
    </div>
    <div v-if="found.meh.length">
      <b>Незручно</b> <span class="text-secondary">{{ found.meh.length }}</span>:
      <template v-for="(p, i) in found.meh" :key="p.nick">{{ i ? ', ' : '' }}<RouterLink :to="`/activity?user=${p.nick}`" :title="hint(p)">{{ p.name || p.nick }}</RouterLink></template>
    </div>
  </div>
</template>

<style scoped>
.who { padding: .25rem 0 .25rem 1rem; border-left: 2px solid var(--bs-primary); }
.who a { color: inherit; }
</style>
