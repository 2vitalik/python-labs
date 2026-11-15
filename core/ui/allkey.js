// a click with a modifier held acts on all its neighbours, not on its own place (T298), as Alt-click on a file's arrow in
// a GitHub PR or ⌥-click on a Finder triangle. The hint names ⌥ / Alt, yet Shift, ⌘ and Ctrl do the same: some Linux
// desktops keep Alt-click for moving windows. While ⌥ / Alt is down <html> wears `all-key` — the buttons that would act on
// all show it (style.css `.every`)
const mac = /mac|iphone|ipad/i.test(navigator.userAgentData?.platform || navigator.platform || '')
export const ALL_KEY = mac ? '⌥' : 'Alt'
export const ALL_HOW = `${ALL_KEY}-клік чи утримати`
export const toAll = (e) => !!e && (e.altKey || e.shiftKey || e.metaKey || e.ctrlKey)

const root = document.documentElement
const mark = (e) => root.classList.toggle('all-key', e.altKey)
addEventListener('keydown', mark)
addEventListener('keyup', mark)
addEventListener('blur', () => root.classList.remove('all-key'))
// Shift-click would also select the text from the last click to this one
addEventListener('mousedown', (e) => e.shiftKey && e.target.closest?.('.every') && e.preventDefault())

// a long press does the same (T300): a phone has no keys, and a mouse may hold too. While it is down the button wears
// `holding` — its words show, a ring fills; at HOLD ms it gets a click as if with Alt, there and then (a phone may never
// send the click of a long press), and the real click of the release is swallowed. A move, a scroll, a lift — no hold
const HOLD = 400
let from = null, held = null, timer = 0
function stop() {
  clearTimeout(timer)
  from?.el.classList.remove('holding')
  from = null
}
addEventListener('pointerdown', (e) => {
  stop()
  held = null
  const el = e.button === 0 && e.isPrimary && !toAll(e) && e.target.closest?.('.every')
  if (!el || el.disabled) return
  from = { el, x: e.clientX, y: e.clientY }
  el.classList.add('holding')
  timer = setTimeout(() => {
    stop()
    held = el
    navigator.vibrate?.(15)
    el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, altKey: true }))
  }, HOLD)
})
addEventListener('pointermove', (e) => from && Math.hypot(e.clientX - from.x, e.clientY - from.y) > 8 && stop())
for (const type of ['pointerup', 'pointercancel', 'scroll']) addEventListener(type, stop, true)
addEventListener('keydown', () => (held = null))
addEventListener('contextmenu', (e) => (from || held) && e.target.closest?.('.every') && e.preventDefault())
addEventListener('click', (e) => {
  if (!held || !e.isTrusted) return
  if (e.target.closest?.('.every') === held) {
    e.stopPropagation()
    e.preventDefault()
  }
  held = null
}, true)
