import { reactive } from 'vue'

// the cards whose pencil is on (T310): such a card shows everything that may be changed or added on it — what is still
// empty, «＋» of what is not there yet, a minus by every row — and lights the values a click changes. Kept here, not in
// the card: the columns may deal the cards again (StableColumns), and a card born anew must stay as it was.
// An id is a part's, or `<part>:menu` — a window's transitions alone
const on = reactive(new Set())
export const toolsOn = (id) => on.has(id)
// `ids` — ⌥-click: every card of the section follows this one
export function setTools(id, v = !on.has(id), ids = [id]) {
  for (const k of ids) v ? on.add(k) : on.delete(k)
}
export const anyTools = () => on.size > 0
export const dropTools = () => on.clear()
