import { starts, worst } from './weekSum.js'
import { cats } from './weekWhy.js'

// «what if» on /week (T186): the reasons the teacher could talk people out of, and the people no hour suits

// a «не можу» whose every reason is soft counts as «незручно»; `soft` keeps it told apart on the strips
export function soften(students, soft) {
  if (!soft.size) return students
  const easy = (m) => m.kind === 'no' && cats(m.why).every((c) => soft.has(c))
  return students.map((s) => (s.week?.marks.some(easy)
    ? { ...s, week: { ...s.week, marks: s.week.marks.map((m) => (easy(m) ? { ...m, kind: 'meh', soft: true } : m)) } }
    : s))
}
// the kind as the person marked it
export const was = (m) => (m.soft ? 'no' : m.kind)

// those who can't come to nearly any class the teacher can: they add one to every window and hide the difference between them
export function stuck(laid, frame, len, mine, share = 0.9) {
  const all = starts(frame, len).filter((w) => !mine || worst(mine[w.day], w.r0, w.r0 + w.n) !== 'no')
  const no = (cells) => all.filter((w) => worst(cells[w.day], w.r0, w.r0 + w.n) === 'no').length
  return all.length ? laid.filter(({ cells }) => no(cells) >= share * all.length) : []
}
