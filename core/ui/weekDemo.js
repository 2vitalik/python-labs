import { slots, toMarks } from './week.js'
import { REASONS } from './weekWhy.js'

// a made-up stream for /week?demo=N (T186): the page as it looks when N % of 107 students have marked their week.
// Seeded: a reload draws the same stream, and ?demo=100 is ?demo=50 with the rest filled in
const FRAME = { days: 6, from: 900, to: 1380, step: 15 }
const SIZES = [22, 16, 18, 23, 11, 17]
const EAGER = [1.25, 1, 0.9, 0.85, 0.6, 1.1]  // groups fill their weeks in unevenly
const LAST = ['Шевченко', 'Бондар', 'Ткаченко', 'Коваль', 'Мельник', 'Кравець', 'Олійник', 'Поліщук', 'Савчук', 'Руденко',
  'Мороз', 'Лисенко', 'Гнатюк', 'Дорошенко', 'Зінченко', 'Карпенко', 'Павленко', 'Сидоренко', 'Тимошенко', 'Яковенко']
const FIRST = ['Андрій', 'Олена', 'Максим', 'Ірина', 'Денис', 'Софія', 'Артем', 'Марія', 'Богдан', 'Анна', 'Назар', 'Дарʼя']
const [CLASS, WORK, SPORT, STUDY, ROAD, FAMILY] = REASONS
const DONE = '2026-10-01T15:00:00Z'

// mulberry32: a few lines, and the same numbers on every machine
function random(seed) {
  return () => {
    seed = (seed + 0x6d2b79f5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

// one person's week: their group's classes first — what is put first wins a slot
function week(r, classes) {
  const pick = (a) => a[Math.floor(r() * a.length)]
  const chance = (p) => r() < p
  const cells = Array.from({ length: FRAME.days }, () => Array(slots(FRAME)).fill(null))
  const put = (day, from, to, kind, why = '') => {
    for (let t = Math.max(from, FRAME.from); t < Math.min(to, FRAME.to); t += FRAME.step) cells[day][(t - FRAME.from) / FRAME.step] ||= { kind, why }
  }
  if (chance(0.04)) for (let d = 0; d < 6; d++) put(d, 900, 1380, 'no', WORK)  // never free
  for (const [d, start] of classes) {
    if (!chance(0.9)) continue
    put(d, start, start + 90, 'no', CLASS)
    if (chance(0.25)) put(d, start + 90, start + 135, 'no', ROAD)
  }
  if (chance(0.15)) { const from = pick([900, 1080]); for (let d = 0; d < 5; d++) if (chance(0.8)) put(d, from, from + 240, 'no', WORK) }
  if (chance(0.3)) { const from = pick([1020, 1080, 1110, 1140]); for (const d of [pick([0, 1]), pick([2, 3]), pick([4, 5])]) if (chance(0.8)) put(d, from, from + 90, 'no', SPORT) }
  if (chance(0.1)) put(pick([1, 3, 5]), 1080, 1170, 'no', pick([STUDY, FAMILY, 'гурток з малювання']))
  if (chance(0.35)) for (let d = 0; d < 6; d++) if (chance(0.8)) put(d, pick([1260, 1290, 1320]), 1380, 'meh')
  if (chance(0.2)) put(5, 900, 1380, 'meh')
  if (chance(0.35)) for (const d of [pick([0, 1, 2]), pick([3, 4])]) put(d, 1110, 1230, 'ok')
  return toMarks(cells, FRAME)
}

export function demoWeeks(percent) {
  const r = random(11)
  const luck = random(5)  // who has marked: its own numbers, so the weeks stay the same at any percent
  const students = []
  SIZES.forEach((size, g) => {
    const classes = [0, 1, 2, 3, 4].filter(() => r() < 0.55).map((day) => [day, r() < 0.65 ? 900 : 1005])
    for (let i = 1; i <= size; i++) {
      const [marks, name, nick, tg] = [week(r, classes), `${LAST[Math.floor(r() * 20)]} ${FIRST[Math.floor(r() * 12)]}`, `demo-${g + 1}-${i}`, r() < 0.85]
      const [comment, done] = [r() < 0.1 ? 'можу лише онлайн' : '', r() < 0.9]
      const marked = percent >= 100 || luck() < (percent / 100) * EAGER[g]
      students.push({ nick, name, group: `ПЗПІ-25-${g + 1}`, picture: '', status: 'student', test: false, tg_username: tg ? nick.replaceAll('-', '_') : null,
                      week: marked ? { marks, comment, done_at: done ? DONE : null, updated_at: DONE } : null })
    }
  })
  const me = { marks: [{ day: 1, start: 900, end: 1080, kind: 'no', why: 'пари' }, { day: 3, start: 900, end: 1005, kind: 'no', why: 'пари' }],
               comment: '', done_at: DONE, updated_at: DONE }
  return { frame: FRAME, me, students }
}
