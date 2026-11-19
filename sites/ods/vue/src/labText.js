// words and small formatters of the lab pages (T354): hand-in, the notebook, the teacher's review
export const WAYS = { none: 'без захисту', record: 'записом', live: 'наживо' }
export const MISSING = 'нема в рядку'  // the API's word for an answer the line lacks

// an answer of the line: ✅ right · ❌ wrong · ⬜ not in the line (or no line at all)
export const markOf = (v) => (!v ? '⬜' : v.ok ? '✅' : v.why === MISSING ? '⬜' : '❌')

// a task's key as the reader says it: the report and the ai note are words, a star wears ★
const WORDS = { report: 'рапорт', ai: 'ШІ' }
export const keyWord = (key, role) => WORDS[key] || (role === 'star' && !String(key).startsWith('★') ? `★ ${key}` : String(key))

// the key's number to one digit finer than the step it is checked to: 22.333333333333332 ± 0.01 → 22.333
export function numOf(value, step) {
  if (typeof value !== 'number') return value
  const digits = step > 0 ? Math.max(0, Math.ceil(-Math.log10(step)) + 1) : 6
  return String(Number(value.toFixed(Math.min(digits, 10))))
}

// the teacher's rerun next to the student's own line: same · differs · nothing to compare (the student had no line)
export const sameOf = (run) => (run.same === true ? { text: '✅ рядок збігся з рядком студента', short: '✅ збігся', cls: 'text-success' }
  : run.same === false ? { text: '≠ рядок не збігся з рядком студента', short: '≠ не збігся', cls: 'text-danger' }
    : { text: 'у студента рядка не було — порівнювати нема з чим', short: 'без рядка', cls: 'text-secondary' })

export const fmtSize = (b) => (b >= 1048576 ? `${(b / 1048576).toFixed(1)} МБ` : `${Math.max(1, Math.round((b || 0) / 1024))} КБ`)

// versions oldest first, each with its number — «версія 2 із 3»
export const numbered = (files = []) => [...files].sort((a, b) => new Date(a.at) - new Date(b.at)).map((f, i) => ({ ...f, k: i + 1 }))

// the version a student's one is compared with: the one before it; an executed copy — with the student's file it ran
export function prevOf(files, id) {
  const all = numbered(files)
  const own = all.find((f) => f.run?.file === id)
  if (own) return own.id
  const i = all.findIndex((f) => f.id === id)
  return i > 0 ? all[i - 1].id : null
}

// «кроки 24/24 · графіки 3/3 · висновки 4/4 · ★ 2 · рапорт» out of FACTS.count, each piece whole or not; a count the
// file cannot tell (null, marimo without outputs) is «?»; a lab without such items has no pill for them
export function piecesOf(count) {
  if (!count) return []
  const pair = (word, p) => p?.[1] && { text: `${word} ${p[0] ?? '?'}/${p[1]}`, full: p[0] !== null && p[0] >= p[1] }
  const one = (word, v) => v !== null && v !== undefined && { text: word, full: !!v }
  return [pair('кроки', count.tasks), pair('графіки', count.plots), pair('висновки', count.conclusions),
    count.stars?.[0] && { text: `★ ${count.stars[0]}`, full: true }, one('рапорт', count.report), count.ai && one('ШІ', true)].filter(Boolean)
}
