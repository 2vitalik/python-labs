import { ref } from 'vue'

import { getGuide } from './api.js'

// which pages the guide has and where they open — the site's own: site.guide
export const pages = ref({})  // slug → {title, brief, updated}; bodies come per page
let loading
export function loadGuide() {
  loading ??= getGuide().then((list) => (pages.value = Object.fromEntries(list.map((p) => [p.slug, p]))))
  return loading
}
