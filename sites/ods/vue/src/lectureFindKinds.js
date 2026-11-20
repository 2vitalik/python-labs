import { esc } from '@core/search.js'

// the kinds of a match (CONTRACT §6.2) in the engine's order; each has one colour everywhere (lectureFind.css: .k-<key>)
export const KINDS = [
  { key: 'exact', name: 'точні', head: 'Точний збіг' },
  { key: 'form', name: 'форми слова', head: 'Інша форма слова' },
  { key: 'typo', name: 'схоже написання', head: 'Схоже написання' },
  { key: 'syn', name: 'синоніми', head: 'Синоніми й скорочення' },
  { key: 'sense', name: 'за змістом', head: 'За змістом' },
]
export const kindOf = (key) => KINDS.find((k) => k.key === key)

// the query outlives the list page: back from a lecture, the results are as they were
export const kept = { q: '', kind: '' }

// the place in the lecture: its terms to light up and the slide to stand on (lectureFound.js); a hit by sense has no terms
export const hitLink = (h) => ({ path: `/lectures/${h.lec}`, query: { ...(h.terms?.length ? { find: h.terms.join('|') } : {}), at: h.slide } })

// the snippet with its [[from, to]] marks, escaped; marks that overlap or stand a space apart («метод головних») are one
export function snippetHtml(text, marks = []) {
  const spans = []
  for (const [from, to] of [...marks].sort((a, b) => a[0] - b[0])) {
    const last = spans.at(-1)
    if (last && from <= last[1] + 1 && !text.slice(last[1], from).trim()) last[1] = Math.max(last[1], to)
    else spans.push([from, to])
  }
  let out = '', at = 0
  for (const [from, to] of spans) {
    out += esc(text.slice(at, from)) + '<mark>' + esc(text.slice(from, to)) + '</mark>'
    at = to
  }
  return out + esc(text.slice(at))
}

// hits → sections by kind (the engine's order) → groups by lecture (first seen first); `i` — the row's place in reading order
export function sectionsOf(hits) {
  const out = []
  let i = 0
  for (const k of KINDS) {
    const groups = new Map()
    for (const h of hits.filter((x) => x.kind === k.key)) {
      if (!groups.has(h.lec)) groups.set(h.lec, { lec: h.lec, title: h.title, rows: [] })
      groups.get(h.lec).rows.push(h)
    }
    if (groups.size) out.push({ ...k, groups: [...groups.values()] })
  }
  for (const s of out) for (const g of s.groups) g.rows = g.rows.map((h) => ({ ...h, i: i++ }))
  return out
}
