import { iconOf, statOf, vocab } from './catalog.js'
import { pieces, plain, specOf } from './rules.js'

// what each view of «Правила» shows (T274 §6): RulesSwitch counts it, the views lay it out

export const isContact = (r) => specOf('triggers', r.when.kind)?.group === 'контакт' && r.when.a && r.when.b
export const isControl = (r) => r.when.kind === 'input'
// the time triggers in the order «Що коли відбувається» reads them
export const TIME_KINDS = ['phase_start', 'tick', 'timer', 'schedule', 'idle', 'rng', 'turn_start', 'turn_end']
export const isTimed = (r) => TIME_KINDS.includes(r.when.kind)
// an effect that lasts: «стає ⟨вразливий⟩ на 40 тіків», «завмирає на 3»
export const lasting = (e) => (e.kind === 'set_state' && e.dur) || (e.kind === 'stun' && e.n)
export const lasts = (r) => r.then.some(lasting)

// a stat measured in time — тіки, ходи, секунди, хвилини; «кл/тік» is a speed
const TIME_UNIT = /^(тік|хід|ход|с\.?$|сек|хв)/i
export const timedStats = (entities) => entities.flatMap((p) => (p.stats || [])
  .map((s) => ({ p, s, unit: s.unit || statOf(s.key)?.unit || '' }))
  .filter((x) => TIME_UNIT.test(x.unit)))

// who an entity arg names, as a piece: a side of the trigger resolves to its entity when it has one
export function whoPiece(v, when, parts) {
  const ref = /^@[ab]$/.test(v) ? when?.[v.slice(1)] : v
  const p = parts.find((x) => x.id === ref)
  return p ? { t: 'entity', id: p.id, v: p.title, icon: iconOf(p) } : { t: 'side', v: vocab.value.sides[ref] || vocab.value.sides[v] || '?' }
}

export const whenText = (r, parts) => plain(pieces('triggers', r.when, { parts, when: r.when }))

// neighbours with the same key share one cell: the first row gets span = how many, the rest 0
export function spans(rows, key) {
  let head
  for (const r of rows) {
    if (head && key(head) === key(r)) {
      head.span++
      r.span = 0
    } else {
      head = r
      r.span = 1
    }
  }
  return rows
}
