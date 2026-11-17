import { answers, hasValue, numberOf, option, optionLabel, picks, yes } from './table.js'

// the order of the rows and the groups they fall in (T315 §4): several columns at once, level after level

// a key to sort by; empty cells go last whichever way
export function sortKey(col, row) {
  const v = col.get(row)
  if (!hasValue(v)) return null
  if (col.type === 'number') return numberOf(v)
  if (picks(col)) return Math.min(...answers(v).map((id) => Object.keys(col.options || {}).indexOf(id)).map((i) => (i < 0 ? 999 : i)))
  if (yes(col)) return 0
  return String(v).toLowerCase()
}
export function compare(a, b) {
  if (a === null || b === null) return (a === null) - (b === null)
  return typeof a === 'number' && typeof b === 'number' ? a - b : String(a).localeCompare(String(b), 'uk')
}
// rows by levels [{ col, desc }]: the first decides, the next breaks its ties, the name breaks the last
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
  if (!hasValue(v)) return { key: null, text: yes(col) ? `${col.short} ні` : `${col.short === col.title ? '' : `${col.short} `}порожньо` }
  if (yes(col)) return { key: 0, text: `${col.short} так` }
  if (picks(col)) return { key: sortKey(col, row), text: answers(v).map((id) => optionLabel(option(col, id))).join(', ') }
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
