// what a thing means, under the mouse (T348): in the look of the site's explanations (style.css `.hint-box`), not the
// browser's black box a second late. It comes once the mouse stops on the element — a sweep across a list shows
// nothing — and while one is up the next comes at once; it goes as the mouse leaves or clicks. Keyboard focus shows it
// too, and so does a tap where there is no mouse.
//   v-hint="'ще готується'"   v-hint="{ title: 'Механіки', text: 'картки каталогу на сутності' }"   (\n — a new line)
const WAIT = 300, QUICK = 60, COOL = 400
let box = null, owner = null, timer = 0, warm = 0
// where the mouse was before this event: a page scrolled under a still mouse sends moves that are no moves (peek.js)
let at = {}
const still = (e) => e.screenX === at.x && e.screenY === at.y
const touch = () => !matchMedia('(hover: hover)').matches
const textOf = (v) => (!v ? '' : typeof v === 'string' ? v : [v.title, v.text].filter(Boolean).join(' — '))

// over the element — where the mouse came from in a list going down; no room under the shelf at the top — under it
function fill(el) {
  const v = el._hint, b = document.createElement('b')
  b.textContent = v.title
  box.replaceChildren(...(typeof v === 'string' ? [v] : v.text ? [b, ` — ${v.text}`] : [b]))
  const r = el.getBoundingClientRect()
  const shelf = (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 0) + 4
  const top = r.top - box.offsetHeight - 5
  box.style.top = `${top >= shelf ? top : r.bottom + 5}px`
  box.style.left = `${Math.max(8, Math.min(r.left, innerWidth - box.offsetWidth - 8))}px`
}
function show(el) {
  if (!el.isConnected || !el._hint) return
  box ??= Object.assign(document.createElement('div'), { className: 'hint-box', role: 'tooltip' })
  box.style.animation = Date.now() < warm ? 'none' : ''  // one after another — no fade each time
  document.body.append(box)
  owner = el
  warm = Infinity
  fill(el)
}
function hide() {
  clearTimeout(timer)
  if (!owner) return
  box.remove()
  owner = null
  warm = Date.now() + COOL
}

if (typeof document !== 'undefined') {
  document.addEventListener('mousemove', (e) => (at = { x: e.screenX, y: e.screenY }), { passive: true })  // after the elements' own
  addEventListener('scroll', hide, { passive: true, capture: true })
  document.addEventListener('keydown', (e) => e.key === 'Escape' && hide())
}

function move(e) {
  const el = e.currentTarget
  if (owner === el || still(e)) return
  clearTimeout(timer)
  timer = setTimeout(() => show(el), Date.now() < warm ? QUICK : WAIT)
}
const leave = (e) => (!owner || owner === e.currentTarget) && hide()
const focus = (e) => (touch() || e.target.matches(':focus-visible')) && show(e.currentTarget)
const EVENTS = [['mousemove', move], ['mouseleave', leave], ['mousedown', hide], ['focusin', focus], ['focusout', leave]]
// the words, for a screen reader too; false — they are the same as before
function say(el, v) {
  const text = textOf(v)
  if (text === el._hintText) return false
  el._hint = v
  el._hintText = text
  if (text) el.setAttribute('aria-description', text)
  else el.removeAttribute('aria-description')
  return true
}

export const vHint = {
  mounted(el, { value }) {
    say(el, value)
    for (const [name, fn] of EVENTS) el.addEventListener(name, fn)
  },
  updated(el, { value }) {
    if (say(el, value) && owner === el) value ? fill(el) : hide()
  },
  beforeUnmount(el) {
    for (const [name, fn] of EVENTS) el.removeEventListener(name, fn)
    if (owner === el) hide()
  },
}
