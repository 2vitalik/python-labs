import { ruleJumps } from './windowJumps.js'

// the transitions between windows as trees (T270 §10.4), for the map's two views: which edge is an arrow and which is an extra

export const cut = (s, n) => (s.length > n ? `${s.slice(0, n - 1)}…` : s)

// menu items that lead to another existing window and the rules that open one; parallel items between one pair are
// one edge «Нова гра, Продовжити»
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
  for (const j of ruleJumps(windows, rules)) add(j.from, j.to, j.title)
  const out = {}
  for (const e of pairs.values()) (out[e.from] ??= []).push(e)
  return out
}

const firstRoot = (windows, out) =>
  windows.find((w) => w.task === 'splash-screen' && out[w.id]) || windows.find((w) => w.task === 'main-menu') || windows[0]

// breadth-first from the root: the first edge that reaches a window makes it a child, every other edge is an extra of
// its source; windows the root does not reach start trees of their own, in list order. Labels are the items, uncut.
// → { roots, kids: {id: [child id]}, extras: {id: [{ id: target, label }]}, label: {child id: its arrow's label} }
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
        const items = e.labels.join(', ')
        if (seen.has(e.to)) extras[v].push({ id: e.to, label: items })
        else {
          seen.add(e.to)
          kids[v].push(e.to)
          label[e.to] = items
          queue.push(e.to)
        }
      }
    }
  }
  return { roots, kids, extras, label }
}
