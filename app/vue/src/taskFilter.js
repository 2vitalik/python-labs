import { computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { kidsOf, tasks, zones } from './catalog.js'

// tolerant search over the RU/UA/EN mixed corpus: case + и/і + е/є folded
export const norm = (s) => String(s).toLowerCase().replace(/и/g, 'і').replace(/є/g, 'е')
const esc = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]))

// every match of q wrapped in <mark>; norm() keeps the length, so indices from the folded copy apply to the original
export function hl(text, q, escape = esc) {
  text = String(text ?? '')
  const n = norm(text), nq = norm(q || '')
  let out = '', i = 0, j
  while (nq && (j = n.indexOf(nq, i)) >= 0) {
    out += escape(text.slice(i, j)) + '<mark>' + escape(text.slice(j, j + nq.length)) + '</mark>'
    i = j + nq.length
  }
  return out + escape(text.slice(i))
}
// the same over rendered html: only the text between tags (already escaped by the renderer)
export const markHtml = (html, q) => (q ? html.split(/(<[^>]+>)/).map((s) => (s.startsWith('<') ? s : hl(s, q, (t) => t))).join('') : html)

export function useTaskFilter(fixedGame = '') {
  const route = useRoute()
  const router = useRouter()

  const f = computed(() => ({
    q: route.query.q || '', game: fixedGame || route.query.game || '', algo: route.query.algo === '1',
    zone: route.query.zone || '', sub: route.query.sub || '',
  }))

  async function set(patch) {
    const q = { ...route.query, ...patch }
    for (const k in q) if (!q[k]) delete q[k]
    await router.replace({ query: q })
    if (!('zone' in patch)) return
    await nextTick()  // scroll once the new list is in the DOM: a shorter list would clamp the position back down
    document.getElementById('catalog')?.scrollIntoView()  // guide block above: keep the catalog head on top
  }

  function matches(t) {
    if (f.value.game === 'universal') { if (t.games.length) return false }
    else if (f.value.game && !t.games.includes(f.value.game)) return false
    if (f.value.algo && !t.tags.includes('algo')) return false
    if (!f.value.q) return true
    const kids = kidsOf.value[t.slug] || []
    const hay = norm([t.title, t.slug, t.description, ...t.tags, ...kids.map((k) => `${k.title} ${k.description}`)].join(' '))
    return hay.includes(norm(f.value.q))
  }

  // roots only (a family counts as one card); everything except the zone filter — so the nav shows where matches live
  const found = computed(() => tasks.value.filter((t) => !t.parent && matches(t)))

  const counts = computed(() => {
    const c = { '': found.value.length }
    for (const t of found.value) {
      c[t.zone] = (c[t.zone] || 0) + 1
      c[`${t.zone}/${t.subzone}`] = (c[`${t.zone}/${t.subzone}`] || 0) + 1
    }
    return c
  })

  const grouped = computed(() => {
    const out = []
    for (const [zk, z] of Object.entries(zones.value)) {
      if (f.value.zone && zk !== f.value.zone) continue
      const subs = []
      Object.entries(z.subzones).forEach(([sk, [title, icon]], i) => {
        if (f.value.sub && sk !== f.value.sub) return
        const list = found.value.filter((t) => t.zone === zk && t.subzone === sk)
        if (list.length) subs.push({ key: sk, title, icon, i, list })
      })
      if (subs.length) out.push({ key: zk, title: z.title, icon: z.icon, color: z.color, subs })
    }
    return out
  })

  return { f, set, counts, grouped }
}
