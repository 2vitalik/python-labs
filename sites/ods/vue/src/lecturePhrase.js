import { fits } from './lectureMatch.js'

// a phrase in a block: the query as it is (exact), or a name of the course's group standing whole, in its forms (syn)

const isW = (c) => c !== undefined && /[\p{L}\p{N}]/u.test(c)
const lower = (b, spans) => [...new Set(spans.map(([a, e]) => b.text.slice(a, e).toLowerCase()))]

// the query as it is, at word edges → { b, spans, at, found, near, as }
export function phraseIn(b, p) {
  const spans = []
  for (let j = b.f.indexOf(p); j >= 0; j = b.f.indexOf(p, j + 1)) {
    if (!(isW(p[0]) && isW(b.f[j - 1])) && !(isW(p.at(-1)) && isW(b.f[j + p.length]))) spans.push([j, j + p.length])
  }
  return spans.length ? { b, spans, at: spans[0][0], found: lower(b, spans), near: 0, as: [] } : null
}

// where the specs stand one after another, in order: [[from, to]] — over the words as written, and with a hyphened
// word in its parts («$F$-критерій» is «F», «критерій»; «F-критерій» — one word)
export function runsOf(b, specs) {
  const out = new Map()
  for (const seq of [b.toks.filter((t) => !t[3]), b.toks.filter((t) => !t[2].includes('-'))]) {
    for (let i = 0; i + specs.length <= seq.length; i++) {
      if (specs.every((s, k) => fits(s, seq[i + k][2]))) out.set(seq[i][0], [seq[i][0], seq[i + specs.length - 1][1]])
    }
  }
  return [...out.values()].sort((x, y) => x[0] - y[0])
}

// a block matched by the query's other words and a name's words → the name found whole, or null: the name's words
// scattered over the block are not the name. `found` — the name as written there, for the page to light up
export function named(m, rest, name) {
  const runs = runsOf(m.b, name)
  if (!runs.length) return null
  return { ...m, spans: [...runs, ...m.by.slice(0, rest).flat()], at: runs[0][0], near: 0, loose: false, found: lower(m.b, runs) }
}
