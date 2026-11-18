import { fmtWhen, labName } from '@core/labs.js'

// the site's part of a student's row (routes/student_variants.py → `variants`: lab n → the card): columns of /table and of /students
const LABS = [1, 2, 3, 4, 5]  // as LABS in site.js, which imports this file
const ANSWERS = { all: { emoji: '✅', text: 'усі відповіді правильні', color: 'green' }, some: { emoji: '🟡', text: 'частина правильна', color: 'yellow' },
                  none: { emoji: '❌', text: 'жодної правильної', color: 'red' } }
const right = (v) => (!v?.attempts ? null : v.ok === v.total ? 'all' : v.ok ? 'some' : 'none')  // no line handed in — nothing to say

// a lab's columns stand in its band next to the platform's, and a view says them of «this lab»: lab.vid → lab3.vid
function lab(n) {
  const g = labName(n)
  const v = (r) => r.variants[n]
  const L = (key, type, name, short, get, more = {}) => ({ key: `lab${n}.${key}`, type, name, title: `${g}: ${name.toLowerCase()}`, short, get,
    group: g, cat: 'Лаба', lab: n, ...more })
  return [
    L('vid', 'text', 'Варіант', '🎴', (r) => v(r)?.vid, { fam: 'variant', link: (r) => v(r) && `/labs/${n}/results`,
      hint: (r) => v(r)?.assigned_at && `картку взято ${fmtWhen(v(r).assigned_at)}` }),
    L('ok', 'enum', 'Відповіді', '🎯', (r) => right(v(r)), { fam: 'variant', options: ANSWERS, sub: (r) => (right(v(r)) ? `${v(r).ok}/${v(r).total}` : '') }),
    L('tries', 'number', 'Спроб', '🔁', (r) => v(r)?.attempts, { fam: 'variant' }),
    L('checked', 'date', 'Здано', '📨', (r) => v(r)?.checked_at, { fam: 'variant', title: `${g}: коли перевірено останній рядок` }),
    L('nb', 'link', 'Ноутбук', '📓', (r) => v(r)?.notebook, { fam: 'variant' }),
    L('points', 'number', 'Бали', '💯', (r) => v(r)?.points, { fam: 'points', hint: (r) => v(r)?.note }),
    L('pnote', 'text', 'Нотатка до балів', '🗒', (r) => v(r)?.note, { fam: 'points' }),
  ]
}
export const TABLE_COLS = LABS.flatMap(lab)

// /students: a lab a word — the points, else the answers right, else just the card: «Л1 14б · Л2 2/3 · Л3 🎴»
const word = (n, v) => `Л${n} ${v.points !== null ?`${v.points}б` : v.attempts ? `${v.ok}/${v.total}` : '🎴'}`
const held = (s) => Object.entries(s.variants || {}).sort(([a], [b]) => a - b)  // the teacher's rows carry them, a student's do not
export const STUDENT_COLS = [{ title: 'Лаби', text: (s) => held(s).map(([n, v]) => word(n, v)).join(' · '),
                               to: (s) => `/labs/${held(s).at(-1)?.[0]}/results` }]
export const FACETS = [
  { key: 'card', text: '🎴 картка', title: 'Взяв картку хоч однієї лаби', has: (s) => held(s).length },
  { key: 'line', text: '📨 рядок', title: 'Здав рядок відповідей хоч однієї лаби', has: (s) => held(s).some(([, v]) => v.attempts) },
]
