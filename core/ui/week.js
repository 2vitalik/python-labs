// «Мій тиждень» (T177): the grid and what is marked on it. The API keeps marks — runs of slots of one kind within a day;
// the page paints cells. `frame` is the grid as the API gives it: days, from, to, step — in minutes
export const DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
// kind → the tool's name, and what it says in full
export const KINDS = { no: ['Не можу', 'Не можу — з причиною'], meh: ['Незручно', 'Можу, але незручно'], ok: ['Найкраще', 'Найзручніший час'] }

export const hm = (min) => `${Math.floor(min / 60)}:${String(min % 60).padStart(2, '0')}`
export const span = (m) => `${hm(m.start)}–${hm(m.end)}`
export const slots = (frame) => (frame.to - frame.from) / frame.step
export const startOf = (frame, row) => frame.from + row * frame.step
// [0, 1, 2, 3, 4] → «Пн–Пт», [1, 3] → «Вт, Чт»
export function daysLabel(days) {
  const row = days.length > 2 && days.every((d, i) => d === days[0] + i)
  return row ? `${DAYS[days[0]]}–${DAYS[days.at(-1)]}` : days.map((d) => DAYS[d]).join(', ')
}

// cells[day][row] — { kind, why } or null; marks that lie off the grid (it was changed since) are dropped
export function toCells(marks, frame) {
  const cells = Array.from({ length: frame.days }, () => Array(slots(frame)).fill(null))
  for (const m of marks) {
    for (let t = m.start; t < m.end; t += frame.step) {
      const row = (t - frame.from) / frame.step
      if (cells[m.day]?.[row] === null) cells[m.day][row] = { kind: m.kind, why: m.why }
    }
  }
  return cells
}

// neighbours of one kind and reason become one mark
export function toMarks(cells, frame) {
  const marks = []
  cells.forEach((col, day) => col.forEach((c, row) => {
    const last = marks.at(-1)
    const start = startOf(frame, row)
    if (!c) return
    if (last?.day === day && last.end === start && last.kind === c.kind && last.why === c.why) last.end += frame.step
    else marks.push({ day, start, end: start + frame.step, kind: c.kind, why: c.why })
  }))
  return marks
}
export const settle = (marks, frame) => toMarks(toCells(marks, frame), frame)

// the rectangle between two cells: days and rows, both ends in it
export const rect = (a, b) => ({ d0: Math.min(a.day, b.day), d1: Math.max(a.day, b.day), r0: Math.min(a.row, b.row), r1: Math.max(a.row, b.row) })
// …and where it lies over the grid: CSS for a frame above the cells
export const box = (frame, { d0, d1, r0, r1 }) => ({
  left: `${(d0 / frame.days) * 100}%`, width: `${((d1 - d0 + 1) / frame.days) * 100}%`,
  top: `calc(var(--slot) * ${r0})`, height: `calc(var(--slot) * ${r1 - r0 + 1})`,
})
export const hours = (frame, { d0, d1, r0, r1 }) =>
  `${daysLabel(Array.from({ length: d1 - d0 + 1 }, (_, i) => d0 + i))} ${hm(startOf(frame, r0))}–${hm(startOf(frame, r1 + 1))}`

// a stroke that starts on a cell of the tool's own kind takes that kind off; the eraser takes off any
export const wipes = (cells, a, tool) => tool === 'erase' || cells[a.day][a.row]?.kind === tool

// one stroke over the rectangle a–b. Red drawn across a red that has a reason takes that reason: the mark has grown
export function paint(cells, a, b, tool) {
  const { d0, d1, r0, r1 } = rect(a, b)
  const wipe = wipes(cells, a, tool)
  return cells.map((col, d) => {
    if (d < d0 || d > d1) return col
    const whys = new Set(col.slice(r0, r1 + 1).filter((c) => c?.kind === 'no' && c.why).map((c) => c.why))
    const why = tool === 'no' && whys.size === 1 ? [...whys][0] : ''
    return col.map((c, r) => {
      if (r < r0 || r > r1) return c
      if (wipe) return tool === 'erase' || c?.kind === tool ? null : c
      return c?.kind === tool && c.why ? c : { kind: tool, why }
    })
  })
}
