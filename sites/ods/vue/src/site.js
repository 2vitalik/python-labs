// what this site is; the platform (core/ui) takes it through start() in main.js

// pages are guide slugs, filled by sites/ods/api/content_io.py; `n` — the number in the address
const LECTURES = Array.from({ length: 15 }, (_, i) => i + 1)
  .map((n) => ({ slug: `lec${String(n).padStart(2, '0')}`, path: `/lectures/${n}`, nav: `Лекція ${n}`, kind: 'lectures', n }))
const LABS = [1, 2, 3, 4, 5].map((n) => ({ slug: `lab${n}`, path: `/labs/${n}`, nav: `Лаба ${n}`, kind: 'labs', n }))
export const KINDS = { lectures: 'Лекції', labs: 'Лаби' }

export default {
  name: 'ODS Labs',
  links: [['/lectures', 'Лекції'], ['/labs', 'Лаби'], ['/students', 'Студи'], ['/activity', 'Актив'], ['/my/profile', 'Профіль']],
  guide: [...LECTURES, ...LABS],
}
