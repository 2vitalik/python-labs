import { computed, toValue } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// filters of /students; the state lives in the URL, so a slice can be bookmarked:
// ?group=A,B — only these groups (NONE = «no group») · ?seen=1 / ?gh=0 … — only those who have it / who don't
const NONE = '-'
const FACETS = [
  { key: 'seen', yes: '🔑 зайшли', no: 'ні', title: 'Вхід на сайт', has: (s) => s.seen },
  { key: 'game', yes: '🎮 гра', no: 'без', title: 'Гра створена', has: (s) => s.game.id },
  { key: 'gh', yes: 'GitHub', no: 'без', title: 'GitHub-репозиторій', has: (s) => s.github },
  { key: 'nick', yes: '✈️ нік', no: 'без', title: 'Нікнейм у Telegram', has: (s) => s.tg_username },
  { key: 'bot', yes: '🤖 бот', no: 'без', title: 'Бот привʼязаний', has: (s) => s.tg_linked },
]
const label = (key) => (key === NONE ? 'Без групи' : key)

// groups of test students go last, «no group» right before them
export function byGroup(students) {
  const by = new Map()
  for (const s of students) by.set(s.group, [...(by.get(s.group) || []), s])
  return [...by].map(([name, list]) => ({ name, list, test: list.every((s) => s.test) }))
    .sort((a, b) => a.test - b.test || (a.name === '') - (b.name === '') || a.name.localeCompare(b.name))
}

export function useStudentFilter(students) {
  const route = useRoute()
  const router = useRouter()
  const keys = computed(() => (route.query.group ? String(route.query.group).split(',') : []))
  const inGroup = (s) => !keys.value.length || keys.value.includes(s.group || NONE)
  // a button counts what it would leave, so its own filter (`skip`) stays out of its number
  const fits = (s, skip) => FACETS.every((f) => f.key === skip || !route.query[f.key] || !!f.has(s) === (route.query[f.key] === '1'))

  const shown = computed(() => toValue(students).filter((s) => inGroup(s) && fits(s)))
  const picked = computed(() => keys.value.map(label))
  const active = computed(() => keys.value.length > 0 || FACETS.some((f) => route.query[f.key]))
  const groups = computed(() => byGroup(toValue(students)).map(({ name, list }) => {
    const key = name || NONE
    return { key, name: label(key), on: keys.value.includes(key), n: list.filter((s) => fits(s)).length }
  }))
  const facets = computed(() => FACETS.map((f) => {
    const list = toValue(students).filter((s) => inGroup(s) && fits(s, f.key))
    const yes = list.filter((s) => f.has(s)).length
    return { ...f, value: route.query[f.key], n: { 1: yes, 0: list.length - yes } }
  }))

  const set = (patch) => router.replace({ query: { ...route.query, ...patch } })
  const toggleGroup = (key) => set({ group: (keys.value.includes(key) ? keys.value.filter((k) => k !== key) : [...keys.value, key]).join() || undefined })
  const toggleFacet = (key, v) => set({ [key]: route.query[key] === v ? undefined : v })
  const reset = () => set(Object.fromEntries(['group', ...FACETS.map((f) => f.key)].map((k) => [k, undefined])))

  return { shown, picked, active, groups, facets, toggleGroup, toggleFacet, reset }
}
