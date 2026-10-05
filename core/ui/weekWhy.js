// «Мій тиждень» (T177): why a «не можу» — the reasons offered, and how the marks ask for them
const seg = new Intl.Segmenter('uk', { granularity: 'grapheme' })

export const REASONS = ['🏫 пара за розкладом', '💼 робота', '🏋️ тренування', '📚 інші заняття', '🚌 дорога', '👨‍👩‍👧 сімʼя']
// what a «не можу» says on /week (T186): the chips it names, «своя причина» for typed words, «без причини» for none
export const CATS = [...REASONS, '✏️ своя причина', '❓ без причини']
const OWN = REASONS.length

// the reason's first emoji stands for it on the grid and sorts people on /week; a typed reason may have none
export const emojiOf = (why) => [...seg.segment(why)].find((g) => /\p{Extended_Pictographic}/u.test(g.segment))?.segment || ''
// a chip adds its reason to what is written, or takes it back: «🏫 пара за розкладом, 🚌 дорога»
export function toggleReason(why, reason) {
  const parts = why.split(',').map((p) => p.trim()).filter(Boolean)
  const has = (p) => p.includes(emojiOf(reason))
  return (parts.some(has) ? parts.filter((p) => !has(p)) : [...parts, reason]).join(', ')
}
export const bare = (marks) => marks.filter((m) => m.kind === 'no' && !m.why.trim())
// red marks that share hours and reason are explained as one: a rectangle over Monday–Friday needs one answer
export function reds(marks) {
  const by = new Map()
  for (const m of marks.filter((m) => m.kind === 'no')) {
    const key = `${m.start}-${m.end}-${m.why}`
    by.set(key, [...(by.get(key) || []), m])
  }
  return [...by.values()]
}

// «🏫 пара за розкладом, 🚌 дорога» → [0, 4] · «гурток» → [OWN] · «» → [OWN + 1]
export function cats(why) {
  const parts = why.split(',').map((p) => p.trim()).filter(Boolean)
  if (!parts.length) return [OWN + 1]
  return [...new Set(parts.map((p) => REASONS.findIndex((r) => p.includes(emojiOf(r)))).map((i) => (i < 0 ? OWN : i)))]
}

// who can't come, by reason, the commonest first: under the first one their mark names, as the chips count them
export function byReason(people) {
  const groups = new Map()
  for (const p of people) {
    const title = CATS[cats(p.marks[0].why)[0]]
    groups.set(title, [...(groups.get(title) || []), p])
  }
  return [...groups].sort((a, b) => b[1].length - a[1].length)
}
