// the transitions between windows that no menu item makes: a rule with the effect «відкривається вікно» leads there
// from the game screen, where rules happen. The map of windows and a window's own card both read them

export const why = (rule) => (rule.then.some((e) => e.kind === 'win') ? 'перемога' : rule.then.some((e) => e.kind === 'lose') ? 'поразка' : 'за правилом')

// → [{ from, to, title, rule }]: from — the game screen's id; nothing while the game has no such window
export function ruleJumps(windows, rules) {
  const game = windows.find((w) => w.task === 'game-screen')?.id
  const ids = new Set(windows.map((w) => w.id))
  const out = []
  for (const r of rules) {
    for (const e of r.then) if (e.kind === 'window' && game && ids.has(e.window) && e.window !== game) out.push({ from: game, to: e.window, title: why(r), rule: r.id })
  }
  return out
}
