import { asked } from './asked.js'
import { aliasesOf, COINS, kidsOf, kindOf, subzoneTitle, taskIndex, tasks, vocab, zones } from './catalog.js'

// rows for Picker.vue built from the catalog and the vocab: what may be picked where (T270 §5)

const coin = (t) => COINS[t.coin] || ''
const home = (t) => [zones.value[t.zone]?.title, subzoneTitle(t)].filter(Boolean).join(' · ')

// a card «за запитом» (T319): Picker dims a row with a `tag` and shows the word by its title
const ASKED = { text: 'за запитом', title: 'картки ще нема в основі курсу: монетка — коли викладач відкриє картку' }
const tag = (on) => (on ? ASKED : null)
// such rows after the core ones of their group, the groups as they come
function coreFirst(items) {
  const at = new Map()
  items.forEach((it, i) => at.has(it.group) || at.set(it.group, i))
  return items.sort((a, b) => at.get(a.group) - at.get(b.group) || !!a.tag - !!b.tag)
}

// a card as a row: its coin, its home as the group, the description and the synonyms for the search; `taken` — slugs already here
export function cardItem(t, taken) {
  const parent = t.parent && taskIndex.value[t.parent]
  return {
    key: t.slug, title: parent ? `${parent.title}: ${t.title}` : t.title, icon: t.icon || coin(t) || '·', hint: t.icon ? coin(t) : '',
    group: home(t), desc: t.description || parent?.description, words: aliasesOf(t), taken: taken?.has(t.slug), task: t, tag: tag(asked(t)),
  }
}
// the cards of the given kinds one may claim (a family's parent is a heading — its children are the cards)
export const cardItems = (kinds, taken, filter = () => true) => coreFirst(
  tasks.value.filter((t) => t.status !== 'archived' && kinds.includes(kindOf(t)) && !kidsOf.value[t.slug] && filter(t)).map((t) => cardItem(t, taken)))
export const windowTypeItems = () => coreFirst(cardItems(['window']).map((it) => ({ ...it, group: '' })))

// the vocab's types and parameters come from cards too: a missing `core` is the core
const words = (slug) => aliasesOf(taskIndex.value[slug])
export const roleItems = () => coreFirst(Object.entries(vocab.value.roles).map(([key, r]) =>
  ({ key, title: r.label, icon: r.icon, group: r.group, desc: r.desc, hint: COINS[r.coin] || '', words: words(r.slug), tag: tag(r.core === false) })))
export const statItems = (taken) => coreFirst(vocab.value.stats.map((s) =>
  ({ key: s.key, title: s.label, icon: s.icon, desc: s.desc, hint: s.unit, words: words(s.slug), taken: taken?.has(s.key), stat: s, tag: tag(s.core === false) })))

// a word of a rule as a row; its sentence shape is the description: «А стає … на … тіків»
const shape = (tpl) => tpl.replace(/[[\]]/g, '').replace(/\{a\}/g, 'А').replace(/\{b\}/g, 'Б').replace(/\{\w+(:\+)?\}/g, '…')
export const wordItems = (dic) => Object.entries(vocab.value[dic] || {}).map(([key, w]) => ({ key, title: w.label, group: w.group, desc: shape(w.tpl) }))
