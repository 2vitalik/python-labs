// the transitions between windows as trees (T270 §10.4), for graphLayout.js: which edge is an arrow and which is an extra

export const cut = (s, n) => (s.length > n ? `${s.slice(0, n - 1)}…` : s)

// what a rule that opens a window is called on its arrow
const why = (rule) => (rule.then.some((e) => e.kind === 'win') ? 'перемога' : rule.then.some((e) => e.kind === 'lose') ? 'поразка' : 'за правилом')

// menu items that lead to another existing window; parallel items between one pair are one edge «Нова гра, Продовжити».
// A rule with the effect «відкривається вікно» leads there too — from the game screen, where rules happen
function transitions(windows, menus, rules) {
  const ids = new Set(windows.map((w) => w.id))
  const pairs = new Map()
  const add = (from, to, title) => {
    if (!ids.has(from) || !ids.has(to) || from === to) return
    const k = `${from}>${to}`
    if (!pairs.has(k)) pairs.set(k, { from, to, labels: [] })
    const t = (title || '').trim()
    if (t && !pairs.get(k).labels.includes(t)) pairs.get(k).labels.push(t)
  }
  for (const m of menus) for (const it of m.items || []) add(m.window, it.window, it.title)
  const game = windows.find((w) => w.task === 'game-screen')?.id
  for (const r of rules) for (const e of r.then) if (e.kind === 'window') add(game, e.window, why(r))
  const out = {}
  for (const e of pairs.values()) (out[e.from] ??= []).push(e)
  return out
}

const firstRoot = (windows, out) =>
  windows.find((w) => w.task === 'splash-screen' && out[w.id]) || windows.find((w) => w.task === 'main-menu') || windows[0]

// breadth-first from the root: the first edge that reaches a window makes it a child, every other edge is an extra of
// its source; windows the root does not reach start trees of their own, in list order.
// → { roots, kids: {id: [child id]}, extras: {id: [target id]}, label: {child id: its arrow's label} }
export function forest(windows, menus, rules = []) {
  const out = transitions(windows, menus, rules)
  const seen = new Set(), roots = [], kids = {}, extras = {}, label = {}
  for (let r = firstRoot(windows, out); r; r = windows.find((w) => !seen.has(w.id))) {
    roots.push(r.id)
    seen.add(r.id)
    const queue = [r.id]
    while (queue.length) {
      const v = queue.shift()
      kids[v] = []
      extras[v] = []
      for (const e of out[v] || []) {
        if (seen.has(e.to)) extras[v].push(e.to)
        else {
          seen.add(e.to)
          kids[v].push(e.to)
          label[e.to] = cut(e.labels.join(', '), 28)
          queue.push(e.to)
        }
      }
    }
  }
  return { roots, kids, extras, label }
}
