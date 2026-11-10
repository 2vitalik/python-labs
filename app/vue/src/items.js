import { aliasesOf, COINS, kidsOf, kindOf, subzoneTitle, taskIndex, tasks, vocab, zones } from './catalog.js'

// rows for Picker.vue built from the catalog and the vocab: what may be picked where (T270 §5)

const coin = (t) => COINS[t.coin] || ''
const home = (t) => [zones.value[t.zone]?.title, subzoneTitle(t)].filter(Boolean).join(' · ')

// a card as a row: its coin, its home as the group, the description and the synonyms for the search; `taken` — slugs already here
export function cardItem(t, taken) {
  const parent = t.parent && taskIndex.value[t.parent]
  return {
    key: t.slug, title: parent ? `${parent.title}: ${t.title}` : t.title, icon: t.icon || coin(t) || '·', hint: t.icon ? coin(t) : '',
    group: home(t), desc: t.description || parent?.description, words: aliasesOf(t), taken: taken?.has(t.slug), task: t,
  }
}
// the cards of the given kinds one may claim (a family's parent is a heading — its children are the cards)
export const cardItems = (kinds, taken, filter = () => true) =>
  tasks.value.filter((t) => t.status !== 'archived' && kinds.includes(kindOf(t)) && !kidsOf.value[t.slug] && filter(t)).map((t) => cardItem(t, taken))
export const windowTypeItems = () => cardItems(['window']).map((it) => ({ ...it, group: '' }))

const words = (slug) => aliasesOf(taskIndex.value[slug])
export const roleItems = () => Object.entries(vocab.value.roles).map(([key, r]) =>
  ({ key, title: r.label, icon: r.icon, group: r.group, desc: r.desc, hint: COINS[r.coin] || '', words: words(r.slug) }))
export const statItems = (taken) => vocab.value.stats.map((s) =>
  ({ key: s.key, title: s.label, icon: s.icon, desc: s.desc, hint: s.unit, words: words(s.slug), taken: taken?.has(s.key), stat: s }))

// a word of a rule as a row; its sentence shape is the description: «А стає … на … тіків»
const shape = (tpl) => tpl.replace(/[[\]]/g, '').replace(/\{a\}/g, 'А').replace(/\{b\}/g, 'Б').replace(/\{\w+(:\+)?\}/g, '…')
export const wordItems = (dic) => Object.entries(vocab.value[dic] || {}).map(([key, w]) => ({ key, title: w.label, group: w.group, desc: shape(w.tpl) }))
