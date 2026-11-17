import { postClaim, postPart, putPart } from './api.js'
import { kindOf, statOf, vocab } from './catalog.js'
import { myParts } from './myGame.js'

// «＋ у гру» on /tasks (T274 §3). Most kinds make a claim; a window type, an entity type, a stat and a field option are
// properties of the game's objects — the plus makes or changes the object and the server derives the claim (auto_claims)

// PUT rewrites every field of the part's kind: the rest goes back as it was
const putWith = (p, patch) => putPart(p.id, { ...p, ...patch })

export const hasStat = (part, key) => part.stats.some((s) => s.key === key)

// one at a time: each write re-syncs the game's auto-claims
export async function addStat(task, parts, value) {
  const stat = { key: task.opt, label: task.title, value, unit: statOf(task.opt)?.unit || '' }
  for (const p of parts) await putWith(p, { stats: [...p.stats, stat] })
}

// a field option's `opt` is `property:value`; the field keeps a checkbox as true and a multi choice (or words) as a list.
// `now` — the other value a one-value property holds already: the plus asks before replacing it
function fieldOpt(task, parts) {
  const i = task.opt.indexOf(':')
  const key = task.opt.slice(0, i), value = task.opt.slice(i + 1)
  const spec = vocab.value.field.find((s) => s.key === key) || {}
  const field = parts.find((p) => p.kind === 'field')
  const was = field?.props[key]
  const list = spec.multi || spec.type === 'tags'
  const next = spec.type === 'bool' ? true : list ? [...new Set([].concat(was ?? [], value))] : value
  const name = (v) => spec.options?.[v]?.label || v
  const write = () => (field
    ? putWith(field, { props: { ...field.props, [key]: next } })
    : postPart({ kind: 'field', title: 'Поле', props: { [key]: next } }))
  return { now: spec.type === 'choice' && !list && was && was !== value ? name(was) : '', name: name(value), write }
}

// a window or an entity of the card's type, named in the plus's panel (T278 §1)
export const addPart = (task, { icon, title, description }) => (kindOf(task) === 'window'
  ? postPart({ kind: 'window', task: task.slug, title, description })
  : postPart({ kind: 'entity', role: task.opt, icon, title, description }))

// a game has many entities of one type (enemies): the plus stays beside the tick
export const addsMore = (task) => kindOf(task) === 'role'

// what the plus does: `ask` — a panel asks first (params · stat · replace · part), else `run` writes at once.
// `parts` — the game's (the reader's own unless told); `anchor` — { part } | { rule }: the claim is made there (gameCtx.js)
export function plusOf(task, { parts = myParts.value, anchor } = {}) {
  const kind = kindOf(task)
  if (kind === 'stat') return { ask: 'stat' }
  if (kind === 'window' || kind === 'role') return { ask: 'part' }
  if (kind === 'fieldopt') {
    const opt = fieldOpt(task, parts)
    return { ask: opt.now ? 'replace' : '', run: opt.write, opt }
  }
  return task.slots?.length ? { ask: 'params' } : { run: () => postClaim({ task: task.slug, ...anchor, params: {} }) }
}
