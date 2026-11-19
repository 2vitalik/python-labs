import { ref } from 'vue'

import { request } from '@core/http.js'

// the labs' pages beyond the list of labs (sites/ods/api/models/lab_page.py): a lab's parts, the pages common to all labs
export const labPages = ref([])
let loading
export const loadLabPages = () => (loading ??= request('/api/labpages').then((list) => (labPages.value = list)))

export const partsOf = (n) => labPages.value.filter((p) => p.kind === 'lab' && p.lab === n)
export const commons = () => labPages.value.filter((p) => p.kind === 'common')
export const pathOf = (p) => (p.kind === 'common' ? `/labs/about/${p.part}` : `/labs/${p.lab}${p.part && `/${p.part}`}`)
