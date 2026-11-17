import { computed, inject, provide, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { matches } from './studentSearch.js'
import { columns, nearestLab } from './tableCols.js'
import { changed } from './tableDiff.js'
import { editCell } from './tableEdit.js'
import { passes } from './tableFilter.js'
import { sorter } from './tableOrder.js'
import { viewActs } from './tableSave.js'
import { colOf, index, readState, rel, reorder, shown, sortOf, toQuery, usesLab, without } from './tableViews.js'
import { drafts } from './viewDrafts.js'
import { liveViews, load, setQuiet, store, versionsOf, viewOf } from './viewStore.js'

// everything the parts of /table share (T315 §12.4): the page makes it once — createTable() — and each part takes it with
// useTable(). The state lives in the URL; `set` and its kin write there, and all the rest follows
const KEY = Symbol('table')
export const useTable = () => inject(KEY)
const generic = (c) => (c.lab ? rel(c.key, c.lab) : c.key)  // a column whatever the lab: «другорядна» and «скільки видів» are said of it
const STATE = ['cols', 'group', 'sort', 'lab']
const says = (q) => STATE.some((k) => k in q) || Object.keys(q).some((k) => k.startsWith('f.'))  // the URL carries a state of its own

export function createTable() {
  const route = useRoute()
  const router = useRouter()
  const data = computed(() => store.data)
  const cols = computed(() => (data.value ? columns(data.value) : []))
  const byKey = computed(() => index(cols.value))
  const slug = computed(() => String(route.query.view || liveViews()[0]?.slug || 'all'))
  const view = computed(() => viewOf(slug.value))
  const peek = computed(() => (route.query.v ? versionsOf(slug.value).find((x) => x.n === Number(route.query.v)) : null))  // a past version looked at
  const fill = (s) => ({ ...s, lab: s.lab || (data.value ? nearestLab(data.value.labs) : 1) })
  // a bare ?view=… opens the view with what was changed on it and not saved (viewDrafts.js)
  const asked = computed(() => (route.query.v || says(route.query) || !drafts[slug.value] ? route.query : { ...drafts[slug.value], q: route.query.q }))
  const state = computed(() => fill(readState(asked.value, (peek.value || view.value)?.query)))
  const col = (id) => colOf(id, byKey.value, state.value.lab)
  const shownCols = computed(() => shown(state.value, cols.value))
  const groupCols = computed(() => state.value.group.map(col).filter(Boolean))
  const filters = computed(() => Object.entries(state.value.filters).map(([id, spec]) => ({ col: col(id), spec })).filter((f) => f.col))
  // the rows left by the search and the filters; `skip` — but for that column's own filter (what its totals count over)
  const pool = (skip = '') => (data.value?.rows || []).filter((r) => matches(r, state.value.q) && filters.value.every((f) => f.col.id === skip || passes(f.col, r, f.spec)))
  const rows = computed(() => {
    const levels = state.value.sort.map(sortOf).map((s) => ({ col: col(s.id), desc: s.desc })).filter((l) => l.col)
    return levels.length ? [...pool()].sort(sorter(levels)) : pool()
  })
  const dirty = computed(() => !!view.value && changed(state.value, view.value.query, cols.value))
  const quietSet = computed(() => new Set(data.value?.prefs.quiet || []))
  const usage = computed(() => {  // in how many live views each column stands
    const n = {}
    for (const v of liveViews()) for (const k of new Set(shown(fill(readState({}, v.query)), cols.value).map(generic))) n[k] = (n[k] || 0) + 1
    return n
  })

  // a version looked at stays in the address while the look is changed: the bar over the table keeps saying which it is
  const set = (patch) => router.replace({ query: { ...toQuery({ ...state.value, ...patch }, slug.value), v: route.query.v } })
  function sortBy(id, desc = false, add = false) {
    const level = (desc ? '-' : '') + id
    set({ sort: add ? [...state.value.sort.filter((s) => sortOf(s).id !== id), level] : [level] })
  }

  const t = reactive({
    data, cols, byKey, slug, view, peek, state, shown: shownCols, groupCols, filters, rows, dirty,
    usesLab: computed(() => usesLab(state.value)),
    ui: { panel: '', field: null },  // which panel of the setup line is open (lab · cols · filters · groups · sort), and the own field it edits
    col, pool, set, sortBy, edit: editCell, reload: load,
    ...viewActs({ route, router, slug, view, peek, state, dirty }),
    setCols: (list) => set({ cols: list }),
    hide: (id) => set({ cols: without(state.value, cols.value, id) }),
    move: (id, before) => set({ cols: reorder(state.value, cols.value, id, before) }),  // `before` — an id, '' — to the end
    setFilter: (id, spec) => set({ filters: { ...state.value.filters, [id]: spec || undefined } }),
    quiet: (c) => quietSet.value.has(generic(c)),
    toggleQuiet: (c) => setQuiet(quietSet.value.has(generic(c)) ? [...quietSet.value].filter((k) => k !== generic(c)) : [...quietSet.value, generic(c)]),
    used: (c) => usage.value[generic(c)] || 0,
  })
  provide(KEY, t)
  return t
}
