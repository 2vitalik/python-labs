import { computed, reactive, ref, watch } from 'vue'

import { request } from '@core/http.js'
import { load, save } from '@core/local.js'
import { mockApi } from './aiMock.js'
import { HEADS } from './sections.js'

// «✨ Описати словами» (T289, T291 §14): the student's words → proposals the server has checked against the vocab and the
// catalog; nothing lands in the game without a click. The panel's state and its calls — the contract's §3–§4.
// `?ai=mock` in a dev build answers from aiMock.js: the panel without the backend and the key
const BASE = '/api/my/game/ai'
const real = {
  get: () => request(BASE),
  ask: (text) => request(BASE, 'POST', { text }),
  apply: (id, keys) => request(`${BASE}/${id}/apply`, 'POST', { keys }),
  state: (id, keys, state) => request(`${BASE}/${id}/state`, 'POST', { keys, state }),
}
// asked on every call: the address may gain or lose `?ai=mock` while the module stays loaded
const mocked = () => import.meta.env.DEV && new URLSearchParams(location.search).get('ai') === 'mock'
const api = Object.fromEntries(Object.keys(real).map((k) => [k, (...a) => (mocked() ? mockApi : real)[k](...a)]))

export const ai = reactive({ mode: 'off', why: 'off', left_today: null, left_total: null, max_chars: 4000, drafts: [] })
export const aiShown = computed(() => ai.why !== 'off')

// no answer, a 404 before the backend is there, an error — the same as «off»: no switch, nothing red
export const loadAi = () => api.get().then((r) => Object.assign(ai, r), () => Object.assign(ai, { mode: 'off', why: 'off', drafts: [] }))
const refresh = () => api.get().then((r) => Object.assign(ai, r), () => {})

// «зі списку» | «словами», remembered in this browser; the words not yet sent wait in it too
export const tab = ref(load('add-tab') === 'words' ? 'words' : 'list')
export const setTab = (t) => { tab.value = t; save('add-tab', t) }
export const text = ref(load('ai-text') || '')
watch(text, (t) => save('ai-text', t))

const put = (d) => {
  const i = ai.drafts.findIndex((x) => x.id === d.id)
  if (i < 0) ai.drafts.unshift(d)
  else ai.drafts[i] = d
  return d
}
// the limits move after an ask, and a failed one is kept as a draft with its error: the list is read again either way
export const ask = (words) => api.ask(words).then(put).finally(refresh)
export async function apply(draft, keys) {
  const r = await api.apply(draft.id, keys)
  put(r.draft)
  return r
}
export const mark = (draft, keys, state) => api.state(draft.id, keys, state).then(put)

// the groups in the description's order (contract §8)
export const GROUPS = [
  { key: 'field', ...HEADS.field }, { key: 'entity', ...HEADS.entities }, { key: 'rule', ...HEADS.rules },
  { key: 'window', ...HEADS.windows }, { key: 'level', ...HEADS.levels },
  { key: 'claim', icon: '🃏', title: 'Картки', zone: '' }, { key: 'unknown', icon: '❓', title: 'Не розпізнано', zone: '' },
]
const NOUN = { entity: 'сутність', window: 'вікно', level: 'рівень', rule: 'правило', field: 'поле', claim: 'картка' }
export const itemName = (it) => `${NOUN[it.group] || ''} «${it.data?.title || it.data?.slug || it.data || ''}»`

// what comes along with a proposal and is not in the game yet; a rejected one stops it (T289 §4: the rule greys)
export const needsOf = (d, it) => (it.needs || []).map((k) => d.items.find((x) => x.key === k))
  .filter((x) => x && (x.state === 'open' || x.state === 'rejected'))
export const blocked = (d, it) => needsOf(d, it).some((x) => x.state === 'rejected')
export const addable = (d, it) => it.state === 'open' && it.group !== 'unknown' && !blocked(d, it)

export function tally(d) {
  const n = (f) => d.items.filter(f).length
  return {
    added: n((x) => x.state === 'added'), rejected: n((x) => x.state === 'rejected'), exists: n((x) => x.state === 'exists'),
    open: n((x) => x.state === 'open' && x.group !== 'unknown'), unknown: n((x) => x.state === 'open' && x.group === 'unknown'),
  }
}
