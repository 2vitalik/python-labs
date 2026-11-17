import { computed, inject, provide, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { putFieldValue, putStudentLab } from './api.js'
import { matches } from './studentSearch.js'
import { passes, sorter } from './table.js'
import { columns, nearestLab } from './tableCols.js'
import { changed, colOf, index, readState, rel, shown, sortOf, toQuery, toSaved, usesLab, without } from './tableViews.js'
import { dropDraft, drafts, setDraft } from './viewDrafts.js'
import { createView, liveViews, load, loadVersions, saveView, setQuiet, store, versionsOf, viewOf } from './viewStore.js'

// everything the parts of /table share (T315 §12.4): the page makes it once — createTable() — and each part takes it with
// useTable(). The state lives in the URL; `set` and its kin write there, and all the rest follows
const KEY = Symbol('table')
export const useTable = () => inject(KEY)
const generic = (c) => (c.lab ? rel(c.key, c.lab) : c.key)  // a column whatever the lab: «другорядна» and «скільки видів» are said of it

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
  const state = computed(() => fill(readState(route.query, (peek.value || view.value)?.query)))
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
    for (const v of liveViews()) for (const c of shown(fill(readState({}, v.query)), cols.value)) n[generic(c)] = (n[generic(c)] || 0) + 1
    return n
  })

  const set = (patch) => router.replace({ query: toQuery({ ...state.value, ...patch }, slug.value) })
  const ids = () => shownCols.value.map((c) => c.id)
  function sortBy(id, desc = false, add = false) {
    const level = (desc ? '-' : '') + id
    set({ sort: add ? [...state.value.sort.filter((s) => sortOf(s).id !== id), level] : [level] })
  }
  // another view: what was changed here and not saved waits in the browser, and comes back with the view
  function open(next) {
    if (dirty.value) setDraft(slug.value, toSaved(state.value))
    router.push({ query: { view: next, ...(drafts[next] || {}) } })
  }
  function reset() {
    dropDraft(slug.value)
    router.replace({ query: { view: slug.value } })
  }
  // from a past version back to the view as it is now — with what waits unsaved on it
  const unpeek = () => router.replace({ query: { view: slug.value, ...(drafts[slug.value] || {}) } })
  async function save(note = '') {
    await saveView(slug.value, { query: toSaved(state.value), ...(note ? { note } : {}) })
    reset()
  }
  // what is on screen becomes a view of its own, made from this one; this one is left as it was saved
  async function fork(body) {
    const from = view.value
    const v = await createView({ folder: from.folder, ...body, query: toSaved(state.value), parent: from.slug, parent_version: peek.value?.n || from.version })
    dropDraft(from.slug)
    router.push({ query: { view: v.slug } })
    return v
  }
  // a cell edited: the row takes what the API answers, nothing else reloads
  async function edit(c, row, value) {
    if (c.edit === 'field') {
      const r = await putFieldValue(row.nick, c.field.key, { value, lab: c.lab || 0 })
      if (r.value === null) delete row.fields[r.column]
      else row.fields[r.column] = r.value
    } else if (c.edit === 'mark') {
      row.labs[c.lab] = await putStudentLab(row.nick, c.lab, { [c.field]: value ?? (c.type === 'bool' ? false : '') })  // a mark's text is '' when cleared
    }
  }
  watch(() => route.query.v, (v) => v && !store.versions && loadVersions(), { immediate: true })

  const t = reactive({
    data, cols, byKey, slug, view, peek, state, shown: shownCols, groupCols, filters, rows, dirty,
    usesLab: computed(() => usesLab(state.value)),
    ui: { panel: '', field: null },  // which panel of the setup line is open (lab · cols · filters · groups · sort), and the own field it edits
    col, pool, set, open, reset, unpeek, save, fork, edit, sortBy, reload: load,
    setCols: (list) => set({ cols: list }),
    hide: (id) => set({ cols: without(state.value, cols.value, id) }),
    setFilter: (id, spec) => set({ filters: { ...state.value.filters, [id]: spec || undefined } }),
    quiet: (c) => quietSet.value.has(generic(c)),
    toggleQuiet: (c) => setQuiet(quietSet.value.has(generic(c)) ? [...quietSet.value].filter((k) => k !== generic(c)) : [...quietSet.value, generic(c)]),
    used: (c) => usage.value[generic(c)] || 0,
  })
  provide(KEY, t)
  return t
}
