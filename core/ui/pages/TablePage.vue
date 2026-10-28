<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getTable, putFieldValue, putStudentLab } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import FieldsPanel from '../components/FieldsPanel.vue'
import IconArrows from '../components/IconArrows.vue'
import TableCols from '../components/TableCols.vue'
import TableGrid from '../components/TableGrid.vue'
import TableViews from '../components/TableViews.vue'
import { matches } from '../studentSearch.js'
import { compare, hasValue, passes, sortKey } from '../table.js'
import { columns } from '../tableCols.js'
import { builtIn, changed, readState, resolve, toQuery } from '../tableViews.js'
import { useTitle } from '../title.js'
import { toggleWide, wide } from '../wide.js'

// the table of students (T240): one page, many views. The state lives in the URL (tableViews.js); a view is a name for one
const route = useRoute()
const router = useRouter()
const data = ref(null)
const error = ref('')
const panel = ref('')  // cols · fields · ''
const cols = computed(() => (data.value ? columns(data.value) : []))
const byKey = computed(() => Object.fromEntries(cols.value.map((c) => [c.key, c])))
const views = computed(() => (data.value ? [...builtIn(data.value.labs.map((l) => l.n)), ...data.value.views] : []))
const slug = computed(() => String(route.query.view || 'all'))
const view = computed(() => views.value.find((v) => v.slug === slug.value) || views.value[0])
const state = computed(() => view.value && readState(route.query, view.value))
const shownCols = computed(() => (state.value ? resolve(state.value.cols, cols.value).map((k) => byKey.value[k]) : []))
const groupCol = computed(() => (state.value && state.value.group !== '-' && byKey.value[state.value.group]) || null)
const sortCol = computed(() => state.value && byKey.value[state.value.sort.replace(/^-/, '')])
const dirty = computed(() => !!(state.value && view.value && changed(state.value, view.value, cols.value)))
const groupable = computed(() => cols.value.filter((c) => c.key === 'group' || ['bool', 'link', 'enum', 'lab', 'poll', 'multi'].includes(c.type)))
// quick chips (T246): a shown yes/no or choice column → one click keeps the rows that have something there, with a count
const quick = computed(() => shownCols.value.filter((c) => ['bool', 'link', 'enum'].includes(c.type)))
const quickSpec = (c) => (c.type === 'enum' ? Object.keys(c.options || {}).join() : '1')
const quickOn = (c) => state.value.filters[c.key] === quickSpec(c)
const quickCount = (c) => data.value.rows.filter((r) => matches(r, state.value.q) && hasValue(c.get(r))
  && Object.entries(state.value.filters).every(([k, spec]) => k === c.key || !byKey.value[k] || passes(byKey.value[k], r, spec))).length
const chip = (on) => (on ? 'btn-secondary' : 'btn-outline-secondary')
useTitle(() => view.value && `Таблиця · ${view.value.title}`)

const rows = computed(() => {
  if (!data.value || !state.value) return []
  const list = data.value.rows.filter((r) => matches(r, state.value.q)
    && Object.entries(state.value.filters).every(([k, spec]) => !byKey.value[k] || passes(byKey.value[k], r, spec)))
  if (!sortCol.value) return list
  const dir = state.value.sort.startsWith('-') ? -1 : 1
  return [...list].sort((a, b) => {
    const ka = sortKey(sortCol.value, a)
    const kb = sortKey(sortCol.value, b)
    if (ka === null || kb === null) return (ka === null) - (kb === null)  // empty cells last, whichever way
    return dir * compare(ka, kb) || compare(a.name, b.name)
  })
})

const set = (patch) => router.replace({ query: toQuery({ ...state.value, ...patch }, slug.value) })
const setFilter = (key, spec) => set({ filters: { ...state.value.filters, [key]: spec || undefined } })
const setSort = (key) => set({ sort: state.value.sort === key ? `-${key}` : state.value.sort === `-${key}` ? '' : key })
const flipQuick = (c) => setFilter(c.key, quickOn(c) ? '' : quickSpec(c))
const pickView = (s) => router.replace({ query: { view: s } })
const filterText = (col, spec) => (col.type === 'bool' || col.type === 'link' ? (spec === '1' ? 'так' : 'ні')
  : col.options && spec === Object.keys(col.options).join() ? 'є'
  : col.options ? spec.split(',').map((id) => (id === '-' ? '∅' : col.options[id]?.emoji || col.options[id]?.text || id)).join(' ') : spec)

