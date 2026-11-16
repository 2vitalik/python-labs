// a heading that sticks over its block — a section's, a card's (T306): while it is stuck, a click on its empty space goes
// back to the block's start, the heading landing where it stands in the flow. `v-to-start="'секції'"` — the word of the
// hint; whatever acts in the heading (a button, a link, a value edited in place) keeps its own click
const ACTIVE = 'a, button, input, textarea, select, label, [role=button], [tabindex]'
const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches

// how far the block's start is above the heading: < 0 — the heading is stuck over the block's middle
function above(head) {
  const block = head.parentElement
  const edge = parseFloat(getComputedStyle(block).borderTopWidth) || 0
  return block.getBoundingClientRect().top + edge - head.getBoundingClientRect().top
}
function click(e) {
  const head = e.currentTarget
  const own = e.target.closest(ACTIVE)
  if (own && own !== head && head.contains(own)) return
  const by = above(head)
  if (by >= -1) return
  scrollBy({ top: by, behavior: reduced() ? 'auto' : 'smooth' })
  head.classList.remove('head-stuck')  // at the start it stands in the flow: no more «to the start» under the mouse
  head.title = ''
}
function hover(e) {
  const head = e.currentTarget
  const stuck = above(head) < -1
  if (head.classList.contains('head-stuck') === stuck) return
  head.classList.toggle('head-stuck', stuck)
  head.title = stuck ? `Клік — на початок ${head._word}` : ''
}

export const vToStart = {
  mounted(el, b) {
    el._word = b.value || 'блока'
    el.addEventListener('click', click)
    el.addEventListener('pointerenter', hover)
    el.addEventListener('pointermove', hover)
  },
  updated(el, b) { el._word = b.value || 'блока' },
  unmounted(el) {
    el.removeEventListener('click', click)
    el.removeEventListener('pointerenter', hover)
    el.removeEventListener('pointermove', hover)
  },
}
