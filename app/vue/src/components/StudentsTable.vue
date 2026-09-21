<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

import IconChevron from './IconChevron.vue'

// admin table: a header row per group folds it; «↗» shows that group alone (?group=, crumb on the page);
// the name opens the profile; a row stands out when something is off — not a student, or never signed in;
// Telegram shows what is missing, not what is there: 🚫 = no bot yet (though signed in), «без нікнейма» = bot without a handle
const props = defineProps({ students: Array })
const route = useRoute()
const folded = ref(new Set())
const groups = computed(() => {
  const by = new Map()
  for (const s of props.students) by.set(s.group, [...(by.get(s.group) || []), s])
  return [...by].sort(([a], [b]) => (a === '') - (b === '') || a.localeCompare(b)).map(([name, list]) => ({ name, list }))
})
const toggle = (name) => (folded.value.has(name) ? folded.value.delete(name) : folded.value.add(name))
const foldAll = (yes) => (folded.value = new Set(yes ? groups.value.map((g) => g.name) : []))
const fio = (s) => s.name || s.nick
const repoName = (url) => url.replace('https://github.com/', '')
const rowClass = (s) => ({ 'table-warning': s.status === 'pending', 'table-info': s.status === 'admin', ghost: !s.seen })
</script>

<template>
  <div v-if="groups.length > 1" class="small text-end mb-1">
    <a href="#" class="text-secondary" @click.prevent="foldAll(true)">згорнути всі</a> ·
    <a href="#" class="text-secondary" @click.prevent="foldAll(false)">розгорнути всі</a>
  </div>
  <table class="table align-middle">
    <thead>
      <tr><th>ПІБ</th><th class="text-center">Гра</th><th class="text-center">GitHub</th><th class="text-center">Telegram</th></tr>
    </thead>
    <tbody v-for="g in groups" :key="g.name">
      <tr class="table-light" role="button" @click="toggle(g.name)">
        <th colspan="4" class="fw-semibold">
          <span class="caret text-secondary"><IconChevron :dir="folded.has(g.name) ? 'right' : 'down'" :size="12" /></span>
          {{ g.name || 'Без групи' }} <span class="count">{{ g.list.length }}</span>
          <RouterLink v-if="g.name && !route.query.group" :to="{ query: { group: g.name } }" class="ibtn ms-2"
                      title="Лише ця група" @click.stop>↗</RouterLink>
        </th>
      </tr>
      <template v-if="!folded.has(g.name)">
        <tr v-for="s in g.list" :key="s.nick" class="student" :class="rowClass(s)" :title="s.seen ? null : 'Ще не заходив на сайт'">
          <td>
            <RouterLink :to="`/students/${s.nick}/edit`" class="name">{{ fio(s) }}</RouterLink>
            <span v-if="s.status === 'admin'" class="badge text-bg-secondary fw-normal ms-1">викладач</span>
            <span v-else-if="s.status === 'pending'" class="badge text-bg-warning fw-normal ms-1">очікує</span>
            <div class="email small">{{ s.email }}</div>
          </td>
          <td v-if="s.game.id"><RouterLink :to="`/students/${s.nick}`">{{ s.game.title }}</RouterLink></td>
          <td v-else class="dash">—</td>
          <td v-if="s.github"><a :href="s.github" target="_blank">{{ repoName(s.github) }}</a></td>
          <td v-else class="dash">—</td>
          <td v-if="s.tg_username || s.tg_linked">
            <a v-if="s.tg_username" :href="`https://t.me/${s.tg_username}`" target="_blank">@{{ s.tg_username }}</a>
            <i v-else class="text-body-tertiary">без нікнейма</i>
            <span v-if="!s.tg_linked" title="Бот не привʼязаний"> 🚫</span>
          </td>
          <td v-else-if="s.seen" class="dash"><span title="Бот не привʼязаний">🚫</span></td>
          <td v-else class="dash">—</td>
        </tr>
      </template>
    </tbody>
  </table>
</template>

<style scoped>
/* room on the left for the row numbers, which sit outside the table */
table { width: calc(100% - 1.5rem); margin-left: 1.5rem; }
td, th { padding: .3rem .5rem; }
tbody { counter-reset: n; }
.student td:first-child { position: relative; }
.student td:first-child::before { counter-increment: n; content: counter(n); position: absolute; right: 100%; top: .3rem;
                                  margin-right: .5rem; line-height: 1.5rem; font-size: .75rem; color: var(--bs-tertiary-color); }
.caret { display: inline-block; width: 1rem; }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
.name { color: inherit; text-decoration: none; }
.name:hover { text-decoration: underline; }
.email { color: var(--bs-tertiary-color); line-height: 1.2; }
.dash { text-align: center; color: var(--bs-tertiary-color); }
/* the cell colour is Bootstrap's own variable, plain `color` on the row would not reach it */
.ghost { --bs-table-color: var(--bs-tertiary-color); }
.ghost .name, .ghost a { color: inherit; }
</style>
