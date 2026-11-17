import { fmtWhen } from './labs.js'

// how a cell of each column type reads and what a column adds up to (T240, T315); the filters — tableFilter.js, the order
// of rows and their groups — tableOrder.js, the columns themselves — tableCols.js
const EMPTY = '·'
const PICK = ['enum', 'lab', 'poll', 'multi']  // a cell holds answers out of a list
export const hasValue = (v) => v !== null && v !== undefined && v !== '' && v !== false && !(Array.isArray(v) && !v.length)
export const answers = (v) => (Array.isArray(v) ? v.map(String) : hasValue(v) ? [String(v)] : [])
export const option = (col, id) => col.options?.[id] || { emoji: '', text: String(id) }
export const optionLabel = (o) => [o.emoji, o.text].filter(Boolean).join(' ')
export const numberOf = (v) => (hasValue(v) && !Number.isNaN(Number(v)) ? Number(v) : null)
export const yes = (col) => col.type === 'bool' || col.type === 'link'  // a cell says yes or nothing
export const picks = (col) => PICK.includes(col.type)
export const groupable = (col) => col.key === 'group' || yes(col) || picks(col) || col.type === 'date'  // rows may gather by it
const p2 = (n) => String(n).padStart(2, '0')
export const dayMonth = (iso) => { const d = new Date(iso); return `${p2(d.getDate())}.${p2(d.getMonth() + 1)}` }  // «27.11»

// what the cell shows: the text, a colour, a line under it, the hover; a date goes as `at` — the cell draws it as a chip
export function view(col, row) {
  const v = col.get(row)
  const hint = [col.title, col.hint?.(row)].filter(Boolean)
  const sub = col.sub?.(row) || ''
  const when = typeof sub === 'object' ? sub : {}  // a line under the cell that is a date: { at, pre }
  const out = { text: EMPTY, cls: 'none', sub: typeof sub === 'string' ? sub : '', subAt: when.at || '', subPre: when.pre || '', link: col.link?.(row) || '', title: '' }
  if (col.type === 'bool') Object.assign(out, v === true ? { text: '✅', cls: 'yes' } : {})
  else if (col.type === 'link' && hasValue(v)) Object.assign(out, { text: col.short, cls: 'yes', link: v })
  else if (picks(col) && answers(v).length) {
    const picked = answers(v).map((id) => option(col, id))
    Object.assign(out, { text: picked.map((o) => o.emoji || o.text).join(' '), cls: picked.length === 1 && picked[0].color ? `tone-${picked[0].color}` : 'some' })
    hint.push(...picked.map(optionLabel))
    if (col.doubt) {  // a poll's answers the site cannot confirm are struck
      const doubt = col.doubt(row)
      out.parts = answers(v).map((id) => ({ text: option(col, id).emoji || option(col, id).text, cls: doubt.includes(id) ? 'doubt' : '' }))
      if (doubt.length) hint.push(`⚖️ сайт не бачить: ${doubt.map((id) => option(col, id).emoji).join(' ')}`)
    }
  } else if (col.type === 'number' && hasValue(v)) Object.assign(out, { text: String(v), cls: Number(v) ? 'num' : 'zero' })
  else if (col.type === 'date' && hasValue(v)) Object.assign(out, { text: dayMonth(v), at: v, cls: 'some' }) && hint.push(fmtWhen(v))
  else if (col.type === 'text' && hasValue(v)) Object.assign(out, { text: String(v), cls: 'some' }) && hint.push(String(v))
  if (out.sub) hint.push(out.sub)
  out.title = hint.join('\n')
  return out
}

// what a column adds up to over some rows, as chips: { id, text, n } — `id` is the filter that keeps those rows («1» for
// a checkmark, an answer's id); a number sums and a text counts into a chip without an id
export function facets(col, rows) {
  const vs = rows.map((r) => col.get(r))
  if (col.type === 'number') return [{ id: '', text: 'Σ', n: Math.round(vs.reduce((s, v) => s + (numberOf(v) || 0), 0) * 10) / 10 }]
  if (yes(col)) return [{ id: '1', text: '✅', n: vs.filter(hasValue).length }]
  if (!picks(col)) return [{ id: '', text: '', n: vs.filter(hasValue).length }]
  const n = {}
  for (const v of vs) for (const id of answers(v)) n[id] = (n[id] || 0) + 1
  return Object.keys(col.options || {}).filter((id) => n[id]).map((id) => ({ id, text: option(col, id).emoji || option(col, id).text, n: n[id], title: option(col, id).text }))
}
