import { reactive, ref } from 'vue'

import { load, save } from './local.js'

// cards under the mouse (T284 §2, T287): hold the mouse over a mention of a thing — its card floats beside it; move into
// the card and it stays. Inside a card a mention is a way on, both ways: hold the mouse over it — its card opens from
// this one, a card off a card; click it — this card shows that thing, with a way back, and stays until closed.
//   v-peek="{ kind, id }"      the card comes on hover; a click stays the element's own
//   v-peek.pin="{ kind, id }"  a click opens the card at once and keeps it
// `cards` is the chain on screen, each { stack: [what, …], at }: the first hangs at a mention on the page, the next at a
// mention inside the one before; the first `pinned` of them were clicked and wait for Esc, the cross or a click outside.
// PeekHost draws the chain; the site says what a kind looks like: registerPeeks({ kind: Component })
export const peek = reactive({ cards: [], pinned: 0, host: 0 })
const views = {}
export const registerPeeks = (map) => Object.assign(views, map)
export const peekView = (kind) => views[kind]

// how long the mouse stands still on a mention before its card comes (T344) — the reader's own pace, remembered in this
// browser and changed on any card (PeekPace); there is no «never»: the way back to this choice is a card
export const PACES = { fast: [150, 'швидко'], calm: [400, 'звично'], slow: [900, 'повільно'], rare: [1800, 'після паузи'] }
export const pace = ref(PACES[load('peek-pace')] ? load('peek-pace') : 'calm')
export const setPace = (k) => { pace.value = k; save('peek-pace', k) }
// WAIT_IN — inside a card no sooner than this: a click must win the race; NEXT — a card is up already: the next comes fast;
// GRACE — the way from a mention to its card; LINGER — the mouse left a card and may come right back
const WAIT_IN = 550, NEXT = 150, GRACE = 250, LINGER = 350
const canHover = () => matchMedia('(hover: hover)').matches
let opening, closing
let pending = null  // the mention whose card is about to come, and where the mouse stood when the wait began
// where the mouse really is on the screen: a page scrolled under a still mouse «enters» things too — they do not answer
let at = {}
const still = (e) => e.screenX === at.x && e.screenY === at.y
const hush = () => { clearTimeout(opening); pending = null }
if (typeof document !== 'undefined') {
  document.addEventListener('mousemove', (e) => { at = { x: e.screenX, y: e.screenY } }, { passive: true })
  addEventListener('scroll', hush, { passive: true, capture: true })
}

const rectOf = (el) => { const r = el.getBoundingClientRect(); return { left: r.left + scrollX, top: r.top + scrollY, width: r.width, height: r.height } }
const same = (a, b) => a.kind === b.kind && a.id === b.id
// a mention on the page opens card 0, a mention inside card k — card k + 1
const levelOf = (el) => { const card = el.closest('.peek-card'); return card ? +card.dataset.k + 1 : 0 }

function cut(n) {
  clearTimeout(closing)
  peek.cards.splice(n)
  peek.pinned = Math.min(peek.pinned, peek.cards.length)
}
function open(what, el, level, pinned) {
  hush()
  clearTimeout(closing)
  peek.cards.splice(level, Infinity, { stack: [what], at: rectOf(el) })
  peek.pinned = pinned ? level + 1 : Math.min(peek.pinned, level)
}
// card n and those opened from it go after a moment — unless the mouse comes back; the pinned ones stay
function later(n, ms) {
  clearTimeout(closing)
  closing = setTimeout(() => cut(Math.max(n, peek.pinned)), ms)
}
export function close(n = 0) {
  clearTimeout(opening)
  cut(n)
}
export const stay = (k) => later(k + 1, LINGER)  // the mouse is in card k: it stays, a card opened from it and left — goes
export const leave = () => later(0, LINGER)
export const pin = (k) => (peek.pinned = Math.min(peek.cards.length, Math.max(peek.pinned, k + 1)))  // a click that closed the cards pins nothing
export function go(k, what) {
  clearTimeout(opening)
  cut(k + 1)
  peek.cards[k].stack.push(what)
  pin(k)
}
export function back(k) {
  cut(k + 1)
  peek.cards[k].stack.pop()
}

// the wait begins — and begins anew while the mouse travels over the mention: the card comes once it has stopped
function arm(el, e) {
  const level = levelOf(el)
  if (!el._peek || el._quiet || !peek.host || !canHover() || level < peek.pinned) return
  const up = peek.cards[level]
  if (up?.stack.length === 1 && same(up.stack[0], el._peek)) return clearTimeout(closing)  // back on the mention whose card is up
  const wait = PACES[pace.value][0]
  clearTimeout(opening)
  pending = { el, x: e.screenX, y: e.screenY }
  opening = setTimeout(() => open(el._peek, el, level, false), level ? Math.max(WAIT_IN, wait) : peek.cards.length ? Math.min(NEXT, wait) : wait)
}
const enter = (e) => still(e) || arm(e.currentTarget, e)
function move(e) {
  if (e._peek || still(e)) return
  e._peek = true  // a mention inside a mention: the inner one answers
  const el = e.currentTarget
  if (pending?.el !== el || Math.hypot(e.screenX - pending.x, e.screenY - pending.y) > 4) arm(el, e)
}
function away(e) {
  hush()
  e.currentTarget._quiet = false
  later(levelOf(e.currentTarget), GRACE)
}
function click(e) {
  const el = e.currentTarget, level = levelOf(el)
  if (!el._peek || !peek.host) return
  if (level || el._pin) {  // not the element's own click: at the target a capturing listener runs first
    e.stopImmediatePropagation()
    e.preventDefault()
    if (level) go(level - 1, el._peek)
    else open(el._peek, el, 0, true)
  } else {  // the element's own click takes over: no card till the mouse has left and come back
    el._quiet = true
    close()
  }
}

export const vPeek = {
  mounted(el, b) {
    Object.assign(el, { _peek: b.value, _pin: !!b.modifiers.pin })
    if (el.closest('.peek-card')) el.classList.add('peek-link')
    el.addEventListener('mouseenter', enter)
    el.addEventListener('mousemove', move)
    el.addEventListener('mouseleave', away)
    el.addEventListener('click', click, true)
  },
  updated(el, b) { el._peek = b.value },
  unmounted(el) {
    el.removeEventListener('mouseenter', enter)
    el.removeEventListener('mousemove', move)
    el.removeEventListener('mouseleave', away)
    el.removeEventListener('click', click, true)
  },
}
