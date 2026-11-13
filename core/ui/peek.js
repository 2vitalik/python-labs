import { reactive } from 'vue'

// a card under the mouse (T284 §2): hold the mouse over a mention of a thing — its card floats beside it; move into the
// card and it stays; a click inside goes on to the thing clicked, with a way back. One card at a time, drawn by PeekHost.
//   v-peek="{ kind, id }"      the card comes on hover; a click stays the element's own
//   v-peek.pin="{ kind, id }"  a click opens the card at once and keeps it
// inside a card every v-peek is a link to the next card. The site says what a kind looks like: registerPeeks({ kind: Component })
export const peek = reactive({ stack: [], at: null, pinned: false, host: 0 })
const views = {}
export const registerPeeks = (map) => Object.assign(views, map)
export const peekView = (kind) => views[kind]

const WAIT = 450, GRACE = 250
const canHover = () => matchMedia('(hover: hover)').matches
let timer

const rectOf = (el) => { const r = el.getBoundingClientRect(); return { left: r.left + scrollX, top: r.top + scrollY, width: r.width, height: r.height } }
function open(what, el, pinned) {
  clearTimeout(timer)
  Object.assign(peek, { stack: [what], at: rectOf(el), pinned })
}
export function close() {
  clearTimeout(timer)
  Object.assign(peek, { stack: [], pinned: false })
}
export const stay = () => clearTimeout(timer)
export function leave() {
  clearTimeout(timer)
  if (!peek.pinned) timer = setTimeout(close, GRACE)
}
export const go = (what) => { peek.stack.push(what); peek.pinned = true }
export const back = () => peek.stack.pop()

const inCard = (el) => !!el.closest('.peek-card')
function enter(e) {
  const el = e.currentTarget
  if (!el._peek || !peek.host || !canHover() || peek.pinned || inCard(el)) return
  clearTimeout(timer)
  timer = setTimeout(() => open(el._peek, el, false), peek.stack.length ? 120 : WAIT)  // a card is up already: the next comes fast
}
function click(e) {
  const el = e.currentTarget
  if (!el._peek || !peek.host) return
  if (inCard(el) || el._pin) {  // not the element's own click: at the target a capturing listener runs first
    e.stopImmediatePropagation()
    e.preventDefault()
    if (inCard(el)) go(el._peek)
    else open(el._peek, el, true)
  } else close()  // the element's own click takes over
}

export const vPeek = {
  mounted(el, b) {
    Object.assign(el, { _peek: b.value, _pin: !!b.modifiers.pin })
    if (inCard(el)) el.classList.add('peek-link')
    el.addEventListener('mouseenter', enter)
    el.addEventListener('mouseleave', leave)
    el.addEventListener('click', click, true)
  },
  updated(el, b) { el._peek = b.value },
  unmounted(el) {
    el.removeEventListener('mouseenter', enter)
    el.removeEventListener('mouseleave', leave)
    el.removeEventListener('click', click, true)
  },
}
