import { site } from './site.js'

// what a cell of students × labs says (core/labs.py STATES): the emoji, the word, the look
export const STATES = {
  ok: { emoji: '✅', text: 'вчасно', cls: 'ok' },
  late: { emoji: '🕒', text: 'пізно', cls: 'bad' },
  partial: { emoji: '🟡', text: 'частково', cls: 'meh' },
  miss: { emoji: '❌', text: 'не вклався', cls: 'bad' },
  open: { emoji: '⏳', text: 'подовжено, дата невідома', cls: 'meh' },
  wait: { emoji: '⏱', text: 'ще є час', cls: 'wait' },
  check: { emoji: '🔍', text: 'не перевірено', cls: 'check' },
  norepo: { emoji: '🚫', text: 'без репозиторію', cls: 'bad' },
  noaccess: { emoji: '⚠️', text: 'репозиторій недоступний', cls: 'bad' },
  nodue: { emoji: '—', text: 'дедлайн не заданий', cls: 'none' },
}
export const VERDICTS = { done: 'зроблено', partial: 'частково', none: 'нема' }
export const KINDS = { game: 'гра', tasks: 'вправи без гри', other: 'інший код', none: 'коду нема' }  // what the reviewed code is (T248)
export const doneOf = (required) => (required?.length ? `${required.filter((x) => x === 'done').length}/${required.length}` : '')  // «4/6»
export const reviewLine = (r) => [VERDICTS[r.verdict], doneOf(r.required), KINDS[r.kind]].filter(Boolean).join(' · ')  // «частково · 4/6 · гра»
export const labName = (n) => `Лаба ${n}`
// the labs among the guide's pages, by number: a site whose other pages are numbered too marks each with `kind`
export const labPages = () => site.guide.filter((s) => s.n && (s.kind ?? 'labs') === 'labs')
export const labPath = (n) => labPages().find((g) => g.n === Number(n))?.path || ''
export const hasWord = (cell) => cell.mark?.met === true || cell.mark?.met === false  // the teacher's word stands on the cell

// «5 лист., 23:59» local; `day` — the date alone
export const fmtWhen = (iso, day = false) => (iso ? new Date(iso).toLocaleString('uk-UA',
  day ? { day: 'numeric', month: 'short' } : { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '')

// <input type="datetime-local"> speaks local time without a zone; the API speaks ISO with one
export function toInput(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  const p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`
}
export const fromInput = (v) => (v ? new Date(v).toISOString() : null)
export const endOfDay = (date) => `${date}T23:59`  // what a new deadline starts from

// everything about one cell, for a hover
export function describe(cell, name, lab) {
  const st = STATES[cell.state]
  const f = cell.facts
  const lines = [`${name} · ${labName(lab)}`, `${st.emoji} ${st.text}`]
  if (cell.due) lines.push(`дедлайн ${fmtWhen(cell.due)}${cell.mark?.until ? ` · подовжено, було ${fmtWhen(cell.base)}` : ''}`)
  if (cell.mark?.reason) lines.push(`причина: ${cell.mark.reason}`)
  if (cell.mark?.asked) lines.push(`просив подовжити${cell.mark.asked_for ? `: ${cell.mark.asked_for}` : ''}`)
  lines.push(f.before || f.after ? `комітів до дедлайну ${f.before}${f.window !== f.before ? ` (у вікні лаби ${f.window})` : ''} · після ${f.after}` : 'комітів нема')
  if (f.last) lines.push(`останній до дедлайну: ${fmtWhen(f.last)}`)
  if (cell.review) lines.push(`звіт: ${reviewLine(cell.review)}${cell.review.stale ? ' (інший зріз)' : ''}${cell.review.summary ? ` — ${cell.review.summary}` : ''}`)
  if (hasWord(cell)) lines.push(`слово викладача: ${cell.mark.met ? 'вклався' : 'не вклався'}`)
  if (cell.mark?.note) lines.push(`нотатка: ${cell.mark.note}`)
  return lines.join('\n')
}
