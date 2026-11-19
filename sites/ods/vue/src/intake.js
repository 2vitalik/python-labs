import { getStudents } from '@core/api.js'
import { fmtWhen } from '@core/labs.js'

import { LABS } from './site.js'

// «Вхідні» (T368 §2.7) without the screen: the filters, the words of a forwarded file and its state on the site
export const LAB_NUMS = LABS.map((l) => l.n)

// the pills of «Показати»: [word, what its count counts]; a row fits one of them, the lab chosen, and is not set aside
export const SHOWS = {
  all: ['усі', 'усі повідомлення'],
  nobody: ['без студента', 'повідомлення людей, чий студент ще невідомий'],
  todo: ['не перенесено', 'ноутбуки, що ще не стали версією «Моєї лаби»'],
  asks: ['просять час', 'повідомлення, де просять більше часу'],
}
const FITS = {
  all: () => true,
  nobody: (p) => !p.student,
  todo: (p, r) => !!r.file?.kind && !r.file.version,
  asks: (p, r) => r.asks,
}
export const filterOf = (q) => ({ show: FITS[q.show] ? q.show : 'all', lab: Number(q.lab) || null, skipped: q.skipped === '1' })
export const fits = (p, r, f) => (f.skipped || !r.skip) && FITS[f.show](p, r) && (!f.lab || r.file?.lab === f.lab)
export const count = (people, f) => people.reduce((n, p) => n + p.rows.filter((r) => fits(p, r, f)).length, 0)
export const pickRows = (people, f) => new Set(people.flatMap((p) => p.rows.filter((r) => fits(p, r, f)).map((r) => r.id)))
export const labsOf = (people) => [...new Set(people.flatMap((p) => p.rows.map((r) => r.file?.lab).filter(Boolean)))].sort((a, b) => a - b)
export const skippedOf = (people) => people.reduce((n, p) => n + p.rows.filter((r) => r.skip).length, 0)

// whose the talk is: how the site knows it, why it guesses — [word, the longer why under the mouse]
export const HOW = { tg: ['за Telegram', 'цей Telegram студент привʼязав на сайті'], hand: ['вказано', 'ти вказав сам'] }
export const GUESS = {
  card: ['за карткою', 'у ноутбуці — картка цього студента'],
  username: ['за ніком', 'нік у Telegram збігся з ніком студента'],
  name: ['за імʼям', 'імʼя в Telegram схоже на імʼя студента'],
}

// what a file is to the site now: site — a version of «Моя лаба» · none — not a notebook · nolab — which lab is unknown ·
// nobody — whose is unknown · mine — the teacher's own notebook: the site never brings it over by itself · trouble —
// it did not become a version · move — it can
export function stateOf(file, student, mine) {
  if (file.version) return 'site'
  if (!file.kind) return 'none'
  if (!file.lab) return 'nolab'
  if (!student) return 'nobody'
  if (mine) return 'mine'
  return file.trouble ? 'trouble' : 'move'
}

const lateOf = (x) => (x.late === true ? 'late' : x.late === false ? 'ok' : 'free')  // free — no deadline
const LATE = { late: 'після дедлайну', ok: 'вчасно' }
const score = (x) => (x.total !== null && x.total !== undefined ? `${x.ok ?? 0}/${x.total} ✅` : '')

// a card's number as said in a line: ПЗПІ-24-04 → 04, the whole of it under the mouse
const short = (vid) => String(vid).split('-').pop()

// «Лаба 2 · варіант 07 · 13/14 ✅ · вчасно»: what the site read in a notebook, a piece each; `lab` — the teacher may
// correct it while the file is not a version yet
export function factsOf(file) {
  if (!file.kind) return []
  const late = lateOf(file)
  return [
    file.lab && { text: `Лаба ${file.lab}`, lab: !file.version },
    file.vid && { text: `варіант ${short(file.vid)}`, hint: `картка ${file.vid}` },
    !file.line ? { text: 'без рядка відповідей', cls: 'quiet' }
      : score(file) ? { text: score(file) } : { text: 'рядок є', hint: 'ключа картки нема — перевірити нема з чим' },
    LATE[late] && { text: LATE[late], cls: late, hint: `дедлайн ${fmtWhen(file.due)}` },
  ].filter(Boolean)
}

// a number of a strip: its tone — filled once the file is on the site, a frame of that tone till then — and the hint
export const toneOf = (c) => [lateOf(c), c.version && 'moved']
export const cellHint = (c) => ({
  title: `${c.vid || c.n} · ${c.who || 'хтось'}`,
  text: [fmtWhen(c.sent_at), score(c) || 'без рядка відповідей', LATE[lateOf(c)], c.version && 'на сайті'].filter(Boolean).join(' · '),
})

// the stream's students for «чий це»: fetched once, when a list is first opened
let list = null
export const students = () => (list ??= getStudents()
  .then((all) => all.filter((s) => s.status === 'student').map((s) => ({
    key: s.nick, title: s.name || s.nick, group: s.group || 'без групи', words: [s.nick, s.tg_username].filter(Boolean),
    tag: s.test ? { text: 'тест', title: 'тестовий студент' } : undefined,
  })))
  .catch((e) => { list = null; throw e }))
