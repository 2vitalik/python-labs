// «Мій тиждень» (T177): why a «не можу» — the reasons offered, and how the marks ask for them
const seg = new Intl.Segmenter('uk', { granularity: 'grapheme' })

export const REASONS = ['🏫 пара за розкладом', '💼 робота', '🏋️ тренування', '📚 інші заняття', '🚌 дорога', '👨‍👩‍👧 сімʼя']

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
