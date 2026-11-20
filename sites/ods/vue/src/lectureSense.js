import { fold, tokens } from './lectureText.js'

// «за змістом» (search/keys.json): a slide's keys say how a student would ask about it in other words; a query whose
// words all stand in one key — by lemma, as written, as a word's start while it is typed, or by a shared stem — finds it

// a rough stem: keys are written apart from the lectures, so the lexicon may not know their words («нормальність» ~ «нормальні»)
const stem = (a, b) => {
  let i = 0
  while (i < a.length && a[i] === b[i]) i++
  return i >= Math.max(5, Math.min(a.length, b.length) - 3)
}

export function sensesOf(data, lex, ix) {
  const keys = []
  for (const [slug, slides] of Object.entries(data && typeof data === 'object' ? data : {})) {
    if (!slides || typeof slides !== 'object') continue  // `v`
    for (const [n, list] of Object.entries(slides)) {
      if (!ix.first.has(`${slug}#${n}`) || !Array.isArray(list)) continue  // a lecture the reader has not got, or no such slide
      for (const key of list) {
        const toks = tokens(fold(String(key)), false)
        keys.push({ slug, slide: Number(n), key: String(key), toks, ids: toks.map((t) => lex.lemmas(t[2])) })
      }
    }
  }
  // the query's words → [{ slug, slide, key, toks, marks }]: a slide once, by its shortest key that holds them all
  return (qs) => {
    const out = new Map(), qids = qs.map((w) => lex.lemmas(w))
    for (const k of keys) {
      const marks = []
      for (const [i, w] of qs.entries()) {
        const t = k.toks.findIndex(([, , kw], j) => kw === w || qids[i].some((id) => k.ids[j].includes(id))
          || (w.length >= 3 && kw.startsWith(w)) || stem(kw, w))
        if (t < 0) break
        marks.push(k.toks[t].slice(0, 2))
      }
      const at = `${k.slug}#${k.slide}`
      if (marks.length === qs.length && (!out.has(at) || out.get(at).toks.length > k.toks.length)) out.set(at, { ...k, marks })
    }
    return [...out.values()]
  }
}
