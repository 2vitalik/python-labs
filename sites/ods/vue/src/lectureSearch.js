import { getGuidePage } from '@core/api.js'
import { textOf } from '@core/drafts.js'
import { loadGuide } from '@core/guide.js'
import { headingId } from '@core/headings.js'
import { norm } from '@core/search.js'

import { lectures, shortTitle } from './lectures.js'

// search over the texts of all lectures (LectureFind): fetched once, then cut into sections and matched locally

// markdown as plain words; a short formula keeps its letters ($S_{1}^{2}$ → S_1^2), a long one is «…»
const FORMULA = /\$\$([^\n]+?)\$\$|\$([^\n$]+?)\$/g
const letters = (tex) => {
  const s = tex.replace(/\\[a-zA-Z]+|[{}\\]/g, '').replace(/\s+/g, ' ').trim()
  return s.length <= 15 ? s : '…'
}
const inline = (md) => md.replace(FORMULA, (_, block, line) => ` ${letters(block ?? line)} `)
  .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ').replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
  .replace(/<!--\s*слайд[^>]*-->|<!--|-->|<\/?[a-zA-Z][^>]*>|\{#[\w-]+\}/g, ' ')
  .replace(/[*`\\]/g, '').replace(/\|/g, ' ').replace(/\s+/g, ' ').trim()
const words = (md) => inline(md.replace(/^:::.*$/gm, ' ')  // the slides' fences (slideMd.js): «::: колонки» is markup, not words
  .replace(/^[ \t]*(#{1,6}|>|[-*+]|\d+\.)[ \t]+/gm, '').replace(/^[ \t|:-]+$/gm, ' '))

// a lecture cut at its h2/h3 — the sections of its contents, with tocOf's ids; the part before them belongs to the title
function cut(text, title) {
  const out = [{ id: '', head: title, src: [] }]
  let fence = false
  for (const l of text.split('\n')) {
    if (/^\s*```/.test(l)) fence = !fence
    const m = !fence && l.match(/^#{2,3}\s+(.*)$/)
    if (!m) out.at(-1).src.push(l)
    else {
      const [id, head] = headingId(m[1])
      out.push({ id, head: inline(head), src: [] })
    }
  }
  return out.map(({ id, head, src }) => {
    const body = words(src.join('\n'))
    return { id, head, body, h: norm(head), b: norm(body) }  // norm() keeps the length: an index in one is one in the other
  })
}

let texts = []  // [{n, slug, page}] with the bodies, after loadTexts()
let loading
export function loadTexts() {
  loading ??= loadGuide()
    .then(() => Promise.all(lectures().map(async (s) => ({ ...s, page: await getGuidePage(s.slug).catch(() => null) }))))
    .then((list) => (texts = list.filter((t) => t.page)), (e) => { loading = null; throw e })
  return loading
}

const cuts = new Map()  // slug → [text, sections]: cut again only when the text is another (the admin's drafts on/off)
function sectionsOf({ slug, page }) {
  const text = textOf(page)
  if (cuts.get(slug)?.[0] !== text) cuts.set(slug, [text, cut(text, shortTitle(page.title))])
  return cuts.get(slug)[1]
}

// ~120 characters around the match, cut at spaces
function around(body, folded, q) {
  const j = Math.max(0, folded.indexOf(q))
  let from = Math.max(0, j - 50), to = Math.min(body.length, j + q.length + 70)
  const s = body.indexOf(' ', from), e = body.lastIndexOf(' ', to)
  if (from && s >= 0 && s < j) from = s + 1
  if (to < body.length && e > j + q.length) to = e
  return (from ? '…' : '') + body.slice(from, to) + (to < body.length ? '…' : '')
}

// [{n, slug, title, id, heading, snippet}], a section once: matches in headings first, then in the text;
// `heading` '' — the start of the lecture (its title matched, or the text before the first section)
export function find(q, limit = 30) {
  const nq = norm(q.trim())
  if (nq.length < 2) return []
  const heads = [], rest = []
  for (const t of texts) {
    for (const s of sectionsOf(t)) {
      const to = s.h.includes(nq) ? heads : s.b.includes(nq) ? rest : null
      to?.push({ n: t.n, slug: t.slug, title: shortTitle(t.page.title), id: s.id, heading: s.id ? s.head : '', snippet: around(s.body, s.b, nq) })
    }
  }
  return [...heads, ...rest].slice(0, limit)
}
