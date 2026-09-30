<script setup>
import { computed, ref } from 'vue'

import { mark, moment, optionLabel, whoKey, whoName } from '../polls.js'
import { byGroup } from '../studentFilter.js'
import Avatar from './Avatar.vue'
import IconChevron from './IconChevron.vue'

// students × polls (T174): a cell is the student's answer, the emoji of what they chose; «·» — no vote, ↩︎ — taken back.
// A header row per group folds it; below the students — everyone else who voted, so no vote is out of sight.
// `data` — GET /api/polls/matrix with the rows the page kept
const props = defineProps({ data: { type: Object, required: true } })
const polls = computed(() => props.data.polls)
const groups = computed(() => byGroup(props.data.rows))
const folded = ref(new Set())
const toggle = (name) => (folded.value.has(name) ? folded.value.delete(name) : folded.value.add(name))
const text = (c, p) => (!c ? '·' : c.ids.length ? mark(p.options, c.ids) : '↩︎')
const hint = (c, p, name) => `${name} · ${p.title}\n${!c ? 'голосу нема' : c.ids.length ? c.ids.map((i) => optionLabel(p.options[i] || {})).join(', ') : '↩︎ голос відкликано'}`
  + (c ? `\n${moment(c.at)}` : '')
const head = (p) => [p.question, ...p.options.map((o, i) => `${o.emoji || i + 1} — ${o.text}`), moment(p.sent_at)].join('\n')
const answered = (r) => polls.value.filter((p) => r.cells[p.id]?.ids.length).length
const total = (p) => props.data.rows.filter((r) => r.cells[p.id]?.ids.length).length
const role = (w) => (w.status === 'admin' ? 'викладач' : w.test ? 'тестовий' : w.status === 'pending' ? 'очікує' : w.nick ? '' : 'бот не знає')
</script>

<template>
  <div class="wrap border rounded">
    <table class="table table-sm table-hover align-middle mb-0">
      <thead>
        <tr>
          <th class="name">Студент</th>
          <th v-for="p in polls" :key="p.id" class="poll" :title="head(p)"><RouterLink :to="`/polls/${p.id}`">{{ p.title }}</RouterLink></th>
          <th class="sum" title="Скільки з цих опитувань — з відповіддю">Σ</th>
        </tr>
      </thead>
      <tbody v-for="g in groups" :key="g.name">
        <tr class="table-light" role="button" @click="toggle(g.name)">
          <th class="name"><IconChevron :dir="folded.has(g.name) ? 'right' : 'down'" :size="12" class="text-secondary" />
            {{ g.name || 'Без групи' }} <span class="count">{{ g.list.length }}</span></th>
          <td :colspan="polls.length + 1"></td>
        </tr>
        <template v-if="!folded.has(g.name)">
          <tr v-for="r in g.list" :key="r.nick">
            <th class="name fw-normal">
              <Avatar :user="r" :size="20" /> <RouterLink :to="`/activity?user=${r.nick}`">{{ r.name || r.nick }}</RouterLink>
              <span v-if="!r.tg_linked" title="Бот не привʼязаний: голоси цієї людини — серед «Інших голосів» як невідомий акаунт"> 🚫</span>
            </th>
            <td v-for="p in polls" :key="p.id" class="cell" :class="{ none: !r.cells[p.id] }" :title="hint(r.cells[p.id], p, r.name || r.nick)">
              {{ text(r.cells[p.id], p) }}</td>
            <td class="sum">{{ answered(r) || '' }}</td>
          </tr>
        </template>
      </tbody>
      <tbody v-if="data.others.length">
        <tr class="table-light">
          <th class="name">Інші голоси <span class="count">{{ data.others.length }}</span></th>
          <td :colspan="polls.length + 1" class="small text-secondary">викладачі, тестові й ті, кого сайт не знає: бота не привʼязали</td>
        </tr>
        <tr v-for="o in data.others" :key="whoKey(o.who)">
          <th class="name fw-normal">
            <Avatar v-if="o.who.nick" :user="o.who" :size="20" /> {{ whoName(o.who) }} <small class="text-secondary">{{ role(o.who) }}</small>
          </th>
          <td v-for="p in polls" :key="p.id" class="cell" :class="{ none: !o.cells[p.id] }" :title="hint(o.cells[p.id], p, whoName(o.who))">
            {{ text(o.cells[p.id], p) }}</td>
          <td class="sum">{{ answered(o) || '' }}</td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <th class="name fw-normal text-secondary">Відповіли студенти</th>
          <td v-for="p in polls" :key="p.id" class="cell small text-secondary">{{ total(p) }}</td>
          <td></td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<style scoped>
.wrap { overflow-x: auto; }
th, td { white-space: nowrap; }
/* the names stay in sight while the polls scroll; Bootstrap's cell background keeps them opaque */
.name { position: sticky; left: 0; z-index: 1; min-width: 12rem; max-width: 18rem; overflow: hidden; text-overflow: ellipsis; }
.name a { color: inherit; text-decoration: none; }
.name a:hover { text-decoration: underline; }
.poll { min-width: 3.5rem; max-width: 7rem; white-space: normal; text-align: center; font-size: .75rem; font-weight: 600; line-height: 1.2; vertical-align: bottom; }
.poll a { color: inherit; text-decoration: none; }
.poll a:hover { text-decoration: underline; }
.cell { text-align: center; font-size: 1.05rem; }
.cell.none { color: var(--bs-tertiary-color); }
.sum { text-align: center; color: var(--bs-secondary-color); font-size: .85rem; }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
/* a phone: the names give the polls room */
@media (max-width: 576px) { .name { min-width: 8rem; max-width: 10rem; } }
</style>
