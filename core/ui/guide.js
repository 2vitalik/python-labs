import { ref } from 'vue'

import { getGuide } from './api.js'
import { site } from './site.js'

// which pages the guide has and where they open — the site's own: site.guide
export const pages = ref({})  // slug → {title, brief, updated}; bodies come per page
// the labs among them, by number: a site whose other pages are numbered too (ods: lectures) marks them with `kind`
export const labPages = () => site.guide.filter((s) => s.n && (s.kind ?? 'labs') === 'labs')
let loading
export function loadGuide() {
  loading ??= getGuide().then((list) => (pages.value = Object.fromEntries(list.map((p) => [p.slug, p]))))
  return loading
}
