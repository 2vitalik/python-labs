import { byGroup } from './studentFilter.js'
import { was } from './weekIf.js'
import { cats, emojiOf } from './weekWhy.js'

// the stream's week as strips (T186): a day is everyone's column side by side, group by group, and a person
// keeps their place in every day

// minutes of a kind in a person's week as they marked it: a softened reason moves nobody
const minutes = (s, kind) => s.week.marks.reduce((n, m) => n + (was(m) === kind ? m.end - m.start : 0), 0)
const busier = (a, b) => minutes(b.s, 'no') - minutes(a.s, 'no') || minutes(b.s, 'meh') - minutes(a.s, 'meh') || (a.s.name || '').localeCompare(b.s.name || '')

// rows r0 … r0+n of a day as CSS: whatever lies over the strips is placed in slots
export const place = (r0, n) => ({ top: `calc(var(--slot) * ${r0})`, height: `calc(var(--slot) * ${n})` })

// a person's marks of a day as a strip draws them: where each lies, the reasons a «не можу» names, the emoji a wide strip shows
export function dayMarks(marks, day, frame, roomy) {
  const row = (min) => (min - frame.from) / frame.step
  return marks.filter((m) => m.day === day).map((m) => {
    const red = was(m) === 'no'
    return { m, style: place(row(m.start), row(m.end) - row(m.start)), cats: red ? cats(m.why) : [],
             sign: roomy && red ? emojiOf(m.why) || (m.why.trim() ? '✏️' : '❓') : '' }
  })
}

// the groups of `students` in their order: `size` — everyone in it, `list` — those of `laid` (lay() of weekSum.js),
// the busiest first, or by name. A group where nobody has marked stays: the estimate counts its size
export function arrange(laid, students, sort) {
  return byGroup(students).map(({ name, list }) => {
    const marked = laid.filter((p) => p.s.group === name)
    return { name, size: list.length, list: sort === 'name' ? marked : [...marked].sort(busier) }
  })
}
