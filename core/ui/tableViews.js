import { labName } from './labs.js'

// the views of /table (T240): a view = columns + grouping + sort + filters, carried by the URL exactly as a saved one carries its `query`.
// Built-in views name columns by key, or by a family that grows on its own: polls:lab1 — polls tagged lab1 · fields:lab1 — own fields on lab 1 · fields: — on students
const LAB = (n) => [`seen`, `bot`, `gh`, `repo`, `commits`, `lab${n}`, `lab${n}.before`, `lab${n}.after`, `lab${n}.last`, `lab${n}.due`, `lab${n}.asked`,
  `lab${n}.ext`, `lab${n}.met`, `lab${n}.note`, `polls:lab${n}`, `fields:lab${n}`]
export const builtIn = (labs) => [
  { slug: 'all', title: 'Усе', emoji: '📋', query: { cols: ['fio', 'seen', 'bot', 'tg', 'gh', 'repo', 'commits', ...labs.map((n) => `lab${n}`), 'fields:'].join(), group: 'group' } },
  { slug: 'start', title: 'Старт', emoji: '🚀', query: { cols: 'fio,seen,last,bot,tg,gh,repo,commits,lastc,polls:start', group: 'group' } },
  ...labs.map((n) => ({ slug: `lab${n}`, title: labName(n), emoji: '📅', query: { cols: LAB(n).join(), group: 'group' } })),
]

// «lab1», «Лаба 1», «л1», «дедлайн 1» → lab1: a poll's tag names the lab its answers are about
export const labTag = (t) => {
  const m = String(t).toLowerCase().replace(/\s+/g, '').match(/^(?:lab|l|лаба|лаб|л|дедлайн|deadline|дл)(\d+)$/)
  return m ? `lab${m[1]}` : ''
}
export const normTag = (t) => labTag(t) || String(t).toLowerCase().trim()

// a view's column list → the keys that exist now; a family token opens into its members
export function resolve(keys, cols) {
  const out = []
  for (const k of keys) {
    if (k.startsWith('polls:')) out.push(...cols.filter((c) => c.poll && (!k.slice(6) || c.tags.some((t) => normTag(t) === k.slice(6)))).map((c) => c.key))
    else if (k.startsWith('fields:')) out.push(...cols.filter((c) => c.own && (c.lab || 0) === (Number(k.slice(7).replace(/\D/g, '')) || 0)).map((c) => c.key))  // fields:lab2 → lab 2
    else if (cols.some((c) => c.key === k)) out.push(k)
  }
  return [...new Set(out)]
}

export const split = (s) => String(s || '').split(',').filter(Boolean)
export const filtersOf = (q) => Object.fromEntries(Object.entries(q).filter(([k, v]) => k.startsWith('f.') && v !== undefined && v !== '').map(([k, v]) => [k.slice(2), String(v)]))

// the state out of the URL: a URL with `cols` says it all; one without takes the view's query and lays its own group/sort/q/filters over it
export function readState(query, view) {
  const base = view?.query || {}
  const own = 'cols' in query
  const filters = own || Object.keys(filtersOf(query)).length ? filtersOf(query) : filtersOf(base)
  const pick = (k) => (query[k] !== undefined ? String(query[k]) : base[k])
  return { cols: split(own ? query.cols : base.cols), group: pick('group') ?? 'group', sort: pick('sort') || '', q: String(query.q || ''), filters }
}

export function toQuery(state, view) {
  const f = Object.fromEntries(Object.entries(state.filters).map(([k, v]) => [`f.${k}`, v]))
  return { view, cols: state.cols.join(), group: state.group || '-', sort: state.sort || undefined, q: state.q || undefined, ...f }
}

// what a view keeps: the same shape the URL has, less the search
export const toSaved = (state) => Object.fromEntries(Object.entries(toQuery(state)).filter(([k, v]) => k !== 'view' && k !== 'q' && v !== undefined))
const norm = (q) => JSON.stringify(Object.entries(q).filter(([, v]) => v !== undefined && v !== '').sort())
export const changed = (state, view, cols) => norm({ ...toSaved(state), cols: resolve(state.cols, cols).join() })
  !== norm({ ...view.query, cols: resolve(split(view.query.cols), cols).join(), group: view.query.group || '-' })
