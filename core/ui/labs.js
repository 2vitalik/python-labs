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
export const labName = (n) => `Лаба ${n}`
export const labPath = (n) => site.guide.find((g) => g.n === Number(n))?.path || ''
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
  lines.push(f.before || f.after ? `комітів до дедлайну ${f.before}${f.window !== f.before ? ` (у вікні лаби ${f.window})` : ''} · після ${f.after}` : 'комітів нема')
  if (f.last) lines.push(`останній до дедлайну: ${fmtWhen(f.last)}`)
  if (cell.review) lines.push(`звіт: ${VERDICTS[cell.review.verdict]}${cell.review.stale ? ' (інший зріз)' : ''}${cell.review.summary ? ` — ${cell.review.summary}` : ''}`)
  if (hasWord(cell)) lines.push(`слово викладача: ${cell.mark.met ? 'вклався' : 'не вклався'}`)
  if (cell.mark?.note) lines.push(`нотатка: ${cell.mark.note}`)
  return lines.join('\n')
}
