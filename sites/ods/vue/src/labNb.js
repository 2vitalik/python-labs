import { ref, watch } from 'vue'

import { load, save } from '@core/local.js'

// what of a notebook the reader looks at — all · own · notes; one choice for every notebook, remembered in this browser
export const MODES = [['all', 'усе'], ['own', 'лише своє'], ['notes', 'висновки']]
export const nbMode = ref(MODES.some(([k]) => k === load('nb-mode')) ? load('nb-mode') : 'all')
watch(nbMode, (m) => save('nb-mode', m))
