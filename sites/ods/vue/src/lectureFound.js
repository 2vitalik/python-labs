import { norm } from '@core/search.js'

// the terms of a search (?find=a|b, T374 §6.3) in a lecture as drawn: ranges over its text nodes, painted by the CSS Custom
// Highlight API (lectureFind.css) — the DOM that Vue draws through v-html stays as it is. A formula, a slide's number and
// what is hidden (a slide's own block in the text) are not the text read
const SKIP = '.katex, .slide-mark, script, style'
const BLOCK = 'p, li, td, th, h1, h2, h3, h4, h5, h6, blockquote, dt, dd, figcaption, pre'
const reEsc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
const fold = (s) => norm(s).replace(/[’ʼ]/g, "'")  // as the engine folds (lectureText.js); the length stays

// a term is whole words, as the engine found them: «компонент» does not light up «компонента» (that form comes as a term
// of its own); spaces in a phrase stand for any line break of the text
const W = '[\\p{L}\\p{N}]'
function pattern(terms) {
  const want = [...new Set(terms.map((t) => fold(t.trim())).filter((t) => t.length >= 2))].sort((a, b) => b.length - a.length)
  return want.length && new RegExp(`(?<!${W})(?:${want.map((t) => reEsc(t).replace(/\s+/g, '\\s+')).join('|')})(?!${W})`, 'gu')
}

// [Range] in reading order; the nodes of one block are matched as one string, so a phrase crosses its bold and its colours
export function rangesOf(root, terms) {
  const re = root && pattern(terms)
  if (!re) return []
  const out = [], shown = new Map()
  let group = [], block = null, at = 0
  const flush = () => {
    const text = fold(group.map((g) => g.node.data).join(''))
    for (const m of text.matchAll(re)) out.push(rangeAt(group, m.index, m.index + m[0].length))
    group = []
    at = 0
  }
  const walk = document.createTreeWalker(root, NodeFilter.SHOW_TEXT)
  for (let node = walk.nextNode(); node; node = walk.nextNode()) {
    const el = node.parentElement
    if (!shown.has(el)) shown.set(el, !el.closest(SKIP) && (el.checkVisibility?.({ visibilityProperty: true }) ?? true))
    if (!shown.get(el)) continue
    const b = el.closest(BLOCK) || el
    if (b !== block) (flush(), (block = b))
    group.push({ node, at })
    at += node.data.length
  }
  flush()
  return out
}
function rangeAt(group, from, to) {
  const start = group.findLast((g) => g.at <= from), end = group.findLast((g) => g.at < to)
  const r = new Range()
  r.setStart(start.node, from - start.at)
  r.setEnd(end.node, to - end.at)
  return r
}

export const canPaint = () => !!(window.CSS?.highlights && window.Highlight)
export const unpaint = () => canPaint() && ['lec-find', 'lec-find-hot', 'lec-find-now'].forEach((n) => CSS.highlights.delete(n))
// the one stood on over the rest; `hot` — the first seconds, brighter
export function paint(ranges, cur, hot) {
  if (!canPaint()) return
  unpaint()
  const now = new Highlight(...(ranges[cur] ? [ranges[cur]] : []))
  now.priority = 1
  CSS.highlights.set(hot ? 'lec-find-hot' : 'lec-find', new Highlight(...ranges.filter((_, i) => i !== cur)))
  CSS.highlights.set('lec-find-now', now)
}
