import katex from 'katex'

import { pale } from './lectureChangeSpots.js'

// the edits lit inside a rendered block (T374 PAGE §4): <mark>s put into the markdown before it renders; inside a formula —
// \textcolor of a colour no formula has, which changes.css paints as the same mark. A formula that breaks with it, or an
// edit across a formula's edge, lights the formula whole
const MATH = /\$\$[^\n]+?\$\$|\$[^\n$]+?\$/g
const SOLID = /`[^`\n]+`|<\/?[a-z][^>\n]*>|!?\[[^\]\n]*\]\([^)\n]*\)/gi  // not to be cut: code, an html tag, a link, a picture
// without «#»: KaTeX takes bare hex, and `{#…}` would be taken for an anchor by the platform's renderMd
export const TINT = { del: 'c10001', ins: '00c101', 'del pale': 'c10002', 'ins pale': '00c102' }

const spans = (re, text) => [...text.matchAll(re)].map((m) => ({ s: m.index, e: m.index + m[0].length }))


// a piece that closes a tag opened before it or opens one closed after it (`<c-b>` of the lecturer's colours): the tag is
// closed at the mark's edge and opened again on the other side, so the mark and the tag nest
const VOID = /^(br|img|hr|wbr)$/i
function marked(p, cls) {
  const open = [], lead = []
  for (const [, close, name] of p.matchAll(/<(\/?)([a-z][\w-]*)[^>]*>/gi)) {
    if (VOID.test(name)) continue
    if (!close) open.push(name)
    else if (open.at(-1) === name) open.pop()
    else lead.push(name)
  }
  const tags = (names, end) => names.map((n) => `<${end ? '/' : ''}${n}>`).join('')
  return `${tags(lead, true)}<mark class="chg ${cls}">${tags([...lead].reverse())}${p}${tags([...open].reverse(), true)}</mark>${tags(open)}`
}

// a mark may not cross a line (a list item goes on, a quote's «>») nor a table's cell — each piece gets its own;
// a table's rule row stays bare
function wrap(piece, cls, table) {
  if (!piece) return `<mark class="chg ${cls}"></mark>`
  return piece.split(table ? /(\n|\|)/ : /(\n)/).map((p, i) => {
    if (i % 2 || !p.trim() || /^\s*:?-+:?\s*$/.test(p)) return p
    const m = p.match(i ? /^(\s*(?:>\s*)*(?:[-*+]\s+|\d+[.)]\s+)?)([\s\S]*?)(\s*)$/ : /^(\s*)([\s\S]*?)(\s*)$/)
    return `${m[1]}${marked(m[2], cls)}${m[3]}`
  }).join('')
}
// only markup (a colour's tag, `**`): the rendered text has nothing to light — nor a caret where only markup came or went
const BARE = /^(\s|<\/?[a-z][^>]*>|\*+|_+)+$/i
const seen = (text, r) => !BARE.test(text.slice(r.s, r.e)) && !(r.s === r.e && BARE.test(r.other || ''))
export const markupOnly = (e) => BARE.test(e.del + e.ins)
const renders = (tex, block) => {
  try { katex.renderToString(tex, { displayMode: block, throwOnError: true, strict: false }); return true } catch { return false }
}

export function markMd(text, ranges) {
  const maths = spans(MATH, text).map((m) => ({ ...m, d: text.startsWith('$$', m.s) ? 2 : 1, inner: [] }))
  const solid = [...maths, ...spans(SOLID, text)]
  const plain = []
  for (const r of ranges.filter((x) => seen(text, x))) {
    const m = r.e > r.s && maths.find((x) => r.s >= x.s + x.d && r.e <= x.e - x.d)
    if (m) { m.inner.push(r); continue }
    let { s, e } = r
    for (const x of solid) if ((s < x.e && e > x.s) || (s === e && s > x.s && s < x.e)) [s, e] = [Math.min(s, x.s), Math.max(e, x.e)]
    plain.push({ ...r, s, e })
  }
  const covered = (m) => plain.some((p) => p.s <= m.s && p.e >= m.e)
  const swaps = []
  for (const m of maths.filter((x) => x.inner.length && !covered(x))) {
    let tex = text.slice(m.s + m.d, m.e - m.d)
    for (const r of [...m.inner].sort((x, y) => y.s - x.s)) {
      const s = r.s - m.s - m.d, e = r.e - m.s - m.d
      tex = `${tex.slice(0, s)}\\textcolor{${TINT[r.cls]}}{${tex.slice(s, e)}}${tex.slice(e)}`
    }
    if (renders(tex, m.d === 2)) swaps.push({ s: m.s, e: m.e, html: `${'$'.repeat(m.d)}${tex}${'$'.repeat(m.d)}` })
    else plain.push({ s: m.s, e: m.e, cls: (m.inner.find((r) => !pale(r)) || m.inner[0]).cls })
  }
  const table = text.trimStart().startsWith('|')
  for (const p of plain.sort((x, y) => x.s - y.s || pale(x) - pale(y))) {
    const last = swaps.findLast((w) => w.plain)
    if (last && p.s < last.e) continue  // widened into one before it
    swaps.push({ s: p.s, e: p.e, plain: true, html: wrap(text.slice(p.s, p.e), p.cls, table) })
  }
  let out = '', at = 0
  for (const w of swaps.sort((x, y) => x.s - y.s || !!y.plain - !!x.plain)) {
    if (w.s < at) continue
    out += text.slice(at, w.s) + w.html
    at = w.e
  }
  return out + text.slice(at)
}
