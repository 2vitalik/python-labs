<script setup>
import { computed, ref } from 'vue'

import { STATES, fmtWhen, labName, labPath } from '../labs.js'
import { byGroup } from '../studentFilter.js'
import Avatar from './Avatar.vue'
import IconChevron from './IconChevron.vue'
import LabCell from './LabCell.vue'
import LabEdit from './LabEdit.vue'

// students × labs (T235): a header row per group folds it; a cell opens the editor of that pair under the student's row;
// ✏️ in a lab's header asks the page for the deadline form; 🐙 — the repository as the last pull saw it
const props = defineProps({ data: { type: Object, required: true } })
const emit = defineEmits(['deadline', 'cell'])
const labs = computed(() => props.data.labs)
const groups = computed(() => byGroup(props.data.rows))
const folded = ref(new Set())
const picked = ref(null)  // {nick, lab}
const toggle = (name) => (folded.value.has(name) ? folded.value.delete(name) : folded.value.add(name))
const pick = (nick, lab) => (picked.value = picked.value?.nick === nick && picked.value.lab === lab ? null : { nick, lab })
const isPicked = (nick, lab) => picked.value?.nick === nick && picked.value.lab === lab
const due = (l) => l.deadlines.find((d) => !d.groups.length)
const dueTitle = (l) => l.deadlines.map((d) => `${fmtWhen(d.at)} · ${d.groups.join(', ') || 'для всіх'}`).join('\n') || 'дедлайн не заданий'
const repoTitle = (r) => (r.repo ? [r.repo.url, r.repo.ok ? `${r.repo.commits} комітів · ${r.repo.branch}` : r.repo.error,
  r.repo.last ? `останній ${fmtWhen(r.repo.last)}` : '', `pull ${fmtWhen(r.repo.pulled_at)}`].filter(Boolean).join('\n') : r.github ? `${r.github}\nще не клоновано` : 'посилання нема')
const repoMark = (r) => (!r.github ? '—' : !r.repo ? '🐙' : r.repo.ok ? '🐙' : '⚠️')
const total = (l) => Object.entries(STATES).filter(([k]) => k !== 'nodue')
  .map(([k, s]) => [s.emoji, props.data.rows.filter((r) => r.cells[l.n].state === k).length]).filter(([, n]) => n)
</script>

<template>
  <div class="wrap border rounded">
    <table class="table table-sm align-middle mb-0">
      <thead>
        <tr>
          <th class="name">Студент</th>
          <th class="repo" title="Репозиторій">🐙</th>
          <th v-for="l in labs" :key="l.n" class="lab" :title="dueTitle(l)">
            <RouterLink v-if="labPath(l.n)" :to="labPath(l.n)">{{ labName(l.n) }}</RouterLink><template v-else>{{ labName(l.n) }}</template>
            <a href="#" class="ibtn ms-1" title="Дедлайн" @click.prevent="emit('deadline', l.n)">✏️</a>
            <small class="d-block fw-normal text-secondary">{{ due(l) ? fmtWhen(due(l).at) : l.deadlines.length ? 'по групах' : '—' }}<template v-if="due(l) && l.deadlines.length > 1"> +</template></small>
          </th>
        </tr>
      </thead>
      <tbody v-for="g in groups" :key="g.name">
        <tr class="table-light" role="button" @click="toggle(g.name)">
          <th class="name"><IconChevron :dir="folded.has(g.name) ? 'right' : 'down'" :size="12" class="text-secondary" /> {{ g.name || 'Без групи' }} <span class="count">{{ g.list.length }}</span></th>
          <td :colspan="labs.length + 1"></td>
        </tr>
        <template v-if="!folded.has(g.name)">
          <template v-for="r in g.list" :key="r.nick">
            <tr>
              <th class="name fw-normal"><Avatar :user="r" :size="20" /> <RouterLink :to="`/students/${r.nick}/edit`">{{ r.name || r.nick }}</RouterLink></th>
              <td class="repo" :title="repoTitle(r)"><a v-if="r.github" :href="r.github" target="_blank" class="text-decoration-none">{{ repoMark(r) }}</a><span v-else class="text-body-tertiary">—</span></td>
              <td v-for="l in labs" :key="l.n" class="cell"><LabCell :cell="r.cells[l.n]" :name="r.name || r.nick" :lab="l.n" :active="isPicked(r.nick, l.n)" @click="pick(r.nick, l.n)" /></td>
            </tr>
            <tr v-if="picked?.nick === r.nick">
              <td :colspan="labs.length + 2" class="p-2 editor">
                <LabEdit :key="picked.lab" :nick="r.nick" :lab="picked.lab" :cell="r.cells[picked.lab]" @saved="emit('cell', r.nick, picked.lab, $event)" @close="picked = null" />
              </td>
            </tr>
          </template>
        </template>
      </tbody>
      <tfoot>
        <tr>
          <th class="name fw-normal text-secondary">Разом</th>
          <td></td>
          <td v-for="l in labs" :key="l.n" class="sum"><span v-for="[e, n] in total(l)" :key="e" class="me-1">{{ e }}{{ n }}</span></td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<style scoped>
.wrap { overflow-x: auto; }
th, td { white-space: nowrap; }
.editor { white-space: normal; max-width: 0; }  /* the editor wraps inside the table's width instead of stretching it */
.name { position: sticky; left: 0; z-index: 1; min-width: 12rem; max-width: 18rem; overflow: hidden; text-overflow: ellipsis; }
.name a, .lab a { color: inherit; text-decoration: none; }
.name a:hover, .lab a:hover { text-decoration: underline; }
.lab { min-width: 5rem; text-align: center; font-size: .85rem; line-height: 1.2; vertical-align: bottom; }
.repo { text-align: center; width: 2rem; }
.cell { padding: .1rem; text-align: center; }
.sum { text-align: center; color: var(--bs-secondary-color); font-size: .8rem; white-space: normal; }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
@media (max-width: 576px) { .name { min-width: 8rem; max-width: 10rem; } }
</style>
