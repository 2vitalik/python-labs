import { watch } from 'vue'

import { toSaved } from './tableViews.js'
import { dropDraft, drafts, setDraft } from './viewDrafts.js'
import { createView, loadVersions, saveView, store } from './viewStore.js'

// what is done with the look on screen (T315 §7): saved into its view, made a view of its own, put back; and the draft —
// a look changed and not saved waits in the browser under its view, whatever way the page was left
export function viewActs({ route, router, slug, view, peek, state, dirty }) {
  const bare = (s) => router.replace({ query: { view: s } })
  // the sources apart: a getter's fresh array would always read as a change, and writing a draft would call this again
  watch([slug, dirty, () => JSON.stringify(toSaved(state.value))], ([s, changed, look]) => {
    if (!view.value || route.query.v) return  // nothing read yet · a past version looked at is no draft
    if (!changed) return drafts[s] && dropDraft(s)
    if (JSON.stringify(drafts[s]) !== look) setDraft(s, JSON.parse(look))
  })
  watch(() => route.query.v, (v) => v && !store.versions && loadVersions(), { immediate: true })

  function reset() {
    dropDraft(slug.value)
    bare(slug.value)
  }
  async function save(note = '') {
    await saveView(slug.value, { query: toSaved(state.value), ...(note ? { note } : {}) })
    reset()
  }
  // what is on screen becomes a view of its own, made from this one — or from the version looked at; this one stays as saved
  async function fork(body) {
    const from = view.value
    const v = await createView({ folder: from.folder, ...body, query: toSaved(state.value), parent: from.slug, parent_version: peek.value?.n || from.version })
    dropDraft(from.slug)
    router.push({ query: { view: v.slug } })
    return v
  }
  return { reset, save, fork, open: (next) => router.push({ query: { view: next } }), unpeek: () => bare(slug.value) }
}
