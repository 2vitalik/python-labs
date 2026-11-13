import { computed } from 'vue'

import { useEd } from './ed.js'
import { sentence } from './rules.js'

// the transitions between windows that no menu item makes: a rule with the effect «відкривається вікно» leads there
// from the game screen, where rules happen. The map of windows and a window's own card both read them

const cut = (s, n) => (s.length > n ? `${s.slice(0, n - 1)}…` : s)

// a rule's reason in a word or two (T284 §1): the game's end, the key pressed, the pair that met, else the start of КОЛИ
export function why(rule, parts) {
  if (rule.then.some((e) => e.kind === 'win')) return 'перемога'
  if (rule.then.some((e) => e.kind === 'lose')) return 'поразка'
  const w = rule.when || {}
  const name = (id) => parts.find((p) => p.id === id)?.title
  if (w.kind === 'input' && w.action) return cut(String(w.action), 18)
  if (w.kind === 'contact' && name(w.a) && name(w.b)) return cut(`${name(w.a)} × ${name(w.b)}`, 26)
  return cut(sentence(rule, parts).when.replace(/\p{Extended_Pictographic}️?\s*/gu, '').trim(), 24) || 'правило'
}

// → [{ from, to, title, rule }]: from — the game screen's id; nothing while the game has no such window
export function ruleJumps(windows, rules, parts) {
  const game = windows.find((w) => w.task === 'game-screen')?.id
  const ids = new Set(windows.map((w) => w.id))
  const out = []
  for (const r of rules) {
    for (const e of r.then) if (e.kind === 'window' && game && ids.has(e.window) && e.window !== game) out.push({ from: game, to: e.window, title: why(r, parts), rule: r.id })
  }
  return out
}

// the described game's rule jumps, for a piece of the editor
export const useJumps = () => { const ed = useEd(); return computed(() => ruleJumps(ed.windows, ed.rules || [], ed.parts)) }
