import { computed, toValue } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { site } from './site.js'

// filters of /students; the state lives in the URL, so a slice can be bookmarked:
// ?group=A,B — only these groups (NONE = «no group») · ?seen=1 / ?gh=0 … — only those who have it / who don't
const NONE = '-'
const SEEN = { key: 'seen', text: '🔑 вхід', title: 'Вхід на сайт', has: (s) => s.seen }
const REST = [
  { key: 'gh', text: '🐙 git', title: 'GitHub-репозиторій', has: (s) => s.github },
  { key: 'nick', text: '✈️ нік', title: 'Нікнейм у Telegram', has: (s) => s.tg_username },
  { key: 'bot', text: '🤖 бот', title: 'Бот привʼязаний', has: (s) => s.tg_linked },
]
const label = (key) => (key === NONE ? 'Без групи' : key)
// on a chip: «ПЗПІ-25-1» → «25-1», «ПЗПІи-25-1» → «25-1и», no group → «—»
const short = (key) => (key === NONE ? '—' : key.replace(/^\p{Lu}+(\p{Ll}*)-(.+)$/u, '$2$1'))
// «ПЗПІ-25-3» → «ПЗПІ-25»: the regular groups of a year share the «25-*» chip; «-0» and «ПЗПІи» stay out of it
const year = (key) => key.match(/^(\p{Lu}+-\d+)-[1-9]\d*$/u)?.[1]

// groups of test students go last, «no group» right before them
export function byGroup(students) {
  const by = new Map()
  for (const s of students) by.set(s.group, [...(by.get(s.group) || []), s])
  return [...by].map(([name, list]) => ({ name, list, test: list.every((s) => s.test) }))
    .sort((a, b) => a.test - b.test || (a.name === '') - (b.name === '') || a.name.localeCompare(b.name))
}

export function useStudentFilter(students) {
  const FACETS = [SEEN, ...site.students.facets, ...REST]  // the site's own go after «вхід»
  const route = useRoute()
  const router = useRouter()
  const keys = computed(() => (route.query.group ? String(route.query.group).split(',') : []))
  const inGroup = (s) => !keys.value.length || keys.value.includes(s.group || NONE)
  // a button counts what it would leave, so its own filter (`skip`) stays out of its number
  const fits = (s, skip) => FACETS.every((f) => f.key === skip || !route.query[f.key] || !!f.has(s) === (route.query[f.key] === '1'))

  const shown = computed(() => toValue(students).filter((s) => inGroup(s) && fits(s)))
  const active = computed(() => keys.value.length > 0 || FACETS.some((f) => route.query[f.key]))
  // a chip stands for one group or, «25-*», for a whole year of them; pressed = every group of it is picked
  const chip = (list, text, name) => ({
    text, name, keys: list.map((g) => g.key), on: list.every((g) => keys.value.includes(g.key)), n: list.reduce((n, g) => n + g.n, 0),
  })
  const groups = computed(() => {
    const all = byGroup(toValue(students)).map(({ name, list }) => ({ key: name || NONE, n: list.filter((s) => fits(s)).length }))
    const years = {}
    for (const g of all) if (year(g.key)) (years[year(g.key)] ||= []).push(g)
    const wild = Object.entries(years).filter(([, list]) => list.length > 1)
      .map(([key, list]) => chip(list, `${short(key)}-*`, `${list[0].key} … ${list.at(-1).key}`))
    return [...wild, ...all.map((g) => chip([g], short(g.key), label(g.key)))]
  })
  // for the crumb and the title: a whole year reads as one name; several names go short, or the heading wraps
  const picked = computed(() => {
    const wild = groups.value.filter((g) => g.on && g.keys.length > 1)
    const list = groups.value.filter((g) => g.on && !wild.some((w) => w !== g && w.keys.includes(g.keys[0])))
    return list.map((g) => (list.length > 1 ? g.text : g.name))
  })
  const facets = computed(() => FACETS.map((f) => {
    const list = toValue(students).filter((s) => inGroup(s) && fits(s, f.key))
    const yes = list.filter((s) => f.has(s)).length
    return { ...f, value: route.query[f.key], n: { 1: yes, 0: list.length - yes } }
  }))

  const set = (patch) => router.replace({ query: { ...route.query, ...patch } })
  const toggleGroup = (g) => set({ group: (g.on ? keys.value.filter((k) => !g.keys.includes(k)) : [...new Set([...keys.value, ...g.keys])]).join() || undefined })
  const toggleFacet = (key, v) => set({ [key]: route.query[key] === v ? undefined : v })
  const reset = () => set(Object.fromEntries(['group', ...FACETS.map((f) => f.key)].map((k) => [k, undefined])))

  return { shown, picked, active, groups, facets, toggleGroup, toggleFacet, reset }
}
