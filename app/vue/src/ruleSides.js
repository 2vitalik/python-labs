import { iconOf, vocab } from './catalog.js'

// the sides of a rule's trigger (T278 §7): ЯКЩО and ТО name the entity a side stands for, not its letter; the letter
// stays where the entity alone is ambiguous — the side is «будь-хто», or one entity is on both sides — and then КОЛИ
// shows it too, next to that side: «будь-хто ᴬ»

const twin = (when) => !!when?.a && when.a === when.b
const ambiguous = (when, s) => when?.[s] === '*' || twin(when)
const letter = (s) => vocab.value.sides[`@${s}`]

// the trigger's sides that КОЛИ marks with their letter: the ambiguous ones ЯКЩО / ТО refer to → { a: 'А' }
export function marks(rule) {
  const used = [...(rule.cond || []), ...(rule.then || [])].flatMap(Object.values)
  return Object.fromEntries(['a', 'b'].filter((s) => used.includes(`@${s}`) && ambiguous(rule.when, s)).map((s) => [s, letter(s)]))
}

// @a / @b in ЯКЩО / ТО as a piece: the trigger's entity there, or the bare letter when the side is «будь-хто»
export function sidePiece(s, ctx) {
  const p = ctx.parts.find((x) => x.id === ctx.when?.[s])
  const l = letter(s)
  if (!p) return { t: 'side', v: l, tip: `сторона ${l} з КОЛИ: ${vocab.value.sides[ctx.when?.[s]] || '?'}` }
  return { t: 'entity', id: p.id, v: p.title, icon: iconOf(p), sub: twin(ctx.when) ? l : '', tip: `та сама, що в КОЛИ (${l}) — показати` }
}

// how the form's list names a side of the trigger: «👻 Привид — той, що в КОЛИ (Б)», «будь-хто з КОЛИ (А)»
export function sideName(v, when, parts) {
  if (v === '@both') return 'обидва з КОЛИ (А і Б)'
  if (v === '*') return vocab.value.sides['*']
  const ref = when?.[v.slice(1)]
  const p = parts.find((x) => x.id === ref)
  const l = vocab.value.sides[v]
  return p ? `${iconOf(p)} ${p.title} — той, що в КОЛИ (${l})` : `${vocab.value.sides[ref] || 'сторона'} з КОЛИ (${l})`
}
