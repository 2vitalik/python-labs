import { homeOf } from './features.js'

// the features a game already has something in (T319): they are shown whatever the switch, and cannot be turned off.
// A claim on a part counts for the part's feature — it reads there; a claim on no part (one about the game as a whole,
// about the levels in general, or one still waiting for its place) — for its card's home
const ON_PART = { entity: 'mechanics', window: 'elements', field: 'field', level: 'levels' }

export function dataOf({ game, parts, claims, info }) {
  const out = new Set()
  if (game.phases?.length) out.add('phases')
  if (game.moments) out.add('moments')
  for (const p of parts) {
    if (p.kind === 'entity' && (p.stats?.length || p.states?.length)) out.add('stats')
    if (p.kind === 'field') out.add('field')
    if (p.kind === 'level') out.add('levels')
    if (p.kind === 'level' && p.props?.map) out.add('map')
  }
  const kinds = Object.fromEntries(parts.map((p) => [p.id, p.kind]))
  for (const c of claims) {
    const t = info(c.task)
    if (c.auto || c.rule || !t) continue
    const home = c.part ? ON_PART[kinds[c.part]] : homeOf(t)
    if (home) out.add(home)
  }
  return out
}
