// where a search stands in a lecture's text (FoundBar): slide N's first match, the next or the previous one; the page goes
// there at once — a smooth ride over a long text takes seconds — and the block lights up for a moment
const after = (a, b) => !!(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING)  // b comes after a
const padTop = () => parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0  // what sticks at the top

// the first match between slide `at`'s number and the next one → { i }; none there → { i: -1, mark } — the slide's start.
// A slide without a number of its own (a mark inside a list stays a comment) is the nearest numbered one before it
export function firstOf(root, ranges, at) {
  if (at === undefined) return { i: ranges.length ? 0 : -1 }
  const all = [...root.querySelectorAll('.slide-at')]
  const k = all.findLastIndex((m) => Number(m.textContent) <= Number(at)), mark = all[k], next = all[k + 1]
  const i = ranges.findIndex((r) => !mark || after(mark, r.startContainer))
  return i >= 0 && (!next || after(ranges[i].startContainer, next)) ? { i } : { i: -1, mark }
}

// where the reader's eye goes: a third down the window, under whatever sticks at the top
export const eyeLine = () => Math.max(padTop() + 16, innerHeight * 0.3)
// from the one stood on, round; none yet — from the eye's line
export function nextOf(ranges, cur, d) {
  const n = ranges.length, line = eyeLine()
  if (cur >= 0) return (cur + d + n) % n
  const i = d > 0 ? ranges.findIndex((r) => r.getBoundingClientRect().top > line) : ranges.findLastIndex((r) => r.getBoundingClientRect().bottom < line)
  return i >= 0 ? i : d > 0 ? 0 : n - 1
}

// a range or a block to the eye's line; one already in sight stays put
export function standOn(el, force = false) {
  const r = el.getBoundingClientRect()
  if (force || r.top < padTop() || r.bottom > innerHeight - 72) scrollBy({ top: r.top - eyeLine(), behavior: 'instant' })
}
let timer
export function flash(nodes) {
  const blocks = nodes.map((n) => (n.nodeType === 1 ? n : n.parentElement).closest('li, p, tr, h1, h2, h3, h4, blockquote, dd, dt, pre') || n)
  clearTimeout(timer)
  document.querySelectorAll('.flash').forEach((t) => t.classList.remove('flash'))
  void document.body.offsetWidth  // the same block lit twice runs its animation again
  blocks.forEach((b) => b.classList.add('flash'))
  timer = setTimeout(() => blocks.forEach((b) => b.classList.remove('flash')), 2500)
}
