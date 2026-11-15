// a click with a modifier held acts on all its neighbours, not on its own place (T298), as Alt-click on a file's arrow in
// a GitHub PR or ⌥-click on a Finder triangle. The hint names ⌥ / Alt, yet Shift, ⌘ and Ctrl do the same: some Linux
// desktops keep Alt-click for moving windows. While ⌥ / Alt is down <html> wears `all-key` — the buttons that would act on
// all show it (style.css `.every`)
const mac = /mac|iphone|ipad/i.test(navigator.userAgentData?.platform || navigator.platform || '')
export const ALL_KEY = mac ? '⌥' : 'Alt'
export const toAll = (e) => !!e && (e.altKey || e.shiftKey || e.metaKey || e.ctrlKey)

const root = document.documentElement
const mark = (e) => root.classList.toggle('all-key', e.altKey)
addEventListener('keydown', mark)
addEventListener('keyup', mark)
addEventListener('blur', () => root.classList.remove('all-key'))
// Shift-click would also select the text from the last click to this one
addEventListener('mousedown', (e) => e.shiftKey && e.target.closest?.('.every') && e.preventDefault())

