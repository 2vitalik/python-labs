import { slots, startOf, toCells } from './week.js'
import { REASONS, emojiOf } from './weekWhy.js'

// the stream's week (T177): everyone's marks laid over one grid — who is in the way of a class at a given hour

// done — «Готово» is pressed · draft — marked, not finished: counted too · none — nothing to count
export const stateOf = (s) => (s.week?.done_at ? 'done' : s.week?.marks.length ? 'draft' : 'none')
// those whose week says something, each with it as cells
export const lay = (students, frame) => students.filter((s) => stateOf(s) !== 'none').map((s) => ({ s, cells: toCells(s.week.marks, frame) }))

// counts[day][row] — how many people marked the slot with each kind
export function tally(laid, frame) {
  const counts = Array.from({ length: frame.days }, () => Array.from({ length: slots(frame) }, () => ({ no: 0, meh: 0, ok: 0 })))
  for (const { cells } of laid) cells.forEach((col, d) => col.forEach((c, r) => c && counts[d][r][c.kind]++))
  return counts
}

const RANK = { ok: 0, free: 1, meh: 2, no: 3 }
// what a person says to rows r0…r1 of a day: their worst slot decides, and «ok» takes every slot
export function worst(col, r0, r1) {
  let w = 'ok'
  for (let r = r0; r < r1; r++) {
    const kind = col[r]?.kind || 'free'
    if (RANK[kind] > RANK[w]) w = kind
  }
  return w
}

// every start of a class `len` minutes long, with how many people say what to it; `mine` — the teacher's own cells
export function windows(laid, frame, len, mine) {
  const n = Math.ceil(len / frame.step)
  const out = []
  for (let day = 0; day < frame.days; day++) {
    for (let r0 = 0; r0 + n <= slots(frame); r0++) {
      const start = startOf(frame, r0)
      const w = { day, r0, n, start, end: start + len, no: 0, meh: 0, free: 0, ok: 0, mine: mine ? worst(mine[day], r0, r0 + n) : 'free' }
      for (const { cells } of laid) w[worst(cells[day], r0, r0 + n)]++
      out.push(w)
    }
  }
  return out
}

const better = (a, b) => a.no - b.no || a.meh - b.meh || b.ok - a.ok || a.day - b.day || a.start - b.start
// the best of them that don't run into each other: of two starts less than a class apart only the better stays
export function best(list, len, count = Infinity) {
  const out = []
  for (const w of [...list].sort(better)) {
    if (out.length === count) break
    if (!out.some((o) => o.day === w.day && Math.abs(o.start - w.start) < len)) out.push(w)
  }
  return out
}

// who is in the way of a window: each with the marks that say so
export function who(laid, w) {
  const out = { no: [], meh: [] }
  for (const { s, cells } of laid) {
    const kind = worst(cells[w.day], w.r0, w.r0 + w.n)
    if (kind in out) out[kind].push({ ...s, marks: s.week.marks.filter((m) => m.day === w.day && m.kind === kind && m.start < w.end && m.end > w.start) })
  }
  return out
}

// …and by reason, the commonest first: a chip's emoji names the group, a typed reason goes under ✏️
export function byReason(people) {
  const groups = new Map()
  for (const p of people) {
    const why = p.marks[0].why.trim()
    const emoji = emojiOf(why)
    const title = REASONS.find((r) => emoji && r.includes(emoji)) || emoji || (why ? '✏️ своя причина' : '❓ без причини')
    groups.set(title, [...(groups.get(title) || []), p])
  }
  return [...groups].sort((a, b) => b[1].length - a[1].length)
}
