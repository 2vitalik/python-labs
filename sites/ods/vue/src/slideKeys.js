import { onMounted, onUnmounted, ref } from 'vue'

import { box as shot } from '@core/lightbox.js'

// a screen of a slide that scrolls: down (1) or up (-1)
export const turn = (body, step) => body.scrollBy({ top: step * 0.85 * body.clientHeight,
  behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' })

// how a reader walks the slides (T359 §4): ← → PgUp PgDn Space or a swipe, F — the whole screen of `root`; there the bar
// and the pointer step aside after 2.5 s without a move (`idle`, `wake` on mousemove). O — the lecturer's own slide
// (`orig`, SlideOrig: it lets go of it when there are none). `go(±1)` is the component's
export function useSlideKeys(root, body, go, orig) {
  const idle = ref(false)
  const canFull = document.fullscreenEnabled
  // a browser may refuse (no gesture, a frame without the right): the slides stay as they are
  const full = () => (document.fullscreenElement ? document.exitFullscreen() : root.value.requestFullscreen()).catch(() => {})

  let timer
  function wake() {
    idle.value = false
    clearTimeout(timer)
    if (document.fullscreenElement) timer = setTimeout(() => (idle.value = true), 2500)
  }
  // a slide that scrolls (slideFit.js) is read to its end first: a key pages its body, and only from the very bottom
  // (← from the top) the next slide comes — a clicker sends these keys too. The bar's ‹ › and a swipe go straight on;
  // so do the keys over the lecturer's picture
  function page(step) {
    const b = body.value
    const room = orig.value || !b?.classList.contains('scroll') ? 0 : step > 0 ? b.scrollHeight - b.clientHeight - b.scrollTop : b.scrollTop
    if (room > 1) turn(b, step)
    return room > 1
  }
  // an open picture (the lightbox) takes ← → for itself; а and щ — F and O on the Ukrainian layout
  function key(e) {
    if (shot.value || e.altKey || e.ctrlKey || e.metaKey || e.target.closest?.('input, textarea, select, [contenteditable]')) return
    const step = { ArrowRight: 1, PageDown: 1, ' ': 1, ArrowLeft: -1, PageUp: -1 }[e.key]
    const letter = e.key.toLowerCase()
    if (step) {
      e.preventDefault()
      if (!page(step)) go(step)
    } else if (canFull && ['f', 'а'].includes(letter)) full()
    else if (['o', 'щ'].includes(letter)) orig.value = !orig.value
  }

  // a swipe: sideways more than 50 px and half as much again as it went up or down (up and down scroll the body)
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
