import { reactive } from 'vue'

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

// WAIT — the mouse rests on a mention before its card comes (inside a card longer: a click must win the race);
// GRACE — the way from a mention to its card; LINGER — the mouse left a card and may come right back
const WAIT = 450, WAIT_IN = 550, GRACE = 350, LINGER = 600
const canHover = () => matchMedia('(hover: hover)').matches
let opening, closing

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
  clearTimeout(opening)
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

function enter(e) {
  const el = e.currentTarget, level = levelOf(el)
  if (!el._peek || !peek.host || !canHover() || level < peek.pinned) return
  const up = peek.cards[level]
  if (up?.stack.length === 1 && same(up.stack[0], el._peek)) return clearTimeout(closing)  // back on the mention whose card is up
  clearTimeout(opening)
  opening = setTimeout(() => open(el._peek, el, level, false), level ? WAIT_IN : peek.cards.length ? 150 : WAIT)  // a card is up already: the next comes fast
}
function away(e) {
  clearTimeout(opening)
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
  } else close()  // the element's own click takes over
}

export const vPeek = {
  mounted(el, b) {
    Object.assign(el, { _peek: b.value, _pin: !!b.modifiers.pin })
    if (el.closest('.peek-card')) el.classList.add('peek-link')
    el.addEventListener('mouseenter', enter)
    el.addEventListener('mouseleave', away)
    el.addEventListener('click', click, true)
  },
  updated(el, b) { el._peek = b.value },
  unmounted(el) {
    el.removeEventListener('mouseenter', enter)
    el.removeEventListener('mouseleave', away)
    el.removeEventListener('click', click, true)
  },
}
