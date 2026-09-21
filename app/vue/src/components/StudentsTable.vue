<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

// admin table: a header row per group folds it; «↗» shows that group alone (?group=, crumb on the page)
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
</script>

<template>
  <div v-if="groups.length > 1" class="small text-end mb-1">
    <a href="#" class="text-secondary" @click.prevent="foldAll(true)">згорнути всі</a> ·
    <a href="#" class="text-secondary" @click.prevent="foldAll(false)">розгорнути всі</a>
  </div>
  <table class="table table-hover align-middle">
    <thead>
      <tr><th>ПІБ</th><th>Гра</th><th>GitHub</th><th>Telegram</th><th>Статус</th></tr>
    </thead>
    <tbody v-for="g in groups" :key="g.name">
      <tr class="table-light" role="button" @click="toggle(g.name)">
        <th colspan="5" class="fw-semibold">
          <span class="caret text-secondary">{{ folded.has(g.name) ? '▸' : '▾' }}</span>
          {{ g.name || 'Без групи' }} <span class="count">{{ g.list.length }}</span>
          <RouterLink v-if="g.name && !route.query.group" :to="{ query: { group: g.name } }" class="ibtn ms-2"
                      title="Лише ця група" @click.stop>↗</RouterLink>
        </th>
      </tr>
      <template v-if="!folded.has(g.name)">
        <tr v-for="s in g.list" :key="s.nick" role="button" @click="$router.push(`/students/${s.nick}/edit`)">
          <td>{{ fio(s) }}<div class="text-secondary small">{{ s.email }}</div></td>
          <td>
            <RouterLink v-if="s.game.id" :to="`/students/${s.nick}`" @click.stop>{{ s.game.title }}</RouterLink>
            <span v-else class="text-secondary">—</span>
          </td>
          <td>
            <a v-if="s.github" :href="s.github" target="_blank" @click.stop>{{ repoName(s.github) }}</a>
            <span v-else class="text-secondary">—</span>
          </td>
          <td>
            <span v-if="s.tg_username">
              <a :href="`https://t.me/${s.tg_username}`" target="_blank" @click.stop>@{{ s.tg_username }}</a> <span v-if="s.tg_linked">✅</span>
            </span>
            <span v-else class="text-secondary">—</span>
          </td>
          <td><span class="badge" :class="s.status === 'student' ? 'text-bg-primary' : 'text-bg-secondary'">{{ s.status }}</span></td>
        </tr>
      </template>
    </tbody>
  </table>
</template>

<style scoped>
.caret { display: inline-block; width: 1rem; }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
</style>
