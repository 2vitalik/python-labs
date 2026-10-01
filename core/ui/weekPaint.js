import { onMounted, onUnmounted, ref } from 'vue'

import { slots } from './week.js'

const HOLD = 250  // ms a finger rests before it paints: a swipe is for scrolling the page
const SLOP = 8  // px it may wander meanwhile
const CALM = 300  // ms after a scroll when a touch is still its tail: the tap that stops a fling paints nothing

// strokes on the week grid: a mouse paints at once, a finger — after a hold, a tap — one cell.
// `area()` — the element the cells fill, `frame()` — the grid; `done(a, b)` gets the two corner cells of a finished stroke.
// `drag` — the corners while it goes on
export function usePaint(area, frame, done) {
  const drag = ref(null)
  let timer = 0
  let from = null  // where the finger came down
  let scrolled = 0

  function cell(p) {
    const box = area().getBoundingClientRect()
    const at = (v, size, n) => Math.min(n - 1, Math.max(0, Math.floor((v / size) * n)))  // off the grid — its edge
    return { day: at(p.clientX - box.left, box.width, frame().days), row: at(p.clientY - box.top, box.height, slots(frame())) }
  }
  function start(p) {
    document.activeElement?.blur()  // a reason being typed settles first
    drag.value = { a: cell(p), b: cell(p) }
  }
  function move(p) {
    const b = cell(p)
    if (b.day !== drag.value.b.day || b.row !== drag.value.b.row) drag.value = { ...drag.value, b }
  }
  function end() {
    const { a, b } = drag.value
    drag.value = null
    done(a, b)
  }
  function drop() {
    clearTimeout(timer)
    timer = 0
    drag.value = null
  }

  const mouse = (fn) => (e) => e.pointerType !== 'touch' && fn(e)
  const down = mouse((e) => {
    if (e.button) return
    area().setPointerCapture(e.pointerId)  // the stroke goes on when the pointer leaves the grid
    start(e)
  })
  const drive = mouse((e) => drag.value && move(e))
  const up = mouse(() => drag.value && end())

  function touch(e) {
    drop()
    if (e.touches.length > 1 || Date.now() - scrolled < CALM) return
    from = e.touches[0]
    timer = setTimeout(() => {
      timer = 0
      start(from)
      navigator.vibrate?.(10)
    }, HOLD)
  }
  function slide(e) {
    const t = e.touches[0]
    if (drag.value) {
      if (!e.cancelable) return drop()  // the page took the finger for a scroll
      e.preventDefault()  // or it scrolls under the stroke; pointer events can't stop that, touch events can
      move(t)
    } else if (timer && Math.hypot(t.clientX - from.clientX, t.clientY - from.clientY) > SLOP) drop()
  }
  function lift() {
    if (timer) {
      clearTimeout(timer)
      timer = 0
      start(from)
    }
    if (drag.value) end()
  }
  function scroll() {
    scrolled = Date.now()
    if (timer) drop()
  }
  const menu = (e) => e.preventDefault()  // a long press is a stroke here

  const EVENTS = [['pointerdown', down], ['pointermove', drive], ['pointerup', up], ['pointercancel', mouse(drop)], ['touchstart', touch, { passive: true }],
                  ['touchmove', slide, { passive: false }], ['touchend', lift], ['touchcancel', drop], ['contextmenu', menu]]
  onMounted(() => {
    EVENTS.forEach(([name, fn, options]) => area().addEventListener(name, fn, options))
    window.addEventListener('scroll', scroll, { passive: true })
  })
  onUnmounted(() => {
    clearTimeout(timer)
    window.removeEventListener('scroll', scroll)
  })
  return { drag }
}
