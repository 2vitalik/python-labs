import { reactive } from 'vue'

// «Основа · Усі» on the catalog (T319): with «Основа» the cards «за запитом» wait behind a dashed row at the end of their
// subcategory or family, a click there shows them in place. The state `{ all, more }` — /tasks's own, the reader's choice
// remembered; a window over a game (T318) keeps one in its filter. `more` — the scopes opened by their row, while the page lives
const KEY = 'tasks-all'
const page = reactive({ all: localStorage.getItem(KEY) === '1', more: {} })
export const stateOf = (local) => local || page
export const allRemembered = () => page.all

export function setAll(s, on) {
  s.all = on
  if (s === page) localStorage.setItem(KEY, on ? '1' : '0')
}
export const isMore = (s, key) => !!s.more?.[key]
export const toggleMore = (s, key) => { s.more = { ...s.more, [key]: !s.more?.[key] } }
