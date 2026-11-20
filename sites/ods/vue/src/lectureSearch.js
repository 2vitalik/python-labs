import { getGuidePage } from '@core/api.js'
import { textOf } from '@core/drafts.js'
import { loadGuide } from '@core/guide.js'

import { engine } from './lectureEngine.js'
import { lectures, shortTitle } from './lectures.js'

// search over the texts of all lectures (LectureFind): the texts and the search's data come once, then every query is
// local; the logic is lectureEngine.js, this file — only what comes over the network

// the search's data (CONTRACT §6.1): a missing file (404, no network) turns its layer off
const DATA = ['lexicon', 'thesaurus', 'keys']
const media = (name) => fetch(`/api/media/lecsearch/${name}.json`).then((r) => (r.ok ? r.json() : null)).catch(() => null)

let texts = [], data = {}  // [{n, slug, page}] with the bodies, after loadTexts()
let loading
export function loadTexts() {
  loading ??= Promise.all([
    loadGuide().then(() => Promise.all(lectures().map(async (s) => ({ ...s, page: await getGuidePage(s.slug).catch(() => null) })))),
    Promise.all(DATA.map(media)),
  ]).then(([list, files]) => {
    texts = list.filter((t) => t.page)
    data = Object.fromEntries(DATA.map((name, i) => [name, files[i]]))
  }, (e) => { loading = null; throw e })
  return loading
}

// built again only when a text is another (the admin's drafts on/off)
let built = null, seen = []
function current() {
  const now = texts.map((t) => textOf(t.page))
  if (!built || now.length !== seen.length || now.some((t, i) => t !== seen[i])) {
    built = engine(texts.map((t, i) => ({ lec: t.n, slug: t.slug, title: shortTitle(t.page.title), text: now[i] })), data)
    seen = now
  }
  return built
}

// q → { hits, counts, fixed } (CONTRACT §6.2); each kind cut at `limit`, counts — before the cut
export const find = (q, limit = 12) => current()(q, limit)
