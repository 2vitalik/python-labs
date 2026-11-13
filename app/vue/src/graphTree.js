import { ruleJumps } from './windowJumps.js'

// the transitions between windows as trees (T270 §10.4), for the map's two views: which edge is an arrow and which is an extra

export const cut = (s, n) => (s.length > n ? `${s.slice(0, n - 1)}…` : s)

// what makes a transition, to read: the items of «Переходи й дії» and the rules' reasons, each a list in words
// via: [{ kind: item | rule, title }] → { item: 'Нова гра, Продовжити', rule: 'перемога' }
export const viaWords = (via) => Object.fromEntries(['item', 'rule'].map((k) => [k, via.filter((v) => v.kind === k).map((v) => v.title).join(', ')]))
export const viaText = (via) => { const w = viaWords(via); return [w.item, w.rule && `⚡ ${w.rule}`].filter(Boolean).join(' ') }

// menu items that lead to another existing window and the rules that open one; parallel ones between one pair are one edge
function transitions(windows, menus, rules) {
  const ids = new Set(windows.map((w) => w.id))
  const pairs = new Map()
  const add = (from, to, kind, title) => {
    if (!ids.has(from) || !ids.has(to) || from === to) return
    const k = `${from}>${to}`
    if (!pairs.has(k)) pairs.set(k, { from, to, via: [] })
    const t = (title || '').trim()
    if (t && !pairs.get(k).via.some((v) => v.kind === kind && v.title === t)) pairs.get(k).via.push({ kind, title: t })
  }
  for (const m of menus) for (const it of m.items || []) add(m.window, it.window, 'item', it.title)
  for (const j of ruleJumps(windows, rules)) add(j.from, j.to, 'rule', j.title)
  const out = {}
  for (const e of pairs.values()) (out[e.from] ??= []).push(e)
  return out
}

const firstRoot = (windows, out) =>
  windows.find((w) => w.task === 'splash-screen' && out[w.id]) || windows.find((w) => w.task === 'main-menu') || windows[0]

const HUB_MIN = 3, HUBS = 3  // a window that many extras lead to is a hub; the busiest few get a colour of their own

// breadth-first from the root: the first edge that reaches a window makes it a child, every other edge is an extra of
// its source; windows the root does not reach start trees of their own, in list order.
// → { roots, kids: {id: [child id]}, extras: {id: [{ id: target, via }]}, via: {child id: its arrow's via}, hub: {id: 1…} }
export function forest(windows, menus, rules = []) {
  const out = transitions(windows, menus, rules)
  const seen = new Set(), roots = [], kids = {}, extras = {}, via = {}, aimed = {}
  for (let r = firstRoot(windows, out); r; r = windows.find((w) => !seen.has(w.id))) {
    roots.push(r.id)
    seen.add(r.id)
    const queue = [r.id]
    while (queue.length) {
      const v = queue.shift()
      kids[v] = []
      extras[v] = []
      for (const e of out[v] || []) {
        if (seen.has(e.to)) {
          extras[v].push({ id: e.to, via: e.via })
          aimed[e.to] = (aimed[e.to] || 0) + 1
        } else {
          seen.add(e.to)
          kids[v].push(e.to)
          via[e.to] = e.via
          queue.push(e.to)
        }
      }
    }
  }
  const busiest = Object.keys(aimed).filter((id) => aimed[id] >= HUB_MIN).sort((a, b) => aimed[b] - aimed[a]).slice(0, HUBS)
  return { roots, kids, extras, via, hub: Object.fromEntries(busiest.map((id, i) => [id, i + 1])) }
}
