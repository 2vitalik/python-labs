import { labPages, loadLabPages, pathOf } from './labPages.js'

// where a guide page lives on this site, by its slug — for «Історія правок» (site.history.place): its address, the way
// to it, and for a lecture the catalogue of what differs from the lecturer's slides (T374)
const lab = (p) => (p.kind === 'common' ? p.nav : `Лаба ${p.lab}${p.part ? ` · ${p.nav}` : ''}`)

export function place(slug) {
  loadLabPages().catch(() => null)  // once a page load; the list is a ref — whoever reads this in a computed sees it come
  const n = Number(/^lec(\d+)$/.exec(slug)?.[1])
  if (n) return { path: `/lectures/${n}`, crumbs: [['/lectures', 'Лекції'], [`/lectures/${n}`, `Лекція ${n}`]],
                  more: { to: `/lectures/changes?lec=${n}`, text: 'Що змінено проти слайдів лектора — каталог змін' } }
  const old = /^old-lab(\d+)$/.exec(slug)?.[1]
  if (old) return { path: `/labs/old/${old}`, crumbs: [['/labs', 'Лаби'], [`/labs/old/${old}`, `Архів · лаба ${old}`]] }
  const p = labPages.value.find((x) => x.slug === slug)
  if (p) return { path: pathOf(p), crumbs: [['/labs', 'Лаби'], [pathOf(p), lab(p)]] }
  return { path: '/', crumbs: [] }
}
