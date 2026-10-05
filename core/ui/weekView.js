import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { usePolling } from './activity.js'
import { getWeeks } from './api.js'
import { useStudentFilter } from './studentFilter.js'
import { slots, toCells } from './week.js'
import { soften, stuck } from './weekIf.js'
import { arrange } from './weekStrips.js'
import { best, lay, tally, windows } from './weekSum.js'

// /week for the teacher (T177, T186): what the overview and a day's page share. The view lives in the URL — it can be bookmarked
// and goes along between them: ?group= · ?len= (minutes) · ?view=heat · ?layer= · ?sort=name · ?soft=2,4 · ?stuck=0 · ?demo=50
export const LAYERS = { no: 'Не можуть', meh: 'Незручно', ok: 'Найкраще' }
const NARROW = '(max-width: 767.98px)'  // six days of strips don't fit a phone, the numbers do

export function useWeekView() {
  const route = useRoute()
  const router = useRouter()
  const data = ref(null)
  const error = ref('')
  const set = (patch) => router.replace({ query: { ...route.query, ...patch } })
  // a value of the address; the usual one stays out of it
  const param = (key, usual, parse = String) => computed({
    get: () => (route.query[key] === undefined ? usual : parse(route.query[key])),
    set: (v) => set({ [key]: v === usual ? undefined : v }),
  })
  const len = param('len', 90, (v) => (Number(v) > 0 ? Number(v) : 90))
  const view = param('view', matchMedia(NARROW).matches ? 'heat' : 'strips')
  const layer = param('layer', 'no', (v) => (v in LAYERS ? v : 'no'))
  const sort = param('sort', 'busy', (v) => (v === 'name' ? v : 'busy'))
  const withStuck = computed({ get: () => route.query.stuck !== '0', set: (v) => set({ stuck: v ? undefined : '0' }) })
  const soft = computed({  // the reasons counted as «незручно»: indexes of CATS (weekWhy.js)
    get: () => new Set(String(route.query.soft || '').split(',').filter(Boolean).map(Number)),
    set: (v) => set({ soft: [...v].sort().join() || undefined }),
  })
  const demo = computed(() => Number(route.query.demo) || 0)
  const day = computed(() => (route.params.day ? Number(route.params.day) - 1 : null))
  const skip = ref(true)  // the hours the teacher can't are no hours for a class
  const at = ref(null)  // the window pinned: its day and first row

  async function load() {
    try {
      const next = demo.value ? (await import('./weekDemo.js')).demoWeeks(demo.value) : await getWeeks()
      if (JSON.stringify(next) !== JSON.stringify(data.value)) data.value = next  // a refresh with nothing new redraws nothing
      error.value = ''
    } catch (e) {
      error.value = e.message
    }
  }
  watch(demo, load, { immediate: true })
  usePolling(() => demo.value || load(), 30)  // the numbers grow while the stream fills its weeks in

  const frame = computed(() => data.value?.frame)
  const { shown, groups: chips, toggleGroup } = useStudentFilter(() => data.value?.students || [])
  const mine = computed(() => data.value?.me && toCells(data.value.me.marks, frame.value))
  const all = computed(() => lay(soften(shown.value, soft.value), frame.value))
  const stuckOnes = computed(() => stuck(all.value, frame.value, len.value, mine.value))
  const out = computed(() => new Set(withStuck.value ? [] : stuckOnes.value.map((p) => p.s.nick)))
  const laid = computed(() => all.value.filter((p) => !out.value.has(p.s.nick)))
  const groups = computed(() => arrange(laid.value, shown.value.filter((s) => !out.value.has(s.nick)), sort.value))
  const total = computed(() => groups.value.reduce((n, g) => n + g.size, 0))
  const counts = computed(() => tally(laid.value, frame.value))
  const list = computed(() => windows(laid.value, frame.value, len.value, mine.value, groups.value))
  const busy = computed(() => list.value.some((w) => w.mine === 'no'))
  const open = computed(() => list.value.filter((w) => !skip.value || w.mine !== 'no'))
  // 1–5 of the week, the same on the overview and on a day's page; with nobody marked every window is as good as any
  const tops = computed(() => (laid.value.length ? best(open.value, len.value, 5) : []))
  const free = computed(() => (day.value === null ? open.value : open.value.filter((w) => w.day === day.value)))  // the list under the grid
  // the window that starts at a row; a start too late for a class is the last one that fits
  const windowAt = (d, row) => list.value.find((w) => w.day === d && w.r0 === Math.min(row, slots(frame.value) - w.n))
  const picked = computed(() => at.value && windowAt(at.value.day, at.value.r0))
  const pick = (d, row) => (at.value = d === null || picked.value === windowAt(d, row) ? null : { day: d, r0: row })

  return { data, error, frame, day, demo, chips, toggleGroup, shown, len, view, layer, sort, soft, withStuck, skip,
           mine, laid, groups, total, counts, list, busy, free, tops, stuckOnes, windowAt, picked, pick }
}
