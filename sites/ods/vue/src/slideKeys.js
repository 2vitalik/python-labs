import { onMounted, onUnmounted, ref } from 'vue'

import { box as shot } from '@core/lightbox.js'

// how a reader walks the slides (T359 §4): ← → PgUp PgDn Space or a swipe, F — the whole screen of `root`; there the bar
// and the pointer step aside after 2.5 s without a move (`idle`, `wake` on mousemove). `go(±1)` is the component's
export function useSlideKeys(root, go) {
  const idle = ref(false)
  const canFull = document.fullscreenEnabled
  const full = () => (document.fullscreenElement ? document.exitFullscreen() : root.value.requestFullscreen())

  let timer
  function wake() {
    idle.value = false
    clearTimeout(timer)
    if (document.fullscreenElement) timer = setTimeout(() => (idle.value = true), 2500)
  }
  // an open picture (the lightbox) takes ← → for itself
  function key(e) {
    if (shot.value || e.altKey || e.ctrlKey || e.metaKey || e.target.closest?.('input, textarea, select, [contenteditable]')) return
    const step = { ArrowRight: 1, PageDown: 1, ' ': 1, ArrowLeft: -1, PageUp: -1 }[e.key]
    if (step) {
      e.preventDefault()
      go(step)
    } else if (canFull && ['f', 'а'].includes(e.key.toLowerCase())) full()  // а — the same key on the Ukrainian layout
  }

  // a swipe: sideways more than 50 px and half as much again as it went up or down
  let touch = null
  const touchDown = (e) => (touch = e.touches.length === 1 ? e.touches[0] : null)
  function touchUp(e) {
    const dx = touch && e.changedTouches[0].clientX - touch.clientX, dy = touch && e.changedTouches[0].clientY - touch.clientY
    if (Math.abs(dx) > 50 && Math.abs(dx) > 1.5 * Math.abs(dy)) go(dx < 0 ? 1 : -1)
    touch = null
  }

  const ON = [['keydown', key], ['fullscreenchange', wake]]
  onMounted(() => ON.forEach(([event, fn]) => document.addEventListener(event, fn)))
  onUnmounted(() => {
    clearTimeout(timer)
    ON.forEach(([event, fn]) => document.removeEventListener(event, fn))
  })
  return { idle, canFull, full, wake, touchDown, touchUp }
}
