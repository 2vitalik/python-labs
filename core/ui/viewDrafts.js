import { reactive } from 'vue'

import { load, save } from './local.js'

// a view changed and left unsaved waits in the browser (T315 §7): its query by slug; the tab wears a dot while one waits
const KEY = 'table-drafts'
const read = () => { try { return JSON.parse(load(KEY) || '{}') } catch { return {} } }
export const drafts = reactive(read())
const keep = () => save(KEY, JSON.stringify(drafts))
export function setDraft(slug, query) {
  drafts[slug] = query
  keep()
}
export function dropDraft(slug) {
  delete drafts[slug]
  keep()
}
