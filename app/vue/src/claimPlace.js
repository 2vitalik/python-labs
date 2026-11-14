import { iconOf, kidsOf, kindOf, taskIndex } from './catalog.js'
import { myClaims, myParts, myRules, myTasks } from './myGame.js'
import { sentence } from './rules.js'
import { HEADS, ZONES } from './sections.js'

const cut = (s, n) => (s.length > n ? `${s.slice(0, n - 1)}…` : s)

// what a claim is anchored to: { id — where «show me» jumps, text — the anchor in words }; null — a card about the game
// as a whole: it lies in its category's section and has no anchor to name
export function claimPlace(c, { parts, rules, info }) {
  const p = c.part && parts.find((x) => x.id === c.part)
  if (p) return { id: `p-${p.id}`, text: `${iconOf(p)} ${p.title}` }
  const r = c.rule && rules.find((x) => x.id === c.rule)
  if (r) return { id: `r-${r.id}`, text: `правило: ${cut(sentence(r, parts).when, 28)}` }
  if (c.auto && c.task === 'moment-frames') return { id: 'moments', text: '🎞️ як це грається' }  // claimed by a drawn scenario (T276)
  const kind = kindOf(info(c.task))  // unanchored: a level card lives in «Рівні», a game card in its zone, the rest wait in their section's strip
  return kind === 'level' ? { id: 'levels', text: '🪜 рівні' } : kind === 'game' ? null : { id: `c-${c.id}`, text: 'ще без місця' }
}

// every place a catalog card has in the reader's own game — for the tick on /tasks: the claim's own row, or the object
// itself when the claim made itself (a type, a parameter) and has no row
export function myPlaces(slug) {
  const t = myTasks.value[slug] || taskIndex.value[slug]
  const zone = ZONES.find((z) => z.zones.includes(t?.zone)) || ZONES[0]
  const section = `${HEADS[zone.id].icon} ${HEADS[zone.id].title}`
  const places = myClaims.value.filter((c) => c.task === slug).map((c) => ({
    id: c.auto && c.part ? `p-${c.part}` : `c-${c.id}`,
    text: claimPlace(c, { parts: myParts.value, rules: myRules.value, info: () => t })?.text || section,
  }))
  // repeats of a card in one place (T291 §13) read alike: the second and later ones say which they are
  const seen = {}
  return places.map((p) => ({ ...p, text: (seen[p.text] = (seen[p.text] || 0) + 1) > 1 ? `${p.text} · ${seen[p.text]}-й раз` : p.text }))
}

// a family's cards in the reader's game, at any depth, each with its places (T291 §7); the family itself too — a claim made
// before the card was split into variants names it, and nothing else on /tasks would show it
export function familyPlaces(task, out = []) {
  const places = myPlaces(task.slug)
  if (places.length) out.push({ task, places })
  for (const k of kidsOf.value[task.slug] || []) familyPlaces(k, out)
  return out
}
