import { onBeforeUnmount, onMounted, watch } from 'vue'

import { seenTableView } from './api.js'
import { viewOf } from './viewStore.js'

// «відкривав» or «працював» (T315 §9): a view on screen for OPEN ms was opened; WORK seconds of active time on it with ACTS
// actions is work. Active — the tab is in sight and something was done within IDLE; the seconds go to the API on leaving
const OPEN = 3000, IDLE = 60000, WORK = 60, ACTS = 5
const EVENTS = ['pointerdown', 'keydown', 'wheel']

export function useViewWork(slug) {
  let cur = '', opened = false, used = false, secs = 0, acts = 0, last = 0, timer, tick
  const tell = (body) => seenTableView(cur, body).catch(() => {})
  function mark(kind) {  // open | use: the view in hand counts it at once, the API is told
    const v = viewOf(cur)
    const now = new Date().toISOString()
    if (v) Object.assign(v, kind === 'open' ? { opens: v.opens + 1, opened_at: now } : { uses: v.uses + 1, used_at: now })
    tell({ [kind]: true })
  }
  function second() {
    if (document.visibilityState !== 'visible' || Date.now() - last > IDLE) return
    secs++
    if (used || secs < WORK || acts < ACTS) return
    used = true
    mark('use')
  }
  function stop(beacon = false) {
    clearTimeout(timer)
    clearInterval(tick)
    if (!cur || !opened || !secs) return
    const v = viewOf(cur)
    if (v) v.seconds += secs
    if (beacon) navigator.sendBeacon?.(`/api/views/${cur}/seen`, JSON.stringify({ seconds: secs }))  // the page is going: fetch would be cut
    else tell({ seconds: secs })
    secs = 0
  }
  function start(next) {
    stop()
    cur = next || ''
    opened = used = false
    secs = acts = 0
    last = Date.now()
    if (!cur) return
    timer = setTimeout(() => { opened = true; mark('open') }, OPEN)
    tick = setInterval(second, 1000)
  }
  const act = () => { acts++; last = Date.now() }
  const leave = () => stop(true)
  onMounted(() => {
    for (const e of EVENTS) document.addEventListener(e, act, { passive: true })
    addEventListener('pagehide', leave)
    watch(slug, (s) => start(s), { immediate: true })
  })
  onBeforeUnmount(() => {
    for (const e of EVENTS) document.removeEventListener(e, act)
    removeEventListener('pagehide', leave)
    stop()
  })
}
