// the state of a view of /table (T315 §12.1): columns, levels of grouping and sort, «this lab», filters — carried by the URL exactly
// as a saved view carries its `query`. A column's id may speak of «this lab»: lab · lab.before · f.<field>.lab · polls:lab ·
// fields:lab read with lab=N as labN · labN.before · f.<field>.N · polls:labN · fields:labN — one view serves every lab

// «lab1», «Лаба 1», «л1», «дедлайн 1» → lab1: a poll's tag names the lab its answers are about
export const labTag = (t) => {
  const m = String(t).toLowerCase().replace(/\s+/g, '').match(/^(?:lab|l|лаба|лаб|л|дедлайн|deadline|дл)(\d+)$/)
  return m ? `lab${m[1]}` : ''
}
export const normTag = (t) => labTag(t) || String(t).toLowerCase().trim()

export const abs = (id, lab) => (!lab ? id
  : id === 'lab' ? `lab${lab}`
  : id.startsWith('lab.') ? `lab${lab}${id.slice(3)}`
  : /^(polls|fields):lab$/.test(id) ? `${id}${lab}`
  : /^f\.[^.]+\.lab$/.test(id) ? `${id.slice(0, -3)}${lab}` : id)
export const isRel = (id) => abs(id, 1) !== id
// a column of lab N, said as «this lab»
export function rel(key, lab) {
  const n = String(lab)
  if (!lab) return key
  if (key === `lab${n}`) return 'lab'
  if (key.startsWith(`lab${n}.`)) return `lab${key.slice(3 + n.length)}`
  if (/^f\.[^.]+\.\d+$/.test(key) && key.endsWith(`.${n}`)) return `${key.slice(0, -n.length)}lab`
  return key
}

export const split = (s) => String(s || '').split(',').filter(Boolean)
export const sortOf = (s) => ({ id: s.replace(/^-/, ''), desc: s.startsWith('-') })
export const index = (cols) => Object.fromEntries(cols.map((c) => [c.key, c]))
// the column an id names now, wearing that id: the page sorts, filters and hides by it
export const colOf = (id, byKey, lab) => (byKey[abs(id, lab)] ? { ...byKey[abs(id, lab)], id } : undefined)

// a family grows on its own: polls:lab1 — polls tagged lab1 · fields:lab1 — own fields on lab 1 · fields: — on students
function open(id, cols, lab) {
  const a = abs(id, lab)
  if (a.startsWith('polls:')) return cols.filter((c) => c.poll && (!a.slice(6) || c.tags.some((t) => normTag(t) === a.slice(6)))).map((c) => c.key)
  if (!a.startsWith('fields:')) return [id]
  const n = Number(a.slice(7).replace(/\D/g, '')) || 0
  return cols.filter((c) => c.own && (c.lab || 0) === n).map((c) => (a === id ? c.key : rel(c.key, n)))
}
// the columns a state shows, families opened, each once
export function shown(state, cols) {
  const byKey = index(cols)
  const seen = new Set()
  return state.cols.flatMap((id) => open(id, cols, state.lab)).map((id) => colOf(id, byKey, state.lab))
    .filter((c) => c && !seen.has(c.key) && seen.add(c.key))
}

// the state's columns with one hidden: only the family it stood in opens, the others still grow on their own
export const without = (state, cols, id) => state.cols.flatMap((k) => {
  const ids = open(k, cols, state.lab)
  return ids.includes(id) ? ids.filter((x) => x !== id) : [k]
})

export const filtersOf = (q) => Object.fromEntries(Object.entries(q).filter(([k, v]) => k.startsWith('f.') && v !== undefined && v !== '').map(([k, v]) => [k.slice(2), String(v)]))

// the state out of the URL: a URL with `cols` says it all; one without takes the view's query and lays its own over it
export function readState(query, base = {}) {
  const own = 'cols' in query
  const filters = own || Object.keys(filtersOf(query)).length ? filtersOf(query) : filtersOf(base)
  const pick = (k) => (query[k] !== undefined ? String(query[k]) : base[k])
  const group = pick('group') ?? 'group'
  return { cols: split(own ? query.cols : base.cols), group: group === '-' ? [] : split(group), sort: split(pick('sort')),
           lab: Number(pick('lab')) || 0, q: String(query.q || ''), filters }
}

// does the state speak of «this lab» anywhere: only then its `lab` means something
export const usesLab = (s) => [...s.cols, ...s.group, ...s.sort.map((x) => sortOf(x).id), ...Object.keys(s.filters)].some(isRel)

export function toQuery(state, view) {
  const f = Object.fromEntries(Object.entries(state.filters).map(([k, v]) => [`f.${k}`, v]))
  return { view, cols: state.cols.join(), group: state.group.join() || '-', sort: state.sort.join() || undefined,
           lab: (usesLab(state) && state.lab) || undefined, q: state.q || undefined, ...f }
}
// what a view keeps: the same shape the URL has, less the view's name and the search
export const toSaved = (state) => Object.fromEntries(Object.entries(toQuery(state)).filter(([k, v]) => k !== 'view' && k !== 'q' && v !== undefined).map(([k, v]) => [k, String(v)]))

// a query in one spelling, to compare two (tableDiff.js): families opened, ids said for «this lab» wherever they are of it —
// so «Лаба 1» and its copy turned to lab 2 differ by the lab alone
export function canon(query, cols) {
  const s = readState({}, query)
  const say = (id) => rel(abs(id, s.lab), s.lab)
  const out = { cols: shown(s, cols).map((c) => say(c.id)), group: s.group.map(say), sort: s.sort.map((x) => (sortOf(x).desc ? '-' : '') + say(sortOf(x).id)),
                filters: Object.fromEntries(Object.entries(s.filters).map(([k, v]) => [say(k), v]).sort()) }
  return { ...out, lab: usesLab(out) ? s.lab : 0 }
}
export const changed = (state, query, cols) => JSON.stringify(canon(toSaved(state), cols)) !== JSON.stringify(canon(query, cols))
