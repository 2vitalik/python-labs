import { groupOf, KINDS, sizeOf } from './lectureChanges.js'

// the page's filters (T374 PAGE §2), all in the address: a row of pills is a key, its values — a list through commas
// (?lec=5&group=content,lang); `for` — a ready set that is not a row's value; `auto` — the look's automatic items too
const VALUE = {
  lec: (it) => String(it.lec), group: groupOf, kind: (it) => it.kind, sev: (it) => String(it.sev), status: (it) => it.status,
  where: (it) => it.where, origin: (it) => it.origin, size: sizeOf,
}
export const ROWS = Object.keys(VALUE)
export const valueOf = (it, key) => VALUE[key](it)

export const PRESETS = {
  crit: { word: 'Критичне', hint: 'критичність 3 — зміст був хибний', query: { sev: '3' } },
  lector: {
    word: 'Для лектора', hint: 'помилки, що є на слайдах лектора: суттєве й критичне або те, що чекає рішення', query: { for: 'lector' },
    fits: (it) => it.origin === 'slide' && (it.sev >= 2 || it.status === 'open'),
  },
  lang: { word: 'Мова', hint: 'усе про мову', query: { group: 'lang' } },
  look: { word: 'Оформлення', hint: 'усе оформлення, з автоматичним', query: { group: 'look' } },
}

const list = (v) => (v ? String(v).split(',').filter(Boolean) : [])
export function filterOf(q) {
  const f = Object.fromEntries(ROWS.map((k) => [k, list(q[k])]))
  return { ...f, q: String(q.q || '').trim().toLowerCase(), auto: q.auto === '1', for: PRESETS[q.for]?.fits ? q.for : '' }
}
export const busy = (q) => [...ROWS, 'q', 'auto', 'for'].some((k) => q[k])

const lookKind = (k) => KINDS[k]?.[1] === 'look'
export const lookAuto = (it) => it.auto && groupOf(it) === 'look'

// `skip` — rows left out: a row's pills count what each would leave with the other rows kept. The look's automatic items
// (thousands of them) hide unless asked for: by «з оформленням», by the look group or one of its kinds — and a pill of
// those counts them, for a click on it shows them
export function fits(it, f, skip = []) {
  for (const k of ROWS) if (!skip.includes(k) && f[k].length && !f[k].includes(VALUE[k](it))) return false
  if (lookAuto(it) && !f.auto && !skip.includes('group') && !skip.includes('kind') && !f.group.includes('look') && !f.kind.some(lookKind)) return false
  if (f.for && !PRESETS[f.for].fits(it)) return false
  return !f.q || it.hay.includes(f.q)
}

// value → how many a row's pill would leave
export function tally(items, f, key) {
  const n = {}
  for (const it of items) if (fits(it, f, [key])) n[VALUE[key](it)] = (n[VALUE[key](it)] || 0) + 1
  return n
}

// a pill clicked: on → off, off → on beside the others of its row
export function toggled(f, key, v) {
  const now = f[key].includes(v) ? f[key].filter((x) => x !== v) : [...f[key], v]
  return { [key]: now.length ? now.join(',') : undefined }
}

// a ready set replaces every filter but the lecture and the words looked for; pressed — when the address is just it
export const cleared = () => Object.fromEntries([...ROWS, 'auto', 'for'].filter((k) => k !== 'lec').map((k) => [k, undefined]))
export const presetQuery = (p, on) => ({ ...cleared(), ...(on ? {} : PRESETS[p].query) })
export const presetOn = (q, p) => Object.keys(cleared()).every((k) => (q[k] || undefined) === PRESETS[p].query[k])
