import { plural } from './plural.js'
import { dayMonth } from './table.js'
import { viewOf } from './viewStore.js'

// a view's use and origin in words (T315 §7, §9), the same on its hover card and in the library
const times = (n) => `${n} ${plural(n, 'раз', 'рази', 'разів')}`
const spent = (s) => (s >= 3600 ? `${Math.round(s / 360) / 10} год` : s >= 60 ? `${Math.round(s / 60)} хв` : '')

// «працював 4 рази · востаннє 12.11 · разом 37 хв» · «лише відкривав · 3 рази» · «ще не відкривав»
export function workLine(v) {
  if (v.uses) return [`працював ${times(v.uses)}`, `востаннє ${dayMonth(v.used_at)}`, spent(v.seconds) && `разом ${spent(v.seconds)}`].filter(Boolean).join(' · ')
  return v.opens ? `лише відкривав · ${times(v.opens)}` : 'ще не відкривав'
}
export const worked = (v) => v.uses > 0
// when it was last in hands, to order by: worked on beats merely opened
export const lastTouch = (v) => v.used_at || v.opened_at || ''

// «зроблено з „Лаба 1“ · версії 2» — or whose it is, when made of nothing
export function originLine(v) {
  if (!v.parent) return v.by ? '' : 'вид сайту'
  const p = viewOf(v.parent)
  return `зроблено з «${p ? p.title : v.parent}»${p ? '' : ' (видалено)'}${v.parent_version ? ` · версії ${v.parent_version}` : ''}`
}
