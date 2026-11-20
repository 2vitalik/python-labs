import { fixerOf } from './lectureFuzzy.js'
import { indexOf } from './lectureIndex.js'
import { lexiconOf } from './lectureLex.js'
import { matchAll, specsOf } from './lectureMatch.js'
import { named, phraseIn } from './lecturePhrase.js'
import { sensesOf } from './lectureSense.js'
import { hitOf, senseHit } from './lectureSnip.js'
import { STOP, fold, tokens, words } from './lectureText.js'
import { thesOf } from './lectureThes.js'

// the search over the lectures' blocks (CONTRACT §6.2), no network: lectures [{ lec, slug, title, text }] and data
// { lexicon, thesaurus, keys } — any may be missing, its layer is then off → find(q, limit) → { hits, counts, fixed }
export const KINDS = ['exact', 'form', 'typo', 'syn', 'sense']
const TERMS = 30  // strings per lecture for its page to light up

export function engine(lectures, data = {}) {
  const ix = indexOf(lectures), lex = lexiconOf(data.lexicon)
  const stop = (w) => STOP.has(w) || lex.stop.has(w)
  const thes = thesOf(data.thesaurus, lex, stop), fix = fixerOf(ix, lex), senses = sensesOf(data.keys, lex, ix)
  const known = (w) => lex.knows(w) || thes.knows(w) || ix.words.some((v) => v.startsWith(w))
  const content = (ws) => (ws.some((w) => !stop(w)) ? ws.filter((w) => !stop(w)) : ws)

  return function find(q, limit = 12) {
    const src = String(q ?? '').replace(/\s+/g, ' ').trim(), p = fold(src)
    const out = { hits: [], counts: Object.fromEntries(KINDS.map((k) => [k, 0])), fixed: null }
    if (p.length < 2) return out
    const qt = tokens(p, false), ws = qt.map((t) => t[2]), as = qt.map(([a, e]) => src.slice(a, e)), need = content(ws)
    const taken = new Set(), pool = Object.fromEntries(KINDS.map((k) => [k, []])), terms = {}
    const typed = (w) => as[ws.indexOf(w)] ?? w
    const lemma = (x) => (lex.lemma(x.tok, x.w) === x.found ? typed(x.w) : lex.lemma(x.tok, x.w))  // not «компонент → компонент»
    const formVia = (x) => (x.part ? `${typed(x.w)}… → ${x.found}` : `${x.found} → ${lemma(x)}`)

    // every block a kind matched lends its strings to the kind's terms in its lecture (a letter alone would light up every
    // formula) — unless its words stand apart: those go to its own hit only; the block itself goes to the first kind only
    const take = (kind, list, via) => {
      for (const m of list) {
        const t = (terms[`${kind}#${m.b.slug}`] ??= new Set())
        if (!m.loose) m.found.forEach((f) => f.length > 1 && t.size < TERMS && t.add(f))
        if (taken.has(m.b.i)) continue
        taken.add(m.b.i)
        pool[kind].push({ ...m, via: via(m) })
      }
    }
    take('exact', ix.blocks.map((b) => phraseIn(b, p)).filter(Boolean), () => '')
    take('form', matchAll(ix, need.flatMap((w) => specsOf(w, lex))),
      (m) => m.as.filter((x) => x.tok !== x.w).map(formVia).join(', ') || (m.loose ? 'усі слова, не поруч' : `${src} → ${m.found[0]}`))

    const odd = need.filter((w) => !known(w)), fixes = new Map(odd.map((w) => [w, fix(w)]))
    if (odd.length && [...fixes.values()].every(Boolean)) {
      const specs = need.flatMap((w) => (fixes.has(w) ? specsOf(fixes.get(w).to, lex, false) : specsOf(w, lex)))
      const said = odd.map((w) => `${typed(w)} → ${fixes.get(w).as}`).join(', ')
      take('typo', matchAll(ix, specs), () => said)
      if (pool.typo.length) out.fixed = ws.map((w, i) => fixes.get(w)?.as ?? as[i]).join(' ')
    }

    const syn = thes.match(ws), rest = syn && content([...ws.slice(0, syn.from), ...ws.slice(syn.to)])
    for (const alt of syn?.alts || []) {  // the other name stands whole, in its forms; the query's other words — anywhere
      const own = rest.flatMap((w) => specsOf(w, lex)), name = words(alt).flatMap((w) => specsOf(w, lex, false))
      take('syn', matchAll(ix, [...own, ...name]).map((m) => named(m, own.length, name)).filter(Boolean),
        () => `${as.slice(syn.from, syn.to).join(' ')} = ${alt}`)
    }

    // in a kind: a heading first, then the words nearer each other, then the lecture's number and the text's order
    const order = (x, y) => y.b.head - x.b.head || x.near - y.near || x.b.lec - y.b.lec || x.b.i - y.b.i
    for (const kind of KINDS.slice(0, 4)) {
      out.counts[kind] = pool[kind].length
      out.hits.push(...pool[kind].sort(order).slice(0, limit)
        .map((m) => hitOf(kind, m, [...new Set([...terms[`${kind}#${m.b.slug}`], ...(m.loose ? m.found : [])])])))
    }

    // a slide the words found already is not shown again «за змістом»
    const seen = new Set(Object.values(pool).flat().map((m) => `${m.b.slug}#${m.b.slide}`))
    const sense = (need.length ? senses(need) : []).filter((k) => !seen.has(`${k.slug}#${k.slide}`))
      .map((k) => ({ k, near: k.toks.length - need.length, lec: ix.first.get(`${k.slug}#${k.slide}`).lec }))
      .sort((x, y) => x.near - y.near || x.lec - y.lec || x.k.slide - y.k.slide)
    out.counts.sense = sense.length
    out.hits.push(...sense.slice(0, limit).map((s) => senseHit(s.k, ix)))
    return out
  }
}
