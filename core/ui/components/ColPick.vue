<script>
// the sections of the column catalog in their order: the profile, the repo, the lab, the polls, the site's own pages, one's
// own columns last — the catalog of «Колонки» shows them the same way
const FIRST = ['Профіль', 'Репозиторій', 'Лаба', 'Опитування']
const rank = (cat) => (FIRST.includes(cat) ? FIRST.indexOf(cat) : cat === 'Свої' ? 9 : 5)
export function bySection(cols) {
  const out = new Map()
  for (const c of cols) out.set(c.cat, [...(out.get(c.cat) || []), c])
  return [...out].map(([cat, list]) => ({ cat, cols: list })).sort((a, b) => rank(a.cat) - rank(b.cat))
}
export const hit = (c, q) => [c.name, c.title, c.short].some((s) => String(s || '').toLowerCase().includes(q.trim().toLowerCase()))
</script>

<script setup>
import { computed, onMounted, ref } from 'vue'

import { useTable } from '../tableCtx.js'
import { rel } from '../tableViews.js'
import SetupName from './SetupName.vue'

// one column picked out of all («＋ фільтр», «＋ рівень», «＋ ще за…»): a search, then the columns the view shows, then the
// rest by sections — a lab's columns only for «this lab», by their relative id. Enter takes the first. `only` — which
// columns will do; `skip` — the ids already taken
const props = defineProps({ only: Function, skip: { type: Array, default: () => [] } })
const emit = defineEmits(['pick'])
const t = useTable()
const q = ref('')
const find = ref()
const taken = computed(() => new Set(props.skip.map((id) => t.col(id)?.key)))
const ok = (c) => (!props.only || props.only(c)) && !taken.value.has(c.key) && hit(c, q.value)
const inView = computed(() => t.shown.filter(ok))
const rest = computed(() => {
  const seen = new Set(t.shown.map((c) => c.key))
  return bySection(t.cols.filter((c) => !seen.has(c.key) && (!c.lab || c.lab === t.state.lab) && ok(c))
    .map((c) => ({ ...c, id: c.lab ? rel(c.key, c.lab) : c.key })))
})
const first = () => inView.value[0] || rest.value[0]?.cols[0]
const enter = () => first() && emit('pick', first())
onMounted(() => find.value?.focus({ preventScroll: true }))
</script>

<template>
  <div>
    <input ref="find" v-model="q" type="search" class="form-control form-control-sm" placeholder="Знайти колонку" @keydown.enter.prevent="enter">
    <div class="cp-list">
      <template v-if="inView.length">
        <div class="cp-cap">у виді</div>
        <button v-for="c in inView" :key="c.key" type="button" class="cp-row" @click="emit('pick', c)"><SetupName :col="c" /></button>
      </template>
      <template v-for="s in rest" :key="s.cat">
        <div class="cp-cap">{{ s.cat }}</div>
        <button v-for="c in s.cols" :key="c.key" type="button" class="cp-row" @click="emit('pick', c)"><SetupName :col="c" /></button>
      </template>
      <div v-if="!inView.length && !rest.length" class="small text-secondary p-1">Нічого не знайдено</div>
    </div>
  </div>
</template>

<style scoped>
.cp-list { max-height: 15rem; margin-top: .3rem; overflow-y: auto; }
.cp-cap { margin: .4rem .35rem .1rem; font-size: .66rem; font-weight: 600; letter-spacing: .05em; text-transform: uppercase; color: var(--bs-secondary-color); }
.cp-row { display: flex; width: 100%; min-width: 0; padding: .15rem .35rem; border: 0; border-radius: .3rem; background: none; color: inherit; font-size: .82rem; text-align: start; }
.cp-row:hover, .cp-row:focus-visible { background: var(--bs-tertiary-bg); }
</style>
