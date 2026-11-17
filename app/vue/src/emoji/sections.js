import { load, save } from '@core/local.js'
import { find, suggest } from './search.js'

// what the picker lists (T309): for a query — the found, the best first; else «за назвою й типом» (search.js suggest),
// «нещодавні» (this browser's last picks) and the groups. All of it through the colour filter and, for a storyboard's
// legend, without letters, digits and punctuation: its text reads them as text (momentsText.js)
const KEY = 'emoji-recent'
const PLAIN = /^[\p{L}\p{N}\p{P}]$/u
const seg = new Intl.Segmenter('uk', { granularity: 'grapheme' })
const sign = (s) => [...seg.segment(s)].length === 1 && !PLAIN.test(s)
export const recent = () => (load(KEY) || '').split(' ').filter(Boolean)
export const remember = (char) => save(KEY, [char, ...recent().filter((c) => c !== char)].slice(0, 22).join(' '))
export const fits = (text, legend) => !legend || text.split(/[,\s]+/).filter(Boolean).every(sign)  // «🔑, 🗝️» — one line's icons

// { list: [{ key, title, items }], why: Map item → the word that found it, as: the query in the other layout }
export function sections(data, { q, color, hint, legend }) {
  const ok = (it) => (!color || it.colors.includes(color)) && fits(it.char, legend)
  const row = (key, title, items) => ({ key, title, items: items.filter(ok) })
  if (q.trim()) {
    const { rows, as } = find(data.items, q)
    const found = row('found', 'знайдено', rows.map((r) => r.it))
    return { list: [{ ...found, title: `знайдено ${found.items.length}`, items: found.items.slice(0, 220) }], why: new Map(rows.map((r) => [r.it, r.why])), as }
  }
  const list = [row('hint', 'за назвою й типом', hint ? suggest(data.items, hint) : []),
    row('recent', 'нещодавні', recent().map((c) => data.by.get(c)).filter(Boolean)),
    ...data.groups.map((g) => row(g.key, g.title, g.items))]
  return { list: list.filter((s) => s.items.length), why: new Map() }
}
