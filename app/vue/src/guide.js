import { ref } from 'vue'

import { getGuide } from './api.js'

// guide sections in reading order: slug = data/guide/<slug>.md; `page` = own route rendered by GuidePage
export const SECTIONS = [
  { slug: 'game', path: '/games', nav: 'Ігри' },  // text on top of the catalog page (GuideHead)
  { slug: 'labs', path: '/labs', nav: 'Лабораторні', page: true },
  { slug: 'tasks', path: '/tasks', nav: 'Завдання' },
  { slug: 'score', path: '/score', nav: 'Оцінювання', page: true },
  { slug: 'howto', path: '/howto', nav: 'Як здавати', page: true },
]
export const LABS = [1, 2, 3, 4, 5].map((n) => ({ slug: `lab${n}`, path: `/labs/${n}`, n }))
export const ALL = SECTIONS.flatMap((s) => (s.slug === 'labs' ? [s, ...LABS] : [s]))  // /guide page order

export const pages = ref({})  // slug → {title, brief, updated}; bodies come per page
let loading
export function loadGuide() {
  loading ??= getGuide().then((list) => (pages.value = Object.fromEntries(list.map((p) => [p.slug, p]))))
  return loading
}
