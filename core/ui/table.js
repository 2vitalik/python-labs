import { fmtWhen } from './labs.js'

// how a cell of each column type reads, filters, sorts, groups and sums (T240, T315); the columns themselves — tableCols.js
const EMPTY = '·'
const DAY = 864e5
const PICK = ['enum', 'lab', 'poll', 'multi']  // a cell holds answers out of a list
const has = (v) => v !== null && v !== undefined && v !== '' && v !== false && !(Array.isArray(v) && !v.length)
const list = (v) => (Array.isArray(v) ? v.map(String) : has(v) ? [String(v)] : [])
const opt = (col, id) => col.options?.[id] || { emoji: '', text: String(id) }
const label = (o) => [o.emoji, o.text].filter(Boolean).join(' ')
const number = (v) => (has(v) && !Number.isNaN(Number(v)) ? Number(v) : null)
export const yes = (col) => col.type === 'bool' || col.type === 'link'  // a cell says yes or nothing
export const picks = (col) => PICK.includes(col.type)
export const groupable = (col) => col.key === 'group' || yes(col) || picks(col) || col.type === 'date'  // rows may gather by it
const p2 = (n) => String(n).padStart(2, '0')
const localDay = (iso) => { const d = new Date(iso); return `${d.getFullYear()}-${p2(d.getMonth() + 1)}-${p2(d.getDate())}` }
export const dayMonth = (iso) => { const d = new Date(iso); return `${p2(d.getDate())}.${p2(d.getMonth() + 1)}` }  // «27.11»

// what the cell shows: the text, a colour, a line under it, the hover; a date goes as `at` — the cell draws it as a chip
export function view(col, row) {
  const v = col.get(row)
  const hint = [col.title, col.hint?.(row)].filter(Boolean)
  const sub = col.sub?.(row) || ''
  const when = typeof sub === 'object' ? sub : {}  // a line under the cell that is a date: { at, pre }
  const out = { text: EMPTY, cls: 'none', sub: typeof sub === 'string' ? sub : '', subAt: when.at || '', subPre: when.pre || '', link: col.link?.(row) || '', title: '' }
  if (col.type === 'bool') Object.assign(out, v === true ? { text: '✅', cls: 'yes' } : {})
  else if (col.type === 'link' && has(v)) Object.assign(out, { text: col.short, cls: 'yes', link: v })
  else if (picks(col) && list(v).length) {
    const picked = list(v).map((id) => opt(col, id))
    Object.assign(out, { text: picked.map((o) => o.emoji || o.text).join(' '), cls: picked.length === 1 && picked[0].color ? `tone-${picked[0].color}` : 'some' })
    hint.push(...picked.map(label))
    if (col.doubt) {  // a poll's answers the site cannot confirm are struck
      const doubt = col.doubt(row)
      out.parts = list(v).map((id) => ({ text: opt(col, id).emoji || opt(col, id).text, cls: doubt.includes(id) ? 'doubt' : '' }))
      if (doubt.length) hint.push(`⚖️ сайт не бачить: ${doubt.map((id) => opt(col, id).emoji).join(' ')}`)
    }
  } else if (col.type === 'number' && has(v)) Object.assign(out, { text: String(v), cls: Number(v) ? 'num' : 'zero' })
  else if (col.type === 'date' && has(v)) Object.assign(out, { text: dayMonth(v), at: v, cls: 'some' }) && hint.push(fmtWhen(v))
  else if (col.type === 'text' && has(v)) Object.assign(out, { text: String(v), cls: 'some' }) && hint.push(String(v))
  if (out.sub) hint.push(out.sub)
  out.title = hint.join('\n')
  return out
}

// a column's filter, as the URL writes it (T315 §12.1): + has a value · - empty, for every type; bool/link 1|0 · answers: ids,
// «-» among them = empty · number 3-5 3- -5 >3 <3 3 · text a substring · date >day <day ~N (the last N days) ^N (older)
export function passes(col, row, spec) {
  const v = col.get(row)
  if (!spec) return true
  if (spec === '+' || spec === '-') return has(v) === (spec === '+')
  if (yes(col)) return has(v) === (spec === '1')
  if (col.type === 'date') {
    if (spec === '1' || spec === '0') return has(v) === (spec === '1')
    if (!has(v)) return false
    const days = (Date.now() - new Date(v)) / DAY
    return spec[0] === '~' ? days <= Number(spec.slice(1)) : spec[0] === '^' ? days > Number(spec.slice(1))
      : spec[0] === '>' ? localDay(v) >= spec.slice(1) : localDay(v) <= spec.slice(1)
  }
  if (col.type === 'number') {
    const n = number(v)
    if (n === null) return false
    const m = spec.match(/^(\d*\.?\d*)-(\d*\.?\d*)$/)  // a-b · a- · -b: inclusive
    if (m && (m[1] || m[2])) return (!m[1] || n >= Number(m[1])) && (!m[2] || n <= Number(m[2]))
    return spec[0] === '>' ? n > Number(spec.slice(1)) : spec[0] === '<' ? n < Number(spec.slice(1)) : n === Number(spec)
  }
  if (col.type === 'text') return has(v) && String(v).toLowerCase().includes(spec.toLowerCase())
  const want = spec.split(',')
  const got = list(v)
  return (want.includes('-') && !got.length) || got.some((id) => want.includes(id))
}

