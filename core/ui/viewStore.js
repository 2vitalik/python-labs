import { reactive } from 'vue'

import * as api from './api.js'

// what /table and its library of views share (T315 §7–§8): the table's payload — rows, columns' sources, views, the teacher's
// prefs — read once; every change of a view goes to the API and its answer comes back into the list
export const store = reactive({ data: null, error: '', versions: null })

export async function load() {
  try {
    store.data = await api.getTable()
    store.error = ''
  } catch (e) {
    store.error = e.message
  }
}
export const viewOf = (slug) => store.data?.views.find((v) => v.slug === slug)
export const liveViews = () => (store.data?.views || []).filter((v) => !v.archived_at)
function put(v) {
  const i = store.data.views.findIndex((x) => x.slug === v.slug)
  if (i < 0) store.data.views.push(v)
  else store.data.views[i] = v
  if (v.folder && !store.data.prefs.folders.includes(v.folder)) store.data.prefs.folders.push(v.folder)
  store.versions = null  // a save may have added one
  return v
}

export const createView = async (body) => put(await api.postTableView(body))
// a copy of a view as it is saved: it remembers what it was made from and stands right after it
export async function copyView(v) {
  const c = await createView({ title: `${v.title} (копія)`, emoji: v.emoji, about: v.about, query: v.query, folder: v.folder, tags: v.tags,
                               pinned: v.pinned, parent: v.slug, parent_version: v.version })
  const order = liveViews().map((x) => x.slug).filter((s) => s !== c.slug)
  order.splice(order.indexOf(v.slug) + 1, 0, c.slug)
  await orderViews(order)
  return c
}
export const saveView = async (slug, patch) => put(await api.putTableView(slug, patch))
export const archiveView = async (slug, on = true) => put(await api.archiveTableView(slug, on))
export async function removeView(slug) {
  await api.deleteTableView(slug)
  store.data.views = store.data.views.filter((v) => v.slug !== slug)
  store.versions = null
}
// the order of the tabs and of the library: the slugs given go first, in that order
export async function orderViews(slugs) {
  slugs.forEach((s, i) => (viewOf(s).order = i))
  store.data.views.sort((a, b) => a.order - b.order)
  store.data.views = (await api.orderTableViews(slugs)).views
}
// { folders: [...] } — their order; { rename: [old, new] } — a folder renamed with its views («» dissolves it)
export async function setFolders(body) {
  const r = await api.postViewFolders(body)
  store.data.prefs.folders = r.folders
  store.data.views = r.views
}
export const setQuiet = async (quiet) => (store.data.prefs = await api.putTablePrefs({ quiet }))

export async function loadVersions() {
  store.versions = (await api.getViewVersions()).versions
}
export const versionsOf = (slug) => (store.versions || []).filter((v) => v.view === slug)
export async function editVersion(slug, n, patch) {
  const v = await api.putViewVersion(slug, n, patch)
  const i = (store.versions || []).findIndex((x) => x.view === slug && x.n === n)
  if (i >= 0) store.versions[i] = v
  return v
}
export const restoreVersion = async (slug, n) => put(await api.restoreViewVersion(slug, n))
