import { answers, dayMonth, hasValue, numberOf, option, yes } from './table.js'

// a column's filter, as the URL writes it (T315 §12.1): + has a value · - empty, for every type; bool/link 1|0 · answers: ids,
// «-» among them = empty · number 3-5 3- -5 >3 <3 3 · text a substring · date >day <day ~N (the last N days) ^N (older)
const DAY = 864e5
const RANGE = /^(\d*\.?\d*)-(\d*\.?\d*)$/  // a-b · a- · -b: inclusive
const p2 = (n) => String(n).padStart(2, '0')
const localDay = (iso) => { const d = new Date(iso); return `${d.getFullYear()}-${p2(d.getMonth() + 1)}-${p2(d.getDate())}` }

export function passes(col, row, spec) {
  const v = col.get(row)
  if (!spec) return true
  if (spec === '+' || spec === '-') return hasValue(v) === (spec === '+')
  if (yes(col)) return hasValue(v) === (spec === '1')
  if (col.type === 'date') {
    if (spec === '1' || spec === '0') return hasValue(v) === (spec === '1')
    if (!hasValue(v)) return false
    const days = (Date.now() - new Date(v)) / DAY
    return spec[0] === '~' ? days <= Number(spec.slice(1)) : spec[0] === '^' ? days > Number(spec.slice(1))
      : spec[0] === '>' ? localDay(v) >= spec.slice(1) : localDay(v) <= spec.slice(1)
  }
  if (col.type === 'number') {
    const n = numberOf(v)
    if (n === null) return false
    const m = spec.match(RANGE)
    if (m && (m[1] || m[2])) return (!m[1] || n >= Number(m[1])) && (!m[2] || n <= Number(m[2]))
    return spec[0] === '>' ? n > Number(spec.slice(1)) : spec[0] === '<' ? n < Number(spec.slice(1)) : n === Number(spec)
  }
  if (col.type === 'text') return hasValue(v) && String(v).toLowerCase().includes(spec.toLowerCase())
  const want = spec.split(',')
  const got = answers(v)
  return (want.includes('-') && !got.length) || got.some((id) => want.includes(id))
}

// the same filter in a word or two, for the line that says how the view is set
export function filterText(col, spec) {
  if (spec === '+') return 'є'
  if (spec === '-') return 'порожньо'
  if (yes(col) || (col.type === 'date' && (spec === '1' || spec === '0'))) return spec === '1' ? 'так' : 'ні'
  if (col.type === 'date') return { '~': `за ${spec.slice(1)} дн.`, '^': `давніше ${spec.slice(1)} дн.`, '>': `від ${dayMonth(spec.slice(1))}`, '<': `до ${dayMonth(spec.slice(1))}` }[spec[0]] || spec
  if (col.type === 'number') {
    const m = spec.match(RANGE)
    return m && m[1] && m[2] ? `${m[1]}–${m[2]}` : m && m[1] ? `від ${m[1]}` : m && m[2] ? `до ${m[2]}` : spec.replace(/^([<>])/, '$1 ')
  }
  if (col.type === 'text') return `«${spec}»`
  return spec.split(',').map((id) => (id === '-' ? '∅' : option(col, id).emoji || option(col, id).text)).join(' ')
}
