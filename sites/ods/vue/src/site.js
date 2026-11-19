import { FACETS, STUDENT_COLS, TABLE_COLS } from './labCols.js'

// what this site is; the platform (core/ui) takes it through start() in main.js

// pages are guide slugs, filled by sites/ods/api/content_io.py; `n` — the number in the address
const LECTURES = Array.from({ length: 15 }, (_, i) => i + 1)
  .map((n) => ({ slug: `lec${String(n).padStart(2, '0')}`, path: `/lectures/${n}`, nav: `Лекція ${n}`, kind: 'lectures', n }))
export const LABS = [1, 2, 3, 4, 5].map((n) => ({ slug: `lab${n}`, path: `/labs/${n}`, nav: `Лаба ${n}`, kind: 'labs', n }))
export const KINDS = { lectures: 'Лекції', labs: 'Лаби' }

export default {
  name: 'ODS Labs',
  // the platform's entries carry the same words as on the python site
  links: [['/lectures', 'Лекції', null, false, 'book'], ['/labs', 'Лаби', null, false, 'flask'], ['/lessons', 'Пари', 'admin', false, 'cap'],
    ['/students', 'Студи', null, false, 'users'], ['/deadlines', 'Строки', null, false, 'alarm'], ['/table', 'Звід', null, false, 'table'],
    ['/intake', 'Вхідні', null, false, 'send'], ['/activity', 'Актив', null, false, 'chart'], ['/polls', 'Polls', null, false, 'bars'], ['/week', 'Week', null, false, 'calendar'],
    ['/my/profile', 'Профіль', null, false, 'user']],
  guide: [...LECTURES, ...LABS],
  colls: { variants: 'варіант лаби', lab_gates: 'доступ до лаби' },
  students: { page: 'Лаби', cols: STUDENT_COLS, facets: FACETS },
  table: { cols: TABLE_COLS },
}