// the same filter in a word or two, for the line that says how the view is set
export function filterText(col, spec) {
  if (spec === '+') return 'є'
  if (spec === '-') return 'порожньо'
  if (yes(col) || (col.type === 'date' && (spec === '1' || spec === '0'))) return spec === '1' ? 'так' : 'ні'
  if (col.type === 'date') return { '~': `за ${spec.slice(1)} дн.`, '^': `давніше ${spec.slice(1)} дн.`, '>': `від ${dayMonth(spec.slice(1))}`, '<': `до ${dayMonth(spec.slice(1))}` }[spec[0]] || spec
  if (col.type === 'number') {
    const m = spec.match(/^(\d*\.?\d*)-(\d*\.?\d*)$/)
    return m && m[1] && m[2] ? `${m[1]}–${m[2]}` : m && m[1] ? `від ${m[1]}` : m && m[2] ? `до ${m[2]}` : spec.replace(/^([<>])/, '$1 ')
  }
  if (col.type === 'text') return `«${spec}»`
  return spec.split(',').map((id) => (id === '-' ? '∅' : opt(col, id).emoji || opt(col, id).text)).join(' ')
}

// a key to sort by; empty cells go last whichever way
export function sortKey(col, row) {
  const v = col.get(row)
  if (!has(v)) return null
  if (col.type === 'number') return number(v)
  if (picks(col)) return Math.min(...list(v).map((id) => Object.keys(col.options || {}).indexOf(id)).map((i) => (i < 0 ? 999 : i)))
  if (yes(col)) return 0
  return String(v).toLowerCase()
}
export function compare(a, b) {
  if (a === null || b === null) return (a === null) - (b === null)
  return typeof a === 'number' && typeof b === 'number' ? a - b : String(a).localeCompare(String(b), 'uk')
}
// rows by several columns at once: [{ col, desc }] — the first decides, the next breaks its ties, the name breaks the last
export const sorter = (levels) => (a, b) => {
  for (const { col, desc } of levels) {
    const ka = sortKey(col, a)
    const kb = sortKey(col, b)
    if (ka === null || kb === null) {
      if (ka !== kb) return (ka === null) - (kb === null)
      continue
    }
    const d = compare(ka, kb)
    if (d) return desc ? -d : d
  }
  return compare(a.name || '', b.name || '')
}

// the group a row falls in by a column: a label and a key to order the groups
export function groupOf(col, row) {
  const v = col.get(row)
  if (!has(v)) return { key: null, text: yes(col) ? `${col.short} ні` : `${col.short === col.title ? '' : `${col.short} `}порожньо` }
  if (yes(col)) return { key: 0, text: `${col.short} так` }
  if (picks(col)) return { key: sortKey(col, row), text: list(v).map((id) => label(opt(col, id))).join(', ') }
  if (col.type === 'date') return { key: String(v).slice(0, 7), text: new Date(v).toLocaleDateString('uk-UA', { month: 'long', year: 'numeric' }) }
  return { key: sortKey(col, row), text: String(v) }
}
// rows in groups inside groups, a level per column: [{ id, key, text, col, rows, kids }] — `kids` is null at the last level
export function groups(rows, cols, path = '') {
  if (!cols.length) return null
  const out = new Map()
  for (const r of rows) {
    const g = groupOf(cols[0], r)
    const id = `${path}/${g.key}`
    if (!out.has(id)) out.set(id, { ...g, id, col: cols[0], rows: [] })
    out.get(id).rows.push(r)
  }
  return [...out.values()].sort((a, b) => (a.key === null) - (b.key === null) || compare(a.key, b.key))
    .map((g) => ({ ...g, kids: groups(g.rows, cols.slice(1), g.id) }))
}

// what a column adds up to over some rows, as chips: { id, text, n } — `id` is the filter that keeps those rows («1» for
// a checkmark, an answer's id); a number sums and a text counts into a chip without an id
export function facets(col, rows) {
  const vs = rows.map((r) => col.get(r))
  if (col.type === 'number') return [{ id: '', text: 'Σ', n: Math.round(vs.reduce((s, v) => s + (number(v) || 0), 0) * 10) / 10 }]
  if (yes(col)) return [{ id: '1', text: '✅', n: vs.filter(has).length }]
  if (!picks(col)) return [{ id: '', text: '', n: vs.filter(has).length }]
  const n = {}
  for (const v of vs) for (const id of list(v)) n[id] = (n[id] || 0) + 1
  return Object.keys(col.options || {}).filter((id) => n[id]).map((id) => ({ id, text: opt(col, id).emoji || opt(col, id).text, n: n[id], title: opt(col, id).text }))
}
export const optionLabel = label
export const hasValue = has
