import { headingId } from '@core/headings.js'

import { bare, fold, inline, tokens } from './lectureText.js'

// a lecture → its blocks (a paragraph, a list item, a table, a code block, a heading) with the slide and the contents'
// section they stand in; then the index over all of them, built once: word → blocks, how often a word is, how it is written
const MARK = /^<!--\s*слайд\s+(\d+)[^>]*-->\s*$/
const NOTE = /<!--(?!\s*слайд\s)[\s\S]*?(?:-->|$)/g  // drafts and notes («правка 05-A6») are not the lecture's words
const HEAD = /^(#{1,6})\s+(.*)$/
const ITEM = /^[ \t>]*([-*+]|\d+\.)[ \t]/
const BLANK = /^[ \t>]*(:::.*)?$/
const isRow = (l) => l?.trimStart().startsWith('|')

// [{ lec, slug, title, slide, id, heading, text, head }]; before the first mark — the slide of the first mark's number;
// `id` / `heading` — the h2/h3 above, as tocOf has them ('' — the lecture's start)
export function blocksOf(text, meta) {
  const src = (text || '').replace(NOTE, (m) => (m.includes('\n') ? '\n\n' : ' '))
  const out = []
  let slide = Number(src.match(/<!--\s*слайд\s+(\d+)/)?.[1] ?? 1), id = '', heading = '', fence = false, buf = []
  const push = (t, head) => t && out.push({ ...meta, slide, id, heading, text: t, head })
  const flush = () => {
    if (buf.length) push(bare(buf.join('\n')), false)
    buf = []
  }
  for (const l of src.split('\n')) {
    if (/^\s*```/.test(l)) {
      if (!fence) flush()
      buf.push(l)
      if (!(fence = !fence)) flush()
      continue
    }
    if (fence) { buf.push(l); continue }
    const m = l.match(MARK), h = !m && l.match(HEAD)
    if (m || h || BLANK.test(l) || ITEM.test(l) || (buf.length && isRow(l) !== isRow(buf.at(-1)))) flush()
    if (m) slide = Number(m[1])
    else if (h) {
      if (h[1].length === 2 || h[1].length === 3) {
        [id, heading] = headingId(h[2])
        heading = inline(heading)
      }
      push(inline(h[2]), true)
    } else if (!BLANK.test(l)) buf.push(l)
  }
  flush()
  return out
}

// lectures [{ lec, slug, title, text }] → { blocks, post: word → block ids, vocab: word → { n, as }, words, first }
export function indexOf(lectures) {
  const blocks = lectures.flatMap(({ text, ...meta }) => blocksOf(text, meta))
  const post = new Map(), vocab = new Map(), first = new Map()  // first: `slug#slide` → the slide's first block
  blocks.forEach((b, i) => {
    b.i = i
    b.f = fold(b.text)
    b.toks = tokens(b.f)
    if (!first.has(`${b.slug}#${b.slide}`)) first.set(`${b.slug}#${b.slide}`, b)
    for (const [a, e, w] of b.toks) {
      const p = post.get(w)
      if (!p) post.set(w, [i])
      else if (p.at(-1) !== i) p.push(i)
      const v = vocab.get(w)
      if (v) v.n++
      else vocab.set(w, { n: 1, as: b.text.slice(a, e) })
    }
  })
  return { blocks, post, vocab, words: [...vocab.keys()], first }
}
