import { fmtWhen } from './labs.js'

// how a cell of each column type reads, filters, sorts, groups and sums (T240); the columns themselves — tableCols.js
const EMPTY = '·'
const has = (v) => v !== null && v !== undefined && v !== '' && v !== false && !(Array.isArray(v) && !v.length)
const list = (v) => (Array.isArray(v) ? v.map(String) : has(v) ? [String(v)] : [])
const opt = (col, id) => col.options?.[id] || { emoji: '', text: String(id) }
const label = (o) => [o.emoji, o.text].filter(Boolean).join(' ')
const number = (v) => (has(v) && !Number.isNaN(Number(v)) ? Number(v) : null)

// what the cell shows: the text, a colour, a line under it, the hover
export function view(col, row) {
  const v = col.get(row)
  const hint = [col.title, col.hint?.(row)].filter(Boolean)
  const out = { text: EMPTY, cls: 'none', sub: col.sub?.(row) || '', link: col.link?.(row) || '', title: '' }
  if (col.type === 'bool') Object.assign(out, v === true ? { text: '✅', cls: 'yes' } : {})
  else if (col.type === 'link' && has(v)) Object.assign(out, { text: col.short, cls: 'yes', link: v })
  else if (['enum', 'lab', 'poll', 'multi'].includes(col.type) && list(v).length) {
    const picked = list(v).map((id) => opt(col, id))
    Object.assign(out, { text: picked.map((o) => o.emoji || o.text).join(' '), cls: picked.length === 1 && picked[0].color ? `tone-${picked[0].color}` : 'some' })
    hint.push(...picked.map(label))
    if (col.doubt) {  // a poll's answers the site cannot confirm are struck
      const doubt = col.doubt(row)
      out.parts = list(v).map((id) => ({ text: opt(col, id).emoji || opt(col, id).text, cls: doubt.includes(id) ? 'doubt' : '' }))
      if (doubt.length) hint.push(`⚖️ сайт не бачить: ${doubt.map((id) => opt(col, id).emoji).join(' ')}`)
    }
  } else if (col.type === 'number' && has(v)) Object.assign(out, { text: String(v), cls: Number(v) ? 'num' : 'zero' })
  else if (col.type === 'date' && has(v)) Object.assign(out, { text: fmtWhen(v, true), cls: 'some' }) && hint.push(fmtWhen(v))
  else if (col.type === 'text' && has(v)) Object.assign(out, { text: String(v), cls: 'some' }) && hint.push(String(v))
  if (col.type === 'bool' && col.sub && out.sub) hint.push(out.sub)
  out.title = hint.join('\n')
  return out
}

// the filter of a column, as the URL writes it: bool/link/date 1|0 · enum/lab/poll/multi ids, «-» = empty · number 3-5 3- -5 >3 <3 3 · text a substring
export function passes(col, row, spec) {
  const v = col.get(row)
  if (!spec) return true
  switch (col.type) {
    case 'bool': case 'link': return has(v) === (spec === '1')
    case 'date': return spec === '1' || spec === '0' ? has(v) === (spec === '1') : has(v) && (spec[0] === '>' ? v >= spec.slice(1) : v <= spec.slice(1))
    case 'number': {
      const n = number(v)
      if (spec === '-') return n === null
      if (n === null) return false
      const m = spec.match(/^(\d*\.?\d*)-(\d*\.?\d*)$/)  // a-b · a- · -b: inclusive
      if (m && (m[1] || m[2])) return (!m[1] || n >= Number(m[1])) && (!m[2] || n <= Number(m[2]))
      return spec[0] === '>' ? n > Number(spec.slice(1)) : spec[0] === '<' ? n < Number(spec.slice(1)) : n === Number(spec)
    }
    case 'text': return spec === '-' ? !has(v) : has(v) && String(v).toLowerCase().includes(spec.toLowerCase())
    default: {
      const want = spec.split(',')
      const got = list(v)
      return (want.includes('-') && !got.length) || got.some((id) => want.includes(id))
    }
  }
}

// a key to sort by; empty cells go last whichever way
export function sortKey(col, row) {
  const v = col.get(row)
  if (!has(v)) return null
  if (col.type === 'number') return number(v)
  if (['enum', 'lab', 'poll', 'multi'].includes(col.type)) return Math.min(...list(v).map((id) => Object.keys(col.options || {}).indexOf(id)).map((i) => (i < 0 ? 999 : i)))
  if (col.type === 'bool' || col.type === 'link') return 0
  return String(v).toLowerCase()
}
export function compare(a, b) {
  if (a === null || b === null) return (a === null) - (b === null)
  return typeof a === 'number' && typeof b === 'number' ? a - b : String(a).localeCompare(String(b), 'uk')
}

// the group a row falls in by a column: a label and a key to order the groups
export function groupOf(col, row) {
  const v = col.get(row)
  if (!has(v)) return { key: null, text: col.type === 'bool' ? `${col.short} ні` : 'порожньо' }
  if (col.type === 'bool' || col.type === 'link') return { key: 0, text: `${col.short} так` }
  if (['enum', 'lab', 'poll', 'multi'].includes(col.type)) return { key: sortKey(col, row), text: list(v).map((id) => label(opt(col, id))).join(', ') }
  if (col.type === 'date') return { key: String(v).slice(0, 7), text: new Date(v).toLocaleDateString('uk-UA', { month: 'long', year: 'numeric' }) }
  return { key: sortKey(col, row), text: String(v) }
}

// the «Разом» cell: how many ✅, a count per answer, a sum
export function total(col, rows) {
  const vs = rows.map((r) => col.get(r))
  if (col.type === 'number') return String(vs.reduce((s, v) => s + (number(v) || 0), 0))
  if (['enum', 'lab', 'poll', 'multi'].includes(col.type)) {
    const n = {}
    for (const v of vs) for (const id of list(v)) n[id] = (n[id] || 0) + 1
    return Object.keys(col.options || {}).filter((id) => n[id]).map((id) => `${opt(col, id).emoji || id}${n[id]}`).join(' ')
  }
  return String(vs.filter(has).length)
}
export const optionLabel = label
export const hasValue = has
