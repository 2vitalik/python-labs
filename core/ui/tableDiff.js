import { plural } from './plural.js'
import { filterText } from './table.js'
import { canon, colOf, index, sortOf } from './tableViews.js'

// a view in words, and what differs between two (T315 §7–§8): both read queries as tableViews.js canon() spells them
const count = (n) => `${n} ${plural(n, 'колонка', 'колонки', 'колонок')}`
const arrow = (s) => (sortOf(s).desc ? '↓' : '↑')
// how the ids of one query read: a column's mark, its full name, its filter in words
function reader(all, lab) {
  const byKey = index(all)
  const col = (id) => colOf(id, byKey, lab || 1)
  const mark = (id) => col(id)?.short || id
  return {
    mark,
    name: (id) => (col(id) && col(id).short !== col(id).name ? `${mark(id)} ${col(id).name}` : col(id)?.name || id),
    filter: (id, spec) => (col(id) ? `${mark(id)} ${filterText(col(id), spec)}` : `${id} ${spec}`),
    path: (ids) => ids.map(mark).join(' › '),
    sort: (list) => list.map((s) => `${mark(sortOf(s).id)} ${arrow(s)}`).join(', '),
  }
}

// what a view is made of, part by part: [{ what, text }] — «лаба 2», «14 колонок», «Група › 📅», «🤖 ні», «Σ ↓»
export function describe(query, all) {
  const q = canon(query, all)
  const r = reader(all, q.lab)
  return [
    q.lab ? { what: 'lab', text: `лаба ${q.lab}` } : null,
    { what: 'cols', text: count(q.cols.length) },
    q.group.length ? { what: 'group', text: r.path(q.group) } : null,
    Object.keys(q.filters).length ? { what: 'filters', text: Object.entries(q.filters).map(([id, spec]) => r.filter(id, spec)).join(', ') } : null,
    q.sort.length ? { what: 'sort', text: r.sort(q.sort) } : null,
  ].filter(Boolean)
}

// from query `a` to query `b`: `brief` — a few words for one line («＋2 колонки», «фільтр 🤖», «лаба 1 → 2»), `lines` —
// every change by name: { what, kind: add | del | chg | move, text }; `same` — nothing differs
export function diff(a, b, all) {
  const x = canon(a, all)
  const y = canon(b, all)
  const rx = reader(all, x.lab || y.lab)
  const ry = reader(all, y.lab || x.lab)
  const brief = []
  const lines = []
  const say = (what, kind, text) => lines.push({ what, kind, text })
  if (x.lab && y.lab && x.lab !== y.lab) brief.push(`лаба ${x.lab} → ${y.lab}`) && say('Лаба', 'chg', `${x.lab} → ${y.lab}`)
  const added = y.cols.filter((id) => !x.cols.includes(id))
  const gone = x.cols.filter((id) => !y.cols.includes(id))
  if (added.length) brief.push(`＋${count(added.length)}`)
  if (gone.length) brief.push(`−${count(gone.length)}`)
  added.forEach((id) => say('Колонки', 'add', ry.name(id)))
  gone.forEach((id) => say('Колонки', 'del', rx.name(id)))
  const kept = (list, other) => list.filter((id) => other.includes(id)).join()
  if (kept(x.cols, y.cols) !== kept(y.cols, x.cols)) brief.push('порядок колонок') && say('Колонки', 'move', 'інший порядок')
  if (x.group.join() !== y.group.join()) brief.push('групи') && say('Групи', 'chg', `${rx.path(x.group) || 'без груп'} → ${ry.path(y.group) || 'без груп'}`)
  if (x.sort.join() !== y.sort.join()) brief.push('сортування') && say('Сортування', 'chg', `${rx.sort(x.sort) || 'без сортування'} → ${ry.sort(y.sort) || 'без сортування'}`)
  const ids = [...new Set([...Object.keys(x.filters), ...Object.keys(y.filters)])].filter((id) => x.filters[id] !== y.filters[id])
  for (const id of ids) {
    if (!(id in x.filters)) say('Фільтри', 'add', ry.filter(id, y.filters[id]))
    else if (!(id in y.filters)) say('Фільтри', 'del', rx.filter(id, x.filters[id]))
    else say('Фільтри', 'chg', `${rx.filter(id, x.filters[id])} → ${ry.filter(id, y.filters[id])}`)
  }
  if (ids.length) brief.push(ids.length === 1 ? `фільтр ${ry.mark(ids[0])}` : `фільтри (${ids.length})`)
  return { brief, lines, same: !lines.length }
}
