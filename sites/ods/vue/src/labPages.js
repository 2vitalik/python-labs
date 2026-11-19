import { ref } from 'vue'

import { request } from '@core/http.js'

import { getLabs } from './api.js'

// the labs' pages beyond the list of labs (sites/ods/api/models/lab_page.py): a lab's parts, the pages common to all labs
export const labPages = ref([])
let loading
export const loadLabPages = () => (loading ??= request('/api/labpages').then((list) => (labPages.value = list)))

export const partsOf = (n) => labPages.value.filter((p) => p.kind === 'lab' && p.lab === n)
export const commons = () => labPages.value.filter((p) => p.kind === 'common')
export const pathOf = (p) => (p.kind === 'common' ? `/labs/about/${p.part}` : `/labs/${p.lab}${p.part && `/${p.part}`}`)

// a lab's pages (or the common ones, n = 0) in their order; in a row of them a lab's own page is its «Огляд»
export const lineOf = (n) => [...(n ? partsOf(n) : commons())].sort((a, b) => a.order - b.order)
export const pageWord = (p) => (p.kind === 'lab' && !p.part ? 'Огляд' : p.nav)

// the labs with cards (T200) — «Моя лаба» — asked once a page load
let cards
export const labsWithCards = () => (cards ??= getLabs().catch(() => []))
