// how a word of a query is looked for in a block, and the blocks holding every word of a query

// a word → its specs: any form of its lemmas as a whole word; a word the lexicon does not know — as a word's start, it may
// be still typed (`part` off or one letter — as a whole word); an unknown hyphened word — by its parts: «$t$-критерій»
// reads as two
export function specsOf(w, lex, part = true) {
  const forms = lex.spread(w)
  if (forms) return [{ w, forms }]
  if (w.includes('-')) return w.split('-').flatMap((p) => specsOf(p, lex, part))
  return [part && w.length > 1 ? { w, part: w } : { w, forms: new Set([w]) }]
}
export const fits = (s, w) => (s.forms ? s.forms.has(w) : w.startsWith(s.part))

// the blocks with every spec, in order: [{ b, spans, by, at, near, loose, found, as }] — the matched places (all, and per
// spec), where the tightest run of them starts, how far apart beyond side by side, the words found (as written, lower
// case), per spec the word found
export function matchAll(ix, specs) {
  if (!specs.length) return []
  let ids = null
  for (const s of specs) {
    const set = new Set()
    for (const w of s.forms ?? ix.words.filter((v) => v.startsWith(s.part))) {
      for (const i of ix.post.get(w) || []) if (!ids || ids.has(i)) set.add(i)
    }
    if (!(ids = set).size) return []
  }
  return [...ids].sort((a, b) => a - b).map((i) => placed(ix.blocks[i], specs)).filter(Boolean)
}

function placed(b, specs) {
  const hits = []  // [token, spec, mark from, mark to, the token: folded, from, to]
  b.toks.forEach(([a, e, w], t) => specs.forEach((s, k) => {
    if (fits(s, w)) hits.push([t, k, a, s.forms ? e : a + s.part.length, w, a, e])
  }))
  const cnt = specs.map(() => 0)
  let have = 0, lo = 0, best = null
  hits.forEach((h, hi) => {
    if (cnt[h[1]]++ === 0) have++
    for (; have === specs.length; lo++) {
      if (!best || h[0] - hits[lo][0] < best.span) best = { span: h[0] - hits[lo][0], lo, hi }
      if (--cnt[hits[lo][1]] === 0) have--
    }
  })
  if (!best) return null
  const run = hits.slice(best.lo, best.hi + 1), near = Math.max(0, best.span - specs.length + 1)
  const said = (from, to) => b.text.slice(from, to).toLowerCase()
  const loose = specs.length > 1 && near > 0  // the words not side by side: the page lights each of them up
  const each = [...new Set(hits.map((h) => said(h[5], h[6])))]
  return {
    b,
    spans: hits.map((h) => [h[2], h[3]]),
    by: specs.map((_, k) => hits.filter((h) => h[1] === k).map((h) => [h[2], h[3]])),
    at: run[0][2],
    near,
    loose,
    found: specs.length > 1 && !loose ? [said(run[0][5], Math.max(...run.map((h) => h[6])))] : each,
    as: specs.map((s, k) => {
      const h = run.find((x) => x[1] === k)
      return { w: s.w, tok: h[4], found: said(h[5], h[6]), part: !s.forms }
    }),
  }
}
