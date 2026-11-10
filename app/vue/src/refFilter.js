import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { user } from '@core/user.js'
import { refKind } from './ideas.js'

// the filters of /ideas live in the address (?kind=idea&zone=entities&sub=roles&state=all&mine=1), so a view can be shared;
// no state means the new ones for the teacher (his queue) and everything for a student (his idea with its answer)
export function useRefFilter(refs) {
  const route = useRoute()
  const router = useRouter()
  const first = () => (user.value?.status === 'admin' ? 'inbox' : 'all')
  const f = computed(() => ({
    kind: route.query.kind || '', zone: route.query.zone || '', sub: route.query.sub || '',
    state: route.query.state || first(), mine: route.query.mine === '1',
  }))

  function set(patch) {
    const q = { ...route.query, ...patch }
    for (const k in q) if (!q[k] || (k === 'state' && q[k] === first())) delete q[k]
    router.replace({ query: q })
  }
  const clear = () => router.replace({ query: { state: 'all' } })

  const checks = {
    kind: (r, v) => !v.kind || refKind(r) === v.kind,
    zone: (r, v) => !v.zone || r.zone === v.zone,
    sub: (r, v) => !v.sub || r.subzone === v.sub,
    state: (r, v) => v.state === 'all' || (r.status || 'inbox') === v.state,
    mine: (r, v) => !v.mine || r.mine,
  }
  const pass = (r, ...skip) => Object.entries(checks).every(([k, ok]) => skip.includes(k) || ok(r, f.value))
  // a row's counts skip its own filter: each chip tells what picking it would show
  function tally(key, ...skip) {
    const c = { '': 0 }
    for (const r of refs.value) {
      if (!pass(r, ...skip)) continue
      c['']++
      const k = key(r)
      if (k) c[k] = (c[k] || 0) + 1
    }
    return c
  }
  const counts = computed(() => ({
    kind: tally(refKind, 'kind'),
    zone: tally((r) => r.zone, 'zone', 'sub'),
    sub: tally((r) => r.subzone, 'sub'),
    state: tally((r) => r.status || 'inbox', 'state'),
    mine: tally((r) => r.mine && 'mine', 'mine'),
  }))
  const shown = computed(() => refs.value.filter((r) => pass(r)))

  return { f, set, clear, counts, shown }
}
