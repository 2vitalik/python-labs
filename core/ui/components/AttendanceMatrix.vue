<script setup>
import { computed, ref } from 'vue'

import { fmtDate, fmtDur } from '../lesson.js'
import { byGroup } from '../studentFilter.js'
import Avatar from './Avatar.vue'
import IconChevron from './IconChevron.vue'

// students × lessons (T222): a cell is the minutes in Zoom, the fuller the meeting the deeper the green; «·» — was not there.
// A header row per group folds it; Σ — lessons attended (at least a quarter of each), the hours in all
const props = defineProps({ data: { type: Object, required: true } })
const lessons = computed(() => props.data.lessons)
const groups = computed(() => byGroup(props.data.rows))
const folded = ref(new Set())
const toggle = (name) => (folded.value.has(name) ? folded.value.delete(name) : folded.value.add(name))
const share = (c, l) => Math.min(1, c.seconds / (l.seconds || 1))
const look = (c, l) => (c ? { backgroundColor: `color-mix(in srgb, var(--bs-success) ${Math.round(10 + 60 * share(c, l))}%, var(--bs-body-bg))` } : null)
const hint = (c, l, name) => `${name} · ${l.label}${l.title ? ` · ${l.title}` : ''}\n${c ? `${fmtDur(c.seconds)} · ${Math.round(100 * share(c, l))} % заняття` : 'не було'}`
const been = (r) => lessons.value.filter((l) => r.cells[l.slug]?.present).length
const hours = (r) => lessons.value.reduce((n, l) => n + (r.cells[l.slug]?.seconds || 0), 0)
const total = (l) => props.data.rows.filter((r) => r.cells[l.slug]?.present).length
</script>

<template>
  <div class="wrap border rounded">
    <table class="table table-sm table-hover align-middle mb-0">
      <thead>
        <tr>
          <th class="name">Студент</th>
          <th v-for="l in lessons" :key="l.slug" class="lesson" :title="[l.label, l.title, fmtDate(l.date, true), fmtDur(l.seconds)].filter(Boolean).join('\n')">
            <RouterLink :to="`/lessons/${l.slug}`">{{ l.label }}<small class="d-block fw-normal text-secondary">{{ fmtDate(l.date) || '—' }}</small></RouterLink>
          </th>
          <th class="sum" title="Занять, де був хоча б чверть часу · годин у всіх">Σ</th>
        </tr>
      </thead>
      <tbody v-for="g in groups" :key="g.name">
        <tr class="table-light" role="button" @click="toggle(g.name)">
          <th class="name"><IconChevron :dir="folded.has(g.name) ? 'right' : 'down'" :size="12" class="text-secondary" />
            {{ g.name || 'Без групи' }} <span class="count">{{ g.list.length }}</span></th>
          <td :colspan="lessons.length + 1"></td>
        </tr>
        <template v-if="!folded.has(g.name)">
          <tr v-for="r in g.list" :key="r.nick">
            <th class="name fw-normal"><Avatar :user="r" :size="20" /> <RouterLink :to="`/students/${r.nick}/edit`">{{ r.name || r.nick }}</RouterLink></th>
            <td v-for="l in lessons" :key="l.slug" class="cell" :class="{ none: !r.cells[l.slug], pale: r.cells[l.slug] && !r.cells[l.slug].present }"
                :style="look(r.cells[l.slug], l)" :title="hint(r.cells[l.slug], l, r.name || r.nick)">{{ r.cells[l.slug] ? Math.round(r.cells[l.slug].seconds / 60) : '·' }}</td>
            <td class="sum">{{ been(r) || '' }}<small v-if="hours(r)" class="d-block">{{ fmtDur(hours(r)) }}</small></td>
          </tr>
        </template>
      </tbody>
      <tfoot>
        <tr>
          <th class="name fw-normal text-secondary">Були</th>
          <td v-for="l in lessons" :key="l.slug" class="cell small text-secondary" :title="l.unknown ? `${l.unknown} імен, яких реєстр не знає — «хто це?» на сторінці заняття` : ''">
            {{ total(l) }}<span v-if="l.unknown" class="text-warning"> +{{ l.unknown }}?</span></td>
          <td></td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<style scoped>
.wrap { overflow-x: auto; }
th, td { white-space: nowrap; }
/* the names stay in sight while the lessons scroll; Bootstrap's cell background keeps them opaque */
.name { position: sticky; left: 0; z-index: 1; min-width: 12rem; max-width: 18rem; overflow: hidden; text-overflow: ellipsis; }
.name a, .lesson a { color: inherit; text-decoration: none; }
.name a:hover, .lesson a:hover { text-decoration: underline; }
.lesson { min-width: 3.6rem; text-align: center; font-size: .8rem; line-height: 1.2; vertical-align: bottom; }
.cell { text-align: center; font-variant-numeric: tabular-nums; min-width: 3rem; }
.cell.none { color: var(--bs-tertiary-color); }
.cell.pale { color: var(--bs-secondary-color); }
.sum { text-align: center; color: var(--bs-secondary-color); font-size: .85rem; line-height: 1.1; }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
@media (max-width: 576px) { .name { min-width: 8rem; max-width: 10rem; } }
</style>
