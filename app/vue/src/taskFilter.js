import { computed, inject, nextTick, provide } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { asked } from './asked.js'
import { aliasesOf, kidsOf, tasks, zones } from './catalog.js'
import { isMore, stateOf } from './coreMode.js'

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

// the filter of a catalog not on /tasks (T318, CatalogWindow): its state lives in an object, not in the address —
// reactive { q, game, algo, zone, sub, all, more } and `only(task)`: the cards the place is about
const KEY = 'task-filter'
export const provideTaskFilter = (state) => provide(KEY, state)
// what a card marks in its text: the words searched for
export function useTaskQuery() {
  const local = inject(KEY, null)
  const route = useRoute()
  return computed(() => (local ? local.q : route.query.q) || '')
}
// «Основа · Усі» (coreMode.js): its state — the window's own or the page's — and whether the cards «за запитом» wait
// behind their rows now: a search by words finds among all of them
export function useCardsMode() {
  const s = stateOf(inject(KEY, null))
  const q = useTaskQuery()
  return { s, coreOnly: computed(() => !s.all && !q.value) }
}

export function useTaskFilter(fixedGame = '') {
  const route = useRoute()
  const router = useRouter()
  const local = inject(KEY, null)
  const src = computed(() => local || route.query)
  const { s: mode, coreOnly } = useCardsMode()
  const hidden = (t) => coreOnly.value && asked(t)

  const f = computed(() => ({
    q: src.value.q || '', game: fixedGame || src.value.game || '', algo: src.value.algo === '1',
    zone: src.value.zone || '', sub: src.value.sub || '',
  }))

  async function set(patch) {
    if (local) return Object.assign(local, patch)
    const q = { ...route.query, ...patch }
    for (const k in q) if (!q[k]) delete q[k]
    await router.replace({ query: q })
    if (!('zone' in patch)) return
    await nextTick()  // scroll once the new list is in the DOM: a shorter list would clamp the position back down
    document.getElementById('catalog')?.scrollIntoView()  // guide block above: keep the catalog head on top
  }

  // a family is in when one of its cards is
  const inScope = (t) => !local?.only || local.only(t) || (kidsOf.value[t.slug] || []).some(local.only)

  function matches(t) {
    if (!inScope(t)) return false
    if (f.value.game === 'universal') { if (t.games.length) return false }
    else if (f.value.game && !t.games.includes(f.value.game)) return false
    if (f.value.algo && !t.tags.includes('algo')) return false
    if (!f.value.q) return true
    const kids = kidsOf.value[t.slug] || []
    const hay = norm([t.title, t.slug, t.description, ...t.tags, ...aliasesOf(t),
                      ...kids.map((k) => `${k.title} ${k.description} ${aliasesOf(k).join(' ')}`)].join(' '))
    return hay.includes(norm(f.value.q))
  }

  // roots only (a family counts as one card); everything except the zone filter — so the nav shows where matches live
  const found = computed(() => tasks.value.filter((t) => !t.parent && matches(t)))

  // what is shown: the cards «за запитом» behind their rows are not counted
  const counts = computed(() => {
    const shown = found.value.filter((t) => !hidden(t))
    const c = { '': shown.length }
    for (const t of shown) {
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
        // `more` — how many wait behind the row, shown in place once it is opened; a subcategory with nothing in the core
        // stays as its heading and that row: the taxonomy is whole
        const more = list.filter(hidden).length
        if (list.length) subs.push({ key: sk, title, icon, i, more, list: isMore(mode, `${zk}/${sk}`) ? list : list.filter((t) => !hidden(t)) })
      })
      if (subs.length) out.push({ key: zk, title: z.title, icon: z.icon, color: z.color, subs })
    }
    return out
  })

  // the categories and subcategories the catalog has cards of at all: every one on /tasks, the place's own in a window
  const subsIn = computed(() => (local?.only ? new Set(tasks.value.filter((t) => !t.parent && inScope(t)).map((t) => `${t.zone}/${t.subzone}`)) : null))
  const zonesIn = computed(() => (subsIn.value
    ? Object.fromEntries(Object.entries(zones.value).filter(([zk]) => [...subsIn.value].some((k) => k.startsWith(`${zk}/`))))
    : zones.value))

  return { f, set, counts, grouped, zonesIn, subsIn, local: !!local, mode, coreOnly, total: computed(() => found.value.length) }
}
