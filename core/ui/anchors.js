import { iconHtml } from './iconHtml.js'

// hash targets inside guide text: scroll, open enclosing <details>, flash the section for a moment
const HEADING = /^H[1-6]$/
const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches
let timer

// the band of the window nothing sticks over: under the menu (--nav-h, px) and a page's stuck heading (--stick-h, rem)
function band() {
  const css = getComputedStyle(document.documentElement)
  const px = (v) => (parseFloat(v) || 0) * (v.trim().endsWith('rem') ? parseFloat(css.fontSize) : 1)
  return px(css.getPropertyValue('--nav-h')) + px(css.getPropertyValue('--stick-h'))
}
// a thing just added (T296 §9): the page moves only when it is out of sight, and only as far as it takes
function reveal(el) {
  const r = el.getBoundingClientRect(), top = band()
  if (r.top >= top && r.bottom <= innerHeight) return
  const by = r.top < top || r.height > innerHeight - top ? r.top - top - 8 : r.bottom - innerHeight + 8
  scrollBy({ top: by, behavior: reduced() ? 'auto' : 'smooth' })
}

// `near` — the reader is already here (they have just added it): no jump to the top, the flash says where it is
export function flash(id, { near = false } = {}) {
  const el = id && document.getElementById(id)
  if (!el) return false
  for (let d = el.closest('details'); d; d = d.parentElement?.closest('details')) d.open = true
  const block = el.closest('li') || el.closest('h1, h2, h3, h4, p, tr') || el
  const targets = [block]
  if (HEADING.test(block.tagName)) {  // a heading lights up with its section: up to the next heading of the same or higher level
    for (let n = block.nextElementSibling; n && !(HEADING.test(n.tagName) && n.tagName <= block.tagName); n = n.nextElementSibling) targets.push(n)
  }
  // a target screens away is reached at once: a smooth ride over a long text takes seconds
  const far = Math.abs(block.getBoundingClientRect().top) > 2 * innerHeight
  if (near) reveal(block)
  else block.scrollIntoView({ block: 'start', behavior: far ? 'instant' : reduced() ? 'auto' : 'smooth' })  // 'auto' obeys Bootstrap's smooth
  if (el.closest('.noflash')) return true  // catalog zones, the /method contents box: scroll only, the colour would cover a whole block
  clearTimeout(timer)
  document.querySelectorAll('.flash').forEach((t) => t.classList.remove('flash'))
  void block.offsetWidth  // restart the animation when the same target is hit twice
  targets.forEach((t) => t.classList.add('flash'))
  timer = setTimeout(() => targets.forEach((t) => t.classList.remove('flash')), 2500)
  return true
}

export const toTop = () => window.scrollTo({ top: 0, behavior: reduced() ? 'auto' : 'smooth' })

export async function copyLink(a) {
  const url = location.origin + location.pathname + a.getAttribute('href')
  try { await navigator.clipboard.writeText(url) } catch { return }
  a.innerHTML = iconHtml('check')
  setTimeout(() => (a.innerHTML = iconHtml('link')), 1500)
}

// clicks inside rendered markdown: the link icon copies, #hash scrolls+flashes, site links go through the router
export function guideClick(e, router) {
  const a = e.target.closest('a')
  if (!a || e.metaKey || e.ctrlKey || a.target === '_blank') return
  const href = a.getAttribute('href') || ''
  const query = router.currentRoute.value.query  // a hash-only location would drop the catalog's ?filters
  if (a.classList.contains('link')) {
    e.preventDefault()
    router.replace({ query, hash: href })
    copyLink(a)
  } else if (href.startsWith('#')) {
    e.preventDefault()
    router.push({ query, hash: href })
    flash(href.slice(1))
  } else if (href.startsWith('/')) {
    e.preventDefault()
    router.push(href)
  }
}
