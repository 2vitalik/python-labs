import { esc, norm } from './search.js'

// the search behind Picker.vue: every word of the query must hit somewhere, and the row says where when it is not the title
export const words = (q) => norm(q).split(/\s+/).filter(Boolean)

export function match(it, qs) {
  const title = norm(it.title)
  let score = 0, why = ''
  for (const w of qs) {
    if (title.startsWith(w)) { score += 10; continue }
    if (title.includes(w)) { score += 7; continue }
    const syn = (it.words || []).find((s) => norm(s).includes(w))
    const at = syn ? -1 : norm(it.desc || '').indexOf(w)
    if (syn) { score += 5; why ||= `синонім: ${syn}` }
    else if (at >= 0) { score += 1; why ||= `в описі: …${it.desc.slice(Math.max(0, at - 18), at + w.length + 24).trim()}…` }
    else if (norm(`${it.group || ''} ${it.hint || ''}`).includes(w)) { score += 2; why ||= `розділ: ${it.group || it.hint}` }
    else if (norm(String(it.key)).includes(w)) { score += 2; why ||= `код: ${it.key}` }
    else return null
  }
  return { ...it, score, why }
}

export const search = (items, qs) => (qs.length ? items.map((it) => match(it, qs)).filter(Boolean).sort((a, b) => b.score - a.score) : items)

// every word of the query marked in the text; norm() keeps the length, so its indices fit the original
export function mark(text, qs) {
  text = String(text ?? '')
  const n = norm(text), on = new Array(text.length).fill(false)
  for (const w of qs) for (let i = n.indexOf(w); i >= 0; i = n.indexOf(w, i + w.length)) on.fill(true, i, i + w.length)
  let out = ''
  for (let i = 0, j; i < text.length; i = j) {
    for (j = i; j < text.length && on[j] === on[i];) j++
    out += on[i] ? `<mark>${esc(text.slice(i, j))}</mark>` : esc(text.slice(i, j))
  }
  return out
}
