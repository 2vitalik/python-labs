// a hit as the pages get it (CONTRACT §6.2): ~120 characters of the block around its first match, cut at spaces,
// and the matches' places in that snippet

function merged(spans) {
  const out = []
  for (const [a, e] of [...spans].sort((x, y) => x[0] - y[0])) {
    if (out.length && a <= out.at(-1)[1]) out.at(-1)[1] = Math.max(out.at(-1)[1], e)
    else out.push([a, e])
  }
  return out
}

export function snip(text, spans, at, width = 120) {
  const all = merged(spans), end = all.find(([a, e]) => a <= at && at < e)?.[1] ?? at
  let from = Math.max(0, at - 50), to = Math.min(text.length, from + width)
  if (to === text.length) from = Math.max(0, to - width)
  const s = text.indexOf(' ', from), e = text.lastIndexOf(' ', to)
  if (from && s >= 0 && s < at) from = s + 1
  if (to < text.length && e >= end) to = e
  const pre = from ? '…' : ''
  return {
    snippet: pre + text.slice(from, to) + (to < text.length ? '…' : ''),
    marks: all.filter(([a, b]) => a >= from && b <= to).map(([a, b]) => [a - from + pre.length, b - from + pre.length]),
  }
}

export function hitOf(kind, m, terms) {
  const { b } = m
  return { kind, lec: b.lec, slug: b.slug, title: b.title, slide: b.slide, id: b.id, heading: b.heading,
    ...snip(b.text, m.spans, m.at), terms, via: m.via }
}

// «за змістом»: the key, then how the slide starts (its first blocks); the marks — the key's words the query stands in
export function senseHit(k, ix) {
  const b = ix.first.get(`${k.slug}#${k.slide}`)
  let start = ''
  for (let i = b.i; i < ix.blocks.length && ix.blocks[i].slug === b.slug && ix.blocks[i].slide === b.slide && start.length < 100; i++) {
    start += (start ? ' · ' : '') + ix.blocks[i].text
  }
  const { snippet } = snip(start, [], 0, 100 - Math.min(60, k.key.length))
  return { kind: 'sense', lec: b.lec, slug: b.slug, title: b.title, slide: b.slide, id: b.id, heading: b.heading,
    snippet: `${k.key} — ${snippet}`, marks: merged(k.marks), terms: [], via: `за змістом: ${k.key}` }
}
