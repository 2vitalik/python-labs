import { stem, wordsOf } from './search.js'
import { draws, maxVersion } from './support.js'

// the picker's data (emoji/build.mjs → data.json, its own chunk), fetched when a picker first opens and made ready to
// search: { items, groups: [{ key, title, sign, items }], by: Map char → item }, without what this device cannot draw.
// An item: { char, uk, en, colors, names · words — [word, stem] to search, rank — how near the head of its group it
// stands: what is hand-picked there is the likeliest in a game; faces and things give way a little, plain symbols and
// flags — to every emoji }
const LATE = { faces: 15, things: 15, digits: 10, text: 60, flags: 200 }
const prep = (...texts) => wordsOf(texts.join(' ')).map((w) => [w, stem(w)])
let loading

export function ready(d, max = 99, flags = true) {
  const all = d.items.map(([char, uk, en, ukw, enw, ruw, colors, v], i) =>
    ({ char, uk, en, colors, v, i, rank: 999, names: prep(uk, en), words: prep(ukw, enw, ruw) }))
  const groups = d.groups.filter((g) => flags || g.key !== 'flags')
    .map((g) => ({ ...g, items: g.items.map((i) => all[i]).filter((it) => it.v <= max) }))
  for (const g of groups) g.items.forEach((it, n) => (it.rank = Math.min(it.rank, n + (LATE[g.key] || 0))))
  const items = [...new Set(groups.flatMap((g) => g.items))]
  return { items, groups, by: new Map(items.map((it) => [it.char, it])) }
}
export const loadEmoji = () => (loading ??= import('./data.json').then(({ default: d }) => ready(d, maxVersion(), draws('🇺🇦'))))