async function load() {
  try {
    data.value = await getTable()
  } catch (e) {
    error.value = e.message
  }
}
// a cell edited: the row takes what the API answers, nothing else reloads
async function save(col, row, value) {
  if (col.edit === 'field') {
    const r = await putFieldValue(row.nick, col.field.key, { value, lab: col.lab || 0 })
    if (r.value === null) delete row.fields[r.column]
    else row.fields[r.column] = r.value
  } else if (col.edit === 'mark') {
    row.labs[col.lab] = await putStudentLab(row.nick, col.lab, { [col.field]: value ?? (col.type === 'bool' ? false : '') })  // a mark's text is '' when cleared
  }
}
onMounted(load)
</script>

<template>
  <div>
    <Crumbs :items="[['/students', 'Студенти'], 'Таблиця']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
      <h1 class="h3 mb-0">Таблиця</h1>
      <span v-if="data" class="text-secondary">{{ rows.length }}<template v-if="rows.length !== data.rows.length"> з {{ data.rows.length }}</template></span>
      <input v-if="state" type="search" :value="state.q" class="form-control form-control-sm w-auto ms-auto" placeholder="Пошук: ПІБ, нік…"
             title="За початком слова: прізвище, імʼя, нік, Telegram" @input="set({ q: $event.target.value })">
      <button type="button" class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center px-2" :class="{ 'ms-auto': !state }"
              :title="wide ? 'Назад у колонку сторінки' : 'Таблиця на всю ширину'" @click="toggleWide"><IconArrows :out="!wide" /></button>
    </div>
    <TableViews v-if="state" :views :slug :dirty :state @pick="pickView" @saved="data.views = $event" />
    <div v-if="state" class="d-flex flex-wrap align-items-center gap-2 mb-2 small">
      <button type="button" class="btn btn-sm" :class="panel === 'cols' ? 'btn-secondary' : 'btn-outline-secondary'" @click="panel = panel === 'cols' ? '' : 'cols'">
        ▦ Колонки <span class="count">{{ shownCols.length }}</span></button>
      <label class="d-flex align-items-center gap-1">Групи:
        <select class="form-select form-select-sm w-auto" :value="state.group" @change="set({ group: $event.target.value })">
          <option value="-">без груп</option>
          <option v-for="c in groupable" :key="c.key" :value="c.key">{{ c.short === c.title ? c.title : `${c.short} ${c.title}` }}</option>
        </select>
      </label>
      <button type="button" class="btn btn-sm" :class="panel === 'fields' ? 'btn-secondary' : 'btn-outline-secondary'" @click="panel = panel === 'fields' ? '' : 'fields'">
        ⚙️ Мої поля <span class="count">{{ data.fields.length }}</span></button>
      <template v-for="(spec, key) in state.filters" :key="key">
        <span v-if="byKey[key]" class="badge rounded-pill text-bg-light border fw-normal" :title="byKey[key].title">{{ byKey[key].short }} {{ filterText(byKey[key], spec) }}
          <a href="#" class="text-reset text-decoration-none ms-1" title="Прибрати фільтр" @click.prevent="setFilter(key, '')">✕</a></span>
      </template>
      <a v-if="dirty" href="#" class="text-secondary" @click.prevent="pickView(slug)">скинути до виду</a>
    </div>
    <div v-if="quick.length" class="d-flex flex-wrap align-items-center gap-1 mb-2">
      <button v-for="c in quick" :key="c.key" type="button" class="btn btn-sm chip" :class="chip(quickOn(c))"
              :title="`${c.title}: ${quickOn(c) ? 'зняти фільтр' : 'лише ті, у кого є'}`" @click="flipQuick(c)">{{ c.short }} {{ quickCount(c) }}</button>
    </div>
    <TableCols v-if="panel === 'cols'" :cols :picked="shownCols.map((c) => c.key)" @change="set({ cols: $event })" @close="panel = ''" />
    <FieldsPanel v-if="panel === 'fields'" :fields="data.fields" @changed="load" @close="panel = ''" />
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <TableGrid v-if="state" :rows :cols="shownCols" :group="groupCol" :sort="state.sort" :filters="state.filters" @sort="setSort" @filter="setFilter" @save="save" />
    <p v-if="state" class="small text-secondary mt-2">
      Чіпи над таблицею — швидкий фільтр «у кого є» по колонці, з лічильником. Заголовок колонки: клік — сортування, ▾ — фільтр, наведи — що це. Клітинки з рамкою при наведенні редагуються: 🙋 і свої поля — кліком, стан лаби — редактором під рядком.
      Голоси беруться з опитувань щоразу живими; факти репозиторіїв — з останнього <code>bin/repos pull</code> → <code>push</code>.
    </p>
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; font-size: .85em; }
</style>
