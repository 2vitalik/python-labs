import { ref } from 'vue'

import { getGuide } from './api.js'

// guide sections in reading order: slug = data/guide/<slug>.md; `page` = own route rendered by GuidePage
export const SECTIONS = [
  { slug: 'game', path: '/games', nav: 'Ігри' },  // text on top of the catalog page (GuideHead)
  { slug: 'labs', path: '/labs', nav: 'Лаби', page: true },
  { slug: 'tasks', path: '/tasks', nav: 'Таски' },
  { slug: 'score', path: '/score', nav: 'Бали', page: true },
  { slug: 'howto', path: '/howto', nav: 'Здача', page: true },
]
export const CHANGES = { slug: 'changes', path: '/changes', nav: 'Що змінилось', page: true }  // not in the menu: linked from the home page
export const LABS = [1, 2, 3, 4, 5].map((n) => ({ slug: `lab${n}`, path: `/labs/${n}`, n }))
export const ALL = [...SECTIONS.flatMap((s) => (s.slug === 'labs' ? [s, ...LABS] : [s])), CHANGES]  // /guide page order

export const pages = ref({})  // slug → {title, brief, updated}; bodies come per page
let loading
export function loadGuide() {
  loading ??= getGuide().then((list) => (pages.value = Object.fromEntries(list.map((p) => [p.slug, p]))))
  return loading
}
